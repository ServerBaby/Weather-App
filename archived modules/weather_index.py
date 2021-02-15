#!/usr/bin/env python3

""" NOTE: THIS IS A DRAFT ONLY VERSION OF THIS FILE
linked modules not all uploaded yet so don't try to run """

import json
import logging
from pprint import pprint
import requests
from elasticsearch import Elasticsearch
from dl_data import *

# from time import sleep


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    pprint(res)


def create_index(es_object, index_name):
    created = False
    # index settings
    var_to_name = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
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
                    "wind_spd_kt": {"type": "integer"},
                    "local_image_b64": {"type": "text"}
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=var_to_name)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, id=my_id, body=record)  # doc_type='observation',
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
        print("ERROR: " + str(ex.info))

    finally:
        return weather_data


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    # connect to elasticsearch
    es = connect_elasticsearch()

    # Get data from website:
    result = eval(str(get_data()))

    # create index and stick data in it?
    my_id = (str(result['local_date_time_full']))
    if es is not None:
        if create_index(es, 'weather_index'):
            out = store_record(es, 'weather_index', result)
            print('Data indexed successfully')

    # Searches for stuff, currently searching air_temp greater or equal to 25 degrees
    if es is not None:
        # search_object = {'query': {'match': {'cloud': 'partly cloudy'}}}
        # search_object = {'_source': ['local_date_time_full'],
        #                 'query': {'match': {'wmo': 99435}}}
        search_object = {'_source': ['local_date_time_full'],
                         'query': {'range': {'air_temp': {'gte': 25}}}}
        search(es, 'weather_index', json.dumps(search_object))
