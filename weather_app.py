#!/usr/bin/env python3

import requests
import json
import datetime

# Gets information from website and turns it into a usable format
x = requests.get('http://www.bom.gov.au/fwo/IDQ60801/IDQ60801.99435.json')
y = json.loads(x.text)["observations"]["data"]

# [0] is the position of the most recent dataset inserted into the list of datasets ["data"] 
z = y[0]

# Creates a heading for displaying the current dataset with it's time as part of the heading
t1 = datetime.datetime.strptime(z["local_date_time_full"], "%Y%m%d%H%M%S")
t2 = datetime.datetime.strftime(t1, '%A, %d %B %Y %H:%M:%S')
print("{:<25}{}".format('Current Local Conditions',t2))

# Removes the unnecessary "sort order" value; prints the current dataset
z.pop("sort_order", None)
for k, v in z.items():
    print(("{}: ".format(k)).ljust(25, " ") + "{}".format(v))
