from os import system #for screen cleaning

def print_pat1(list_pat1):
    '''
    Receives a list with the charactes that are part of a variable line in the board and prints it as a string;
    INPUT: list of characters.
    OUTPUT: none. It prints the line by itself.
    '''
    str_pat1 = str()
    for char in list_pat1:
        str_pat1 += char
    print(str_pat1)
    
#End of print_pat1().
    

def print_board(board):
    '''
    Prints the game board, reflecting the advancement of the game.
    INPUT: a list with nine elements that represents the board.
    OUTPUT: none. It prints the board by itself.
    '''
    dic_pat1 = {'fil0':' ', 'pos0':' ' , 'fil1':' | ' , 'pos1':' ' , 'fil2':' | ' , 'pos2':' ' , 'fil3':' '}
    str_pat2 = '---|---|---'

    #First line (6,7,8 here, 7,8,9 for the user).
    print('\n')
    dic_pat1['pos0'] = board[6]
    dic_pat1['pos1'] = board[7]
    dic_pat1['pos2'] = board[8]
    print_pat1(list(dic_pat1.values()))
    print(str_pat2)
    
    #Second line (3,4,5 here, 4,5,6 for the user).
    dic_pat1['pos0'] = board[3]
    dic_pat1['pos1'] = board[4]
    dic_pat1['pos2'] = board[5]
    print_pat1(list(dic_pat1.values()))
    print(str_pat2)
    
    #Third line (0,1,2 here, 1,2,3 for the user).
    dic_pat1['pos0'] = board[0]
    dic_pat1['pos1'] = board[1]
    dic_pat1['pos2'] = board[2]
    print_pat1(list(dic_pat1.values()))
    
#End of print_board().


def check_victory(board,pl):
    '''
    Checks if there's a victory in a board. Returns the number of the player who won. Players characters of
    choice must be informed in the second parameter.
    INPUT: -1: a list with 9 positions, representing the board;
           -2: a list with the characters of choice of players and and to in [1] and [2]. [0] should be empty.
    OUTPUT: if there's a winner, returns who it is (1 or 2); if it's a draw, returns 3. If the game is not over,
            returns 0.
    '''
    possible_victories = list([[0,1,2],[0,4,8],[0,3,6],[1,4,7],[2,5,8],[2,4,6],[6,7,8],[3,4,5]])
    
    #We'll put the characters contained in all the possible winning scenarios in a set. If it contains only
    #an 'x' or an 'o' we have a winner.
    for x in possible_victories:
        set_of_chars = set()
        for y in x:
            set_of_chars.add(board[y])
        
        if len(set_of_chars) == 1:
            popped = set_of_chars.pop()
    
            if popped == 'x' or popped == 'o':
                #Marking the winning line.
                for i in x:
                    board[i] = board[i].upper()
                
                #Capturing the player who won.
                for pos,z in enumerate(pl):
                    if z == popped:
                        return pos
    
    #If we still have blank spaces an no winner, we can keep on playing.
    if ' ' in board:
        return 0
    #We have no winner but no more blank spaces in the board. It's a draw.
    else:
        return 3
    
##############
# Main logic #
##############

#Selecting X or O.
#-----------------
# - pl[1] contains the character player 1 is using (x/o).
# - pl[2] contains the character player 2 is using  (x/o).

pl = list(' '*3)
_ = system('clear') 
while pl[1].lower() not in ['x','o']:
    pl[1] = input ('Player 1, select X or O: ')
    if pl[1].lower() == 'x':
        pl[2] = 'o'
    else:
        pl[2] = 'x'
    
#Confirming the players are ready to play and starting, and restarting, if wished, the game.
#-------------------------------------------------------------------------------------------
# - board is a list with the nine positions in the board, from 0 to 8 internally.
# - turn contains the number of the player whose turn is in place.
# - winner has the number of the player who won the game. If zero, the game is still running.
# - move receives the postion the player wants to fill.

play = input('Are you ready to play (y)? ')
_ = system('clear') 

turn = 1
while play.lower() == 'y':
    board = list(' '*9)
    winner = int()
    
    while winner == 0:
        valid_move = bool()
        while valid_move  == False:
            #Asking for the move.
            move = int()
            while int(move) not in range(1,10):
                print_board(board)
                move = input(f'\nPlayer{turn}, where do you want to place your {pl[turn].upper()}? ')
                _ = system('clear') 
                
                if move.isdigit() == False:
                    move = 0
                    continue
                
            move = int(move) - 1 #Because inside we work with a range from 0 to 8. Tranforming to int too.
            
            #Validating the move.
            if int(move) not in range(0,9):
                valid_move = False
            elif board[move] != ' ':
                valid_move = False
            else:
                valid_move = True
        
        #Valid move. Register it.
        else:
            board[move] = pl[turn]
            
        #Check victory.
        winner = check_victory(board,pl)
        if winner in [1,2]:
            print(f"\nWe have a winner: Player{winner}!")
            print_board(board)
            continue
        elif winner == 3:
            print("\nWe have a DRAW!")
            print_board(board)
            continue
            
        #Passing the turn.
        if turn == 1:
            turn = 2
        else:
            turn = 1
    
    play = input('\nDo you want to play again (y)? ')
    _ = system('clear') 
else:
    print('Good bye!')