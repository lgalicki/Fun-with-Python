#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receives a file name and creates a zipped backup of it in the backups folder.
If the folder does not exist, it is created. The zip file name will be the name
of the zipped file + date and time.

This script was designed to be ran via command line, preferably being schedule
with crontab. The name of the file to be backed up must be informed as a
parameter when the script is called.

@author: luciano
"""
import os
import datetime
import zipfile
import sys
import traceback
import performance_measure as pm

@pm.performance_measure
def create_zip(file_name):
    '''
    Creates the zip file.

    Parameters
    ----------
    file_name : str
        Should be a valid file in the folder the script is located.

    Raises
    ------
    OSError
        If the informed file name is invalid.

    Returns
    -------
    zip_file_name : str
        Relative path and of the zip file created.

    '''
    # Evaluating the file name - TEMPORARY CODE!
    if not os.path.isfile(file_name):
        raise OSError(f'Invalid file: "{file_name}".')

    # Let's see if the backups directory exists. If it doesn't, let's create it
    if not os.path.exists('backups'):
        os.mkdir('backups')

    # Formatting the file name of the zip file
    date_time = str(datetime.datetime.now())
    date_time = date_time.replace('-', '')
    date_time = date_time.replace(' ', '-')
    date_time = date_time.replace(':', '')
    date_time = date_time[:-7]
    zip_file_name = f'backups/{file_name}_{date_time}.zip'

    # Creating the zipped backup
    backup_zip = zipfile.ZipFile(zip_file_name, 'w')
    backup_zip.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
    backup_zip.close()
    return zip_file_name


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise RuntimeError('Invalid usage. Inform file to be backed up as'
                               ' argument.')

        EX_RES = create_zip(sys.argv[1])
        ZIPPED_NAME = EX_RES[0]
        ELAPSED_TIME = EX_RES[1]
        print(f'{ZIPPED_NAME} created. Elapsed time: {ELAPSED_TIME}.')

    except (OSError, RuntimeError) as exception:
        print(exception)

    except Exception as exception:
        TB = traceback.format_exc()
        print(exception.with_traceback(TB))
