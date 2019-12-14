from random import randint
from os import system #For screen cleaning.
from IPython.display import clear_output #For screen cleaning in Jupyter Notebook.

def clear_screen():
    clear_output()
    _ = system('clear')

    
class Column():
    '''
    A Column object is one of the possible columns in which a ball will end. These columns are at the end
    of the board. When executed, these will be represented from a label which starts with one and jump from
    one to one. The left most column will be labeled 1.
    The column label is 1, 2, 3, etc. and it's the one displayed to the user at the end. The value, on the 
    other hand, is the value which a ball could have at the end of its run. If it goes to the left, its value
    receives itself minus 1, and if it goes to the right it receives itself plus one.
    '''
    
    qt_balls = 0
    
    def __init__(self,label,value):
        self.label = label
        self.value = value
    
    def print_column(self,tot_balls):
        percentage = self.qt_balls / tot_balls * 100
        return f"{self.label} - {self.qt_balls} - {percentage:0.1f}"
    
    def add_ball(self):
        self.qt_balls += 1

        
class Board():
    '''
    A Board object is the full Galton Board. It has columns at its bottom and the pins which are used to
    determine the path followed by the balls. The quantity of possibilies is the amound of pins the balls
    have to go through, and this quantity of possibilites determine the ammount of columns the board will have.
    The ammount of tests is (ammount of possibilities - 1)
    '''
    def __init__(self,qt_possibilities):
        self.columns = list()
        value = (qt_possibilities - 1) * -1
        
        for i in range(1,qt_possibilities + 1):
            self.columns.append(Column(i,value))
            value += 2

    def print_board(self,tot_balls):
        for column in self.columns:
            print(column.print_column(tot_balls))
            
    def add_ball(self,column_value):
        for column in self.columns:
            if column.value  == column_value:
                column.add_ball()
                break
            
            
class Ball():
    value = 0
    
    def change_value(self,ammount):
        self.value += ammount
        
    def shuffle(self,qt_tests):
        qt_tests_ran = 0
        #We generate a random 1 or 2. 1 means the ball will go to the left, whilst 2 determines the ball
        #goes to the right. At the end of the run, we have the value of the column where the ball ended.
        #I said the VALUE, ok?!
        while qt_tests_ran < qt_tests:
            if randint(1,2) == 1:
                self.change_value(-1)
            else:
                self.change_value(+1)
                
            qt_tests_ran += 1
        return self.value
    
        
if __name__ == '__main__':
    clear_screen()
    while True:
        try:
            qt_balls = int(input('Quantity of balls: '))
            if qt_balls < 1:
                continue
        except:
            continue
        else:
            break

    while True:
        try:
            qt_possibilities = int(input('Quantity of possibilities: '))
            if qt_possibilities < 1:
                continue
        except:
            continue
        else:
            break
    
    board = Board(qt_possibilities)
    
    qt_balls_generated = 0
    while qt_balls_generated < qt_balls:
        ball = Ball()
        ball_final_position = ball.shuffle(qt_possibilities - 1)
        board.add_ball(ball_final_position)
        
        qt_balls_generated += 1
        
    board.print_board(qt_balls)