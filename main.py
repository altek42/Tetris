import GeneticTetris
import Genetic2
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

	p= Genetic2.Program()
	p.StartNew(30)
	# p.StartLoad(30,2)

#w: 8
#h: 21
	# p = qnetwork.Program()
	# p.StartLoad(name="QNet_1")
	# p.StartNew(name="QNet_2")

	# p.Play(name="QNet_2")
	# p.Play(name="QNet_1")

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
