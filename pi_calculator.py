"""
Let's calculate pi using several different methods.'
"""
import sys
import cleaner

def catch_num(message):
    '''
    A simple generic function to capture numbers on screen.
    Parameters
    ----------
    msg : string
        Message to be shown along the input.

    Returns
    -------
    num: int
    '''
    while True:
        try:
            num = int(input(message))
        except:
            continue
        else:
            break
    return num


def gregory_leibniz(nr_iterations):
    '''
    π = (4/1) - (4/3) + (4/5) - (4/7) + (4/9) - (4/11) + (4/13) - (4/15) ...
    Parameters
    ----------
    nr_iterations : int
        The number of times you wish to iterate through the algorythm

    Returns
    -------
    Pi: float
    '''
    divisor = 1
    signal = 1
    pi = float()
    for _ in range(nr_iterations):
        pi += (4 / divisor) * signal
        signal *= -1
        divisor += 2
    return pi


def nilakantha(nr_iterations):
    '''
    π = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - 4/(8*9*10) + 4/(10*11*12) - 4/(12*13*14) ...
    Parameters
    ----------
    nr_iterations : int
        The number of times you wish to iterate through the algorythm

    Returns
    -------
    Pi: float
    '''
    pi = 3
    signal = 1
    var = 2
    for _ in range(nr_iterations):
        pi += 4 / ((var) * (var + 1) * (var + 2)) * signal
        signal *= -1
        var += 2
    return pi


if __name__ == '__main__':
    OPTION = str()

    while OPTION not in ['1', '2', 'x', 'X']:
        cleaner.clear_screen()
        print('Chooose your method:')
        print('--------------------')
        print('1. Gregory Leibniz series')
        print('2. Nilakantha series')
        print('x. Exit')
        OPTION = input('Choose your poison: ')

    if OPTION in ['x', 'X']:
        sys.exit()

    elif OPTION == '1':
        MSG = 'How many times do you want to iterate through the algorithm? '
        NR_ITER = catch_num(MSG)
        RESULT = gregory_leibniz(NR_ITER)
        print(f'Pi is ≃ {RESULT}')

    elif OPTION == '2':
        MSG = 'How many times do you want to iterate through the algorithm? '
        NR_ITER = catch_num(MSG)
        RESULT = nilakantha(NR_ITER)
        print(f'Pi is ≃ {RESULT}')
        