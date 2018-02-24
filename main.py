from Display import *
from Tetris.Tetris import *

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)


def Main():
	t = Tetris()
	# ll = []
	p = Display()
	p.Run(t)

	# p.InputEnable(False)
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())
	# ll.append(Tetris())

	# p.RunList(ll)
	pass

if __name__=="__main__":
	Main()
