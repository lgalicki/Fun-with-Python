#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:49:45 2020

@author: Luciano Galicki

This module contains a decorator you can use to measure the time it takes for
your functions to be executed.
"""
import time
from datetime import timedelta
import functools

def performance_measure(func):
    '''
    A decorator that will calculate the amount of time a function takes to be
    executed.

    Parameters
    ----------
    func : function
        The function to be decorated and measured.

    Returns
    -------
    tuple
        It contais two positions: the return of the decorated function is placed
        in the first postion, and in the second the ammount of time calculated
        by this decorator in timedelta format.

    '''

    @functools.wraps(func)
    def wrapper_performance_measure(*args, **kwargs):
        '''
        Wrapper function of the decorator.
        '''
        ini_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - ini_time
        formatted_time = timedelta(seconds=elapsed_time)
        return result, formatted_time

    return wrapper_performance_measure


if __name__ == ('__main__'):
    @performance_measure
    def example(secs):
        '''
        Created to demonstrate the usage of the decorator.
        '''
        time.sleep(secs)
        return [1, 2, 3], ('a', 'b', 'c')

    RES = example(2)
    print(f'Function returned: {RES[0]}')
    print(f'Its execution time was: {RES[1]}')
