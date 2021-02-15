#!/usr/bin/env python3

import dl_img_conv_b64

# URL of the image being used (Can be changed to whatever you'd like)
image_url = "https://weathercams.airservicesaustralia.com/wp-content/uploads/airports/041529/041529_045.jpg"

# using the method "conv_img_to_b64" from the "DownloadConvert" class, download an image and convert it to base64
output = dl_img_conv_b64.DownloadConvert().conv_img_to_b64(image_url)

print(output)   # print that base64 code to the console
