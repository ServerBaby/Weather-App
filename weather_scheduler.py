#!/usr/bin/env python3

"""Weather Application - Elasticsearch index to hold weather data

Download and manipulate 

This script allows the user to create an Elasticsearch index to hold 
Bureau of Meteorology (Australia) Data for a chosen location.  The 
script creates a new Elasticsearch document containing the most recent
set of data from the BOM website for the chosen location, including 
additional fields containing the time in an Elasticsearch "friendly" 
format, and the wind direction converted into an angle (from a compass 
point), as well as adding an extra field that is the base64 encoded 
image of the location at that time, taken from the AirServices 
Australia website.

Currently being tested on data from Toowoomba Wellcamp Airport.
`http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json`

This script requires that several pypi modules be installed within the
Python environment you are running this script in.  These modules are
`logging` to provide standard error messages, `elasticsearch`, the 
official low-level client for Elasticsearch that assists the script to 
connect to Elasticsearch,create an index with mappings and store data 
in that index, and `apscheduler` to allow scheduling of Python code to  
be executed at set intervals.

This script also requires several accompanying custom modules be 
installed.  These modules are: `dl_data` which contains the scripts
to download the data from the BOM and ASA websites, and two modules
that `dl_data` depends on: `dl_img_conv_b64` (script to download and
convert images to base64) and `wellcamp_urls` (containing the links 
to the most recent data and image from the target location, currently
Wellcamp Airport).

The weather_app python file can be imported as a module and contains 
the following functions:

    * connect_es - connects to Elasticsearch 
    * create_index - creates an Elasticsearch index including the 
        index settings and mappings for the Weather App.
    * get_data - downloads the data from the BOM and ASA websites
    * store_record - stores the downloaded data
    * create_es_doc - inserts the stored downloaded data into an 
        Elasticsearch document
    * __main__ - combines the above functions to create the Elastic-
        search index "weather_index" and adds a new set of data to 
        the index every 30 minutes.
"""

import logging
from elasticsearch import Elasticsearch
from apscheduler.schedulers.blocking import BlockingScheduler
from weather_comment_dl_data import *


def connect_es():
    host_es = None				# creates the host_es variable
    host_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])	 # defines host_es as connection to elasticsearch
    print('Connecting to Elasticsearch')
    if host_es.ping():      				# ping(params=None, headers=None)  Returns whether the cluster is running.
        print('Connected successfully\n')
    else:
        print('Connection failed')
    return host_es				# returns the connection to the cluster


def create_index(es_conn, index_name):
    index_created = False
    doc_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "epoch_date": {"type": "date", "format": "epoch_millis"},
                "wind_angle": {"type": "float"},
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
        if not es_conn.indices.exists(index_name):
            es_conn.indices.create(index=index_name, ignore=400, body=doc_body)
            print('Created Index')
        index_created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return index_created


def store_record(doc_object, index_name, record):
    is_stored = True
    try:
        doc_object.index(index=index_name, id=my_id, body=record)   # Creates or updates a document in an index.
        print('Data indexed successfully')
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def get_data():
    weather_data = {}				# creates empty dictionary to hold the data
    print('Connecting to BOM Website')
    try:
        weather_data = DownloadData().dl_weather(data_url, image_url)	  # grabs the data from BOM
        print('Data downloaded successfully\n')
    except Exception as ex:
        print('Exception while getting data')
        print("ERROR: " + str(ex))
    finally:
        return weather_data					# returns the full dictionary


def create_es_doc():
    es = connect_es()
    got_data = (get_data())
    global my_id
    my_id = str((got_data['local_date_time_full']))
    try:
        if es is not None:					# if the elasticsearch cluster can be connected to
            if create_index(es, 'weather_index'):		# if ‘weather index’ is created go on, otherwise create it
                created_doc = store_record(es, 'weather_index', got_data)		# store a doc with the  dictionary in it
                print('Document ' + str(my_id) + ' created\n')
                return created_doc
    except Exception as ex:
        print('Error in creating document ' + str(my_id))
        print(str(ex))


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(create_es_doc, 'interval', seconds=300, misfire_grace_time=30)
    print('Starting Weather App\nPress Ctrl+C to exit at any time\n')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
