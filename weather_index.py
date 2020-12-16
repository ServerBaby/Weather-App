#!/usr/bin/env python3

""" NOTE: THIS IS A DRAFT ONLY VERSION OF THIS FILE
linked modules not all uploaded yet so don't try to run """

import json
import logging
from dl_data import *

from pprint import pprint
from time import sleep

import requests
from elasticsearch import Elasticsearch


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    pprint(res)


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "weather_properties": {
                "date_uploaded": {"type": "date"},
                "original_image_filename": {"type": "text"},
                "source_json_url": {"type": "text"},
                "image_base64": {"type": "text"},
                "text_description": {"type": "text"},
                "image_hash": {"type": "text"},
                "observation": {
                    "properties": {
                        "wmo": {"type": "integer"},
                        "name": {"type": "text"},
                        "history_product": {"type": "text"},
                        "local_date_time": {"type": "text"},
                        "local_date_time_full": {"type": "date"},
                        "aifstime_utc": {"type": "date"},
                        "lat": {"type": "float"},
                        "lon": {"type": "float"},
                        "apparent_t": {"type": "float"},
                        "cloud": {"type": "text"},
                        "cloud_base_m": {"type": "text"},
                        "cloud_oktas": {"type": "integer"},
                        "cloud_type": {"type": "text"},
                        "cloud_type_id": {"type": "text"},
                        "delta_t": {"type": "float"},
                        "gust_kmh": {"type": "integer"},
                        "gust_kt": {"type": "integer"},
                        "air_temp": {"type": "float"},
                        "dewpt": {"type": "float"},
                        "press": {"type": "float"},
                        "press_msl": {"type": "float"},
                        "press_qnh": {"type": "float"},
                        "press_tend": {"type": "text"},
                        "rain_trace": {"type": "float"},
                        "rel_hum": {"type": "integer"},
                        "sea_state": {"type": "text"},
                        "swell_dir_worded": {"type": "text"},
                        "swell_height": {"type": "text"},
                        "swell_period": {"type": "text"},
                        "vis_km": {"type": "text"},
                        "weather": {"type": "text"},
                        "wind_dir": {"type": "keyword"},
                        "wind_spd_kmh": {"type": "integer"},
                        "wind_spd_kt": {"type": "integer"}

                    }
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, doc_type='properties', body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es


def get_data():
    weather_data = {}
    # what happens if data download fails???
    try:
        weather_data = DownloadData().dl_weather(data_url, image_url)
        print('Data downloaded successfully')

    except Exception as ex:
        print('Exception while getting data')
        print(str(ex))

    finally:
        return json.dumps(weather_data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    es = connect_elasticsearch()
    result = get_data()
    if es is not None:
        if create_index(es, 'current_weather'):
            out = store_record(es, 'current_weather', result)
            print('Data indexed successfully')

#    es = connect_elasticsearch()
    if es is not None:
        search_object = {'query': {'match': {'cloud': 'partly cloudy'}}}
        # search_object = {'_source': ['local_date_time_full'],
        # 'query': {'match': {'cloud': 'Partly cloudy'}}}
        # search_object = {'_source': ['title'], 'query': {'range': {'calories': {'gte': 20}}}}
        search(es, 'current_weather', json.dumps(search_object))
