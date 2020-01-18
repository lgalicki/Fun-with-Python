#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 13:13:38 2020

@author: luciano
This has been implemented in a Jupyter Notebook I called Pandas usage example.
Let's see how it behaves with only pure Python coding.
"""
import pandas as pd

#First we get info about HDI from a first source
print('Retrieving HDI info')
HDI_URL = 'https://countryeconomy.com/hdi'
HDIDFS = pd.read_html(HDI_URL)
HDI = HDIDFS[0]

#Now we get info about GDP (PPP) per capita from a second source
print('Retieving per capita income info')
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
