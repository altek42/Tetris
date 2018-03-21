from Display import *
from Tetris.Tetris import *
import threading
import time

class Program:
	BRICK_LIMIT = 50000
	GAMES_LIMIT = 1

	def __init__(self):
		self.display = Display()
		pass

	def StartNew(self):
		self.tetris = Tetris()
		self.__start()

	def ____debug(self):
		self.__getBestMove()
		pass;


	def __start(self):
		t = threading.Thread(target=self.__netLoop)
		t.daemon = True
		t.start()
		t = threading.Thread(target=self.display.Run,args=(self.tetris,))
		t.daemon = True
		t.start()

		self.____debug()
		t.join()


	def __netLoop(self):
		return
		for i in range(self.GAMES_LIMIT):
			self.moveList = []
			self.__netPlay()
			# learn net
			self.tetris.Restart()

	def __netPlay(self):
		# while not self.tetris.isGameOver:
			# get move
			# move
			# save move
		pass

	"""
		@ret (pos,rot)
	"""
	def __getBestMove(self):
		rotCount = self.tetris.GetBrickRotateCount()
		moves = []
		for pos in range(-5,5):
			for rot in range(rotCount):
				self.__moveTetrisAt(pos,rot)
				self.tetris.ConfirmMove(isSimulation = True)
				print("Wait!",rot,pos)
				time.sleep(0.6)
				self.tetris.ResetBrickPosition()


	def __moveTetrisAt(self,pos,rot):
		for i in range(rot):
			self.tetris.RotateBrickRight()
		if pos > 0:
			for i in range(pos):
				self.tetris.MoveBrickRight()
		elif pos < 0:
			for i in range(-pos):
				self.tetris.MoveBrickLeft()

if __name__ == "__main__":
	import main
	main.Main()
