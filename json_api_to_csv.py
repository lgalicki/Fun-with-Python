#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 13:26:20 2020

@author: luciano
This is an example of how to get JSONed information via an API and saving it
in a CSV file.
"""
import csv
import requests

#Requesting data via GET
CONTENT = requests.get('https://jsonplaceholder.typicode.com/users')

#DECODING JSONed returned data
PY_OBJ = CONTENT.json()

#Opening the file, interpreting the dictionary and writing CSV lines
with open('json_api_csv.csv', 'w') as o_f:
    WRITER = csv.writer(o_f)
    WRITER.writerow(['Name', 'City', 'GPS coordinates', 'Company\'s name'])

    for item in PY_OBJ:
        row = list()
        row.append(item['name'])
        row.append(item['address']['city'])
        row.append(f"{float(item['address']['geo']['lat']),float(item['address']['geo']['lng'])}")
        row.append(item['company']['name'])
        WRITER.writerow(row)

print('Done!')
