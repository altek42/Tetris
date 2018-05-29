import GeneticTetris
from Tetris.Tetris import Tetris
from Display import Display
import ReinforcementTetris

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)


def Main():
	# p = GeneticTetris.Program(False)
	# p.StartNew(30)
	# p.StartLoad(20)

	# t = Tetris()
	# p = Display()
	# p.Run(t)

	p = ReinforcementTetris.Program()
	# p.StartNew("RLT_m")
	# p.StartLoad("RLT2")
	p.StartLoad("RLT_m")
	pass

if __name__=="__main__":
	Main()
