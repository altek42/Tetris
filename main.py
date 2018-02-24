from Display import *
from Tetris.Tetris import *
from Network.NeuronNetwork import *
import pprint

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,80)

class Program:
	def __init__(self,size):
		self.display = Display()
		self.tetrisList = []
		self.population = []
		self.generation = 0

	def Start(self):
		pass

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

	def __createNewUnit(self):
		self.tetrisList.append(Tetris())
		net = NeuronNetwork()
		net.New(17,12,14)
		net.Init()
		self.population.append(net)

def Main():
	p = Program(20)
	p.Start()

	# t = Tetris()
	# ll = []
	# p = Display()
	# p.Run(t)
	# p.RunList(ll)
	pass

if __name__=="__main__":
	Main()
