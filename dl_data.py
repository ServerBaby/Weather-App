#!/usr/bin/env python3

"""Download BOM Data and convert to JSON

This script allows the user to download the most recently available
weather conditions for a specific location from the Bureau of
Meteorology (BOM) website.

Currently being tested on data from Toowoomba Wellcamp Airport.
`http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json`

This script requires that several pypi modules be installed within the
Python environment you are running this script in.  These modules are
`requests` to access online content, `json` to convert data to and from
json format, and `datetime` to change how dates & times are displayed.

This file can also be imported as a module and contains the following
functions:

    * __init__ - to construct the main function
    * dl_weather - returns the BOM data as a dictionary in JSON format
"""

import requests
import json
import datetime

bom_url = "http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json"


class DownloadData:
    """
    A class to download the most recent weather conditions as json data
    from the BOM Website and save it how I want it.

    ...

    Attributes
    ----------
    'bom_url' : str
        The URL of the data to be downloaded from the BOM website
        Defined outside of the scope of the class.

    Methods
    -------
    'dl_weather(bom_url)'
        Downloads the most recent weather conditions at a set location
        as a dictionary, adds to that dictionary the base64
        representation of an image that is the current view of that
        location
    """

    def __init__(self):
        """
        The constructor for DownloadData class.
        Only used to construct the class currently.
        """

        pass

    def dl_weather(self, bom_url):

        # Gets information from website and turns it into a usable format
        x = requests.get(bom_url)
        y = json.loads(x.text)["observations"]["data"]

        # [0] is the position of the most recent dataset inserted into the list of datasets ["data"]
        z = y[0]

        # Removes the unnecessary "sort order" value;
        z.pop("sort_order", None)

        return str(z)

    def dl_time(self, bom_url):
        # defined in previous function
        x = requests.get(bom_url)
        y = json.loads(x.text)["observations"]["data"]
        z = y[0]

        # Creates a heading for displaying the current dataset with it's time as part of the heading
        t1 = datetime.datetime.strptime(z["local_date_time_full"], "%Y%m%d%H%M%S")
        t2 = datetime.datetime.strftime(t1, '%A, %d %B %Y %H:%M:%S')

        # prints the local time that the data was uploaded to the BOM website
        return t2


if __name__ == "__main__":
    """ 
    Function to test the functions in this module
    Uses the method conv_img_to_b64 from the class DownloadConvert to
    downloads and convert a sample image into a utf-8 encoded base64
    string.  This string is then printed to the console/terminal.
    This code will only run if the module is run directly (not imported
    by another module).  It can be used as a unit test for this module.

    ...

    Attributes
    ----------
    image_url : str
        URL of the sample image to be downloaded. 
    output: str
        The string representation of the base64 encoded sample image.
        Encoded into utf-8 format to return string without the [b' '].

    Methods
    -------
    dl_weather(bom_url)
        Downloads an online image, then converts it to Base64 and then 
        returns the result.
    """

    output_weather = DownloadData().dl_weather(bom_url)
    output_time = DownloadData().dl_time(bom_url)
    print(output_time + "\n" + output_weather)
