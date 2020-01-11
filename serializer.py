#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 11:40:16 2020

@author: luciano
Interface for serializing and deserializing data into/from a file.
"""
import json
import pickle
import functools

def evaluate_protocol(func):
    """
    Decorator to evaluate if the informed protocol is valid.
    """
    @functools.wraps(func)
    def wrapper_evaluate_protocol(*args, **kwargs):
        if not isinstance(args[0], str):
            raise TypeError(f'Invalid type in protocol. Should be str, is "{type(args[0])}"')

        if (args[0] not in ['json', 'pickle']):
            raise ValueError(f'Invalid protocol. Should be "json" or "pickle", is "{args[0]}"')

        return func(*args, **kwargs)

    return wrapper_evaluate_protocol


@evaluate_protocol
def serialize(protocol, py_obj, file):
    """
    Serializes the given object using the given protocol in the informed file.

    Parameters
    ----------
    protocol : str
        'json' or 'pickle'. It's case sensistive.
    py_obj : Misc types
        The object to be serialized. Notice JSON doesn't support all Python
        types nor user created objects.
    file : str
        Name of the file to be written.

    Returns
    -------
    None.
    """
    if protocol == 'json':
        with open(file, 'w') as o_f:
            json.dump(py_obj, o_f, ensure_ascii=False, indent=4)

    else:
        with open(file, 'wb') as o_f:
            pickle.dump(py_obj, o_f)

@evaluate_protocol
def deserialize(protocol, file):
    """
    Deserializes the data in the given file using the informed protocol.

    Parameters
    ----------
    protocol : str
        "json" or "pickle". It's case sensitive.
    file : str
        The file to be opened and deserialized.

    Returns
    -------
    The deserialized python object.
    """
    if protocol == 'json':
        with open(file) as o_f:
            py_obj = json.load(o_f)
            return py_obj

    else:
        with open(file, 'rb') as o_f:
            py_obj = pickle.load(o_f)
            return py_obj
