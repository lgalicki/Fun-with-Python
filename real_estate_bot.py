#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:57:27 2020

@author: luciano

This bot will access zapimoveis.com.br, read all the real estate available
based on the information that was given and generate a graph showing the price
per m² in every neighbourhood of the informed CITY.
"""
import requests
from bs4 import BeautifulSoup

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
    if brk_nh_text[1].lower() == CITY.lower():
        return brk_nh_text[0]

    return brk_nh_text[1]


def parse_html(html):
    '''
    Validates HTML and, if it's good, extracts information from it.

    Parameters
    ----------
    html : str
        Must contain HTML from the pages retrieved.

    Returns
    -------
    True if the page had results, else returns False.

    '''
    soup = BeautifulSoup(html, 'html.parser')

    #Here we check if we reached those blank results.
    if soup.h1.text == 'Oops. Não encontramos resultados para esta busca!':
        return False

    #Extracting raw info
    soup.find_all()
    prices = soup.find_all('p', class_='simple-card__price js-price'
                           ' heading-regular heading-regular__bolder align-left')

    sizes = soup.find_all('div', class_='simple-card__actions')

    nhs = soup.find_all('p', class_='color-dark text-regular simple-card__address')

    #Let's make sure we captured the same ammount of prices, sizes and neighbourhoods
    if len(prices) != len(sizes) != len(nhs):
        raise Exception(f'Error parsing HTML. Different qt. of elem.:'
                        ' {len(prices)} {len(sizes)} {len(neighs)}')

    #Cleaning up the raw data
    f_prices = [format_price(price) for price in prices]
    f_sizes = [format_size(size) for size in sizes]
    f_nhs = [format_neighbourhood(nh) for nh in nhs]

    zipped = zip(f_prices, f_sizes, f_nhs)

    return zipped

if __name__ == '__main__':
    #Setting up the variable parts of the URL
    CITY = 'londrina'
    COUNTY = 'pr'
    TRANS = 'venda'
    TYPE_UN = 'apartamentos'
    LOC = f'{COUNTY}+{CITY}'
    PG = 1
    URL = f'https://www.zapimoveis.com.br/{TRANS}/{TYPE_UN}/{LOC}/?pagina={PG}'

    #Setting HEADERS so there will be no 403 error
    HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) '
                            'Gecko/20100101 Firefox/72.0'}

    #Now let's loop through the pages
    RESPONSE = requests.get(url=URL, headers=HEADERS)
    GOOD_PAGE = True
    while RESPONSE.ok and GOOD_PAGE:
        #While parsing we must check if the returned page is good. By good I
        #mean a page with results. The site often returns blank pages with 200
        #return code. When we reach these blank pages there's no need to keep
        #on going.
        GOOD_PAGE = parse_html(RESPONSE.text)

        if GOOD_PAGE:
            print(tuple(GOOD_PAGE))
            PG += 1
            URL = f'https://www.zapimoveis.com.br/{TRANS}/{TYPE_UN}/{LOC}/' \
            f'?pagina={PG}'
            RESPONSE = requests.get(url=URL, headers=HEADERS)
