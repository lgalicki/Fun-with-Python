#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 13:13:38 2020

@author: luciano
This has been implemented in a Jupyter Notebook I called Pandas usage example.
Let's see how it behaves with only pure Python coding.

This has been updated to generate an interactive scatter plot in an HTML file.
"""
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#First we get info about HDI from a first source
print('Retrieving HDI info')
HDI_URL = 'https://countryeconomy.com/hdi'
HDIDFS = pd.read_html(HDI_URL)
HDI = HDIDFS[0]

#Now we get info about GDP (PPP) per capita from a second source
print('Retrieving per capita income info')
INCOME_URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita'
INCOMEDFS = pd.read_html(INCOME_URL)
INCOME = INCOMEDFS[4]

#Formatting the HDI info to easily match it to the income info
HDI.drop(['HDI Ranking', 'HDI Ranking.1', 'Ch.'], 1, inplace=True)
HDI.rename(columns={'Countries': 'Country'}, inplace=True)
HDI['Country'] = HDI['Country'].str.rstrip(' [+]')

#Formatting the income info to easily match it to the HDI info
INCOME.drop(['Rank', 'Year'], 1, inplace=True)
INCOME.columns = ['Country', 'GDP (PPP) percapita (U$)']

#Merging the two DataFrames and eliminating useless numeric index
MERGEDDF = HDI.merge(INCOME, left_on='Country', right_on='Country')
MERGEDDF.set_index('Country', inplace=True)

#It's time to calculate the correlation
CORR = MERGEDDF.corr().iloc[0][1]
print(f'The correlation between HDI and GDP (PPP) per capita is {CORR}')

#Now it's time to generate our scatter plot
X_VALUES = MERGEDDF['HDI']
Y_VALUES = MERGEDDF['GDP (PPP) percapita (U$)']
HOVER_VALUES = MERGEDDF.index

#Defining layout
print('Generating scatter plot')
MARKER = dict(size=5, line={'width':1})
LAYOUT = go.Layout(title="HDI x GDP (PPP) percapita (U$)",
                   xaxis=dict(title="HDI"),
                   yaxis=dict(title="Per capita income"))

#Defining graphical object, determining its layout and data
DATA = [go.Scatter(x=X_VALUES, y=Y_VALUES, hovertext=HOVER_VALUES,
                   mode='markers', marker=MARKER)]
FIG = go.Figure(data=DATA, layout=LAYOUT)

#Generating the graph
pyo.plot(FIG, filename='HDI x Per capita income.html')
