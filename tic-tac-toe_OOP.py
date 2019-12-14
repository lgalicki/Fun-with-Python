from os import system #for screen cleaning
from IPython.display import clear_output #for screen cleaning in Jupyter Notebook

def clear_screen():
    clear_output()
    _ = system('clear')
    
def pass_turn():
    global turn
    
    if turn == 0:
        turn = 1
    else:
        turn = 0

class Player():
    def __init__(self,name):
        self.name = name
        
    def set_char_opt(self,char_opt):
        self.char_opt = char_opt
        
    def move(self,pos,board):
        board.mark_move(pos,char_opt)
        
class Board():
    wins = ((7,8,9),(4,5,6),(1,2,3),(7,4,1),(8,5,2),(9,6,3),(7,5,3),(9,5,1))

    def __init__(self):
        self.reset_self()
    
    def mark_move(self,pos,char_opt):
        self.positions[pos] = char_opt
        
    def check_win(self):
        for win in self.wins:
            if self.positions[win[0]] == self.positions[win[1]] == self.positions[win[2]] != ' ':
                for i in range(3):
                    self.positions[win[i]] = self.positions[win[i]].upper()
                return True
        return False

    def reset_self(self):
        self.positions = list(' '*10)
    
    def check_draw(self):
        if ' ' not in self.positions[1:10]:
            return True
        else:
            return False
    
    def validate_move(self,pos):
        if self.positions[pos] != ' ':
            return False
        else:
            return True
    
    def print_self(self):
        clear_screen()
        print(f'{self.positions[7]} | {self.positions[8]} | {self.positions[9]}') 
        print('-'*9)
        print(f'{self.positions[4]} | {self.positions[5]} | {self.positions[6]}')
        print('-'*9)
        print(f'{self.positions[1]} | {self.positions[2]} | {self.positions[3]}')
        
class Scoreboard():
    def __init__(self):
        self.score = [0]*3
        
    def add_win(self,player):
        self.score[player] += 1
    
    def add_draw(self):
        self.score[2] += 1
        
    def print_self(self):
        print('\nSCOREBOARD')
        print('----------')
        print(f'{players[0].name} - {self.score[0]}')
        print(f'{players[1].name} - {self.score[1]}')
        print(f'Draws - {self.score[2]}')
        
#------------------------------------------------------------------------------------------

clear_screen()
players = list()
turn = 0 #The first game always starts with player one, and the sbsequent one with the player who would be the
         #next in the game that just ended

#Requesting players' names
for i in list(range(2)):
    name = str()
    while name == str():
        name = input(f'Player {i+1}, enter your name: ')
        
    players.append(Player(name))

#Requesting character option
char_opt = ' '
while char_opt not in 'xo':
    char_opt = input(f'\n{players[0].name}, choose "x" or "o": ')
    char_opt = char_opt.lower()
    
players[0].set_char_opt(char_opt)
if char_opt == 'x':
    players[1].set_char_opt('o')
else:
    players[1].set_char_opt('x')

#Creating a board and a score board
game_board = Board()
scoreboard = Scoreboard()

#Playing and replaying whilst desired
replay = 'y'
while replay.lower() == 'y':
    replay = ' '
    
    #Running the game while there's no win nor draw
    while game_board.check_win() == False:
        
        #Requesting position to player who's got the turn
        pos = '0'       
        while pos not in ('123456789') or not game_board.validate_move(int(pos)):
            game_board.print_self()
            pos = input(f'\n{players[turn].name}, where do you want to position your {players[turn].char_opt}? ')

        #Marking the move in the board
        game_board.mark_move(int(pos),players[turn].char_opt)

        #Checking if the game must continue
        if game_board.check_win():
            game_board.print_self()
            print(f'\n{players[turn].name} wins!')
            scoreboard.add_win(turn)
            game_board.reset_self()
            pass_turn()
            break

        if game_board.check_draw():
            game_board.print_self()
            print('\nWe have a draw!')
            scoreboard.add_draw()
            game_board.reset_self()
            pass_turn()
            break
            
        #Passing the turn to the next player
        pass_turn()
        
    #Should we play again?
    while replay.lower() not in ('ny'):
        replay = input('Do you want to play again (y/n)? ')

else:
    scoreboard.print_self()