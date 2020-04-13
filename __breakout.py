from mine import *
from time import sleep, time
import math

class Paddle():
	def __init__(self, x, width):
		self.x = x
		self.width = width
	def setPos(self):
		playerPos = mc.player.getPos()
		if playerPos.x > pillarPos1.x+self.width/2+1 and playerPos.x < pillarPos2.x-self.width/2-1:
			self.x = playerPos.x
	def draw(self):
		mc.setBlocks(self.x-self.width/2, basisPos.y, basisPos.z,
			self.x+self.width/2, basisPos.y, basisPos.z, block.WOOL_RED)
	def erase(self):
		mc.setBlocks(self.x-self.width/2, basisPos.y, basisPos.z,
			self.x+self.width/2, basisPos.y, basisPos.z, block.AIR)
	def reload(self):
		self.erase()
		self.setPos()
		self.draw()

class Ball():
	def __init__(self):
		self.x = basisPos.x
		self.y = basisPos.y + 1
		self.xdir = -1
		self.ydir = -1
	def setPos(self):
		self.x = self.x + self.xdir
		self.y = self.y + self.ydir
	def rebound(self):
		if self.x <= pillarPos1.x+1 or self.x >= pillarPos2.x-1:
			self.xdir *= -1
		if self.y >= pillarPos1.y+14:
			self.ydir *= -1
		if self.x >= paddle.x-paddle.width/2-1 and self.x <= paddle.x+paddle.width/2+1:
			if self.y <= basisPos.y+1:
				self.ydir *= -1
	def judgeGameOver(self):
		if self.y <= basisPos.y:
			gameOver()
	def draw(self):
		mc.setBlock(self.x, self.y, basisPos.z, block.WOOL_WHITE)
	def erase(self):
		mc.setBlock(self.x, self.y, basisPos.z, block.AIR)
	def reload(self):
		tHash = int(math.modf(time())[0]*10)
		if tHash == 0 or tHash == 5:
			self.erase()
			self.rebound()
			self.setPos()
			self.judgeGameOver()
			self.draw()

class Brick():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def collision(self):
		if (ball.y >= brick.y-1 and ball.y <= brick.y+1) and (ball.x == self.x-1 or ball.x == self.x+1):
			ball.xdir *= -1
			if self in bricks:
				bricks.remove(self)
				self.erase()
		if (ball.x >= brick.x-1 and ball.x <= brick.x+1) and (ball.y == self.y-1 or ball.y == self.y+1):
			ball.ydir *= -1
			if self in bricks:
				bricks.remove(self)
				self.erase()
	def draw(self):
		mc.setBlock(self.x, self.y, basisPos.z, block.WOOL_ORANGE)
	def erase(self):
		mc.setBlock(self.x, self.y, basisPos.z, block.AIR)

def drawFrame():
	mc.setBlocks(pillarPos1.x, pillarPos1.y, pillarPos1.z,
		pillarPos1.x, pillarPos1.y+14, pillarPos1.z, block.WOOL_GRAY)
	mc.setBlocks(pillarPos2.x, pillarPos2.y, pillarPos2.z,
		pillarPos2.x, pillarPos2.y+14, pillarPos2.z, block.WOOL_GRAY)
	mc.setBlocks(pillarPos1.x, pillarPos1.y+15, pillarPos1.z,
		pillarPos2.x, pillarPos2.y+15, pillarPos2.z, block.WOOL_GRAY)
	mc.setBlocks(pillarPos1.x, pillarPos1.y+15, pillarPos1.z+1,
		pillarPos2.x, pillarPos2.y, pillarPos2.z+1, block.WOOL_BLACK)

def gameClear():
	mc.postToChat("You Win!")
	exit()

def gameOver():
	mc.postToChat("The Game is Over!")
	exit()


mc = Minecraft()

playerPos = mc.player.getPos()

delay = 0.1

basisPos = Vec3(playerPos.x, playerPos.y, playerPos.z+20)

pillarPos1 = Vec3(basisPos.x-6, basisPos.y, basisPos.z)
pillarPos2 = Vec3(basisPos.x+6, basisPos.y, basisPos.z)

paddle = Paddle(playerPos.x, 2)

ball = Ball()

drawFrame()

bricks = [Brick(basisPos.x-2, basisPos.y+13), Brick(basisPos.x-1, basisPos.y+13), Brick(basisPos.x, basisPos.y+13),
          Brick(basisPos.x+1, basisPos.y+13), Brick(basisPos.x+2, basisPos.y+13),
          Brick(basisPos.x-3, basisPos.y+12), Brick(basisPos.x-2, basisPos.y+12), Brick(basisPos.x-1, basisPos.y+12), Brick(basisPos.x, basisPos.y+12),
          Brick(basisPos.x+1, basisPos.y+12), Brick(basisPos.x+2, basisPos.y+12), Brick(basisPos.x+3, basisPos.y+12),
          Brick(basisPos.x-2, basisPos.y+10), Brick(basisPos.x-1, basisPos.y+10), Brick(basisPos.x, basisPos.y+10),
          Brick(basisPos.x+1, basisPos.y+10), Brick(basisPos.x+2, basisPos.y+10),
          Brick(basisPos.x-3, basisPos.y+9), Brick(basisPos.x-2, basisPos.y+9), Brick(basisPos.x-1, basisPos.y+9), Brick(basisPos.x, basisPos.y+9),
          Brick(basisPos.x+1, basisPos.y+9), Brick(basisPos.x+2, basisPos.y+9), Brick(basisPos.x+3, basisPos.y+9),
          Brick(basisPos.x-2, basisPos.y+7), Brick(basisPos.x-1, basisPos.y+7), Brick(basisPos.x, basisPos.y+7),
          Brick(basisPos.x+1, basisPos.y+7), Brick(basisPos.x+2, basisPos.y+7),
         ]
for brick in bricks:
	brick.draw()

mc.postToChat("The Game Started!")

while True:
	paddle.reload()
	ball.reload()
	for brick in bricks:
		brick.collision()
	if bricks == []:
		gameClear()
	sleep(delay)
