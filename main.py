import GeneticTetris
from Tetris.Tetris import Tetris
from Display import Display

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)


# 1322 - uczone tylko na kształcie 'o'

def Main():
	# p = GeneticTetris.Program()
	# p.StartNew(30)
	# p.StartLoad(1321)

	t = Tetris()
	# # ll = []
	p = Display()
	p.Run(t)
	# # p.RunList(ll)
	pass

if __name__=="__main__":
	Main()
