
import numpy as np
import pygame
import math

# baord definition
_columnCount = 7
_rowCount = 6

# sizing
_squareSize = 100
_width = _columnCount * _squareSize
_height = (_rowCount + 1) * _squareSize  # plus one for a selection row
_size = (_width, _height)

_radius = _squareSize / 3

# colors
_blue = (0,0,255)
_red = (255,0,0)
_yellow = (255,255,0)
_black = (0,0,0)

# https://realpython.com/python-use-global-variable-in-function/
# board
_board = None


def CreateBoard():
    global _board
    _board = np.zeros((_rowCount,_columnCount))

def DrawCursor(screen, xPos, turnId):
    
    centerpoint = (xPos, _squareSize/2)
    if xPos - _radius < 0:
        centerpoint = (_radius, _squareSize/2)
    if xPos + _radius > _width:
        centerpoint = (_width -_radius, _squareSize/2)
        
    color = PlayerColorEncoder(turnId)
    pygame.draw.circle(screen, color, centerpoint, _radius)

def DrawBoard(screen):
    global _board
    screen.fill( _black)
    for x in range(_columnCount):
        for y in range(1,_rowCount+1):
            pygame.draw.rect(screen, _blue, (x*_squareSize, (y)*_squareSize, _squareSize, _squareSize))
            
            # radius = _squareSize / 3
            centerpoint = (x*_squareSize + (_squareSize/2), y * _squareSize + (_squareSize/2))
            
            boardIndex = _board[y-1][x]
            color = PlayerColorEncoder(boardIndex)
           
            pygame.draw.circle(screen, color, centerpoint, _radius)            
    
def DropPiece(column, color):
    global _board
    row = -1
    
    for x in range(0, _rowCount):
        entry = _board[x][column]
        if entry == 0:
            row = x
        else:
            break
    
    if row == -1:
        raise Exception("")
    
    _board[row][column] = color

def GetSelectedColumn(xPos):
    return math.floor(xPos / (_width/ _columnCount)) 

def GetSize():
    return _size

def PlayerColorEncoder(player):
    if player == 1:
        return _red
    elif player == 2:
        return _yellow
    else:
        return _black

def PrintBoard():
    print(_board)

def ValidPosition(column):
    return _board[0][column] == 0

def WinCondition():
    winnerID = 0
    run = 4
    for rowIndex in range(_rowCount):
        for colIndex in range(_columnCount):
            
            fourInColumn = True
            fourInRow = True
            fourInDownRight = True
            fourInDownLeft = True
            
            winnerID = _board[rowIndex][colIndex]
            if winnerID == 0:
                continue
            for runIndex in range(run):
                columnPlusZ = colIndex + runIndex
                rowPlusZ = rowIndex + runIndex
                columnMinusZ = colIndex - runIndex
                # print("{w}: {c}, {r}, {c2}".format(w=winnerID, c=columnPlusZ,r=rowPlusZ,c2=columnMinusZ))
                try:
                    fourInRow = fourInRow and (columnPlusZ < _columnCount)
                    fourInColumn = fourInColumn and rowPlusZ < _rowCount
                    fourInDownRight = fourInDownRight and  columnPlusZ < _columnCount and rowPlusZ < _rowCount
                    fourInDownLeft = fourInDownLeft and rowPlusZ < _rowCount and columnMinusZ >= 0
                    if fourInRow is True:
                        fourInRow = _board[rowIndex][columnPlusZ] == winnerID
                        # print("Row: {r}".format(r=board[rowIndex][columnPlusZ]))
                    if fourInColumn is True:
                        fourInColumn = _board[rowPlusZ][colIndex] == winnerID
                        # print("Column: {c}".format(c=board[rowPlusZ][colIndex]))
                    if fourInDownRight is True:
                        fourInDownRight = _board[rowPlusZ][columnPlusZ] == winnerID
                    if fourInDownLeft is True:
                        fourInDownLeft = _board[rowPlusZ][columnMinusZ] == winnerID
                except Exception as e:
                    print(e)
            if fourInRow or fourInColumn or fourInDownRight or fourInDownLeft:
                return winnerID
            
    return None

