#!/usr/bin/env python3

def dl_jpg_to_b64(image_url):
    
    import requests # to get image from the web
    import shutil   # to save file locally
    import base64   # to convert the jpg to base64

    # Retrieve the url image; use stream = True to guarantee no interruptions.
    r = requests.get(image_url, stream = True)

    # use slice notation to separate the filename from the image link
    filename = image_url.split("/")[-1]

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Create a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)    
        f.close() 
        # Open file with rb ( read binary ) permission.
        with open(filename, "rb") as f:
            # encode the data in the file into base64 
            the_image = base64.b64encode(f.read())
        # To print the base64 without the [b'   '], decode the string to utf-8 format
        print(the_image.decode('utf-8'))
        f.close() 
    else:
        # in case the image isn't retrieved successfully:
        print('Image Couldn\'t be retreived')
