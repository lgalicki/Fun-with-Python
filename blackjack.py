from random import shuffle
from os import system #For screen cleaning.
from IPython.display import clear_output #For screen cleaning in Jupyter Notebook.

def clear_screen():
    clear_output()
    _ = system('clear')

class Card():
    def __init__(self,number,suit):
        self.number = number
        self.suit = suit
        
    def __str__(self):
        return f"{self.number}{self.suit}"

    
class Deck():
    def __init__(self):
        self.cards = list()
        for i in list(range(1,14)):
            for j in ['♥','♦','♣','♠']:
                if i == 1:
                    self.cards.append(Card('A',j))
                elif i == 11:
                    self.cards.append(Card('Q',j))
                elif i == 12:
                    self.cards.append(Card('J',j))
                elif i == 13:
                    self.cards.append(Card('K',j))
                else:
                    self.cards.append(Card(str(i),j))
                    
    def __str__(self):
        deck_str = str()
        for card in self.cards:
            deck_str = deck_str + ' ' + str(card)
        deck_str = deck_str[1:len(deck_str)]
        return deck_str
    
    def __len__(self):
        return len(self.cards)
    
    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        drawn_card = self.cards.pop()
        return drawn_card

    
class Hand():
    def __init__(self):
        self.cards = list()
        
    def __len__(self):
        return len(self.cards)
        
    def add_card(self,card):
        self.cards.append(card)
        
    def __str__(self):
        hand_str = str()
        for card in self.cards:
            hand_str = hand_str + ' ' + str(card)
        hand_str = hand_str[1:len(hand_str)]
        return hand_str
    
    def evaluate(self):
        #First we check the whole hand and attribute the value of 1 to the aces.
        total = int()
        for card in self.cards:
            #These are the tens.
            if str(card)[0] == '1':
                total += 10
            #These are the aces.
            elif str(card)[0] == 'A':
                total += 1
            #These are the faces
            elif str(card)[0] in ['Q','J','K']:
                total += 10
            #These are the numbers from 2 to 9.
            else:
                total += int(str(card)[0])
                
        #Then we rerun it atrributing, if possible, 11 (+10 in this case), to the aces.
        for card in self.cards:
            if str(card)[0] == 'A':
                if total <= 11:
                    total += 10
        
        return total

    
class Player():
    def draw_initial_hand(self,deck):
        self.hand = Hand()
        self.draw_card(deck)
        self.draw_card(deck)
        
    def draw_card(self,deck):
        self.hand.add_card(deck.draw_card())
        
    def show_hand(self):
        return str(self.hand)
    
        
class HumanPlayer(Player):
    def __init__(self):
        self.stash = 1000
        
    def bet(self,value):
        if value > self.stash:
            return False
        else:
            self.stash -= value
            return True
        
    def add_credits(self,value):
        self.stash += value
        
        
class CpuPlayer(Player):
    def show_initial_hand(self):
        return f"{str(self.hand.cards[0])} + a hidden card"
    
    def play(self,deck,opponent_score):
        while self.hand.evaluate() < 17 or self.hand.evaluate() < opponent_score:
            self.draw_card(deck)
    
    
def print_round(credits,bet,player_hand,skynet_hand):
    clear_screen()
    print(f'Remaining credits: {credits}')
    print(f'Current bet......: {bet}')
    print(f'Your hand....: {player_hand}')
    print(f"Dealer's hand: {skynet_hand}")

    
if __name__ == '__main__':
    player = HumanPlayer()
    skynet = CpuPlayer()
    
    clear_screen()
    keep_playing = str()
    while keep_playing not in ['y','n']:
        keep_playing = input('Are you ready to play (y/n)? ').lower()
    
    
    while keep_playing == 'y':
        #Creating and shuffling a full deck.
        game_deck = Deck()
        game_deck.shuffle()
        
        #Asking for initial bet.
        while True:
            try:
                clear_screen()
                print(f'Remaining credits: {player.stash}')
                bet = int(input('Place your bet: '))
            except:
                continue
            else:
                if bet > 0:
                    if player.bet(bet):
                        break
                    else:
                        continue
                else:
                    continue
        
        #Drawing initial hand for dealer and player.
        player.draw_initial_hand(game_deck)
        skynet.draw_initial_hand(game_deck)

        move = 'h'
        #While player is hitting.
        while move == 'h':
            
            #Asking for next move.
            move = str()
            while move not in ['h','s']:
                print_round(player.stash,bet,player.show_hand(),skynet.show_initial_hand())                
                move = input('\nDo you want to hit or stand (h/s)? ').lower()
            
            #Player hits. One more card should be drawn.
            if move == 'h':
                player.draw_card(game_deck)
                  
                #If the hand surpasses 21 a stand is assumed so we can evaluate who's the winner.
                if player.hand.evaluate() > 21:
                    move = 's'
                  
        #Here we start to evaluate the hands to check who's the winner.
        #--------------------------------------------------------------
        #At first we must see if the player's hand surpassed 21. If not, the dealer must play.
        if player.hand.evaluate() <= 21:
            skynet.play(game_deck,player.hand.evaluate())
                  
        #Now let's evaluate the results.
        print_round(player.stash,bet,player.show_hand(),skynet.show_hand())
        
        player_hand = player.hand.evaluate()
        skynet_hand = skynet.hand.evaluate()
        
        if player_hand > 21:
            result = 'You lose'
        elif skynet_hand > 21:
            result = 'You win'
            player.add_credits(bet * 2)
        elif player_hand > skynet_hand:
            result = 'You win'
            player.add_credits(bet * 2)
        elif player_hand < skynet_hand:
            result = 'You lose'
        else:
            result = 'Push'
            player.add_credits(bet)
            
        print(f'{result}: {player_hand} vs {skynet_hand}')
                  
        #Asking for replay
        keep_playing = str()
        while keep_playing not in ['y','n'] and player.stash > 0:
            keep_playing = input('Do you want to continue the game (y/n)? ').lower()
        else:
            print(f'\nGame over! Your final credits: {player.stash}.')