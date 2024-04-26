import numpy as np
import pygame
import sys
from board import * 

    
# SET UP

CreateBoard()
pygame.init()
screen = pygame.display.set_mode(GetSize())

# font
font = pygame.font.SysFont("monospace", 75)

gameOver = False
turn = 0
winner = None


#  GAME LOOP
while not gameOver:    
    turnId = turn % 2 + 1
    
    DrawBoard(screen)
    
    xPos, yPos = pygame.mouse.get_pos()
    DrawCursor(screen, xPos, turnId)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # must be capital
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            try:
                selectionInt = GetSelectedColumn(xPos)
                if ValidPosition(selectionInt):
                    DropPiece(selectionInt, turnId)
                    DrawBoard(screen)
                    winner = WinCondition()
                    gameOver = winner is not None
                    turn += 1
                    
            except Exception as e:
                print(e)
                exit()

# VICTORY PAGE LOOP
close = False
while not close:   
    DrawBoard(screen)
    
    label = font.render("Player {winner} wins!".format(winner=winner), 1, PlayerColorEncoder(winner))
    screen.blit(label, (40, 10))
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # must be capital
            close = True
            sys.exit()