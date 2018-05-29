from Display import *
from Tetris.Tetris import *
import threading
import time
from Network.NeuronNetwork import *
from Network.NetworkFunctions import *
import pprint
import numpy as np
import random

class Program:
	BRICK_LIMIT = 50000
	GAMES_LIMIT = 100000

	def __init__(self):
		self.display = Display()
		pass

	def StartNew(self, name="RLT_0"):
		self.tetris = Tetris()
		self.name = name
		self.tetris.SetBrickLimit(Program.BRICK_LIMIT)
		self.net = NeuronNetwork()
		self.net.New(12,200,1)
		self.net.Init();
		self.__start()

	def StartLoad(self, name="RLT_0"):
		self.tetris = Tetris()
		self.name = name
		self.tetris.SetBrickLimit(Program.BRICK_LIMIT)
		self.net = NeuronNetwork()
		self.net.Load(directory="Reinforcement",name=self.name)
		self.__start()

	def ____debug(self):
		self.__getBestMove()
		pass;


	def __start(self):
		t = threading.Thread(target=self.__netLoop)
		t.daemon = True
		t.start()
		# t = threading.Thread(target=self.display.Run,args=(self.tetris,))
		# t.daemon = True
		# t.start()
		self.display.Run(self.tetris)
		# self.____debug()
		t.join()


	def __netLoop(self):
		for i in range(self.GAMES_LIMIT):
		# for i in range(1):
			self.moveList = []
			self.__netPlay()
			self.__netLearn()
			print("GAME: ",i,
				"\tSCORE: ",self.tetris.score,
				"\tBRICKS: ",self.tetris.GetArrangedBrickCount())
			self.net.Save(directory="Reinforcement",name=self.name)
			self.tetris.Restart()
		self.display.Exit();

	def __netPlay(self):
		self.history = []
		while not self.tetris.isGameOver:
			(move, data)= self.__getBestMove()
			(pos,rot) = move
			self.__moveTetrisAt(pos,rot)
			self.tetris.ConfirmMove()
			self.history.append(data)
			if len(self.history) > 19:
				del self.history[0]

	# def __netLearn(self):
	# 	it = 0
	# 	inData=[]
	# 	reward=[]
	# 	for (i, o) in self.history:
	# 		inData.append(i)
	# 		it+=1
	# 		if(it < len(self.history)):
	# 			reward.append(o + 0.5 * self.history[it][1])
	# 	del inData[-1]
	# 	self.net.Train(inData,reward,200,0.2)
	def __netLearn(self):
		inData=[]
		reward=[]
		g=1.0
		self.history.reverse()
		for (i, o) in self.history:
			inData.append(i)
			reward.append(g)
			g=g-0.05
		self.net.Train(inData,reward,1,0.5)

	def __getBestMove(self):
		rotCount = self.tetris.GetBrickRotateCount()
		moves = {}
		inMove = {}
		for pos in range(-5,5):
			for rot in range(rotCount):
				self.__moveTetrisAt(pos,rot)
				self.tetris.ConfirmMove(isSimulation = True)
				(board,brick) = self.tetris.GetBoard()
				inData = self.__prepareInputForNet(board,brick)
				y = self.net.Sim(inData)
				moves[(pos,rot)] = y[0]
				inMove[(pos,rot)] = inData
				# print ("[",pos," ",rot,"] ",y)
				self.tetris.ResetBrickPosition()
		if random.random() < 0.1:
			m = random.choice(list(moves))
		else:
			m = min(moves, key=moves.get)
		return (m, (inMove[m],moves[m]))

	def __moveTetrisAt(self,pos,rot):
		for i in range(rot):
			self.tetris.RotateBrickRight()
		if pos > 0:
			for i in range(pos):
				self.tetris.MoveBrickRight()
		elif pos < 0:
			for i in range(-pos):
				self.tetris.MoveBrickLeft()

	def __prepareInputForNet(self,board,brick):
		levels = [0 for x in board[0]];
		holes = 0
		lineIt =21
		fullLineCounter=0
		for line in board:
			lineIt -= 1
			cellIt=-1
			fulllLine = True
			for cell in line:
				cellIt+=1
				if cell != 0:
					if levels[cellIt] ==0:
						levels[cellIt] = lineIt
				else:
					fulllLine = False
					if levels[cellIt] > lineIt:
						holes += 1
			if fulllLine:
				fullLineCounter += 1

		levels = [x/20 for x in levels]
		#bricks = [0.0 for x in range(7)]
		#bricks[brick] = 1.0
		if holes == 0:
			holes = 0.0
		elif 1 <= holes < 5:
			holes = 0.25
		elif 5 <= holes < 10:
			holes = 0.5
		elif 10 <= holes < 15:
			holes = 0.75
		else:
			holes = 1.0

		#levels.extend(bricks)
		levels.append(holes)
		levels.append(float(fullLineCounter)/4)
		return levels
		pass

if __name__ == "__main__":
	import main
	main.Main()
