from Display import *
from Tetris.Tetris import *
import pprint
import threading
import os
import configparser
import random

POPULATION_DIR = '.\\POPULATION_GEN2'
GAMES_LIMIT = 50000

class Program:

	BRICK_LIMIT = 50000

	def __init__(self, isDisplay=True):
		self.__isDisplay = isDisplay
		if isDisplay:
			self.display = Display()
		self.tetrisList = []
		self.population = []
		self.generation = 0

	def StartNew(self,size):
		self.__createNewPopulation(size)
		self.__actions = self.tetrisList[0].GetAllActions()
		self.__start()

	def StartLoad(self,size,gen):
		self.__loadPopulation(size,gen)
		self.__actions = self.tetrisList[0].GetAllActions()
		self.__start()

	def __createNewPopulation(self,size):
		for i in range(size):
			self.__createNewUnit()

	def __createNewUnit(self):
		t = Tetris()
		t.SetBrickLimit(self.BRICK_LIMIT)
		self.tetrisList.append(t)
		self.population.append( Unit() )

	def __start(self):
		t = threading.Thread(target=self.__mainLoop)
		t.daemon = True
		t.start()
		if self.__isDisplay:
			self.display.RunList(self.tetrisList)
		t.join()

	def __mainLoop(self):
		for game in range(GAMES_LIMIT):
			th = []
			for i in range(len(self.population)):
				t = threading.Thread(target=self.__unitPlay,args=(i,))
				t.daemon = True
				t.start()
				th.append(t)

			for item in th:
				item.join()

			self.__showFit()
			self.__createNextPopulation()
			for item in self.tetrisList:
				item.Restart()

	def __showFit(self):
		fits = []
		for item in self.population:
			fits.append(item.fit)
		print(self.generation,fits,"<",max(fits),min(fits),int(sum(fits)/len(fits)),">")


	def __unitPlay(self, index):
		unit = self.population[index]
		tetris= self.tetrisList[index]
		while not tetris.isGameOver:
			(pos,rot) = self.__getBestMove(tetris,unit)
			tetris.MoveBrickAt(pos, rot)
			tetris.ConfirmMove()
		unit.fit = tetris.GetScore()
		unit.Save(POPULATION_DIR, self.generation, index)

	def __getBestMove(self,tetris,unit):
		best = None
		fit = None
		for action in self.__actions:
			pos, rot = action
			tetris.MoveBrickAt(pos,rot)
			tetris.ConfirmMove(isSimulation = True)
			board, brick = tetris.GetBoard()
			value = self.__rate(board, unit)
			if fit == None or fit < value:
				fit = value
				best = action
			tetris.ResetBrickPosition()
		return best

	def __rate(self, board, unit):
		val, clear, holes, blockades = self.__getState(board)
		rate = val * unit.Height
		rate += clear * unit.Clear
		rate += holes * unit.Holes
		rate += blockades * unit.Blockades
		return rate

	def __getState(self, board):
		vec = [0 for x in range(8)]
		vecBlock = [0 for x in range(8)]
		clear = 0
		holes = 0
		blockades = 0
		yLen = len(board)
		xLen = len(board[0])
		fullLine = False
		for y in range(yLen):
			fullLine = True
			for x in range(xLen):
				if board[y][x] == 0:
					fullLine = False
				if vec[x] == 0 and board[y][x] != 0:
					vec[x] = yLen-y
					vecBlock[x] += 1
				elif vec[x] != 0 and board[y][x] == 0:
					holes += 1
					blockades += vecBlock[x]
					vecBlock[x] = 0
			if fullLine:
				clear+=1
		return sum(vec), clear, holes, blockades

	def __createNextPopulation(self):
		self.population = self.__selectNewPopulation()
		size = len(self.population)
		for i in range(0, size, 2):
			self.__crossUnits(i,i+1)
		for i in range(size):
			self.__mutateUnit(i)
		self.generation+=1

	def __mutateUnit(self, i):
		unit = self.population[i]
		r = np.random.rand()
		if r < 0.1:
			unit.Height = self.__mutateValue(unit.Height)
		r = np.random.rand()
		if r < 0.1:
			unit.Clear = self.__mutateValue(unit.Clear)
		r = np.random.rand()
		if r < 0.1:
			unit.Holes = self.__mutateValue(unit.Holes)
		r = np.random.rand()
		if r < 0.1:
			unit.Blockades = self.__mutateValue(unit.Blockades)

	def __mutateValue(self,value):
		et = np.random.rand() - 0.5
		et *= 2
		if et < 0:
			et -= 0.5
		else:
			et += 0.5
		return et*value

	def __crossUnits(self, u1, u2):
		r = np.random.rand()
		if r < 0.2:
			return
		r = np.random.randint(0,10)
		unit1 = self.population[u1]
		unit2 = self.population[u2]
		if r == 0 or r==4 or r==5 or r==6:
			unit1.Height, unit2.Height = unit2.Height, unit1.Height
		if r == 1 or r==4 or r==7 or r==8:
			unit1.Clear, unit2.Clear = unit2.Clear, unit1.Clear
		if r == 2 or r==5 or r==7 or r==9:
			unit1.Holes, unit2.Holes = unit2.Holes, unit1.Holes
		if r == 3 or r==6 or r==8 or r==9:
			unit1.Blockades, unit2.Blockades = unit2.Blockades, unit1.Blockades


	def __selectNewPopulation(self):
		size = len(self.population)
		newPopulation = []
		for i in range(size):
			champion = self.__getChampion(self.population,3)
			unit = copy.deepcopy(champion)
			unit.fit=0
			newPopulation.append(unit)
		return newPopulation

	def __getChampion(self, population, k):
		best = None
		for i in range(k):
			r = np.random.randint(0,len(population))
			unit = population[r]
			if best == None or best.fit < unit.fit:
				best = unit
		return best

	def __loadPopulation(self,size,gen):
		self.generation = gen
		for i in range(size):
			t = Tetris()
			t.SetBrickLimit(self.BRICK_LIMIT)
			self.tetrisList.append(t)
			u = Unit()
			u.Load(POPULATION_DIR, gen, i)
			self.population.append( u )


class Unit(object):
	__lock = threading.Lock()
	__config = configparser.ConfigParser()

	def __init__(self):
		super(Unit, self).__init__()
		self.Height = random.random()
		self.Clear = random.random()
		self.Holes = random.random()
		self.Blockades = random.random()
		self.fit = 0

	def Save(self, directory, name, number):
		with self.__lock:
			self.__config['Unit_'+str(number)] = {
					'height': self.Height,
					'clear': self.Clear,
					'holes': self.Holes,
					'blockades': self.Blockades,
					'fit': self.fit
				}
			if not os.path.exists(directory):
				os.makedirs(directory)
			with open(directory+"\\"+str(name), 'w') as configfile:
				self.__config.write(configfile)

	def Load(self, directory, name, number):
		with self.__lock:
			self.__config.read(directory+"\\"+str(name))
			settings = self.__config['Unit_'+str(number)]
			self.Height = float(settings['height'])
			self.Clear = float(settings['clear'])
			self.Holes = float(settings['holes'])
			self.Blockades = float(settings['blockades'])
			self.fit = float(settings['fit'])

	def __str__(self):
		return """[Unit]
Height:		{0}
Clear:		{1}
Holes:		{2}
Blockades:	{3}
""".format(self.Height, self.Clear, self.Holes, self.Blockades)
