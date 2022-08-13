from datetime import datetime, timedelta
import os
from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.operators.python_operator import PythonOperator
from google.cloud.retail import (
    ProductServiceClient, 
    ImportProductsRequest, 
    ProductInputConfig,
    BigQuerySource
)

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
CONFIG_INI = os.environ.get("CONFIG_INI")
AUTH_URL = os.environ.get("AUTH_URL")
PRODUCTS_URL = os.environ.get("PRODUCTS_URL")
CATEGORIES_URL = os.environ.get("CATEGORIES_URL")
SECONDARY_PRODUCTS_URL = os.environ.get("SECONDARY_PRODUCTS_URL")
SECONDARY_CATEGORIES_URL = os.environ.get("SECONDARY_CATEGORIES_URL")
RETAIL_BRANCH = os.environ.get("RETAIL_BRANCH")
CRON_SCHEDULER = os.environ.get("CRON_SCHEDULER")
PRIMARY_CATALOG_TAG = os.environ.get("PRIMARY_CATALOG_TAG")
SECONDARY_CATALOG_TAG = os.environ.get("SECONDARY_CATALOG_TAG")


with models.DAG(
    dag_id="retail_api_catalog_import",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule_interval=CRON_SCHEDULER,
    max_active_runs=1
) as dag:

    # 
    # Import Hybris products catalog into Bigquery using Dataflow
    #
    job_name = 'retail-loader-primary'+datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    hybris_to_bigquery_primary = DataflowStartFlexTemplateOperator(
        task_id="Hybris_primary_to_BigQuery",
        body={
            "launchParameter": {
                "containerSpecGcsPath": f"gs://{PROJECT_ID}-retail-api-loader-dataflow-template/dataflow/templates/retail-api-loader.json",
                "jobName": job_name,
                "parameters": {
                    "auth-url": AUTH_URL,
                    "products-url":PRODUCTS_URL,
                    "categories-url":CATEGORIES_URL,
                    "bq_dataset":f"{PROJECT_ID}:retail_api",
                    "temp_gcs_bucket":f"gs://{PROJECT_ID}-temp-import-retail-api",
                    "config_file_gsutil_uri":f"gs://{PROJECT_ID}-retail-api-row-catalog-data/config.INI",
                    "catalog_type":"primary",
                    "catalog_tag":PRIMARY_CATALOG_TAG
                },
                "environment": {
                    "network": "retail-api-vpc",
                    "subnetwork": "regions/northamerica-northeast1/subnetworks/retail-api-subnet",
                    "machineType": "n1-standard-1",
                    "numWorkers": "1",
                    "maxWorkers": "1",
                    "ipConfiguration": "WORKER_IP_PRIVATE",
                    "serviceAccountEmail": f"retail-api-sa@{PROJECT_ID}.iam.gserviceaccount.com"
                },
            }
        },
        do_xcom_push=True,
        location="northamerica-northeast1",
        project_id=PROJECT_ID,
        wait_until_finished=True
    )

    job_name = 'retail-loader-secondary'+datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    hybris_to_bigquery_secondary = DataflowStartFlexTemplateOperator(
        task_id="Hybris_secondary_to_BigQuery",
        body={
            "launchParameter": {
                "containerSpecGcsPath": f"gs://{PROJECT_ID}-retail-api-loader-dataflow-template/dataflow/templates/retail-api-loader.json",
                "jobName": job_name,
                "parameters": {
                    "auth-url": AUTH_URL,
                    "products-url":SECONDARY_PRODUCTS_URL,
                    "categories-url":SECONDARY_CATEGORIES_URL,
                    "bq_dataset":f"{PROJECT_ID}:retail_api",
                    "temp_gcs_bucket":f"gs://{PROJECT_ID}-temp-import-retail-api",
                    "config_file_gsutil_uri":f"gs://{PROJECT_ID}-retail-api-row-catalog-data/config.INI",
                    "catalog_type":"secondary",
                    "catalog_tag":SECONDARY_CATALOG_TAG
                },
                "environment": {
                    "network": "retail-api-vpc",
                    "subnetwork": "regions/northamerica-northeast1/subnetworks/retail-api-subnet",
                    "machineType": "n1-standard-1",
                    "numWorkers": "1",
                    "maxWorkers": "1",
                    "ipConfiguration": "WORKER_IP_PRIVATE",
                    "serviceAccountEmail": f"retail-api-sa@{PROJECT_ID}.iam.gserviceaccount.com"
                },
            }
        },
        do_xcom_push=True,
        location="northamerica-northeast1",
        project_id=PROJECT_ID,
        wait_until_finished=True
    )
    # 
    # Import Hybris products catalog from Bigquery to Retail API
    # catalog branch
    #
    def import_catalog():
        client = ProductServiceClient()
        big_query_source = BigQuerySource(
            project_id=PROJECT_ID,
            dataset_id="retail_api",
            table_id="catalog_api"
        )
        input_config = ProductInputConfig(big_query_source=big_query_source)
        import_request = ImportProductsRequest(
            parent=f'projects/{PROJECT_ID}/locations/global/catalogs/default_catalog/branches/{RETAIL_BRANCH}',
            input_config=input_config

        )
        client.import_products(request=import_request)

    load_catalog_from_bigquery = PythonOperator(
        task_id='Load_catalog_from_BigQuery',
        python_callable=import_catalog,
    )
    hybris_to_bigquery_primary >> hybris_to_bigquery_secondary >> load_catalog_from_bigquery