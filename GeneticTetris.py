from Display import *
from Tetris.Tetris import *
from Network.NeuronNetwork import *
from Network.Genetic import *
import pprint
import queue
import threading
import time
import random

POPULATION_DIR = '.\\POPULATION'

class Program:

	BRICK_LIMIT = 50000

	def __init__(self, isDisplay=True):
		self.__isDisplay = isDisplay
		if isDisplay:
			self.display = Display()
		self.genetic = Genetic()
		self.tetrisList = []
		self.population = []
		self.generation = 0


	def StartNew(self,size):
		self.__createNewPopulation(size)
		self.__start()

	def StartLoad(self,generation):
		self.generation = generation
		self.__loadPopulation(POPULATION_DIR)
		self.__start()

	def __start(self):
		t = threading.Thread(target=self.__netLoop)
		t.daemon = True
		t.start()
		if self.__isDisplay:
			self.display.RunList(self.tetrisList)
		t.join()

	def __netLoop(self):
		for i in range(5000):
			th = []
			for i in range(len(self.population)):
				t = threading.Thread(target=self.__netPlay,args=(i,))
				t.daemon = True
				t.start()
				th.append(t)

			for item in th:
				item.join()

			self.__showFit()
			self.__savePopulation(POPULATION_DIR)
			self.__createNextPopulation()
			for item in self.tetrisList:
				item.Restart()

	def __showFit(self):
		fits = []
		for item in self.population:
			fits.append(item.fit)
		print(self.generation,fits,"<",max(fits),min(fits),int(sum(fits)/len(fits)),">")

	def __getBestMove(self,tetris,net):
		rotCount = tetris.GetBrickRotateCount()
		moves = {}
		inMove = {}
		for pos in range(-5,5):
			for rot in range(rotCount):
				self.__moveTetrisAt(pos,rot,tetris)
				tetris.ConfirmMove(isSimulation = True)
				(board,brick) = tetris.GetBoard()
				inData = self.__prepareInputForNet(board,brick)
				y = net.Sim(inData)
				moves[(pos,rot)] = y[0]
				inMove[(pos,rot)] = inData
				tetris.ResetBrickPosition()
		# if random.random() < 0.1:
		# 	m = random.choice(list(moves))
		# else:
		m = max(moves, key=moves.get)
		return (m)

	def __netPlay(self, index):
		net = self.population[index]
		tetris= self.tetrisList[index]
		while not tetris.isGameOver:
			(pos,rot) = self.__getBestMove(tetris,net)
			self.__moveTetrisAt(pos,rot,tetris)
			tetris.ConfirmMove()
		net.fit = tetris.GetScore()

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

		# levels.extend(bricks)
		levels.append(holes)
		levels.append(float(fullLineCounter)/4)
		return levels
		pass

	def __moveTetrisAt(self,pos,rot,tetris):
		for i in range(rot):
			tetris.RotateBrickRight()
		if pos > 0:
			for i in range(pos):
				tetris.MoveBrickRight()
		elif pos < 0:
			for i in range(-pos):
				tetris.MoveBrickLeft()

	def __createNewPopulation(self,size):
		for i in range(size):
			self.__createNewUnit()

	def __createNextPopulation(self):
		self.population = self.genetic.SelectNewPopulation(self.population)
		populationSize = len(self.population)
		for i in range(0,populationSize,2):
			self.genetic.CrossNetworks(self.population[i],self.population[i+1])
		for i in range(0,populationSize):
			self.genetic.MutateNetwork(self.population[i])
		self.generation+=1

	def __savePopulation(self,directory):
		directory+="\\{}".format(self.generation)
		for i in range(len(self.population)):
			net = self.population[i]
			net.Save(directory,str(i))

	def __loadPopulation(self,directory):
		directory+="\\{}".format(self.generation)
		files = os.listdir(directory)
		self.population = []
		for i in files:
			net = NeuronNetwork()
			net.Load(directory,i)
			self.population.append(net)
			t = Tetris()
			t.SetBrickLimit(self.BRICK_LIMIT)
			self.tetrisList.append(t)

	def __createNewUnit(self):
		t = Tetris()
		t.SetBrickLimit(self.BRICK_LIMIT)
		self.tetrisList.append(t)
		net = NeuronNetwork()
		net.New(12,100,1)
		net.Init()
		self.population.append(net)
