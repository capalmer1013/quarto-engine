from os import linesep
import random
import math
import time

COORDS = [(x, y) for x in range(4) for y in range(4)]
COLOR = 0
HEIGHT = 1
SHAPE = 2
HOLLOW = 3

class Piece(object):
    def __init__(self, color, height, shape, hollow):
        self.attr_tup = (color, height, shape, hollow)
    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.attr_tup == other.attr_tup

    def __repr__(self):
        return "{} {} {} {}".format(int(self.color), int(self.height), int(self.shape), int(self.hollow))
    
    @staticmethod
    def generateAllPieces():
        return [Piece(*[bool(num & (1<<n)) for n in range(4)]) for num in range(16)]
    
    @staticmethod
    def checkForEquality(pieces):
        if None in pieces:
            return False
        color = set([x.attr_tup[COLOR] for x in pieces])
        height = set([x.attr_tup[HEIGHT] for x in pieces])
        shape = set([x.attr_tup[SHAPE] for x in pieces])
        hollow = set([x.attr_tup[HOLLOW] for x in pieces])
        if len(color) == 1 or len(height) == 1 or len(shape) == 1 or len(hollow) == 1:
            return True
        return False

class Board(object):
    def __init__(self, state=None):
        if state:
            self.state=[x[:] for x in state]
            return

        self.state = [[None]*4 for _ in range(4)]

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
        return [x for x in COORDS if self.state[x[0]][x[1]] is None]
    
    def checkForWin(self):
        if any([self.checkRow(), self.checkColumn(), self.checkDiagonals()]):
            return True

        return False
    
    def checkRow(self):
        for x in range(4):
            piecesToCheck = [self.state[x][y] for y in range(4)]
    
            if Piece.checkForEquality(piecesToCheck):
                return True
        return False

    def checkColumn(self):
        for y in range(4):
            piecesToCheck = [self.state[x][y] for x in range(4)]
            
            if Piece.checkForEquality(piecesToCheck):
                return True
        return False

    def checkDiagonals(self):
        piecesToCheck = [self.state[i][i] for i in range(4)] + [self.state[i][3-i] for i in range(4)]
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
    move_count = 1
    # for _ in range(move_count):
    #     spot = random.choice(board.getAvailableSpots())
    #     piece = pieces.pop()
    #     board.place(*spot, piece)
    return recursiveTree(pieces, board, 0, 2)

def recursiveTree(pieces, board, depth=0, depth_limit=6):
    global winCount
    global tieCount
    global totalEliminated
    global playerAWins
    global playerBWins
    global depth_count
    if depth >= depth_limit:
        depth_count += 1
        return None
    result = {}
    for piece in pieces:
        for spot in board.getAvailableSpots():
            newBoard = Board(board.state)
            newPieces = [x for x in pieces]
            newPieces.remove(piece)
            if newBoard.place(*spot, piece):
                winCount += 1
                if len(pieces) % 2==0:
                    playerAWins += 1
                else:
                    playerBWins += 1
                totalEliminated += math.factorial(len(pieces))
                return board
            else:
                result[newBoard] = recursiveTree(newPieces, newBoard, depth+1, depth_limit)
    
    return result

depth_count = 0
totalCombo = math.factorial(16)
totalEliminated = 0
winCount = 0
tieCount = 0
playerAWins = 0
playerBWins = 0
start_time = time.time()
buildTree()
print("{} wins found, {} ties found in {} seconds".format(winCount, tieCount, time.time()-start_time))
print(str(depth_count) + " Nodes visited")
print(str(playerAWins) + " Wins for A")
print(str(playerBWins)+" Wins for B")
