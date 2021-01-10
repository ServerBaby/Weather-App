# Weather-App

This app is designed to display the current weather conditions at a specific location of your choosing.

weather_index.py 
This is version 1 of the main application “Weather-App”.  It downloads the most recently available weather conditions for a specific location, adds an image taken at that location and then add this data (in json format) to an Elasticsearch database.  In addition to using modules from Pypi, this app uses the custom modules “dl_data.py” and “dl_img_conv_b64.py” 

weather_scheduler.py 
This is version 2 of the main application “Weather-App”. It is similar to version 1, except that it includes a scheduler that creates an entry of the current weather conditions in the Elasticsearch database every half hour.


dl_data.py: 
This module allows the user to download the most recently available weather conditions for a specific location from the Bureau of Meteorology (BOM) website, manipulate that data including adding a base64 encoded image of the location at that time, and then converts that data back into json format.

dl_img_conv_b64.py 
This module allows the user to download an image file from the internet and convert it into base64 encoding.  This tool is currently confirmed to work on jpg and png files.

wellcamp_urls.py 
This is a file containing a list of relevant URLs for use in the weather app. Specifically, this file contains the URLs for the data from Toowoomba Wellcamp Airport. The data URL can be changed to any of the Bureau of Meteorology pages containing location specific weather conditions in JSON format and the image URL can be changed to any relevant URL containing an image file.


Modules that have been superseded by the above files:

image_url.py – superseded by wellcamp_urls.py 

weather_app.py – superseded by dl_data.py

weather_app_photo.py – superseded by dl_img_conv_b64.py 


Currently the app is being tested on data from Toowoomba Wellcamp Airport.

From Wikipedia: Toowoomba Wellcamp Airport (IATA: WTB, ICAO: YBWW) is an airport in Wellcamp,
8.4 nautical miles (15.6 km; 9.7 mi) west from the CBD of Toowoomba, Queensland, Australia. 
It was known as Brisbane West Wellcamp Airport until November 2017. 
Time zone:  UTC+10:00 ()
Elevation AMSL:  1,509 ft / 460 m
Coordinates:  27°33′30″S 151°47′36″E
Website	www.wellcamp.com.au


