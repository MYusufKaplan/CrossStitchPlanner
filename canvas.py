from copy import deepcopy
from square import Square
from math import sqrt

class Canvas:
    def __init__(self, matrix, genome, network):
        self.matrix = matrix
        self.squares, self.colorPath, self.colors = prepareVars(matrix)
        self.activeString = None
        self.genome = genome
        self.network = network
        self.mashedInput = self.generateMashed()

    def colorSquare(self, square):
        if square.completed:
            return False
        try:
            self.colorPath[square.color]
            if square.color != self.activeString:
                self.cutString()
                self.activeString = square.color
                lastHole = square.TL
                top = True
            lastHole = self.colorPath[square.color]["path"][-1]["hole"]
            if square.isHalf:
                if lastHole[0] == square.TR[0] and lastHole[1] == square.TR[1]:
                    top = False
                else:
                    top = (sqrt((abs(lastHole[0] - square.TR[0]) ** 2) + (abs(lastHole[1] - square.TR[1]) ** 2)) < sqrt((abs(lastHole[0] - square.BL[0]) ** 2) + (abs(lastHole[1] - square.BL[1]) ** 2)))
            else:
                if lastHole[0] == square.TL[0] and lastHole[1] == square.TL[1]:
                    top = False
                else:
                    top = (sqrt((abs(lastHole[0] - square.TL[0]) ** 2) + (abs(lastHole[1] - square.TL[1]) ** 2)) < sqrt((abs(lastHole[0] - square.BR[0]) ** 2) + (abs(lastHole[1] - square.BR[1]) ** 2)))
            if square.color != self.activeString:
                self.cutString()
                self.activeString = square.color
                lastHole = square.TL
                top = True
        except:
            lastHole = square.TL
            top = True

            
        if top:
            if square.isHalf:
                self.colorPath[square.color]["stringUsed"] += sqrt((abs(lastHole[0] - square.TR[0]) ** 2) + (abs(lastHole[1] - square.TR[1]) ** 2))
                self.colorPath[square.color]["path"].append({"hole": square.TR, "direction": "up"})
                self.colorPath[square.color]["stringUsed"] += sqrt(2)
                self.colorPath[square.color]["path"].append({"hole": square.BL, "direction": "down"})
                square.completed = True
                self.colorPath[square.color]["completed"] += 1
            else:
                self.colorPath[square.color]["stringUsed"] += sqrt((abs(lastHole[0] - square.TL[0]) ** 2) + (abs(lastHole[1] - square.TL[1]) ** 2))
                self.colorPath[square.color]["path"].append({"hole": square.TL, "direction": "up"})
                self.colorPath[square.color]["stringUsed"] += sqrt(2)
                self.colorPath[square.color]["path"].append({"hole": square.BR, "direction": "down"})
                square.isHalf = True
        else:
            if square.isHalf:
                self.colorPath[square.color]["stringUsed"] += sqrt((abs(lastHole[0] - square.BL[0]) ** 2) + (abs(lastHole[1] - square.BL[1]) ** 2))
                self.colorPath[square.color]["path"].append({"hole": square.BL, "direction": "up"})
                self.colorPath[square.color]["stringUsed"] += sqrt(2)
                self.colorPath[square.color]["path"].append({"hole": square.TR, "direction": "down"})
                square.completed = True
                self.colorPath[square.color]["completed"] += 1
            else:
                self.colorPath[square.color]["stringUsed"] += sqrt((abs(lastHole[0] - square.BR[0]) ** 2) + (abs(lastHole[1] - square.BR[1]) ** 2))
                self.colorPath[square.color]["path"].append({"hole": square.BR, "direction": "up"})
                self.colorPath[square.color]["stringUsed"] += sqrt(2)
                self.colorPath[square.color]["path"].append({"hole": square.TL, "direction": "down"})
                square.isHalf = True
        # print("Colored: {},{} {}".format(square.X,square.Y,self.colorPath[square.color]["left"]))
        return True
    
    def potentialStringUsed(self, square):
        stringUsed = sqrt(2)
        try:
            self.colorPath[square.color]
            lastHole = self.colorPath[square.color]["path"][-1]["hole"]
            if square.isHalf:
                if lastHole[0] == square.TR[0] and lastHole[1] == square.TR[1]:
                    top = False
                else:
                    top = (sqrt((abs(lastHole[0] - square.TR[0]) ** 2) + (abs(lastHole[1] - square.TR[1]) ** 2)) < sqrt((abs(lastHole[0] - square.BL[0]) ** 2) + (abs(lastHole[1] - square.BL[1]) ** 2)))
            else:
                if lastHole[0] == square.TL[0] and lastHole[1] == square.TL[1]:
                    top = False
                else:
                    top = (sqrt((abs(lastHole[0] - square.TL[0]) ** 2) + (abs(lastHole[1] - square.TL[1]) ** 2)) < sqrt((abs(lastHole[0] - square.BR[0]) ** 2) + (abs(lastHole[1] - square.BR[1]) ** 2)))
        except:
            return stringUsed
        
        if top:
            if square.isHalf:
                stringUsed += sqrt((abs(lastHole[0] - square.TR[0]) ** 2) + (abs(lastHole[1] - square.TR[1]) ** 2))
            else:
                stringUsed += sqrt((abs(lastHole[0] - square.TL[0]) ** 2) + (abs(lastHole[1] - square.TL[1]) ** 2))
        else:
            if square.isHalf:
                stringUsed += sqrt((abs(lastHole[0] - square.BL[0]) ** 2) + (abs(lastHole[1] - square.BL[1]) ** 2))
            else:
                stringUsed += sqrt((abs(lastHole[0] - square.BR[0]) ** 2) + (abs(lastHole[1] - square.BR[1]) ** 2))
        return stringUsed

    def cutString(self):
        if len(self.colorPath[self.activeString]['path']) == 0:
            return False
        self.colorPath[self.activeString]["stringUsed"] += 5
        self.colorPath[self.activeString]["path"].append({"hole": None, "direction": "cut"})
        return True

    def generateMashed(self):
        lst = []
        for sq in self.squares:
            lst.append(sq.BL[0])
            lst.append(sq.BL[1])
            lst.append(sq.BR[0])
            lst.append(sq.BR[1])
            lst.append(sq.TL[0])
            lst.append(sq.TL[1])
            lst.append(sq.TR[0])
            lst.append(sq.TR[1])
            lst.append(sq.X)
            lst.append(sq.Y)
            lst.append(sq.color)
            lst.append(int(sq.completed))
            lst.append(int(sq.isHalf))
        tup = to_tuple(lst)
        return tup

            

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)

def matrixToSquares(matrix):
    squares = []
    colors = []
    for idxX, row in enumerate(matrix):
        for idxY, sq in enumerate(row):
            squares.append(Square(sq, False,False, (idxX, idxY), (
                idxX, idxY+1), (idxX+1, idxY), (idxX+1, idxY+1)))
            if sq not in colors:
                colors.append(sq)
    return squares, colors







def prepareVars(matrix):
    squares, colors = matrixToSquares(matrix)
    colorPath = {}
    for color in colors:
        colorPath[color] = {"completed": 0,"left": 0, "path": [],"stringUsed":0}
    for sq in squares:
        colorPath[sq.color]["left"] += 1
    return squares,colorPath , colors