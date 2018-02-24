import numpy as np
import copy
import pprint

class Genetic:

	def __init__(self):
		pass

	def CrossNetworks(self, net1, net2):
		r = np.random.rand()
		if r < 0.2:
			return
		(nV1,nV2)=self.__crossArray(net1.weightV,net2.weightV)
		(nW1,nW2)=self.__crossArray(net1.weightW,net2.weightW)
		net1.weightV = nV1
		net2.weightV = nV2
		net1.weightW = nW1
		net2.weightW = nW2

	def __crossArray(self,arr1,arr2):
		(x,y) = np.shape(arr1)
		r = int(np.random.rand() * (x-1))+1
		newArr1 = np.append(arr1[:r], arr2[r:],axis=0)
		newArr2 = np.append(arr2[:r], arr1[r:],axis=0)
		return (newArr1,newArr2)

	def MutateNetwork(self,net):
		self.__mutateArray(net.weightV)
		self.__mutateArray(net.weightW)

	def __mutateArray(self,arr):
		(row,column) = np.shape(arr)
		for x in range(row):
			for y in range(column):
				r = np.random.rand()
				if r > 0.1:
					continue
				arr[x][y] = self.__mutateValue(arr[x][y])

	def __mutateValue(self,value):
		et = np.random.rand() - 0.5
		et = et * 2
		et = value * et
		return -(value+et)

	def SelectNewPopulation(self,oldPopulation):
		return self.__tournamentSelection(oldPopulation)

	def __tournamentSelection(self,oldPopulation):
		populationSize = len(oldPopulation)
		newPopulation = []
		for p in range(populationSize):
			champion = self.__getChampion(oldPopulation,3)
			newUnit = copy.deepcopy(champion)
			newUnit.fit = 0
			newPopulation.append(newUnit)
		return newPopulation

	def __getChampion(self,population,k):
		best = None
		for i in range(k):
			r = int(np.random.rand() * len(population))
			net = population[r]
			if best == None:
				best = net
			else:
				if best.fit < net.fit:
					best = net
		return best

if __name__ == '__main__':
	import p4
