from ttt_util import *

class Player(object):
    def __init__(self):
        self.board = [Identity.EMPTY]*9
        self.game = None
        self.player_identity = None

    # We assume the Game is trustworthy and won't do anythng
    # strange (like pass around invalid game states).

    ###########################################
    # These methods are called by the Player. #
    ###########################################

    # When called, game is registered as self.game and player
    # can begin accepting promptToMove(), updateBoard() and
    # notifyGameOver() messages.
    # Parameters: game (Game object), game to join
    # Return Values: True if game was joined, False if player
    # is already in a game.
    def joinGame(self, game):
        if self.game == None:
            self.game = game
            return True
        else:
            return False

    #########################################
    # These methods are called by the Game. #
    #########################################

    # Called by the server, and assigns board identity (X or O)
    # to the player.
    # Parameters: identity enum
    # Return values: True if identity was set (and player is in
    # a game), False otherwise.
    def assignIdentity(self, identity):
        if self.game == None:
            return False
        else:
            self.player_identity = identity
            return True

    # Game will call updateBoard() to update the player's view
    # of the game state (specifically, just the board).
    # Parameters: location value 1-9 made by player.
    def updateBoard(self, location, identity):
        self.board[location] = identity

    # Game will call promptToMove() to notify the player to
    # make a move.
    # Return values: A move to make (location value 1-9).
    def promptToMove(self):
        pass

    # Game will notify player when the game is over, and game
    # will unregister self.game and can now accept new
    # joinGame() messages.
    def notifyGameOver(self, winner):
        pass

    # Notifies a player about certain information.
    def displayText(self, text):
        pass
