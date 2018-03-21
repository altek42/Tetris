import GeneticTetris
from Tetris.Tetris import Tetris
from Display import Display
import ReinforcementTetris

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)


def Main():
	# p = GeneticTetris.Program()
	# p.StartNew(30)
	# p.StartLoad(1321)

	# t = Tetris()
	# # ll = []
	# p = Display()
	# p.Run(t)
	# # p.RunList(ll)

	p = ReinforcementTetris.Program()
	p.StartNew()
	pass

if __name__=="__main__":
	Main()
