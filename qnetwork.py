from Network.NeuronNetwork import *
from Network.NetworkFunctions import *
from Tetris.Tetris import *
from Tetris.Bricks import QBRICKS
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
		self.settingsFile = "Settings"
		self.bricks = QBRICKS

	def StartNew(self, name="QNet_0"):
		self.__prepare(name)
		self.net.New(36,400,1)
		self.net.Init()
		# self.__saveSettings()
		self.__start(self.__mainLoopTrainig)

	def StartLoad(self, name="QNet_0"):
		# self.__loadSettings(name)
		self.__prepare(name)
		self.net.Load(directory="Reinforcement",name=self.name)
		self.__start(self.__mainLoopTrainig)

	def Play(self, name="QNet_0"):
		self.__prepare(name)
		self.net.Load(directory="Reinforcement",name=self.name)
		self.__start(self.__netPlay)


	def __prepare(self, name="QNet_0"):
		self.name = name
		self.tetris = Tetris(self.bricks)
		self.tetris.SetBrickLimit(Program.BRICK_LIMIT)
		self.net = NeuronNetwork()

	# def __saveSettings(self):
	# 	config = configparser.ConfigParser()
	# 	config[self.name] = {
	# 		'bricks': self.bricks
	# 	}
	# 	with open(self.settingsFile, 'w') as configfile:
	# 		config.write(configfile)
	#
	# def __loadSettings(self, name):
	# 	config = configparser.SafeConfigParser()
	# 	config.read(self.settingsFile)
	# 	settings = config[name]
	# 	self.bricks = []
	# 	settings['bricks']
	# 	print(type(self.bricks))
	# 	print(self.bricks)


	def __start(self, func):
		self.__actions = self.tetris.GetAllActions()
		self.__createActionNet(self.__actions)
		t = threading.Thread(target=func)
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
		self.__netPlay()
		print("BestScore:", bestScore)
		print("BestGame:", bestGame)
		input('Hit Enter...')

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
		emptyCells = 0
		for y in range(yLen):
			for x in range(xLen):
				if vec[x] == 0 and board[y][x] != 0:
					vec[x] = yLen-y
				elif vec[x] != 0 and board[y][x] == 0:
					emptyCells += 1
		return ([x/20 for x in vec], emptyCells)

	def __getNetResponseActions(self):
		state, emptyCells = self.__getState()
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
		return random.randint(0,len(self.__actions)-1)

	def __netPlay(self):
		arg = input('Continue?\nq: exit\n>>')
		while arg != 'q':
			self.tetris.Restart()
			while not self.tetris.isGameOver:
				action = self.__getBestActionIndex()
				(pos,rot) = self.__actions[action]
				self.tetris.MoveBrickAt(pos,rot)
				self.tetris.ConfirmMove()
			print('Score: ',self.tetris.score)
			print('Moves: ',self.tetris.GetArrangedBrickCount())
			print('\n')
			arg = input('Continue?\nq: exit\n>>')
		self.display.Exit();


	def __netLearn(self):
		isFirst = True
		while not self.tetris.isGameOver:
			state, emptyCells = self.__getState()
			r= random.random()
			if r<0.05 or isFirst:
				isFirst = False
				action = self.__getRandomActionIndex()
			else:
				action = self.__getBestActionIndex()

			inputData = state + self.__actionsNet[action]
			y = self.net.Sim(inputData)
			reward = self.tetris.score / 300
			(pos,rot) = self.__actions[action]
			self.tetris.MoveBrickAt(pos,rot)
			self.tetris.ConfirmMove()
			state, emptyCells = self.__getState()
			highest = max(state)
			bonus = 20 - emptyCells
			if highest < 0.5:
				bonus += 10
			if bonus < 0:
				bonus = 0
			reward = (self.tetris.score + bonus) / 300 - reward
			bestQ = self.__getBestQ()
			qValue = reward + self.GAMMA * bestQ

			# print("reward:",reward)
			# print("q:",qValue)
			# print("emptyCells:",emptyCells)
			# if reward>0.01:
			# 	input()
			# loss = (qValue - y)**2
			# print(qValue)
			self.net.Train([inputData],[qValue],1,0.2)
