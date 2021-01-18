from os import linesep
import random
from copy import deepcopy
import math
import time

class Piece(object):
    def __init__(self, color, height, shape, hollow):
        self.color = color
        self.height = height
        self.shape = shape
        self.hollow = hollow
    
    def __eq__(self, other):
        if not hasattr(other, "color") or not hasattr(other, "height") or not hasattr(other, "shape") or not hasattr(other, "hollow"):
            return False
        return self.color == other.color and self.height == other.height and self.shape == other.shape and self.hollow == other.hollow

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
        if len(color) == 1 or len(height) == 1 or len(shape) == 1 or len(hollow) == 1:
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
            row_s = "|"
            for each in row:
                row_s += str(each).ljust(8) + "|"
            result += row_s + linesep
        return result
    
    def place(self, x, y, piece):
        global tieCount
        if self.state[x][y] is not None:
            raise "spot {},{} taken by {}".format(x, y, self.state[x][y])
        self.state[x][y] = piece
        win = self.checkForWin()
        allSpotsTaken = False
        for x in self.state:
            if None in x:
                allSpotsTaken = True
                break
        if not win and not allSpotsTaken:
            tieCount += 1
            #print("TIE")
            #print(tieCount)

        return win

    
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
        piecesToCheck = []
        for i in range(4):
            # print(i)
            # print(self.state[i])
            # print(self.state[i][3-i])
            piecesToCheck.append(self.state[i][i])
            piecesToCheck.append(self.state[i][3-i])
        if Piece.checkForEquality(piecesToCheck):
            return True
        False


def printAvailPieces(p):
    for i in p:
        print(i)

def testRandom():
    pieces = Piece.generateAllPieces()
    random.shuffle(pieces)
    #printAvailPieces(pieces)
    print("--------------------------------")
    board = Board()
    # print(board)

    for i in range(16):
        #print(i)
        spot = random.choice(board.getAvailableSpots())
        piece = pieces.pop()
        if board.place(*spot, piece):
            print(i)
            print("game ended")
            break


    print("end game")
    print("--------------------------------")

    print(board)


def buildTree():
    pieces = Piece.generateAllPieces()
    board = Board()
    move_count = 8
    for _ in range(move_count):
        spot = random.choice(board.getAvailableSpots())
        piece = pieces.pop()
        board.place(*spot, piece)
    return recursiveTree(pieces, board, 0, 12-move_count)

def recursiveTree(pieces, board, depth=0, depth_limit=6):
    global winCount
    global tieCount
    global totalEliminated
    global playerAWins
    global playerBWins
    if depth >= depth_limit:
        return None
    result = {}
    for piece in pieces:
        for spot in board.getAvailableSpots():
            newBoard = deepcopy(board)
            newPieces = deepcopy(pieces)
            newPieces.remove(piece)
            if newBoard.place(*spot, piece):
                winCount += 1
                if len(pieces) % 2==0:
                    playerAWins += 1
                else:
                    playerBWins += 1
                totalEliminated += math.factorial(len(pieces))
                if winCount % 10000 == 0:
                    pass
                    #print(winCount)
                    #print(str(totalCombo - totalEliminated)+" possibilities remaining")
                    #print(str(totalEliminated - winCount)+" eliminations")
                return board
            else:
                result[newBoard] = recursiveTree(newPieces, newBoard, depth+1, depth_limit)
    
    return result


totalCombo = math.factorial(16)
totalEliminated = 0
winCount = 0
tieCount = 0
playerAWins = 0
playerBWins = 0
start_time = time.time()
buildTree()
print("{} wins found, {} ties found in {} seconds".format(winCount, tieCount, time.time()-start_time))
print(str(playerAWins) + " Wins for A")
print(str(playerBWins)+" Wins for B")
