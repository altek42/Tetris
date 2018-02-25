import GeneticTetris

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)




def Main():
	p = GeneticTetris.Program()
	# p.StartNew(30)
	p.StartLoad(560)

	# t = Tetris()
	# # ll = []
	# p = Display()
	# p.Run(t)
	# # p.RunList(ll)
	pass

if __name__=="__main__":
	Main()
