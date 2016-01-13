'''
To Do:
    add reserve piece
    add rotations both left and right
    add sound effects
    add images
    add dropping piece
    extra: add different types of cascading
    add menu
    add pause button
    
'''

'''
Problems:
    what if the row tops out already, do not descend the piece. 
    Code is checking and falling out of order, check then fall 
    not fall then check.


'''

import copy
import random


TOP_BORDER = 30
BOTTOM_BORDER = 30
LEFT_BORDER = 200
RIGHT_BORDER = 30
BOARD_WIDTH = 300
BOARD_HEIGHT = 2*BOARD_WIDTH
SCREEN_WIDTH = BOARD_WIDTH + LEFT_BORDER + RIGHT_BORDER
SCREEN_HEIGHT = BOARD_HEIGHT + TOP_BORDER + BOTTOM_BORDER


class Tile:
    def __init__(self,x,y,pixSize):
        self.x = x
        self.y = y
        self.pixSize = pixSize
    
    def display(self):
        
        rect(self.x*self.pixSize+LEFT_BORDER, (self.y-4)*self.pixSize+TOP_BORDER,self.pixSize,self.pixSize)

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
            if tile.y>3:
                tile.display()
    
    def deleteTile(self,x,y):
        for t in self.tiles:
            if t.x == x and t.y == y:
                del t


class OPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,240,130,0)
        indices = [[x,y],[x,y+1],[x+1,y],[x+1,y+1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))
    
    def rotate(self):
        pass

class LPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,50,130,230)
        indices = [[x,y],[x+1,y],[x+2,y],[x+2,y+1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))
            
class JPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,255,191,28)
        indices = [[x,y+1],[x+1,y+1],[x+2,y],[x+2,y+1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))

class IPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,225,41,99)
        indices = [[x,y],[x+1,y],[x+2,y],[x+3,y]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))

class ZPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,58,170,62)
        indices = [[x,y],[x,y+1],[x+1,y+1],[x+1,y+2]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))
            
class SPiece(Piece):
    def __init__(self,x,y):
        Piece.__init__(self,172,35,178)
        indices = [[x,y+1],[x,y+2],[x+1,y],[x+1,y+1]]
        for r,c in indices:            
            self.tiles.append(Tile(x+r,y+c,BOARD_WIDTH/10))
    


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
            self.cascade(rowNum)

    def cascade(self,rowNum):
        for num in range(rowNum-1,-1,-1):
            toRemove = []
            for tile in self.rowHash[num]:
                tile.y +=1
                toRemove.append(tile)
                self.rowHash[num+1].append(tile)
            for tile in toRemove:
                self.rowHash[num].remove(tile)
    
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
        self.currentPiece = None
        self.sparePiece = None
        self.state = 'play'
        '''
           state can be play, menu, pause, gameover
        '''
        self.font = createFont("Arial",16,True)
        self.setNewPiece()
        
    def display(self):
        #show score
        fill(255)
        text(self.score,100, 50)
        self.board.display()
        self.currentPiece.display()
    
    def update(self):
        if not self.isOver():
            self.timer += 3
            if self.timer%self.speed == 0:
                if self.currentPiece.canFall(self.numRow) and not self.board.isCollision(self.currentPiece,0,1):
                    self.currentPiece.fall()
                else:
                    self.board.addPiece(copy.copy(self.currentPiece))
                    self.board.updateHash(self.currentPiece)
                    if not self.isOver():
                        self.setNewPiece()
            elif self.timer%(self.speed/2) == 0:
                if self.board.rowFull():
                    self.score += 1
                    self.board.removeRows()
                    
    def isOver(self):
        if self.board.rowHash[4] != []:
            print("gameover")
            self.state = 'gameover'
            return True
        else:
            return False
    
    def getNewPiece(self,x,y):
        pieceType = random.randint(0,5)
        if pieceType == 0:
            return OPiece(x,y) 
        elif pieceType == 1:
            return LPiece(x,y)
        elif pieceType == 2:
            return JPiece(x,y)
        elif pieceType == 3:
            return ZPiece(x,y)
        elif pieceType == 4:
            return SPiece(x,y)
        elif pieceType == 5:
            return IPiece(x,y)
            
    def setNewPiece(self):
        self.currentPiece = self.getNewPiece(0,0)
        
    
    def swapCurrentPiece(self):
        if self.swapPiece == None:
            self.swapPiece = self.currentPiece
            self.currentPiece = None
        pass
        
    def moveCurrentPiece(self,xDir,yDir):
        if not self.board.isCollision(self.currentPiece,xDir,yDir) and self.currentPiece.canMove(xDir,yDir,self.numRow,self.numCol):
            self.currentPiece.move(xDir,yDir)

game = Game(24,10)


def setup():
    size(SCREEN_WIDTH,SCREEN_HEIGHT) #change board size
    f = createFont("Arial",24)
    textFont(f)
    textAlign(CENTER, CENTER)
    
def draw():
    if game.state == 'play':
        background(40)
        stroke(255)
        fill(40)
        rect(LEFT_BORDER-1, TOP_BORDER-1, BOARD_WIDTH+2, BOARD_HEIGHT+2)
        stroke(40)
        game.update()
        game.display()
    elif game.state == 'gameover':
        background(40)
        stroke(255)
        fill(40)
        rect(LEFT_BORDER-1, TOP_BORDER-1, BOARD_WIDTH+2, BOARD_HEIGHT+2)
        stroke(40)
        game.display()
        fill(255)
        text("GAME OVER",LEFT_BORDER + BOARD_WIDTH/2, TOP_BORDER + BOARD_HEIGHT/2)
    elif game.state == 'menu':
        pass
    elif game.state == 'paused':
        background(40)
        stroke(255)
        fill(40)
        rect(LEFT_BORDER-1, TOP_BORDER-1, BOARD_WIDTH+2, BOARD_HEIGHT+2)
        stroke(40)
        game.display()
        fill(255)
        text("PAUSED",LEFT_BORDER + BOARD_WIDTH/2, TOP_BORDER + BOARD_HEIGHT/2)
    
    
def keyPressed():
    if game.state == 'play':
        if key == 's':
            print("swap")
            game.swapCurrentPiece()
        if key == ' ':
            print("drop piece")
        elif keyCode == UP:
            print("rotate")
        elif keyCode == DOWN:
            game.moveCurrentPiece(0,1)
        elif keyCode == LEFT:
            game.moveCurrentPiece(-1,0)
        elif keyCode == RIGHT:
            game.moveCurrentPiece(1,0)
        
def mousePressed():
    if game.state == 'play':
        game.state = 'paused'
    elif game.state == 'paused':
        game.state = 'play'
    elif game.state == 'gameover':
        #display screen that says click to restart
        game.__init__(20,10)
    elif game.state == 'menu':
        #define ranges for buttons
        pass
