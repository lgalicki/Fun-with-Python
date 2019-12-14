'''
Use this to clear screen in Jupyter Notebooks and in terminal
'''

from os import system #For screen cleaning.
from IPython.display import clear_output #For screen cleaning in JupyterNotebook.

def clear_screen():
    '''
    Issues both cleaning commands: for Jupyter Notebooks and Linux terminal.
    '''
    clear_output()
    _ = system('clear')
