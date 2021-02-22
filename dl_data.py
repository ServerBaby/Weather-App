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
    * dl_weather - returns all the data as a dictionary in JSON format
    * dl_time_local - extracts a human-readable version of the local 
        time from the BOM data
    * dl_time_utc - extracts the time from the BOM data and expresses 
        it as seconds from epoch.
    * def dl_wind_angle - extracts the wind direction from the BOM 
        data and expresses it as an angle.
"""

import requests
import json
import datetime
import time
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
        The URL of the data to be downloaded from the BOM website.
        Defined outside of the scope of the class.
    'image_url' : str
        The URL of the image to be downloaded from AirServiceAus site.
        Defined outside of the scope of the class.
        
    Methods
    -------
    'dl_weather(data_url, image_url)'
        Downloads the most recent weather conditions at a set location
        as a dictionary; adds three key-value pairs: the base64
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
        Extracts the wind direction from the most recent weather 
        conditions data and returns the direction as an angle (0.0 -
        360.0 degrees).
        Example:  a wind direction of `ESE` returns `112.50`
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
            URL of the data to be downloaded from the BOM website
            Defined outside of the scope of the class.
        'image_url' : str
            URL of the image to be downloaded from AirServiceAus site
            Defined outside of the scope of the class.
        'get_data' : method
            GET request to the specified url.
        'epoch_date' : integer
            UTC time in milli-seconds since epoch.
        'wind_angle' : float
            Wind direction as an angle
        'local_image_b64' : string
            Image of location as a base64 encoded string.
        'weather' : dictionary 
            Dictionary containing all of the downloaded data.
            Initially contains only an exact copy of the most recently  
            uploaded set of data from the relevant page of the BOM 
            website.  The BOM page being downloaded contains a nested
            dictionary, with the desired data located under 
            ["observations"]["data"][0].
            
        Returns
        -------
        'weather' : dictionary (json format)
            The returned dictionary is an updated version of the 
            dictionary that contains the downloaded data from the BOM
            website plus three new key-value pairs (the base64 
            representation of the location image, the time in milli-
            seconds since epoch and the wind direction as an angle) and
            removes the unnecessary "sort order" value (as it is always 
            0 for the most recent dataset).
        The updated weather dictionary is the main output of this 
            module.
            
        Raises
        ------
        status.code if/else statement:
            Checks if the data from the BOM website was retrieved 
            successfully (HTTP Status = 200). If this download fails, 
            (HTTP status code != 200), an error message is printed in 
            the console.
        """

        get_data = requests.get(data_url)

        if get_data.status_code == 200:
        
            weather = json.loads(get_data.text)["observations"]["data"][0]

            weather.update(epoch_date=1000*int(self.dl_time_utc(data_url)))

            weather.update(wind_angle=(self.dl_wind_angle(data_url)))

            li64 = dl_img_conv_b64.DownloadConvert().conv_img_to_b64(image_url)
            weather.update(local_image_b64=li64)

            weather.pop("sort_order", None)

            return weather

        else:
            return str('Data Couldn\'t be retrieved')

    def dl_time_local(self, data_url):
        """
        Method called upon to extract a human-readable version of the 
        local time from the BOM data.
        This method extracts the value in 'local_date_time_full' and
        converts it into the format '%A, %d %B %Y %H:%M:%S'. 
       
        ...
        
        Parameters
        ----------
        'data_url' : str
           URL of the data to be downloaded from the BOM website
           Defined outside of the scope of the class.
        'local_date_time_full' : dictionary key
            Returns the local time that the data was uploaded to the 
            BOM website (in a custom date/time format).
            Defined outside of the scope of the class.
        'get_data' : method
            GET request to the specified url.
        'weather' : dictionary 
            Dictionary containing all of the downloaded data.
            
        Returns
        -------
        't_local' : string
            The local time that the data was uploaded to the BOM 
            website as a string in the format '%A, %d %B %Y %H:%M:%S'.
            
        Raises
        ------
        Not applicable
            Runs in conjunction with dl_weather. dl_weather will raise 
            an error message in the console if the BOM data is unable 
            to be downloaded.
        """

        get_data = requests.get(data_url)
        weather = json.loads(get_data.text)["observations"]["data"][0]

        dd = datetime.datetime
        t_strp_local = dd.strptime(weather["local_date_time_full"], "%Y%m%d%H%M%S")
        t_local = dd.strftime(t_strp_local, '%A, %d %B %Y %H:%M:%S')

        return t_local

    def dl_time_utc(self, data_url):
        """
        Method called upon to extract the Coordinated Universal Time 
        (UTC) from the BOM data.
        This method extracts the value in 'aifstime_utc' and
        then converts it into the format 'seconds since epoch'.

        ...
        
        Parameters
        ----------
        'data_url' : str
           URL of the data to be downloaded from the BOM website
           Defined outside of the scope of the class.
        'aifstime_utc' : dictionary key
            Returns the UTC time that the data was uploaded to the 
            BOM website (in a custom date/time format).
            Defined outside of the scope of the class.
        'get_data' : method
            GET request to the specified url.
        'weather' : dictionary 
            Dictionary containing all of the downloaded data.
            
        Returns
        -------
        't_utc' : float
            The UTC time that the data was uploaded to the BOM website
            as a float in the format seconds since epoch.   
        
        Raises
        ------
        Not applicable
            Runs in conjunction with dl_weather. dl_weather will raise 
            an error message in the console if the BOM data is unable 
            to be downloaded.
        """
    
        get_data = requests.get(data_url)
        weather = json.loads(get_data.text)["observations"]["data"][0]

        dd = datetime.datetime
        t_strp_utc = dd.strptime(weather["aifstime_utc"], "%Y%m%d%H%M%S")
        t_utc = time.mktime(dd.timetuple(t_strp_utc))

        return t_utc

    def dl_wind_angle(self, data_url):
        """
        Method called upon to extract the wind direction from the most 
        recent weather conditions data and return the direction as an 
        angle. 

        This method extracts the value in 'wind_dir' and then converts 
        that value into a float value between 0.0 and 360.0 
        representing the number of degrees in a circle.  If there is no 
        wind, a null value is returned.
         
        ...
        
        Parameters
        ----------
        'data_url' : str
           URL of the data to be downloaded from the BOM website
           Defined outside of the scope of the class.
        'wind_dir' : dictionary key
            Defined on the BOM website as: "Wind direction. Direction
            relative to True North, from which the wind is blowing."
            BOM website (in a custom date/time format).
            Defined outside of the scope of the class.
        'get_data' : method
            GET request to the specified url.
        'weather' : dictionary 
            Dictionary containing all of the downloaded data.
            
        Returns
        -------
        float
            The wind direction converted into a float value between 
            0.0 and 360.0 or, if there is no wind, a null value is 
            returned.
         
        Raises
        ------
        Not applicable
            Runs in conjunction with dl_weather. dl_weather will raise 
            an error message in the console if the BOM data is unable 
            to be downloaded.
        """   

        get_data = requests.get(data_url)
        weather = json.loads(get_data.text)["observations"]["data"][0]

        w = weather["wind_dir"]

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
    """ 
    Function to test this module
    Tests the methods in the class DownloadData:
        - 'dl_weather'
        - 'dl_time_local'
        - 'dl_utc'
        - 'dl_wind_angle'
    This code will only run if the module is run directly (not imported
    by another module).  It can be used as a unit test for this module.
    
    ...

    Attributes
    ----------
    'data_url' : str
       URL of the data to be downloaded from the BOM website
       Defined outside of the scope of the class.
    'image_url' : str
        URL of the image to be downloaded from AirServiceAus site
        Defined outside of the scope of the class.

    Parameters
    ----------
    
    'output_time_local' : string
        The local time that the most recent weather conditions data was 
        uploaded in a neat, human readable format.
        Example: `Monday, 22 February 2021 14:38:00`    
    'output_time_utc' : float
        The time that the most recent weather conditions data was 
        uploaded and returns the value in seconds from epoch.
        Example: `1613929080.0`
    'output_time_utc_neat' : string
        Converts 'output_time_utc' into a standard, human readable 
        format.  Used to confirm that the value in 'output_time_utc'
        has been converted correctly.
        Example: `Sun Feb 21 17:38:00 2021`
    'output_wind_angle' : float
        The wind direction from the most recent weather as an angle.
        Expressed as a float value between 0.0 and 360.0 or null.
        Example:  a wind direction of `ESE` returns `112.5`
    'output_weather' : dictionary
        The most recent weather conditions at a set location as a 
        dictionary; includes the base64 representation of an image 
        that is the current view of that location, UTC time in milli- 
        seconds since epoch, and the wind direction as an angle. 
        Used to confirm that the extra image, time and wind angle 
        fields have been added correctly.

    Returns
    -------
    
    When this module is run as the main function, it prints a copy of 
    these parameters to the console:
        - 'output_time_local'
        - 'output_time_utc'
        - 'output_time_utc_neat'
        - 'output_wind_angle'
        - 'output_weather'
    As 'output_weather' is the main output of this module, the unit 
    test contains 3 extra options to check the contents of the 
    dictionary (including the added fields) that is output when using
     this module inside of another module.  The options available are:
        - Option 1: Prints the output of the main function 
            # Checks that the output is actually a dictionary            
            # Checks all keys and values are present
        - Option 2: Prints the type of the output of the main function
            # Checks that the output is actually a dictionary
        - Option 3: Prints the dictionary keys in the output
            # Checks all (keys) fields have been created
        - Option 4: Prints the output of the main function as key-value
            pairs in the format `key, value`
            # Prints the whole dictionary (similar to option 1) but in 
                a more human readable format  
    """

    output_time_local = DownloadData().dl_time_local(data_url)
    print(output_time_local)
    
    output_time_utc = DownloadData().dl_time_utc(data_url)
    print(output_time_utc)    
    
    output_time_utc_neat = time.asctime(time.gmtime(output_time_utc))
    print(output_time_utc_neat)

    output_wind_angle = (DownloadData().dl_wind_angle(data_url))
    print(output_wind_angle)

    output_weather = DownloadData().dl_weather(data_url, image_url)
        # Select one option to uncomment
    # print(output_weather)                                   # Option 1
    # print(type(output_weather))                             # Option 2
    # for key in output_weather:                              # Option 3
    #    print(key, ', ', type(output_weather[key]))
    # for key in output_weather:                              # Option 4        
    #    print(key, ', ', type(output_weather[key]), ', ', output_weather[key])
