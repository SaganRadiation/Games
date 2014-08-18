# Slide Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame, sys, random, time
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 120

#                 R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK	 =  ( 0,   0,   0)
WHITE    =  (255, 255, 255)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
BASICFONTSIZE = 60

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

STARTTIME = 3 # 10 seconds
	

def makeText(text, top, left, color, bgcolor = None):
	textSurf = BASICFONT.render(text,True,color,bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)

def terminate():
	pygame.quit()
	sys.exit()
	
def checkForQuit():
	for event in pygame.event.get(QUIT):
		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event)

def writeBombText(time):
	formatTime = '00:'+ ('%02.2f' % time).zfill(5)
	textSurf, textRect = makeText(formatTime,0, 0,RED)
	textRect.center = WINDOWWIDTH / 2, WINDOWHEIGHT / 2
	DISPLAYSURF.blit(textSurf,textRect)

	
def fail(animationSpeed = 20):
	DISPLAYSURF.fill(BGCOLOR)
	writeBombText(0)
	origSurf = DISPLAYSURF.copy()
	newSurf = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
	newSurf = newSurf.convert_alpha()
	r,g,b = RED
	for _ in range(7):
		for start, stop, step in ((0, 255, 1), (255,0,-1)):
			for alpha in range(start,stop,animationSpeed * step):
				checkForQuit()
				DISPLAYSURF.blit(origSurf, (0,0))
				newSurf.fill((r,g,b,alpha))
				DISPLAYSURF.blit(newSurf, (0,0))
				pygame.display.update()
				FPSCLOCK.tick(FPS)
	for alpha in range(0,255,animationSpeed):
		checkForQuit()
		DISPLAYSURF.blit(origSurf, (0,0))
		newSurf.fill((r,g,b,alpha))
		DISPLAYSURF.blit(newSurf, (0,0))
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	for alpha in range(255,0, -int(animationSpeed/5)):
		checkForQuit()
		DISPLAYSURF.blit(origSurf, (0,0))
		newSurf.fill((r,g,b,alpha))
		DISPLAYSURF.blit(newSurf, (0,0))
		pygame.display.update()
		FPSCLOCK.tick(FPS)
			

def writeTitle():
	titleSurf = TITLEFONT.render('STOP THE BOMB',True,RED)
	titleRect = titleSurf.get_rect()
	titleRect.center = WINDOWWIDTH/2, WINDOWHEIGHT/5
	DISPLAYSURF.blit(titleSurf,titleRect)
	
def beHappy():
	titleSurf = TITLEFONT.render('YOU DID IT',True,RED)
	titleRect = titleSurf.get_rect()
	titleRect.center = WINDOWWIDTH/2, WINDOWHEIGHT/5
	DISPLAYSURF.blit(titleSurf,titleRect)
	
def writeInfo():
	titleSurf = INFOFONT.render('Press Space to stop the bomb.',True,RED)
	titleRect = titleSurf.get_rect()
	titleRect.center = WINDOWWIDTH/2, WINDOWHEIGHT*4/5
	DISPLAYSURF.blit(titleSurf,titleRect)
	
def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, TITLEFONT, INFOFONT, RESETSURF, RESETRECT, QUITSURF, QUITRECT
	stopTime = 0
	bombTicking = True
	
	pygame.init()
	pygame.font.init()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('Stop the Bomb')
	FPSCLOCK = pygame.time.Clock()
	BASICFONT = pygame.font.SysFont('monospace',80)
	TITLEFONT = pygame.font.Font(None,60)
	INFOFONT = pygame.font.Font(None,30)
	RESETFONT = pygame.font.Font(None,50)
	
	STOPSURF = RESETFONT.render('Stop',True,BLACK,RED)
	STOPRECT = STOPSURF.get_rect()
	STOPRECT.center = WINDOWWIDTH / 2, WINDOWHEIGHT - 110
	
	RESETSURF = RESETFONT.render('Reset',True,BLACK,RED)
	RESETRECT = RESETSURF.get_rect()
	RESETRECT.center = WINDOWWIDTH / 3, WINDOWHEIGHT - 55
	
	QUITSURF = RESETFONT.render('Quit',True,BLACK,RED)
	QUITRECT = QUITSURF.get_rect()
	QUITRECT.center = WINDOWWIDTH * 2 / 3, WINDOWHEIGHT - 55
	
	startTime = time.time()
	won = False
	
	while True:
		checkForQuit()
		DISPLAYSURF.fill(BGCOLOR)
		DISPLAYSURF.blit(STOPSURF,STOPRECT)
		DISPLAYSURF.blit(RESETSURF,RESETRECT)
		DISPLAYSURF.blit(QUITSURF,QUITRECT)
		
		if bombTicking:
			writeTitle()
		elif won:
			beHappy()
			#writeInfo()
			
		timeLeft = STARTTIME + startTime - time.time()
		
		if timeLeft <= 0 and bombTicking:
			stopTime = 0
			writeBombText(stopTime)
			fail()
			bombTicking = False
		elif bombTicking:
			writeBombText(timeLeft)
		else:
			writeBombText(stopTime)
			
		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_SPACE:
					if bombTicking == True:
						won = True
						stopTime = timeLeft
						bombTicking= False
			if event.type == MOUSEBUTTONUP:
				if STOPRECT.collidepoint(event.pos):
					if bombTicking == True:
						won = True
						stopTime = timeLeft
						bombTicking= False
				elif RESETRECT.collidepoint(event.pos):
					startTime = time.time()
					stopTime = 0
					bombTicking = True
					won = False
				elif QUITRECT.collidepoint(event.pos):
					terminate()
		pygame.display.update()

	
if __name__ == '__main__':
	main()