#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:46:37 2020

@author: luciano
We'll use a dummy API to get some JSONed data and test stuff. Here we read a
pseudo list of task to be done and print out only those that were completed.
"""
import requests

#Requesting data via GET
CONTENT = requests.get("http://jsonplaceholder.typicode.com/todos")

#Decoding JSONed returned data
PY_CONTENT = CONTENT.json()

#Running through the dictionaries in the unJSONed list and printing stuff
for task in PY_CONTENT:
    if task['completed'] is True:
        print(task['title'])
