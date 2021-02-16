# Weather-App

The purpose of this app is to download the current weather conditions at a specific location of your choosing and save that data half-hourly into an Elasticsearch Index. 

## weather_app.py 

This is the main module of “Weather-App”.  It downloads the most recently available weather conditions for a specific location from the Bureau of Meteorology (Australia) website, adds an image taken at the same location from the Air Services Australia website, and then add this data to an Elasticsearch index.  In addition to using modules from Pypi, this app uses the custom modules “dl_data.py”, “dl_img_conv_b64.py” and a third custom module that contains the URLs to download the data from.  

## dl_data.py: 

This module allows the user to download the most recently available weather conditions for a specific location from the Bureau of Meteorology (BOM) website, manipulate that data including adding a base64 encoded image of the location at that time, converting the time into an Elasticsearch "friendly" format, and converting the wind direction into an angle (from a compass point), and then converts that data back into json format.

## dl_img_conv_b64.py 

This module allows the user to download an image file from the internet and convert it into base64 encoding.  This tool is currently confirmed to work on any jpg and png files downloaded from the internet.

## wellcamp_urls.py 

This is a custom location module containing a list of relevant URLs for use in the weather app. Specifically, this file contains the URLs for the data from Toowoomba Wellcamp Airport. The data URL can be changed to any of the Bureau of Meteorology pages containing location specific weather conditions in JSON format and the image URL can be changed to any relevant URL containing an image file.  To download the data for another location, simply copy this module, change the URLs to the URLs for your desired location, and if the module name is changed to reflect the new location, the name of this module needs to be updated in the import statements in the module "dl_data" to reflect the new location module.

## Other Folders

Older versions of modules that have been superseded by the above modules are located in the _**archived modules folder**_.  These modules are:

**image_url.py** – superseded by wellcamp_urls.py 

**weather_app_data.py** – superseded by dl_data.py

**weather_app_photo.py** – superseded by dl_img_conv_b64.py 

**weather_index.py** – superseded by weather_app.py



The _**other useful files**_ folder contains the following files:

**weather_index.json** - the json file containing the index mapping for the created Elasticsearch Index

**key to bom terms.pdf** - a key to the meaning of the terms used in the Bureau of Meteorology data

**painless_queries.txt** - several useful scripts written in the Kibana Query Language "Painless".  Includes several scripts on how to add new fields and how to populate those new fields.

## Current Location

Currently the app is being tested on data from _**Toowoomba Wellcamp Airport**_.

From Wikipedia: Toowoomba Wellcamp Airport (IATA: WTB, ICAO: YBWW) is an airport in Wellcamp,
8.4 nautical miles (15.6 km; 9.7 mi) west from the CBD of Toowoomba, Queensland, Australia. 

It was known as Brisbane West Wellcamp Airport until November 2017. 

Time zone:  UTC+10:00 ()

Elevation AMSL:  1,509 ft / 460 m

Coordinates:  27°33′30″S 151°47′36″E

Website	www.wellcamp.com.au


