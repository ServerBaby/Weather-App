#!/usr/bin/env python3

"""Download and manipulate Bureau of Meteorology (Australia) Data

This script allows the user to download the most recently available
weather conditions for a specific location from the Australian Bureau 
of Meteorology (BOM) website, manipulate that data including adding a 
base64 encoded image of the location at that time, converting the time 
into an Elasticsearch "friendly" format, and converting the wind 
direction into an angle (from a compass point), and then converts that 
data back into json format.

Currently being tested on data from Toowoomba Wellcamp Airport.
`http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json`

This script requires that several pypi modules be installed within the
Python environment you are running this script in.  These modules are
`requests` to access online content, `json` to convert data to and from
json format, and `datetime` & `time` to change how dates & times are 
displayed.

This script also requires two accompanying custom modules be installed.
These modules are: `dl_img_conv_b64` (to download an image and convert
to base64) and `wellcamp_urls` (containing the links to the most recent
data and image from the target location, Wellcamp Airport).

The dl_data python file can be imported as a module and contains the
following functions:

    * __init__ - to construct the main function
    * dl_weather - returns all of the data as a dictionary in JSON format
    * dl_time_local - extracts a human-readable version of the local time
        from the BOM data
    * dl_time_utc - extracts the time from the BOM data and expresses it
        as seconds from epoch.
    * def dl_wind_angle - extracts the wind direction from the BOM data 
        and expresses it as an angle (0-360 degrees).
"""

import requests
import json
import datetime
import time
import dl_img_conv_b64
from wellcamp_urls import image_url, data_url


class DownloadData:  
    """
    A class to download the most recent weather conditions at a specific 
    location.  Output in json format.
    
    ...
    
    Attributes
    ----------
    'data_url' : str
        The URL of the data to be downloaded from the Austrlaian BOM website.
        Defined outside of the scope of the class.
    'image_url' : str
        The URL of the image to be downloaded from the AirServiceAus site.
        Defined outside of the scope of the class.

    Methods
    -------
    'dl_weather(data_url, image_url)'
        Downloads the most recent weather conditions at a set location
        as a dictionary; adds to that three key-value pairs: the base64
        representation of an image that is the current view of that 
        location (string), UTC time in milliseconds since epoch 
        (integer), and the wind direction as an angle (float).
    'dl_time_local(data_url)'
        Extracts the time that the most recent weather conditions data
        was uploaded and returns it in a neat, human readable format.
        Example: `Monday, 15 February 2021 13:30:00`
    'dl_time_utc(data_url)'
        Extracts the time that the most recent weather conditions data
        was uploaded and returns the value in seconds from epoch.
        Example: `1613320200.0`
    'dl_wind_angle(data_url)'
        Extracts the wind direction the most recent weather conditions 
        data and returns the direction as an angle (0-360 degrees). 
        Example:  a wind direction of `ESE` returns `112.50`
        
    """

    def __init__(self):
        """
        The constructor for DownloadData class.
        Only used to construct the class currently.
        """

        pass

    def dl_weather(self, data_url, image_url):

        x = requests.get(data_url)

        # Gets information from website and turns it into a usable format
        # [0] is the position of the most recent dataset inserted into the list of datasets ["data"]

        if x.status_code == 200:

            y = json.loads(x.text)["observations"]["data"][0]

            # converts utc time to milli-seconds since epoch and adds it as a new mapping field
            y.update(epoch_date=1000*int(eval((self.dl_time_utc(data_url)))))

            # adds wind angle, converted from wind direction, as a new mapping field
            y.update(wind_angle=(self.dl_wind_angle(data_url)))

            # adds base64 image to data
            y.update(local_image_b64=dl_img_conv_b64.DownloadConvert().conv_img_to_b64(image_url))

            # Removes the unnecessary "sort order" value;
            y.pop("sort_order", None)

            result = y

        else:
            result = str('Data Couldn\'t be retrieved')

        return result

    def dl_time_local(self, data_url):
        # defined in previous function
        x = requests.get(data_url)
        y = json.loads(x.text)["observations"]["data"][0]["local_date_time_full"]

        # Creates a heading for displaying the current dataset with its time as part of the heading
        dd = datetime.datetime
        t_strp_local = dd.strptime(y, "%Y%m%d%H%M%S")
        t_local = dd.strftime(t_strp_local, '%A, %d %B %Y %H:%M:%S')

        # prints the local time that the data was uploaded to the BOM website
        return t_local

    def dl_time_utc(self, data_url):
        # defined in previous function
        x = requests.get(data_url)
        z = json.loads(x.text)["observations"]["data"][0]["aifstime_utc"]

        # Creates a heading for displaying the current dataset with its time as part of the heading
        dd = datetime.datetime
        t_strp_utc = dd.strptime(z, "%Y%m%d%H%M%S")
        t_tuple_utc = dd.timetuple(t_strp_utc)
        t_utc = time.mktime(t_tuple_utc)
        # prints the local time that the data was uploaded to the BOM website
        return str(t_utc)

    def dl_wind_angle(self, data_url):
        # defined in previous function
        x = requests.get(data_url)
        w = json.loads(x.text)["observations"]["data"][0]["wind_dir"]

        # Converts wind direction into an angle as a float
        if w == "N":
            return 0.00
        elif w == "NNE":
            return 22.50
        elif w == "NE":
            return 45.00
        elif w == "ENE":
            return 67.50
        elif w == "E":
            return 90.00
        elif w == "ESE":
            return 112.50
        elif w == "SE":
            return 135.00
        elif w == "SSE":
            return 157.50
        elif w == "S":
            return 180.00
        elif w == "SSW":
            return 202.50
        elif w == "SW":
            return 225.00
        elif w == "WSW":
            return 247.50
        elif w == "W":
            return 270.00
        elif w == "WNW":
            return 292.50
        elif w == "NW":
            return 315.00
        elif w == "NNW":
            return 337.50
        else:
            return None


if __name__ == "__main__":

    output_time_local = DownloadData().dl_time_local(data_url)
    output_time_utc = (DownloadData().dl_time_utc(data_url))

    # Print local time in custom format:
    print(output_time_local)
    # Print utc time in seconds since epoch format:
    print(output_time_utc)
    # Print utc time in a standard format (to provide a visual confirmation of correct conversion)
    print(time.asctime(time.gmtime(float(output_time_utc))))

    output_wind_angle = (DownloadData().dl_wind_angle(data_url))
    # Print wind direction as an angle
    print(output_wind_angle)

    # To check if new fields were added correctly:
    output_weather = DownloadData().dl_weather(data_url, image_url)
    # Option to print all of the data as a dictionary:
#    print(output_weather)
    # Confirm it is actually a dictionary, not a string:
    print(type(output_weather))

    # to check the the types of the values in the dictionary:
#    for key in output_weather:
#        print(key, ', ', type(output_weather[key]))
    # to include the downloaded values with the key and key type:
        # print(key, ', ', type(output_weather[key]), ', ', output_weather[key])
