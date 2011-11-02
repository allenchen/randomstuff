
# enum class for identity of a player in a game.
class Identity:
    O = 0
    X = 1
    EMPTY = 2

DirectionStrings = {
    0 : "upper left",
    1 : "upper middle",
    2 : "upper right",
    3 : "center left",
    4 : "center",
    5 : "center right",
    6 : "lower left",
    7 : "lower middle",
    8 : "lower right"
}

# The game assumes there is exactly two players per game, one
# given an identity X, and another given an identity O.
# It also assumes a board of 3x3.

def identityToString(identity):
    if (identity == Identity.O):
        return "O"
    elif (identity == Identity.X):
        return "X"
    else:
        return " "


# Checks the game to see if it is over.  (specifically, in tic-tac-
# toe, if X or O controls 3 in a row).
# Return: A tuple of (isGameOver?, winner_identity) - boolean, identity
# In the case of a tie, winner is None: (True, None)
def checkTerminalState(board):
    # We could programatically check each column and row and diagonal here,
    # but it's easier and faster to just have precomputed victory conditions
    # on this small board.
    
    # 0|1|2
    # 3|4|5
    # 6|7|8
    
    # If any of these triples of indexes are owned by the same player, then
    # the game is over and that player is the winner.
    
    victory_conditions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
        ]
    
    for condition in victory_conditions:
        if (board[condition[0]] != Identity.EMPTY and
            all(identity == board[condition[0]] for identity in 
                map(lambda x: board[x], condition))):
            return (True, board[condition[0]])            
            
    # Otherwise, no victory detected.
        
    # If no board space is empty (and no winner), it is a tie.
    if (Identity.EMPTY not in board):
        return (True, None)

    # Otherwise, game is not over.
    return (False, None)

# Returns: opposite identity (X for O, O for X)
# Returns Identity.X for any other input.
def getOpposingIdentity(identity):
    if (identity == Identity.X):
        return Identity.O
    else:
        return Identity.X

# Returns: a list of non-empty positions to place a move
def getValidMoves(board):
    r = []
    for i, position in enumerate(board):
        if position == Identity.EMPTY:
            r += [i]

    return r
