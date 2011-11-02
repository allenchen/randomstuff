from ttt_util import *
from player import *

class MachinePlayer(Player):
    # Simply selects the first non-empty slot it encounters and returns that position.
    # Assumes that there is at least one empty board position (or else we wouldn't be
    # asked by the game to make a move).
    # Better algorithms: run minimax on this (the tree is small enough to fully expand
    # in memory).  Alpha/beta pruning isn't really necessary (negligible gains).
    def promptToMove(self):
        for i, value in enumerate(self.board):
            if value == Identity.EMPTY:
                return i
