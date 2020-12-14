#!/usr/bin/env python3

import requests  # to get image from the web
import shutil  # to save file locally
import base64  # to convert the jpg to base64


class DownloadConvert:      # A class to download an image file from the internet and convert it to base64

    def __init__(self):     # Method initiating the DownloadConvert class
        pass                # this method doesn't do anything else other than creating the class currently

    def conv_img_to_b64(self, image_url):     # Method called upon to download the image and convert it to Base64
        # requires the variable "image_url" to be defined in whatever code the method will be acting on
        # "requests.get()" to retrieve the url image from the internet; use stream=True to guarantee no interruptions.
        returned_image = requests.get(image_url, stream=True)
        # use slice notation to separate the filename from the image link and remove the leading "/"
        filename = image_url.split("/")[-1]
        result = ""         # Creates the variable "result"

        if returned_image.status_code == 200:   # Check if image was retrieved successfully, that is HTTP Status = 200
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            returned_image.raw.decode_content = True

            with open(filename, 'wb') as f:     # creates a file in binary format
                # note: it overwrites any local file with the same name
                shutil.copyfileobj(returned_image.raw, f)   # saves the image file locally in this new file
            f.close()                           # closes file, because files shouldn't be left open

            with open(filename, "rb") as f:     # open the file in binary format for use
                the_image = base64.b64encode(f.read())      # encode the data in the file into base64
                result = the_image.decode('utf-8')  # decode string to utf-8 format to return without the [b' ']
            f.close()                           # closes file, because files shouldn't be left open

        else:       # if image download fails, HTTP status code != 200, print error message:
            print('Image Couldn\'t be retrieved')

        return result       # the "result" variable now holds the base64 encoded version of the downloaded image file


if __name__ == "__main__":      # an internal test; when module is run directly, do the following:
    image_url = "https://imgs.xkcd.com/comics/documents.png"    # sample image expressing my dislike of naming things
    # the method conv_img_to_b64 in the DownloadConvert class acts on the given URL to convert it to base64:
    output = DownloadConvert().conv_img_to_b64(image_url)
    print(output)   # prints the base64 version of the image to the console
