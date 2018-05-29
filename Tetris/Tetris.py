from .Bricks import *
import numpy as np
import random
import copy
import pprint
import sys, traceback
from threading import Lock

class Tetris:
	"""
		board[y][x]
	"""
	BOARD_WIDTH = 10
	BOARD_HEIGHT = 21
	lock = Lock()

	def __init__(self):
		self.isGameOver = False
		self.onGameOver = None
		self.__brickLimit = 0
		self.__brickCounter = 0
		self.Restart()

	def Restart(self):
		self.brick = {}
		self.__initBoard()
		self.score = 0
		self.__brickCounter = 0
		self.isGameOver = False

	def __initBoard(self):
		self.board = [[0 for x in range(self.BOARD_WIDTH)] for y in range(self.BOARD_HEIGHT)]
		self.__getNextBrick()

	def GetBoardToPrint(self):
		boardToPrint = copy.deepcopy(self.board)
		boardToPrint = self.__connectBoardWithBrick(boardToPrint,self.brick)
		del boardToPrint[0]
		return boardToPrint

	def GetTetrisForNetwork(self):
		brick = self.__numberToBinary(self.brick['shapeNum'])
		board = self.__getBoardCondition()
		for item in brick:
			board.append(item)
		return board

	def GetBoard(self):
		b = copy.deepcopy(self.board)
		b = self.__connectBoardWithBrick(b,self.brick)
		del b[0]
		return b,self.brick['shapeNum'];

	def SetBrickLimit(self, limit):
		self.__brickLimit = limit

	def GetArrangedBrickCount(self):
		return self.__brickCounter

	def __numberToBinary(self,number):
		condition = []
		for i in range(7):
			if i == number:
				condition.append(1.0)
			else:
				condition.append(0.0)
		return condition

	def __getBoardCondition(self):
		condition = [0.0 for x in range(10)]
		level = 0
		for line in self.board:
			index = -1
			for cell in line:
				index+=1
				if cell == 0.0:
					continue
				if condition[index] == 0:
					condition[index] = 21-level
			level+=1
		minValue = min(condition)
		maxValue = max(condition)-minValue
		if maxValue == 0:
			return condition
		condition = [(x-minValue)/maxValue for x in condition]
		return condition

	def GetData(self):
		return {'board': self.board,
				'brick': self.brick}

	def SetGameOverEvent(self, func):
		self.onGameOver = func

	def __connectBoardWithBrick(self,board,brick):
		y = brick['y']
		rot = brick['rot']
		for brickLine in self.brick['shape'][rot]:
			x = brick['x']
			for item in brickLine:
				if not item == 0:
					if y>20 or x>=10:
						break
					try:
						board[y][x]=item
					except IndexError as e:
						Tetris.lock.acquire()
						pprint.pprint(board)
						print("Y: ",y," X: ",x)
						traceback.print_exc(file=sys.stdout)
						Tetris.lock.release()
						raise e
				x+=1
			y+=1
		return board

	def GetScore(self):
		return self.score

	def GetBrickPosition(self):
		return (self.brick['x'],self.brick['y'])

	def GetBrickRotateCount(self):
		l = len(self.brick['shape'])
		return l;

	def RotateBrickRight(self):
		#(l,x,y) = np.shape(self.brick['shape'])
		l = len(self.brick['shape'])
		rot = self.brick['rot']
		self.brick['rot']-=1
		if self.brick['rot'] < 0:
			self.brick['rot'] = l-1

		if not self.__checkBrickPositionIsValid():
			self.brick['rot'] = rot

	def RotateBrickLeft(self):
		#(l,x,y) = np.shape(self.brick['shape'])
		l = len(self.brick['shape'])
		rot = self.brick['rot']
		self.brick['rot']+=1
		if self.brick['rot'] >= l:
			self.brick['rot'] = 0
		if not self.__checkBrickPositionIsValid():
			self.brick['rot'] = rot

	def MoveBrickDown(self,confirm = True):
		#(l,x,y) = np.shape(self.brick['shape'])
		self.brick['y']+=1
		if confirm:
			self.score+=1
		if not self.__checkBrickPositionIsValid():
			self.brick['y']-=1
			if confirm:
				self.__newTurn()
			return False
		return True

	def ConfirmMove(self,isSimulation = False):
		while self.MoveBrickDown(not isSimulation):
			pass

	def ResetBrickPosition(self):
		self.brick['x'] = 4
		self.brick['y'] = 0
		self.brick['rot'] = 0

	def MoveBrickLeft(self):
		self.brick['x']-=1
		if not self.__checkBrickPositionIsValid():
			self.brick['x']+=1

	def MoveBrickRight(self):
		self.brick['x']+=1
		if not self.__checkBrickPositionIsValid():
			self.brick['x']-=1


	def __newTurn(self):
		self.__connectBoardWithBrick(self.board,self.brick)
		self.__getNextBrick()
		self.__checkFullLines()
		if not self.__checkBrickPositionIsValid():
			self.__gameOver()

	def __checkFullLines(self):
		lines = 0
		for line in self.board:
			fullLine = True
			for item in line:
				if item == 0:
					fullLine=False
					break
			if fullLine:
				lines+=1
				self.board.remove(line)
				self.board.insert(0, [0 for x in range(self.BOARD_WIDTH)])
		self.__addScoreForLines(lines)

	def __addScoreForLines(self,lines):
		if lines == 1:
			self.score+=20
		elif lines == 2:
			self.score+=50
		elif lines == 3:
			self.score+=150
		elif lines == 4:
			self.score+=600

	def __checkBrickPositionIsValid(self):
		brick = self.brick
		board = self.board
		#(lShape,xShape,yShape) = np.shape(brick['shape'])
		y = brick['y']
		rot = brick['rot']
		for brickLine in self.brick['shape'][rot]:
			x = brick['x']
			for item in brickLine:
				if not item == 0:
					if x < 0:
						return False
					elif x >= self.BOARD_WIDTH:
						return False
					elif y >= self.BOARD_HEIGHT:
						return False
					elif not board[y][x]== 0:
						return False
				x+=1
			y+=1
		return True

	def __getNextBrick(self):
		if self.__brickLimit != 0:
			if self.__brickCounter > self.__brickLimit:
				self.score += 1000
				self.__gameOver()
		self.__brickCounter+=1
		self.brick['x'] = 4
		self.brick['y'] = 0
		brickNum = random.randint(0, len(BRICKS) - 1)
		self.brick['shape'] = BRICKS[brickNum]
		self.brick['shapeNum'] = brickNum
		self.brick['rot'] = 0

	def __gameOver(self):
		self.isGameOver=True
		if self.onGameOver != None:
			self.onGameOver(self)
