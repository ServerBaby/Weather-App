#!/usr/bin/env python3

""" NOTE: THIS IS A DRAFT ONLY VERSION OF THIS FILE """
""" linked modules not all uploaded yet so don't try to run """
#!/usr/bin/env python3

"""Download and manipulate BOM Data

This script allows the user to download the most recently available
weather conditions for a specific location from the Bureau of
Meteorology (BOM) website, manipulate that data including adding
a base64 encoded image of the location at that time, and then converts
that data back into json format.

Currently being tested on data from Toowoomba Wellcamp Airport.
`http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json`

This script requires that several pypi modules be installed within the
Python environment you are running this script in.  These modules are
`requests` to access online content, `json` to convert data to and from
json format, and `datetime` to change how dates & times are displayed.

This script also requires two accompanying custom modules be installed.
These modules are: `dl_img_conv_b64` (to download an image and convert
to base64) and `wellcamp_urls` (containing the links to the most recent
data and image from the target location, Wellcamp Airport).

The dl_data python file can be imported as a module and contains the
following functions:

    * __init__ - to construct the main function
    * dl_weather - returns the data as a dictionary in JSON format
    * dl_time - extracts a human-readable version of the local time
        from the BOM data
"""

import requests
import json
import datetime
import dl_img_conv_b64
from wellcamp_urls import image_url, data_url


class DownloadData:
    """
    A class to download the most recent weather conditions at a
    specific location.  Output in json format.


    ...

    Attributes
    ----------
    'data_url' : str
        The URL of the data to be downloaded from the BOM website
        Defined outside of the scope of the class.
    'image_url' : str
        The URL of the image to be downloaded from AirServiceAus site
        Defined outside of the scope of the class.

    Methods
    -------
    'dl_weather(data_url, image_url)'
        Downloads the most recent weather conditions at a set location
        as a dictionary, adds to that data the base64 representation of
        an image that is the current view of that location.
     'dl_time(data_url)'
        Extracts the time that the most recent weather conditions data
        was uploaded and returns it in a neat, human readable format.
    """

    def __init__(self):
        """
        The constructor for DownloadData class.
        Only used to construct the class currently.
        """

        pass

    def dl_weather(self, data_url, image_url):
        """
        Method called upon to create a dictionary of current weather
        conditions at a specific location.
        This method downloads the data from the BOM website, extracts
        the required data and places it into a dictionary, downloads
        an image from AirServices Australia, converts that image into
        a base64 encoded string, and then adds that string to the
        dictionary.

        ...

        Parameters
        ----------
        'data_url' : str
           The URL of the data to be downloaded from the BOM website
           Defined outside of the scope of the class.
        'image_url' : str
            The URL of the image to be downloaded from AirServiceAus site
            Defined outside of the scope of the class.

        """
        # Gets information from website and turns it into a usable format
        # [0] is the position of the most recent dataset inserted into the list of datasets ["data"]
        x = requests.get(data_url)
        y = json.loads(x.text)["observations"]["data"][0]
        # adds base64 image to data
        y.update(local_image_b64=dl_img_conv_b64.DownloadConvert().conv_img_to_b64(image_url))
        # Removes the unnecessary "sort order" value;
        y.pop("sort_order", None)

        return str(y)

    def dl_time(self, data_url):
        # defined in previous function
        x = requests.get(data_url)
        y = json.loads(x.text)["observations"]["data"][0]["local_date_time_full"]

        # Creates a heading for displaying the current dataset with it's time as part of the heading
        t1 = datetime.datetime.strptime(y, "%Y%m%d%H%M%S")
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
    dl_weather(data_url)
        Downloads an online image, then converts it to Base64 and then 
        returns the result.
    """

    output_weather = DownloadData().dl_weather(data_url, image_url)
    output_time = DownloadData().dl_time(data_url)
    print(output_time + "\n" + output_weather)
