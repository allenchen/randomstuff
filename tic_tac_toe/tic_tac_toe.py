from ttt_util import *
from player import *
from game import *
from humanplayer import *
from machineplayer import *

# Launch the game.

g = Game()
mp = MachinePlayer()
hp = HumanPlayer()

g.addPlayer(mp)
g.addPlayer(hp)

g.start()
