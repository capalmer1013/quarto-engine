from os import linesep
import random

class Piece(object):
    def __init__(self, color, height, shape, hollow):
        self.color = color
        self.height = height
        self.shape = shape
        self.hollow = hollow
    
    def __repr__(self):
        return "{} {} {} {}".format(int(self.color), int(self.height), int(self.shape), int(self.hollow))
    
    @staticmethod
    def generateAllPieces():
        result = []
        for num in range(16):
            result.append(Piece(*[bool(num & (1<<n)) for n in range(4)]))
        return result
    
    @staticmethod
    def checkForEquality(pieces):
        color = set([x.color if x is not None else None for x in pieces])
        height = set([x.height if x is not None else None for x in pieces])
        shape = set([x.shape if x is not None else None for x in pieces])
        hollow = set([x.hollow if x is not None else None for x in pieces])
        if None in color or None in height or None in shape or None in hollow:
            return False
        if len(color) == 2 or len(height) == 2 or len(shape) == 2 or len(hollow) == 2:
            return True
        return False

class Board(object):
    def __init__(self):
        self.state = []
        for i in range(4):
            self.state.append([])
            for j in range(4):
                self.state[i].append(None)

    def __str__(self):
        result = ""
        for row in self.state:
            result += str(row) + linesep
        return result
    
    def place(self, x, y, piece):
        if self.state[x][y] is not None:
            raise "spot {},{} taken by {}".format(x, y, self.state[x][y])
        self.state[x][y] = piece

        return self.checkForWin()

    
    def getAvailableSpots(self):
        result = []
        for i in range(4):
            for j in range(4):
                if self.state[i][j] is None:
                    result.append((i, j))
        return result
    
    def checkForWin(self):
        if self.checkRow():
            return True
        if self.checkColumn():
            return True
        if self.checkDiagonals():
            return True
        return False
    
    def checkRow(self):
        for x in range(4):
            piecesToCheck = []
            for y in range(4):
                piecesToCheck.append(self.state[x][y])
            
            if Piece.checkForEquality(piecesToCheck):
                return True
        return False

    def checkColumn(self):
        for y in range(4):
            piecesToCheck = []
            for x in range(4):
                piecesToCheck.append(self.state[x][y])
            
            if Piece.checkForEquality(piecesToCheck):
                return True
        return False

    def checkDiagonals(self):
        pass

def printAvailPieces(p):
    for i in p:
        print(i)

pieces = Piece.generateAllPieces()
random.shuffle(pieces)
printAvailPieces(pieces)
print("-------------------")
board = Board()
print(board)

for i in range(16):
    print(i)
    spot = random.choice(board.getAvailableSpots())
    piece = pieces.pop()
    if board.place(*spot, piece):
        print("game ended")
        break


print("end game")
print("--------------------------------")

print(board)