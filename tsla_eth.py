#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 15:40:57 2020

@author: luciano
Here we'll capture ETHer's historical value and compare it to Tesla's stocks in
a line graph. The info will be captured from two different websites, parsed
with Pandas and displayed graphically with Plotly.

ETHer is a crypto-currency.
"""
from datetime import datetime
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#Importing data into the TSLA DataFrame and formatting it
print('Retrieving TSLA information')
TSLA_URL = 'https://finance.yahoo.com/quote/TSLA/history?p=TSLA'
TSLA_DFS = pd.read_html(TSLA_URL)
TSLA = TSLA_DFS[0]

print('Formatting TSLA information')
TSLA.drop(['Open', 'High', 'Low', 'Adj Close**', 'Volume'], 1, inplace=True)
TSLA.drop(100, inplace=True)
TSLA.columns = ['Date', 'TSLA Value']


#Calculating initial and final data for ETH's URL based on TSLA's dates
INI_DATE = TSLA['Date'][99]
END_DATE = TSLA['Date'][0]

DATE_OBJECT = datetime.strptime(INI_DATE, '%b %d, %Y').date()
INI_DATE = DATE_OBJECT.strftime("%Y%m%d")

DATE_OBJECT = datetime.strptime(END_DATE, '%b %d, %Y').date()
END_DATE = DATE_OBJECT.strftime("%Y%m%d")


#Importing data into the ETH DataFrame and formatting it
print('Retrieving ETH information')
ETH_URL = f'https://coinmarketcap.com/currencies/ETHereum/historical-data/?start={INI_DATE}&end={END_DATE}'
ETH_DFS = pd.read_html(ETH_URL)
ETH = ETH_DFS[2]

print('Formatting ETH information')
ETH.drop(['Open*', 'High', 'Low', 'Volume', 'Market Cap'], 1, inplace=True)
ETH.columns = ['Date', 'ETH Value']


#Merging the two DataFrames and sorting asceding by date
print('Merging and formatting merge')
MERGED_DF = ETH.merge(TSLA, left_on='Date', right_on='Date')

for pos, date in enumerate(MERGED_DF['Date']):
    MERGED_DF['Date'][pos] = datetime.strptime(date, '%b %d, %Y').date()

MERGED_DF.sort_values('Date', inplace=True)


#Setting the data for the two lines
print('Setting up the graphic')
X_VALUES = MERGED_DF['Date']

Y_VALUES = MERGED_DF['ETH Value']
TRACE1 = go.Scatter(x=X_VALUES, y=Y_VALUES, mode='lines', name='ETH')

Y_VALUES = MERGED_DF['TSLA Value']
TRACE2 = go.Scatter(x=X_VALUES, y=Y_VALUES, mode='lines', name='TSLA')

DATA = [TRACE1, TRACE2]


#Formatting for the graph
LAYOUT = go.Layout(title='ETH and TSLA price', yaxis=dict(title='U$'))


#And finally launching it
FIG = go.Figure(data=DATA, layout=LAYOUT)
pyo.plot(FIG, filename='TSLA x ETH.html')
