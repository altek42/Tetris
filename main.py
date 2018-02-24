from Display import *
from Tetris.Tetris import *
from Network.NeuronNetwork import *
from Network.Genetic import *
import pprint
import queue
import threading
import time

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)

POPULATION_DIR = '.\\POPULATION'

class Program:
	def __init__(self):
		# self.display = Display()
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
		t.join()
		# self.display.RunList(self.tetrisList)

	def __netLoop(self):
		for i in range(5000):
			th = []
			for i in range(len(self.population)):
				t = threading.Thread(target=self.__worker,args=(i,))
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
		print(self.generation,fits)


	def __worker(self,index):
		net = self.population[index]
		tetris = self.tetrisList[index]
		while not tetris.isGameOver:
			tetrisStatus = tetris.GetTetrisForNetwork()
			netAnswer = net.Sim(tetrisStatus)
			netAnswer = self.__filterNetAnswer(netAnswer)
			(pos,rot) = self.__parseNetAnswer(netAnswer)
			for i in range(rot):
				tetris.RotateBrickRight()
			(brickX,brickY) = tetris.GetBrickPosition()
			pos-=brickX
			if pos > 0:
				for i in range(pos):
					tetris.MoveBrickRight()
			elif pos < 0:
				for i in range(-pos):
					tetris.MoveBrickLeft()
			tetris.ConfirmMove()
			# time.sleep(0.1)
		net.fit = tetris.GetScore()


	def __parseNetAnswer(self,netAnswer):
		position = netAnswer[:10]
		rotation = netAnswer[10:]
		position = [index for index, value in enumerate(position) if value == 1]
		rotation = [index for index, value in enumerate(rotation) if value == 1]
		if len(position) == 0:
			rPos = int(np.random.rand() * 10)
		else:
			rPos = int(np.random.rand() * len(position))
			rPos = position[rPos]
		if len(rotation) == 0:
			rRot = int(np.random.rand() * 4)
		else:
			rRot = int(np.random.rand() * len(rotation))
			rRot = rotation[rRot]
		return(rPos,rRot)

	def __filterNetAnswer(self,netAnswer):
		answer = []
		for item in netAnswer:
			if item > 0:
				answer.append(1)
			else:
				answer.append(0)
		return answer

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
			self.tetrisList.append(Tetris())

	def __createNewUnit(self):
		self.tetrisList.append(Tetris())
		net = NeuronNetwork()
		net.New(17,30,14)
		net.Init()
		self.population.append(net)

def Main():
	p = Program()
	# p.StartNew(30)
	p.StartLoad(98)

	# t = Tetris()
	# # ll = []
	# p = Display()
	# p.Run(t)
	# # p.RunList(ll)
	pass

if __name__=="__main__":
	Main()
