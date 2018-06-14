from enum import Enum, unique
import numpy as np
from scipy.special import expit

@unique
class NetworkFunctionsType(Enum):
	LINEAR = 1
	SIGMOIDAL = 2

class NetworkFunctions:
	@staticmethod
	def ActivationFunction(x,typeFunc):
		if typeFunc == NetworkFunctionsType.LINEAR:
			return NetworkFunctions.__linearFunc(x)
		if typeFunc == NetworkFunctionsType.SIGMOIDAL:
			return NetworkFunctions.__sigmoidalFunc(x)

	@staticmethod
	def DerivativeFunction(x,typeFunc):
		if typeFunc == NetworkFunctionsType.LINEAR:
			return NetworkFunctions.__derivativeLinearFunc(x)
		if typeFunc == NetworkFunctionsType.SIGMOIDAL:
			return NetworkFunctions.__derivativeSigmoidalFunc(x)

#---------------------------------------------------
	@staticmethod
	def __linearFunc(x):
		return x

	@staticmethod
	def __sigmoidalFunc(x):
		return 1/(1+(np.exp(-x)))

#---------------------------------------------------
	@staticmethod
	def __derivativeLinearFunc(x):
		return 1

	@staticmethod
	def __derivativeSigmoidalFunc(x):
		return x*(1-x)
