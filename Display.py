import pygame
import pprint

class Display:
	FPS = 5

	def __init__(self):
		pygame.init()
		self.screenWidth = 1400
		self.screenHeight = 800
		self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("monospace",20)
		self.isLoop = True
		self.isInput = True
		self.isTetrisList = False


	def Run(self,tetris):
		self.tetris = tetris
		self.tetris.SetGameOverEvent(self.__gameOver)
		self.__mainLoop()

	def RunList(self,tetrisList):
		self.isTetrisList = True
		self.tetrisList = tetrisList
		self.isInput = False
		self.__setDisplayGrid()
		self.__mainLoop()

	def __setDisplayGrid(self):
		levels = 0
		possibleGames = 0
		tetrisBoardCount = len(self.tetrisList)
		gamesWidth = tetrisBoardCount*2

		while possibleGames<gamesWidth:
			gamesWidth = int(gamesWidth/2)
			levels +=1
			oneHeightBoard = (self.screenHeight / levels)
			brickSize = oneHeightBoard-70
			brickSize = brickSize/20
			oneWidthBoard = (brickSize*13)+10
			possibleGames = int(self.screenWidth/oneWidthBoard)

		withSize = int(tetrisBoardCount/levels)
		if tetrisBoardCount % levels > 0:
			withSize+=1
		self.gridRows = levels
		self.gridColumns = withSize
		self.gridTileWidth = oneWidthBoard
		self.gridTileHeight = oneHeightBoard
		self.brickSize = brickSize

	def InputEnable(self,value=True):
		self.isInput = value

	def __mainLoop(self):
		while self.isLoop:
			self.__eventHandller()
			self.__printScreen()
			pass

	def __eventHandller(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.isLoop = False
			if event.type == pygame.KEYUP:
				self.__keyUpEvent(event)
		# action press
		# if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #                 is_blue = not is_blue
		# pressed = pygame.key.get_pressed()
		# if pressed[pygame.K_UP]: y -= 3
	def __keyUpEvent(self,event):
		if self.isInput:
			if event.key == pygame.K_q:
				self.tetris.RotateBrickLeft()
			elif event.key == pygame.K_e:
				self.tetris.RotateBrickRight()
			elif event.key == pygame.K_a:
				self.tetris.MoveBrickLeft()
			elif event.key == pygame.K_d:
				self.tetris.MoveBrickRight()
			elif event.key == pygame.K_s:
				self.tetris.MoveBrickDown()
			elif event.key == pygame.K_SPACE:
				self.tetris.ConfirmMove()
			elif event.key == pygame.K_p:
				self.tetris.ConfirmMove(isSimulation = True)
			elif event.key == pygame.K_o:
				self.tetris.ResetBrickPosition()
		if event.key == pygame.K_ESCAPE:
			self.isLoop = False

	def __printScreen(self):
		self.screen.fill((0, 0, 0))
		if self.isTetrisList:
			self.__printMultiGame()
		else:
			self.__printSingleGame()

		pygame.display.flip()
		self.clock.tick(self.FPS)

	def __printMultiGame(self):
		for j in range(self.gridRows):
			y = self.gridTileHeight * j
			for i in range(self.gridColumns):
				x = self.gridTileWidth * i
				index = i+(j*self.gridColumns)
				if index >= len(self.tetrisList):
					break
				self.__printBoardOnScreen(self.tetrisList[index],(x+10,y+10), 3)


	def __printSingleGame(self):
		self.brickSize = 30
		self.__printBoardOnScreen(self.tetris,(20,20), 4)
		self.__printObjectOnScreen({"score:":self.tetris.GetScore()},(370,20))

	def __printObjectOnScreen(self,obj,pos,color=(255,255,255)):
		text = pprint.pformat(obj)
		lines = text.splitlines()
		x, y = pos
		for item in lines:
			textRender = self.font.render(item, 0, color)
			self.screen.blit(textRender,(x,y))
			y+=textRender.get_height()

	def __printBoardOnScreen(self,tetris,pos,spaces):
		init_x,y = pos
		w,h = (self.brickSize,self.brickSize)
		board = tetris.GetBoardToPrint()
		for line in board:
			x = init_x
			for number in line:
				color = self.__numberToColor(number)
				pygame.draw.rect(self.screen, color, (x,y,w,h))
				x += w + spaces
			y += h + spaces

	def __numberToColor(self,number):
		if number == 0:
			return (44,44,44)
		elif number == 1:
			return (211,32,17)
		elif number == 2:
			return (32,211,17)
		elif number == 3:
			return (32,17,211)
		elif number == 4:
			return (211,32,211)
		elif number == 5:
			return (32,211,211)
		elif number == 6:
			return (211,211,32)
		elif number == 7:
			return (250,150,0)
		else:
			return (0,0,0)

	def __gameOver(self,sender,args=None):
		print("MAIN GAMEOVER")
		# sender.Restart()
