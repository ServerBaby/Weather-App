#!/usr/bin/env python3

"""Download and manipulate BOM Data

The dl_data python file can be imported as a module and contains the
following functions:

    * __init__ - to construct the main function
    * dl_weather - returns the data as a dictionary in JSON format
    * dl_time_local - extracts a human-readable version of the local time
        from the BOM data
    * dl_time_utc - extracts the time from the BOM data and expresses it
        as seconds from epoch.
"""

import requests
import json
import datetime
import time
import dl_img_conv_b64
from wellcamp_urls import image_url, data_url


class DownloadData:   # Output in json format. ???????
    """
    Output in json format. ???????

    Attributes
    ----------
    'data_url' : str -  The URL of the data to be downloaded from the BOM website
    'image_url' : str - The URL of the image to be downloaded from AirServiceAus site

    Methods
    -------
    'dl_weather(data_url, image_url)'
        Downloads the most recent weather conditions at a set location as a dictionary
     'dl_time(data_url)'
        Extracts the time that the most recent weather conditions data was uploaded
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

            # converts utc time to seconds since epoch
            y.update(epoch_date=1000*int(eval((self.dl_time_utc(data_url)))))

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


if __name__ == "__main__":

    output_time_local = DownloadData().dl_time_local(data_url)
    output_time_utc = (DownloadData().dl_time_utc(data_url))

    # Print local time in custom format:
    print(output_time_local)
    # Print utc time in seconds since epoch format:
    print(output_time_utc)
    # Print utc time in a standard format (to provide a visual confirmation of correct conversion)
    print(time.asctime(time.gmtime(float(output_time_utc))))

    # To check if new fields were added correctly:
    output_weather = DownloadData().dl_weather(data_url, image_url)
    # Option to print all of the data as a dictionary:
    print(output_weather)
    # Confirm it is actually a dictionary, not a string:
    print(type(output_weather))

    # to check the the types of the values in the dictionary:
    for key in output_weather:
        print(key, ', ', type(output_weather[key]))
    # to include the downloaded values with the key and key type:
        # print(key, ', ', type(output_weather[key]), ', ', output_weather[key])
