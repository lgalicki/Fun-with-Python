#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:26:44 2020

@author: Luciano Galicki
Basend on code found at:
https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

Validates an e-mail address
"""

import re

def check(em_address):
    """
    Validates an e-mail address.

    Parameters
    ----------
    em_address : string
        The e-mail address to be validated.

    Returns
    -------
    bool
        True if valid, False if invalid.

    """
    # Crearing a regular expression for validation
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex, em_address):
        return True
    return False


if __name__ == '__main__':
    EMAIL = input('Inform e-mail address to be validated: ')
    if check(EMAIL):
        print(f'{EMAIL} is valid')
    else:
        print(f'{EMAIL} is invalid.')
