import random
from ttt_util import *

class Game:
    def __init__(self):
        self.board = [Identity.EMPTY]*9

        # Map of identity enums to player objects
        self.players = {}

        # Identities remaining to give out to players that join
        # the game.
        self.identities_remaining = [ Identity.O, Identity.X ]

        # The player whose turn it is
        self.active_player = None
    
    # Add a player to the game.
    # Parameters: player (Player object) - player to add to gmae
    # Return: True if player was added, False otherwise
    def addPlayer(self, player):
        if (len(self.identities_remaining) == 0):
            return False

        # Determine a player identity to give the player.
        new_identity = self.identities_remaining[0]
        self.identities_remaining.remove(new_identity)

        player.joinGame(self)
        player.assignIdentity(new_identity)

        self.players[new_identity] = player

        return True


    def getIdentity(self, player):
        for k,v in self.players.iteritems():
            if v == player:
                return k
        return None

    # Return: The player object of the given player's opponent.
    # Unspecified behavior if a player is his/her own opponent, or if
    # player has no opponent, or if player is not in game.
    def getOpponent(self, player):
        for v in self.players.values():
            if v != player:
                return v

    # Start the game
    def start(self):
        if (len(self.identities_remaining) != 0):
            print "Game couldn't start - not enough players."
            return False # Couldn't start the game; not enough players

        # Select a random player to begin first.
        self.active_player = random.choice(self.players.values())

        self.run()

    # Main run loop of the game.
    # Ping players and request moves, update board, broadcast move, repeat.
    def run(self):
        # Ping the active player.
        gameOver = False
        while (not gameOver):
            # Prompt player for move.
            move = self.active_player.promptToMove()

            # Check if move is valid.
            if (move not in range(0,9) or self.board[move] != Identity.EMPTY):
                self.active_player.displayText("Invalid move.")
                continue
            
            # Set the game state.
            self.board[move] = self.getIdentity(self.active_player)

            # Broadcast that this move was made to all players.
            for player in self.players.values():
                player.updateBoard(move, self.getIdentity(self.active_player))

            # Check if this game state is terminal.
            terminal_check = checkTerminalState(self.board)
            if (terminal_check[0]):
                # If so, broadcast game over message, and stop this run loop.
                for player in self.players.values():
                    winner = None
                    if (terminal_check[1] != None):
                        winner = self.players[terminal_check[1]]
                    player.notifyGameOver(winner) 
                gameOver = True

            # Set the new active player.
            self.active_player = self.getOpponent(self.active_player)
