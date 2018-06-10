import GeneticTetris
from Tetris.Tetris import Tetris
from Display import Display
import qnetwork
import ReinforcementTetris
import pprint

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)


def Main():
	# t = Tetris()
	# p = Display()
	# p.Run(t)

#w: 8
#h: 21
	p = qnetwork.Program()
	p.StartLoad()
	# p.StartNew()

#w: 10
#h: 21
	# p = GeneticTetris.Program(False)
	# p.StartNew(30)
	# p.StartLoad(20)

	# p = ReinforcementTetris.Program()
	# p.StartNew("RLT_m")
	# p.StartLoad("RLT2")
	# p.StartLoad("RLT_m")
	pass

if __name__=="__main__":
	Main()
