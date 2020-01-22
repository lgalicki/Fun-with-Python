#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:57:27 2020

@author: luciano

This bot will access zapimoveis.com.br, read all the real estate available
based on the information that was given and generate a graph showing the price
per m² in every neighbourhood of the informed CITY.
"""
import sys
import requests
from bs4 import BeautifulSoup
import unidecode
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

def format_price(price):
    '''
    Formats the prices.

    Parameters
    ----------
    price : tag
        The HTML tag that contains the price.

    Returns
    -------
    price : int
        The price in numeric format. If it's impossible to deternine it, None
        is returned.

    '''
    price_text = price.text.replace('\n', '')
    price_text = price_text.strip()
    price_text = price_text.lstrip('R$ ')
    price_text = price_text.replace('.', '')

    if price_text.isnumeric():
        return int(price_text)
    return None


def format_size(size):
    '''
    Formats the sizes.

    Parameters
    ----------
    size : tag
        The HTML tag that contains the size.

    Returns
    -------
    size : int
        The size in numeric format.

    '''
    size_text = size.span.text.replace('\n', '')
    size_text = size_text.strip()
    size_text = size_text.rstrip(' m²')
    size_text = size_text.replace('.', '')
    size_text = [int(s) for s in size_text.split() if s.isdigit()][0]

    return int(size_text)


def format_neighbourhood(neighbourhood):
    '''
    Formats the neighbourhood.

    Parameters
    ----------
    nh : tag
        The HTML tag that contains the size.

    Returns
    -------
    neighbourhood : str
        The neighbourhood.

    '''
    nh_text = neighbourhood.text
    brk_nh_text = nh_text.split(',')
    brk_nh_text = [x.strip() for x in brk_nh_text]

    dec_city = unidecode.unidecode(CITY).title()

    if unidecode.unidecode(brk_nh_text[1]).title() == dec_city:
        return unidecode.unidecode(brk_nh_text[0]).title()

    return unidecode.unidecode(brk_nh_text[1]).title()


def parse_html(html):
    '''
    Validates HTML and, if it's good, extracts information from it.

    Parameters
    ----------
    html : str
        Must contain HTML from the pages retrieved.

    Returns
    -------
    A tuple (zip object, total of items) if the page had results, else returns
    a tuple too, but (False, 0).

    '''
    soup = BeautifulSoup(html, 'html.parser')

    # Here we check if we reached those blank results.
    if soup.h1.text == 'Oops. Não encontramos resultados para esta busca!':
        return False, 0
    total_items = soup.h1.text.split()[0]

    # Extracting raw info
    soup.find_all()
    prices = soup.find_all('p', class_='simple-card__price js-price'
                           ' heading-regular heading-regular__bolder align-left')

    sizes = soup.find_all('div', class_='simple-card__actions')

    nhs = soup.find_all('p', class_='color-dark text-regular simple-card__address')

    # Let's make sure we captured the same ammount of prices, sizes and neighbourhoods
    if len(prices) != len(sizes) != len(nhs):
        raise Exception(f'Error parsing HTML. Different qt. of elem.:'
                        ' {len(prices)} {len(sizes)} {len(neighs)}')

    #Cleaning up the raw data
    f_prices = [format_price(price) for price in prices]
    f_sizes = [format_size(size) for size in sizes]
    f_nhs = [format_neighbourhood(nh) for nh in nhs]

    zipped = zip(f_prices, f_sizes, f_nhs)

    return zipped, total_items


if __name__ == '__main__':
    # Setting up the variable parts of the URL
    CITY = 'curitiba'
    COUNTY = 'pr'
    TRANS = 'venda'
    #TYPE_UN = 'apartamentos'
    TYPE_UN = 'casas'
    LOC = f'{COUNTY}+{CITY}'
    PG = 1
    URL = f'https://www.zapimoveis.com.br/{TRANS}/{TYPE_UN}/{LOC}/?pagina={PG}'

    # Setting HEADERS so there will be no 403 error
    HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) '
                            'Gecko/20100101 Firefox/72.0'}

    # Now let's loop through the pages
    ITEMS = tuple()
    RESPONSE = requests.get(url=URL, headers=HEADERS)
    PARSE_RETURN = (True, 0)
    while RESPONSE.ok and PARSE_RETURN[0]:
        # While parsing we must check if the returned page is good. By good I
        # mean a page with results. The site often returns blank pages with 200
        # return code. When we reach these blank pages there's no need to keep
        # on going.
        PARSE_RETURN = parse_html(RESPONSE.text)

        if PARSE_RETURN[0]:
            PAGE_CONTENTS = PARSE_RETURN[0]
            TOT_ITEMS = PARSE_RETURN[1]
            ITEMS += (tuple(PAGE_CONTENTS))
            PG += 1
            URL = f'https://www.zapimoveis.com.br/{TRANS}/{TYPE_UN}/{LOC}/' \
            f'?pagina={PG}'
            RESPONSE = requests.get(url=URL, headers=HEADERS)

            print(f'Fetching info. {len(ITEMS)} items of {TOT_ITEMS} so far.',
                  end='\r')

    # Now let's set our DataFrame
    DF = pd.DataFrame(ITEMS, columns=['Price', 'Size', 'Neighbourhood'])
    DF.dropna(inplace=True)
    DF['Price m²'] = [int(price / size) for size, price in zip(DF['Size'], DF['Price'])]

    # Generating and formatting a serie with m² mean per neighbourhood
    GROUPED_DF = DF.groupby('Neighbourhood')
    MEAN_SERIES = GROUPED_DF['Price m²'].mean()
    MEAN_SERIES = MEAN_SERIES.astype('int64')

    # Generating the bar graph
    X_AXIS = list(MEAN_SERIES.index)
    Y_AXIS = MEAN_SERIES.values
    LAYOUT = go.Layout(title='Average price per m²', xaxis=dict(title='Neighbourhood'),
                       yaxis=dict(title='R$ per m²'))
    DATA = [go.Bar(x=X_AXIS, y=Y_AXIS)]
    FIG = go.Figure(data=DATA, layout=LAYOUT)
    pyo.iplot(FIG, filename='AvgPerNgh.html')

    # Asking if the user wants to see more details
    MORE_DETAILS = str()
    while MORE_DETAILS.lower() not in ('y', 'n'):
        MORE_DETAILS = input('See details about a neighbourhood? (y/n): ')

        if MORE_DETAILS.lower() == 'n':
            print('Good-bye')
            sys.exit()

        elif MORE_DETAILS.lower() == 'y':
            NH_DET = str()
            while NH_DET not in list(MEAN_SERIES.index) or NH_DET.lower() == 'q':
                ND_DET = input('Name of neighbourhood as shown in the graph (q to quit): ')
                NH_DET = unidecode.unidecode(NH_DET).title()

                if NH_DET.lower() == 'q':
                    print('Good-bye')
                    sys.exit()

                elif NH_DET in list(MEAN_SERIES.index):
                    #Defining layout
                    LAYOUT = go.Layout(title=f'Items in {NH_DET}',
                                       xaxis=dict(title="Price (R$)"),
                                       yaxis=dict(title="Size (m²"))

                    # Creating a DF for the specific neighbourhood
                    NH_DF = DF[DF['Neighbourhood'] == NH_DET]

                    # And the graph for the specific neighbourhood
                    DATA = [go.Scatter(x=NH_DF['Price'], y=NH_DF['Size'],
                                       mode='markers',)]
                    FIG = go.Figure(data=DATA, layout=LAYOUT)
                    pyo.iplot(FIG, filename=f'{NH_DET}.html')

                    MORE_DETAILS = str()
