import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.dataframe.io import read_csv
from apache_beam.dataframe import convert
from apache_beam.pvalue import AsSingleton
from google.cloud import bigquery
from retailapiloader.bq_schema import retail_schema
from retailapiloader.transformers import CategoriesFn, GetCategories, GetProducts, MapToProduct, MergeProducts
from retailapiloader.utils import Utils
from google.cloud import secretmanager
import requests


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--auth-url',
        dest='auth_url',
        default='',
        help='authentication url.')
    parser.add_argument(
        '--products-url',
        dest='products_url',
        default='',
        help='products url.')
    parser.add_argument(
        '--categories-url',
        dest='categories_url',
        default='',
        help='categories url.')
    parser.add_argument(
        '--bq_dataset',
        dest='bq_dataset',
        default="",
        help='BQ dataset to store the catalog data')
    parser.add_argument(
        '--temp_gcs_bucket',
        dest='temp_gcs_bucket',
        default="",
        help='GCS bucket to store BQ load job data')
    parser.add_argument(
        '--config_file_gsutil_uri',
        dest='config_file_gsutil_uri',
        default="",
        help='gsutil uri of the config file')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    utils = Utils(pipeline_options, known_args)
    project_id = known_args.bq_dataset.split(':')[0]
    products_table_spec = known_args.bq_dataset + '.catalog_api'
    logging.info('Using BigQuery table_spec: '+products_table_spec)

    bq_client = bigquery.Client()
    table_exists = True
    try:
        table_id = products_table_spec.replace(':','.')
        bq_client.get_table(table_id)
    except Exception as e:
        table_exists = False

    secret_client = secretmanager.SecretManagerServiceClient()
    api_client_path = secret_client.secret_version_path(project_id, 'api-client', '1')
    api_secret_path = secret_client.secret_version_path(project_id, 'api-secret', '1')
    api_client_response = secret_client.access_secret_version(name=api_client_path)
    api_secret_response = secret_client.access_secret_version(name=api_secret_path)
    api_client = api_client_response.payload.data.decode("UTF-8")
    api_secret = api_secret_response.payload.data.decode("UTF-8")
    api_token = utils.api_authenticate(known_args, api_client, api_secret)
    product_ranges = utils.product_ranges(known_args, api_token)


    with beam.Pipeline(options=pipeline_options) as p:

        categories = (
            p | 'Getting categories' >> beam.Create(['one'])
              | 'Calling categories API' >> beam.ParDo(GetCategories(known_args.categories_url, api_token, utils))
        )

        previous_products = (
            p | 'Create empty products when first import' >> beam.Create([])
        )
        if table_exists:
            previous_products = (
                p | 'Read previous products from BQ' >> beam.io.ReadFromBigQuery(
                        table=products_table_spec, gcs_location=known_args.temp_gcs_bucket)
                | 'Map previous products to key pair' >> beam.Map(lambda x: (int(x['id']),x))
            )


        current_products = (
            p | 'Getting products' >> beam.Create(product_ranges)
              | 'Calling products API' >> beam.ParDo(GetProducts(known_args.products_url, api_token, utils), AsSingleton(categories))
              | 'Map current products to key pair' >> beam.Map(lambda x: (int(x['id']),x))
        )

        merged_products = (
            ({'current': previous_products, 'new': current_products})
            | 'Merge primary products' >> beam.CoGroupByKey()
            | 'Reduce primary products' >> beam.ParDo(MergeProducts())
        )

        # Write products to BigQuery``
        (write_to_BigQuery(merged_products, products_table_spec,
            known_args.temp_gcs_bucket, 'Write to BQ - products'))

        p.run().wait_until_finish()


def write_to_BigQuery(collection, table_spec, gcs_bucket, transformation_name):

        collection | transformation_name >> beam.io.WriteToBigQuery(
                table_spec,
                schema=retail_schema(),
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                custom_gcs_temp_location=gcs_bucket)