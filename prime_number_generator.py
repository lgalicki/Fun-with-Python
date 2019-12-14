def prime_list(qt_asked):
    '''
    Returns a list of primes.
    INPUT: quantity of primes to be returnes
    OUTPUT: list with prime numbers
    '''
    plist = list() #list of prime numbers discovered
    tested_number = 2 #number which will be tested to see if it's prime 
    
    while len(plist) < int(qt_asked):
        append = True
        for pos,test_div in enumerate(plist):
            if tested_number % plist[pos] == 0:
                append = False

        if append == True:
            print(f'{len(plist)+1} => {tested_number}')
            plist.append(tested_number)

        if len(plist) == int(qt_asked):
            return plist
            
        tested_number += 1
        
qtd = input('How many prime numbers do you want? ')
plist = prime_list(qtd)
#print(plist)