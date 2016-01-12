'''
To Do:
    add reserve piece
    add other piece shapes
    add rotations both left and right
    add score
    add border
    add sound effects
    add images
    add cascading
    
'''

import copy
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 2*SCREEN_WIDTH
BORDER_SIZE = SCREEN_WIDTH - 
GAME_WIDTH = 
GAME_HEIGHT = 


class Tile:
    def __init__(self,x,y,pixSize):
        self.x = x
        self.y = y
        self.pixSize = pixSize
    
    def display(self):
        rect(self.x*self.pixSize, self.y*self.pixSize,self.pixSize,self.pixSize)

class Piece:
    def __init__(self,R,G,B):
        self.tiles = []
        self.R = R
        self.G = G
        self.B = B
    
    def canFall(self, numRows):
        for t in self.tiles:
            if (t.y+1) >= numRows:
                return False
        return True
    
    def canMove(self,xDir,yDir,numRows,numCol):
        for t in self.tiles:
            if not (t.y + yDir in range(numRows) and t.x + xDir in range(numCol)):
                return False
        return True 
        
    def fall(self):
        for t in self.tiles:
            t.y += 1
        
    def move(self,xDir,yDir):
        for t in self.tiles:
            t.x += xDir
            t.y += yDir
    
    def display(self):
        fill(self.R, self.G, self.B)
        for tile in self.tiles:
            tile.display()
    
    def deleteTile(self,x,y):
        for t in self.tiles:
            if t.x == x and t.y == y:
                del t


class SquarePiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,240,130,0)
        indices = [[0,0],[0,1],[1,0],[1,1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,SCREEN_WIDTH/10))

class LPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,50,130,230)
        indices = [[0,0],[1,0],[2,0],[2,1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,SCREEN_WIDTH/10))
            
class SquarePiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,240,130,0)
        indices = [[0,0],[0,1],[1,0],[1,1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,SCREEN_WIDTH/10))

class Board:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.rowHash = {i:[] for i in range(numRows)}
        self.pieces = []
        self.Keys = {UP:False, DOWN:False, LEFT:False, RIGHT:False}

    def getTile(self,r,c):
        for tile in self.board:
            if tile.x == r and tile.y == c:
                return tile
            

    def isCollision(self, currentPiece, xDir, yDir):
        for piece in self.pieces:
            for deadTile in piece.tiles:
                for liveTile in currentPiece.tiles:
                    if deadTile.x == liveTile.x + xDir and deadTile.y == liveTile.y + yDir:
                        return True
        return False
    
    def updateHash(self,piece):
        ''' Adds the rows tiles to the counter to see if a row needs to be deleted '''
        for t in piece.tiles:
            self.rowHash[t.y].append(t)
    
    def rowFull(self):
        for rowNum in range(self.numRows):
            if len(self.rowHash[rowNum]) == self.numCols:
                return rowNum
            
    def removeRows(self):
        
        rowNum = self.rowFull()
        if rowNum:
            row = self.rowHash[rowNum]
            #delete all tiles in the full row from the pieces
            for t in row:
                for piece in self.pieces:
                    if t in piece.tiles:
                        piece.tiles.remove(t)
            self.rowHash[rowNum] = []
#             rowNum = self.rowFull()
#             
#         for row in range(self.numRows):
#             tiles = []
#             for piece in self.pieces:
#                 for t in piece.tiles:
#                     if t.y == row:
#                         tiles.append(t)
#             if len(tiles) == self.numCols:
#                 for t in tiles:
#                     
#                 print("filled row", row)
    
    def display(self):
        for piece in self.pieces:
            piece.display()
    
    def addPiece(self,piece):
        self.pieces.append(piece)
    
class Game:
    def __init__(self, numRow, numCol):
        self.numRow = numRow
        self.numCol = numCol
        self.board = Board(numRow, numCol)
        self.score = 0
        self.speed = 20
        self.timer = 0
        self.setNewPiece()
        
    def display(self):
        self.board.display()
        self.currentPiece.display()
    
    def update(self):
        self.timer += 1
        if self.timer%self.speed == 0:
            if self.currentPiece.canFall(self.numRow) and not self.board.isCollision(self.currentPiece,0,1):
                self.currentPiece.fall()
            else:
                self.board.addPiece(copy.copy(self.currentPiece))
                self.board.updateHash(self.currentPiece)
                self.setNewPiece()
        elif self.timer%(self.speed/2) == 0:
            if self.board.rowFull():
                self.score += 1
                self.board.removeRows()
        
    def display(self):
        self.board.display()
        self.currentPiece.display()
    
    def setNewPiece(self):
        self.currentPiece = SquarePiece(0,0)
        pieceType = random.randint(0,1)
        if pieceType == 0:
            self.currentPiece = SquarePiece(0,0) 
        elif pieceType == 1:
            self.currentPiece = LPiece(0,0) 
    
    def moveCurrentPiece(self,xDir,yDir):
        if not self.board.isCollision(self.currentPiece,xDir,yDir) and self.currentPiece.canMove(xDir,yDir,self.numRow,self.numCol):
            self.currentPiece.move(xDir,yDir)

game = Game(20,10)


def setup():
    size(SCREEN_WIDTH,SCREEN_HEIGHT) #change board size
    print(width, height)
def draw():
    background(40)
    game.update()
    game.display()
    
def keyPressed():
    if keyCode == UP:
        print("rotate")
    elif keyCode == DOWN:
        game.moveCurrentPiece(0,1)
    elif keyCode == LEFT:
        game.moveCurrentPiece(-1,0)
    elif keyCode == RIGHT:
        game.moveCurrentPiece(1,0)
    

