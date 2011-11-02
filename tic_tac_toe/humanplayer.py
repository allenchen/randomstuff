import string
from ttt_util import *
from player import *

class HumanPlayer(Player):
    def promptToMove(self):
        valid_input = False

        self.displayBoardAndKey()

        while True:
            user_input = int(input("Where to? "))
            if (user_input not in range(1,10) or 
                self.board[user_input-1] != Identity.EMPTY):
                print "Please enter a valid move!"
            else:
                # Adjust for off by one between user indices
                # and stored indices.
                return user_input - 1

    
    def updateBoard(self, location, identity):
        super(HumanPlayer, self).updateBoard(location, identity)
        if (identity == self.player_identity):
            print "You place",
        else:
            print "Opponent places",
        print "an " + identityToString(identity),
        print "in the " + DirectionStrings[location] + "."

    def notifyGameOver(self, winner):
        if (winner == self):
            print "You win!"
        elif (winner == None):
            print "It was a tie."
        else:
            print "You lost..."
        self.displayBoardAndKey()
    
    def displayText(self, text):
        print text
    
    def displayBoardAndKey(self):
        print "Board: " + ' '*6 + "Movement Key:"
        print string.join(map(identityToString, self.board[0:3]), "|") + ' '*8 + '1|2|3'
        print string.join(map(identityToString, self.board[3:6]), "|") + ' '*8 + '4|5|6'
        print string.join(map(identityToString, self.board[6:9]), "|") + ' '*8 + '7|8|9'
        print
