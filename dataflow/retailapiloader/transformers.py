import apache_beam as beam
import requests
import logging

from retailapiloader.utils import Utils

class CategoriesFn(beam.CombineFn):
    def create_accumulator(self):
        return {}

    def add_input(self, accumulator, input):
        if str(input['code']) not in accumulator:
            accumulator[str(input['code'])] = input
        return accumulator

    def merge_accumulators(self, accumulators):
        merged = {}
        for accum in accumulators:
            merged.update(accum)
        return merged

    def extract_output(self, accumulator):
        return accumulator


class MergeProducts(beam.DoFn):
    def __init__(self, utils:Utils):
        self.utils = utils

    def process(self, element):
        yield self.utils.merge(element)

class GetCategories(beam.DoFn):
    def __init__(self, url:str, api_token:str, utils:Utils):
        self.url = url
        self.api_token = api_token
        self.utils = utils

    def process(self, element):
        headers = {
            'Authorization': f'Bearer {self.api_token}',
        }
        params = (
            ('format', 'json'),
        )
        response = requests.get(self.url, headers=headers, params=params).json()
        online_cat = list(filter(lambda c: c['id'] == 'Online', response['catalogs'][0]['catalogVersions']))
        categories = list(filter(lambda c: c['id'] == '1', online_cat[0]['categories']))
        yield  self.utils.build_categories(categories[0]['subcategories'])


class GetProducts(beam.DoFn):
    def __init__(self, url:str, api_token:str, utils:Utils):
        self.url = url
        self.api_token = api_token
        self.utils = utils

    def process(self, element, categories):
        headers = {
            'Authorization': f'Bearer {self.api_token}',
        }

        params = (
            ('currentPage', f'{element}'),
            ('pageSize', '100'),
            ('fields', 'GOOGLE'),
            ('format', 'json'),
        )
        logging.info(f'Calling get products api currentPage: {element}')
        products = requests.get(self.url, headers=headers, params=params).json()
        logging.info(f'Products returned for currentPage: {element}')
        if 'products' in products:
            products = [self.utils.from_api(product, categories) for product in products['products']]
            for product in products:
                yield product
