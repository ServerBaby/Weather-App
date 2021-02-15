#!/usr/bin/env python3

""" NOTE: THIS IS A DRAFT ONLY VERSION OF THIS FILE
linked modules not all uploaded yet so don't try to run """

import json
import logging
import requests
from elasticsearch import Elasticsearch
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from dummy_dl_data import *


def create_index(es_object, index_name):
    created = False
    # index settings
    doc_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
                "properties": {
                "epoch_date": {"type": "date", "format": "epoch_millis"},
                "wmo": {"type": "integer"},
                "name": {"type": "text"},
                "history_product": {"type": "text"},
                "local_date_time": {"type": "text"},
                "local_date_time_full": {"type": "text"},
                "aifstime_utc": {"type": "text"},
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

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=doc_body)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        elastic_object.index(index=index_name, id=my_id, body=record)
        print('Data indexed successfully')
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    print('Connecting to Elasticsearch')
    if _es.ping():
        print('Connected successfully\n')
    else:
        print('Connection failed')
    return _es


def get_data():
    weather_data = {}
    print('Connecting to BOM Website')
    try:
        weather_data = DownloadData().dl_weather(data_url, image_url)
        print('Data downloaded successfully\n')

    except Exception as ex:
        print('Exception while getting data')
        print(str(ex))
        print("ERROR: " + str(ex.info))

    finally:
        return weather_data


def new_download():
    es = connect_elasticsearch()
    # Get data from website:
    result = (get_data())
    global my_id
    my_id = str((result['local_date_time_full']))
    try:
        if es is not None:
            if create_index(es, 'weather_index'):
                out = store_record(es, 'weather_index', result)
                print('Document ' + str(my_id) + ' created\n')
                return out
    except Exception as ex:
        print('Error in creating document ' + str(my_id))
        print(str(ex))


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(new_download, 'interval', seconds=300, misfire_grace_time=30)
    # seconds=900 is 15 minutes; acts as default in case first firing misses
    print('Starting Weather App\nPress Ctrl+C to exit at any time\n')

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
