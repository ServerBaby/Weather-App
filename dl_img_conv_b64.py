#!/usr/bin/env python3

"""Download Image & Convert to Base64

This script allows the user to download an image file from the internet 
and convert it into base64 encoding.

This tool is currently confirmed to work on jpg and png files.

This script requires that several pypi modules be installed within the 
Python environment you are running this script in.  These modules are
`requests` to access online content, `shutil` to save the image locally
on your device, and `base64` to do the encoding of the binary data of 
the image into base64.

This file can also be imported as a module and contains the following
functions:

    * __init__ - to construct the main function
    * conv_img_to_b64 - returns the image converted into base64 format.
"""


import requests  
import shutil  
import base64  


class DownloadConvert:      
    """ 
    A class to download an image file from the internet and convert it
    to base64.

    ...

    Attributes
    ----------
    'image_url' : str
        The URL of the image to be downloaded.
        Defined outside of the scope of the class.

    Methods
    -------
    'conv_img_to_b64(image_url)'
        Downloads an online image, then converts it to Base64 and then 
        returns the result.
    """

    def __init__(self):    
        """
        The constructor for DownloadConvert class.
        Only used to construct the class currently.
        """
    
        pass 

    def conv_img_to_b64(self, image_url):     
        """
        Method called upon to download the image and convert it to Base64.

        ...

        Parameters
        ----------
        `image_url` : str
            The URL of the image to be downloaded.
            Defined outside of the scope of the method.
        `returned_object` : file-like object
            Object containing the image URL server's response to the HTTP
            GET request.  `raw` is used to create a file-like object
            representation of the response. Use of raw requires that
            stream=True be set on the request. stream=True guarantees no
            interruptions while downloading the image, avoiding corruption
            of the object being downloaded. Setting decode_content=True
            forces the decompression of the response.raw file-like object.
        `filename` : file object (in binary)
            The shutil.copyfileobj() sends the data from returned_object to
            a local file object with the name `filename'.  A new file is
            created if a file named `filename` doesn't exist.  Any local
            file with the same name will be overwrriten.  The name of the
            file object `filename` is created using slice notation to
            separate the name from the image URL.
        `result` : str [in utf-8 format]
            The string representation of the base64 encoded image.
            Encoded into utf-8 format to return string without the [b' '].

        Raises
        ------
        status.code if/else statement:
            Checks if image was retrieved successfully (HTTP Status = 200).
            If image download fails, (HTTP status code != 200), an error
            message is printed in the console.
        """
    
        returned_object = requests.get(image_url, stream=True)
        filename = image_url.split("/")[-1]
        result = ""         

        if returned_object.status_code == 200:   
            returned_object.raw.decode_content = True

            with open(filename, 'wb') as f:     
                shutil.copyfileobj(returned_object.raw, f)   
            f.close()                           

            with open(filename, "rb") as f:      
                result = base64.b64encode(f.read()).decode('utf-8')  
            f.close()                        

        else:       
            print('Image Couldn\'t be retrieved')

        return result       


if __name__ == "__main__":      # an internal test; when module is run directly, do the following:
    """ 
    Function to test this module
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
    conv_img_to_b64(image_url)
        Downloads an online image, then converts it to Base64 and then 
        returns the result.
    """

    image_url = "https://imgs.xkcd.com/comics/documents.png"    
    """ (sample image credit: XKCD) """
        
    output = DownloadConvert().conv_img_to_b64(image_url)
    
    print(output)
