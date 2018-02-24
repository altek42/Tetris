import numpy as np
import numpy.random as random
import os
import configparser
from pprint import pprint
from NetworkFunctions import NetworkFunctionsType
from NetworkFunctions import NetworkFunctions

CONFIG_SIZE = 'SIZE'
CONFIG_INPUT = 'input'
CONFIG_HIDDEN = 'hidden'
CONFIG_OUTPUT = 'output'
CONFIG_OTHER = 'OTHER'
CONFIG_FIT = 'fit'
CONFIG_FUNCTIONS = 'FUNCTIONS'
CONFIG_HIDDEN_FUNC = 'hidden_func'
CONFIG_OUTPUT_FUNC = 'output_func'
CONFIG_WEIGHTS = 'WEIGHTS'
CONFIG_V = 'V'
CONFIG_W = 'W'

class NeuronNetwork:
	def __init__(self):
		self.inputsCount=0
		self.outputCount=0
		self.hiddenCount=0
		self.weightV = []
		self.weightW = []
		self.hiddenFunc = NetworkFunctionsType.SIGMOIDAL
		self.outputFunc = NetworkFunctionsType.LINEAR
		self.name='Net'
		self.fit = 0
		pass

	def New(self,inputSize,hiddenSize,outputSize):
		self.inputsCount = inputSize
		self.hiddenCount = hiddenSize
		self.outputCount = outputSize

	def Init(self,hiddenFunc=NetworkFunctionsType.SIGMOIDAL,outputFunc=NetworkFunctionsType.LINEAR):
		self.hiddenFunc = hiddenFunc
		self.outputFunc = outputFunc
		self.weightV = (random.rand(self.inputsCount+1,self.hiddenCount)*2)-1
		self.weightW = (random.rand(self.hiddenCount+1,self.outputCount)*2)-1

	def Save(self,directory,name = None):
		if name == None:
			name = self.name
		else:
			self.name = name
		config = configparser.ConfigParser()
		config[CONFIG_SIZE] = {CONFIG_INPUT:self.inputsCount,
								CONFIG_HIDDEN:self.hiddenCount,
								CONFIG_OUTPUT:self.outputCount}
		config[CONFIG_OTHER] = {CONFIG_FIT:self.fit}
		config[CONFIG_FUNCTIONS] = {CONFIG_HIDDEN_FUNC:self.hiddenFunc.name,
									CONFIG_OUTPUT_FUNC:self.outputFunc.name}
		config[CONFIG_WEIGHTS] = {CONFIG_V:self.weightV,
								  CONFIG_W:self.weightW}
		with open(directory+"\\"+name, 'w') as configfile:
			config.write(configfile)

	def Load(self,directory,name):
		config = configparser.SafeConfigParser()
		config.read(directory+"\\"+name)
		self.name = name
		setting = config[CONFIG_SIZE]
		self.inputsCount = int(setting[CONFIG_INPUT])
		self.hiddenCount = int(setting[CONFIG_HIDDEN])
		self.outputCount = int(setting[CONFIG_OUTPUT])
		setting = config[CONFIG_OTHER]
		self.fit = int(setting[CONFIG_FIT])
		setting = config[CONFIG_FUNCTIONS]
		self.hiddenFunc = NetworkFunctionsType[setting[CONFIG_HIDDEN_FUNC]]
		self.outputFunc = NetworkFunctionsType[setting[CONFIG_OUTPUT_FUNC]]
		setting = config[CONFIG_WEIGHTS]
		self.weightV = self.__strToArray(setting[CONFIG_V])
		self.weightW = self.__strToArray(setting[CONFIG_W])

	def SetName(self,name):
		self.name = name

	def Sim(self,value):
		y,fi = self.__sim(value)
		return y

	def __sim(self,value):
		if len(value) != self.inputsCount:
			print("Wrong input size. Expected",self.inputsCount,"where",len(value),"was given.")
		x = [value]
		x = np.insert(x, 0, 1)
		s = np.matmul(x,self.weightV)
		fi = NetworkFunctions.ActivationFunction(s,self.hiddenFunc)
		fi2 = np.insert(fi, 0, 1)
		y = np.matmul(fi2,self.weightW)
		y = NetworkFunctions.ActivationFunction(y,self.outputFunc)
		return y,fi

	def Train(self,inData,outData,epochs,eta):
		for e in range(epochs):
			p = np.random.permutation(len(inData))
			inputData = [inData[p[i]] for i in range(len(inData))]
			outputData = [outData[p[i]] for i in range(len(outData))]
			for i in range(len(inputData)):
				y, fi = self.__sim(inputData[i])
				x = np.insert([inputData[i]],0,1)
				delta = outputData[i] - y
				derivative = NetworkFunctions.DerivativeFunction(fi,self.hiddenFunc)
				correction = (eta* delta* self.weightW[:][1:] * np.transpose([derivative]) * x).T
				self.weightV = np.add(self.weightV,correction)
				correction = np.array([eta*delta* np.insert(fi,0,1)]).T
				self.weightW = np.add(self.weightW, correction)

	def __strToArray(self,strArr):
		s = strArr
		s = s.replace('[[', '[')
		s = s.replace('[ ', '[')
		s = s.replace('[', '')
		s = s.replace(']]', '')
		s = s.replace('\n',',')
		s = s.replace(' ',',')
		s = s.replace(',,',',')
		s = s.replace('],',']')
		s = s.split(']')

		a = []
		for line in s:
			d = []
			for number in line.split(','):
				if number == '':
					continue
				d+=[float(number)]
			a+=[d]
		a = np.asarray(a)
		return a

	def __str__(self):
		s = "Name: {}\n".format(self.name)
		s +="\tinputs: {}\n".format(self.inputsCount)
		s +="\thidden: {}\n".format(self.hiddenCount)
		s +="\toutput: {}\n".format(self.outputCount)
		s +="\thidden func: {}\n".format(self.hiddenFunc)
		s +="\toutput func: {}\n".format(self.outputFunc)
		return s
