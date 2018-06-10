from Network.NeuronNetwork import *
from Network.NetworkFunctions import *
from Tetris.Tetris import *
from Display import *
import threading
import pprint
import random

class Program(object):
	BRICK_LIMIT = 5000
	GAMES_LIMIT = 50000
	GAMMA = 0.8

	def __init__(self):
		super(Program, self).__init__()
		self.display = Display()
		self.display.InputEnable(False)


	def StartNew(self, name="QNet_0"):
		self.name = name
		self.tetris = Tetris()
		self.tetris.SetBrickLimit(Program.BRICK_LIMIT)
		self.net = NeuronNetwork()
		self.net.New(36,100,1)
		self.net.Init();
		self.__start()

	def StartLoad(self, name="QNet_0"):
		self.name = name
		self.tetris = Tetris()
		self.tetris.SetBrickLimit(Program.BRICK_LIMIT)
		self.net = NeuronNetwork()
		self.net.Load(directory="Reinforcement",name=self.name)
		self.__start()



	def __start(self):
		self.__actions = self.tetris.GetAllActions()
		self.__createActionNet(self.__actions)
		t = threading.Thread(target=self.__mainLoopTrainig)
		t.daemon = True
		t.start()
		self.display.Run(self.tetris)

	def __mainLoopTrainig(self):
		bestScore = self.tetris.score
		bestGame = 0
		for i in range(self.GAMES_LIMIT):
			self.tetris.Restart()
			self.__netLearn()
			print('GAME:',i,'SCORE:',self.tetris.score,'BEST:',bestScore)
			if bestScore<self.tetris.score:
				bestScore = self.tetris.score
				bestGame = i
			self.net.fit = bestScore
			self.net.Save(directory="Reinforcement",name=self.name)
		input('Net is ready...')
		self.tetris.Restart()
		self.__netPlay()
		print("BestScore:", bestScore)
		print("BestGame:", bestGame)
		input('Hit Enter...')
		self.display.Exit();

	def __createActionNet(self, actions):
		lenAction = len(self.__actions)
		self.__actionsNet = []
		for i in range(lenAction):
			a = [0 for x in range(lenAction)]
			a[i] = 1
			self.__actionsNet.append(a)



	def __getState(self):
		board = self.tetris.GetBoardOnly()
		yLen = len(board)
		xLen = len(board[0])
		vec = [0 for a in range(xLen)]
		for y in range(yLen):
			for x in range(xLen):
				if vec[x] == 0 and board[y][x] != 0:
					vec[x] = yLen-y
		return [x/20 for x in vec]

	def __getNetResponseActions(self):
		state = self.__getState()
		vec = []
		for action in self.__actionsNet:
			s = state + action
			y = self.net.Sim(s)
			vec.append(y[0])
		return vec

	def __getBestQ(self):
		vec = self.__getNetResponseActions()
		return max(vec)

	def __getBestActionIndex(self):
		vec = self.__getNetResponseActions()
		return vec.index(max(vec))

	def __getRandomActionIndex(self):
		state = self.__getState()
		return random.randint(0,len(self.__actions)-1)

	def __netPlay(self):
		while not self.tetris.isGameOver:
			action = self.__getBestActionIndex()
			(pos,rot) = self.__actions[action]
			self.tetris.MoveBrickAt(pos,rot)
			self.tetris.ConfirmMove()


	def __netLearn(self):
		while not self.tetris.isGameOver:
			state = self.__getState()
			r= random.random()
			if r<0.05:
				action = self.__getRandomActionIndex()
			else:
				action = self.__getBestActionIndex()

			inputData = state + self.__actionsNet[action]
			y = self.net.Sim(inputData)
			# self.tetris.SaveState()
			reward = self.tetris.score / 400
			(pos,rot) = self.__actions[action]
			self.tetris.MoveBrickAt(pos,rot)
			self.tetris.ConfirmMove()
			reward = self.tetris.score / 400 - reward
			bestQ = self.__getBestQ()
			# self.tetris.LoadState()
			qValue = reward + self.GAMMA * bestQ
			# loss = (qValue - y)**2
			# print(qValue)
			self.net.Train([inputData],[qValue],1,0.2)
