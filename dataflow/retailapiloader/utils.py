from argparse import Namespace
import json
from math import ceil
from typing import List
import configparser
import requests
from apache_beam.options.pipeline_options import PipelineOptions
from retailapiloader.retail_product import Attribute, AttributeValue, Audience, FulfillmentInfo, Image, PriceInfo, Product, Rating, Ttl
from google.cloud import storage

class Utils:

    def __init__(self, pipeline_options: PipelineOptions, known_args: Namespace):
        options = pipeline_options.get_all_options()
        if options['runner']:
            client = storage.Client()
            config_uri = known_args.config_file_gsutil_uri  
            with open('config.INI', 'wb') as config_file:
                client.download_blob_to_file(config_uri, config_file)
        config = configparser.ConfigParser()
        config.read('config.INI')
        self.tags = config.get('OPTIONS', 'tags')
        if self.tags:
            self.tags = self.tags.split(',')
        self.attributes_key = config.get('OPTIONS', 'attributes_key')
        if self.attributes_key:
            self.attributes_key = self.attributes_key.split(',')
        self.materials = config.get('OPTIONS', 'materials')
        if self.materials:
            self.materials = self.materials.split(',')
        if not known_args.catalog_type == 'primary' and not known_args.catalog_type == 'secondary':
            error = f'Catalog type unknown! Must be either primary or secondary, found: {known_args.catalog_type}'
            raise ValueError(error)
        self.catalog_type = known_args.catalog_type
        self.catalog_tag = known_args.catalog_tag


    def api_authenticate(self, known_args, api_client, api_secret):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'client_id': api_client,
            'client_secret': api_secret,
            'grant_type': 'client_credentials'
        }

        response = requests.post(known_args.auth_url, headers=headers, data=data)
        api_token = response.json()['access_token']
        return api_token

    def product_ranges(self, known_args, api_token):
        headers = {
            'Authorization': f'Bearer {api_token}',
        }

        params = (
            ('currentPage', '1'),
            ('pageSize', '1'),
            ('fields', 'GOOGLE'),
            ('format', 'json'),
        )

        response = requests.get(known_args.products_url, headers=headers, params=params)
        number_of_products = response.json()['totalProductCount']
        return range(1, ceil(number_of_products/100)+1)


    def from_api(self, element, categories_ref:dict) -> Product:
        product = Product()
        product.id = element['productCode']
        product.type = 'PRIMARY'
        product.primaryProductId = element['productCode']
        product.categories = self.build_product_categories(element, categories_ref)
        product.title = element['summary']
        product.description = element['descriptionEn'] if 'descriptionEn' in element else ""
        product.attributes = self.build_attributes(element)
        product.tags = self.build_tags(element)
        product.priceInfo = self.build_price_info(element)
        product.availability = self.build_availability(element)
        product.availableQuantity = 0 if self.catalog_type == 'secondary' else int(element['inventory'])
        product.fulfillmentInfo = self.build_fulfillment_info(element)
        product.uri = element['productGlobalUrl']
        product.images = [Image(element['mainSqGy800X800'], 800, 800)]
        product.audience = self.build_audience(element)
        product.sizes = self.build_sizes(element)
        product.materials = self.build_materials(element)
        return json.loads(json.dumps(product, default=lambda o: o.__dict__)) 

    def merge(self, element):
        # For primary catalog
        if self.catalog_type == 'primary':
            # if in BQ but not in the API call response
            if not element[1]['new']:
                current = element[1]['current'][0]
                current['availability'] = 'OUT_OF_STOCK'
                current['availableQuantity'] = 0
                return current
            else:
                return element[1]['new'][0]
        else:
            # For secondary catalog
            # if not in BQ we add it otherwise we don't 
            if not element[1]['current']:
                return element[1]['new'][0]
            else:
                return element[1]['current'][0]


    def build_attributes(self, line: dict) -> List[Attribute]:
        attributes = []
        for key in self.attributes_key:
            if key in line and not line[key] =='':
                if isinstance(line[key], list):
                    value = AttributeValue(text = line[key], 
                        numbers = [],
                        searchable = False, 
                        indexable = False)
                else:
                    value = AttributeValue(text = [line[key]], 
                        numbers = [],
                        searchable = False, 
                        indexable = False)
                attributes.append(Attribute(key, value))

        catalog_tag_value = AttributeValue(text = [self.catalog_tag], 
                        numbers = [],
                        searchable = False, 
                        indexable = False)
        attributes.append(Attribute('src_catalog_geo', catalog_tag_value))
        return attributes

    def build_tags(self, line: dict) -> List[str]:
        tags = list(filter(None, [line[tag] for tag in self.tags if tag in line]))
        tags.append(self.catalog_tag)
        return tags

    def build_price_info(self, line: dict) -> PriceInfo:
        return PriceInfo('USD', line['salePrice'], line['listPrice'], None, None, None)


    def build_rating(self, line: dict) -> Rating:
        return None


    def build_ttl(self, line: dict) -> Ttl:
        return None


    def build_fulfillment_info(self, line: dict) -> List[FulfillmentInfo]:
        return []


    def build_audience(lself, ine: dict) -> Audience:
        return None

        
    def build_sizes(self, line: dict) -> List[str]:
        try:
            result = []
            sizes = line['sizes']
            for size in sizes:
                if not 'One Size' in size:
                    result.append(size.split(':')[1])
            return result
        except:
            if 'sizes' in line:
                print('sizes: ' + str(line['sizes']) + ' for product '+str(line['productCode']))
            return []


    def build_materials(self, line: dict) -> List[str]:
        return list(filter(None, [line[material] for material in self.materials if material in line]))

    def build_product_categories(self, element: dict, categories_ref: dict) -> List[str]:
        try:
            if not 'category' in element:
                element['category'] = element['categoryGallery']

            category_path_list = []
            for category in element['category']:
                if category in categories_ref:
                    accumulator = categories_ref[category]
                    accumulator = ' > '.join(accumulator)
                    category_path_list.append(accumulator)

            return category_path_list
        except Exception as ex:
            product_id = element['productCode']
            print(f'No categories found for productId: {product_id} fallback to Online Exclusive')
            return 'Online Exclusive'

    def build_availability(self, line: dict) -> str:
        return 'IN_STOCK' if int(line['inventory']) > 0 and self.catalog_type == 'primary' else 'OUT_OF_STOCK'

    def build_available_time(self, line: dict) -> str:
        return line['date_published']

    def build_categories(self, categories:list) -> dict:
        paths={}
        self.build_category_path(paths, categories, [])
        return paths

    def build_category_path(self, paths: dict, sub_categories: list, parent_category_path: list):
        for caterory in sub_categories:
            child_path = parent_category_path
            if 'name' in caterory:
                child_path = child_path + [caterory['name']]
                paths[caterory['id']] = child_path
            if 'subcategories' in caterory:
                self.build_category_path(paths, caterory['subcategories'], child_path)