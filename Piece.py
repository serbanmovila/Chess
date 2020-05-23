import copy

from Configurations import *
from Game import *

class Piece():

    def __init__(self, color, square):
        self.color = color
        self.square = square

    # def isPinned(self, position):
    #
    #     def getDirection(king):
    #         dir = [(ord(self.square[0]) - ord(king[0])), int(self.square[1]) - int(king[1])]
    #         if dir[0]==0 or dir[1]==0:
    #             return[dir[0],dir[1]]
    #
    #         if abs(dir[0]) != abs(dir[1]):
    #             return False
    #
    #         if dir[0] and dir[1]:
    #             dir[0] //= abs(dir[0])
    #             dir[1] //= abs(dir[0])
    #         return [dir[0],dir[1]]
    #
    #     def checkPin(king, pos, direction):
    #         square = str(chr(ord(self.square[0]) + direction[0])) + str(int(self.square[1]) + int(direction[1]))
    #         while 'A' <= square[0] <= COLUMNS_LABELS[len(COLUMNS_LABELS) - 1] and 1 <= int(square[1]) <= ROWS:
    #
    #             for piece in pos:
    #                 if pos[piece].color != self.color:
    #                     if king in pos[piece].getAvailableMoves(pos):
    #                         return True
    #             square = str(chr(ord(square[0]) + direction[0])) + str(int(square[1]) + int(direction[1]))
    #         return False
    #
    #     completePos = copy.deepcopy(position)
    #     pos = copy.deepcopy(position)
    #     del pos[self.square]
    #     king = None
    #     for sq in pos:
    #         if pos[sq].__class__.__name__ == 'King' and pos[sq].color == self.color:
    #             king = sq
    #
    #     direction = getDirection(king)
    #     print(self.isInCheck(king, position))
    #
    #     print(direction)
    #     if direction:
    #         return checkPin(king, pos, direction)
    #     return False

    # def getAvailableMoves(self, position, moveDirections, moveDistance, captureDirections = None, captureDistance = 0):
    #     availableMoves = []
    #     # print(self.square)
    #     # print(self.color)
    #
    #     if captureDirections is None:
    #         captureDirections = moveDirections
    #         captureDistance = moveDistance
    #
    #     for dir in moveDirections:
    #         dist = 1
    #         newSquare = str(chr(ord(self.square[0]) + dir[0])) + str(int(self.square[1:]) + dir[1])
    #         while newSquare not in position and 'A' <= newSquare[0] <= COLUMNS_LABELS[len(COLUMNS_LABELS)-1] and 1 <= int(newSquare[1:]) <= ROWS and dist <= moveDistance:
    #             dist = dist + 1
    #             availableMoves.append(newSquare)
    #             newSquare = str(chr(ord(newSquare[0]) + dir[0])) + str(int(newSquare[1]) + dir[1])
    #
    #     availableMoves = availableMoves + self.getLegalCaptures(position, captureDirections, captureDistance)
    #     return availableMoves

    def getLegalMoves(self, position, moveDirections, moveDistance, captureDirections = None, captureDistance = 0):

        # if self.__class__.__name__ == 'King':
        #     if self.isInCheck(position):
        #         pass
        # elif self.isPinned(position):
        #     return []

        legalMoves = []
        # print(self.square)
        # print(self.color)

        if captureDirections is None:
            captureDirections = moveDirections
            captureDistance = moveDistance

        for dir in moveDirections:
            dist = 1
            newSquare = str(chr(ord(self.square[0]) + dir[0])) + str(int(self.square[1:]) + dir[1])
            while newSquare not in position and 'A' <= newSquare[0] <= COLUMNS_LABELS[len(COLUMNS_LABELS)-1] and 1 <= int(newSquare[1:]) <= ROWS and dist <= moveDistance:
                dist = dist + 1
                legalMoves.append(newSquare)
                newSquare = str(chr(ord(newSquare[0]) + dir[0])) + str(int(newSquare[1]) + dir[1])

        legalMoves = legalMoves + self.getLegalCaptures(position, captureDirections, captureDistance)
        # print(legalMoves)
        return legalMoves

        # return self.getAvailableMoves(position)


    def getLegalCaptures(self, position, captureDirections, captureDistance):
        legalCaptures = []

        for dir in captureDirections:
            dist = 1
            newSquare = str(chr(ord(self.square[0]) + dir[0])) + str(int(self.square[1:]) + dir[1])
            while dist <= captureDistance and 'A' <= newSquare[0] <= COLUMNS_LABELS[len(COLUMNS_LABELS)-1] and 1 <= int(newSquare[1:]) <= ROWS:
                if newSquare in position:
                    if position[newSquare].color != self.color:
                        legalCaptures.append(newSquare)
                    break
                dist = dist + 1
                newSquare = str(chr(ord(newSquare[0]) + dir[0])) + str(int(newSquare[1]) + dir[1])
        return legalCaptures

    # def isInCheck(self, king, position):
    #
    #     for piece in position:
    #         if position[piece].color != position[king].color:
    #             if position[king] in position[piece].getAvailableMoves(position):
    #                 return True
    #     return False



class Queen(Piece):

    def __init__(self, color, square):
        self.name = 'Queen'
        self.moveDistance = max(ROWS, COLUMNS)
        self.captureDistance = max(ROWS, COLUMNS)
        self.moveCount = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     return super().getAvailableMoves(position, ROOK_DIRECTIONS + BISHOP_DIRECTIONS, self.moveDistance)

    def getLegalMoves(self, position):
        return super().getLegalMoves(position, ROOK_DIRECTIONS + BISHOP_DIRECTIONS, self.moveDistance)

class King(Piece):

    def __init__(self, color, square):
        self.name = 'King'
        self.moveDistance = 1
        self.captureDistance = 1
        self.castlingRights = [1,1]
        self.moveCount = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     return super().getAvailableMoves(position, BISHOP_DIRECTIONS + ROOK_DIRECTIONS, self.moveDistance)

    def castles(self, move):
        if move in ['C8', 'G8', 'C1', 'G1']:
            return True
        return False

    def getLegalMoves(self, position):
        legalMoves = list()
        if self.color == 'black':
            if self.moveCount == 0 and self.castlingRights[0] == 1 and 'C8' not in position and 'D8' not in position:
                if 'A8' in position:
                    if position['A8'].moveCount == 0:
                        legalMoves.append('C8')
            if self.moveCount == 0 and self.castlingRights[1] == 1 and 'F8' not in position and 'G8' not in position:
                if 'H8' in position:
                    if position['H8'].moveCount == 0:
                        legalMoves.append('G8')
        else:
            if self.moveCount == 0 and self.castlingRights[0] == 1 and 'C1' not in position and 'D1' not in position:
                if 'A1' in position:
                    if position['A1'].moveCount == 0:
                        legalMoves.append('C1')
            if self.moveCount == 0 and self.castlingRights[1] == 1 and 'F1' not in position and 'G1' not in position:
                if 'H1' in position:
                    if position['H1'].moveCount == 0:
                        legalMoves.append('G1')

        enemy = 'white'
        if self.color == 'white':
            enemy = 'black'

        for piece in position:
            if position[piece].color == enemy and position[piece].name != 'King':
                for move in legalMoves:
                    if move in position[piece].getLegalMoves(position):
                        legalMoves.remove(move)

        return legalMoves + super().getLegalMoves(position, BISHOP_DIRECTIONS + ROOK_DIRECTIONS, self.moveDistance)

class Rook(Piece):

    def __init__(self, color, square):
        self.name = 'Rook'
        self.moveDistance = max(ROWS, COLUMNS)
        self.captureDistance = max(ROWS, COLUMNS)
        self.moveCount = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     return super().getAvailableMoves(position, ROOK_DIRECTIONS, self.moveDistance)

    def getLegalMoves(self, position):
        return super().getLegalMoves(position, ROOK_DIRECTIONS, self.moveDistance)

class Knight(Piece):

    def __init__(self, color, square):
        self.name = 'Knight'
        self.moveDistance = 1
        self.captureDistance = 1
        self.moveCount = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     return super().getAvailableMoves(position, KNIGHT_DIRECTIONS, self.moveDistance)

    def getLegalMoves(self, position):
        return super().getLegalMoves(position, KNIGHT_DIRECTIONS, self.moveDistance)

class Bishop(Piece):

    def __init__(self, color, square):
        self.name = 'Bishop'
        self.moveDistance = max(ROWS, COLUMNS)
        self.captureDistance = max(ROWS, COLUMNS)
        self.moveCount = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     return super().getAvailableMoves(position, BISHOP_DIRECTIONS, self.moveDistance)

    def getLegalMoves(self, position):
        return super().getLegalMoves(position, BISHOP_DIRECTIONS, self.moveDistance)

class Pawn(Piece):

    def __init__(self, color, square):
        self.name = 'Pawn'
        self.moveDistance = 2
        self.captureDistance = 1
        self.moveCount = 0
        self.enPassantMove = 0
        Piece.__init__(self, color, square)

    # def getAvailableMoves(self, position):
    #     if self.color == 'black':
    #         pawn_directions = copy.deepcopy(PAWN_DIRECTIONS)
    #         pawn_captures = copy.deepcopy(PAWN_CAPTURES)
    #
    #         for i in range(0, len(pawn_directions)):
    #             pawn_directions[i][1] = min(pawn_directions[i][1], - pawn_directions[i][1])
    #         for i in range(0, len(pawn_captures)):
    #             pawn_captures[i][1] = min(pawn_captures[i][1], - pawn_captures[i][1])
    #         if self.square[1] != '7':
    #             self.moveDistance = 1
    #         return super().getAvailableMoves(position, pawn_directions, self.moveDistance, pawn_captures,
    #                                      self.captureDistance)
    #     else:
    #         if self.square[1] != '2':
    #             self.moveDistance = 1
    #         return super().getAvailableMoves(position, PAWN_DIRECTIONS, self.moveDistance, PAWN_CAPTURES,
    #                                      self.captureDistance)

    def enPassant(self, position):

        legalMoves = []

        if self.color == 'black':
            if int(self.square[1]) == 4:
                possiblePawnsEP = [str(chr(ord(self.square[0]) - 1)) + str(4), str(chr(ord(self.square[0]) + 1)) + str(4)]
                print("possible for " + self.square + ' ' + str(possiblePawnsEP))
                for square in possiblePawnsEP:
                    if square in position:
                        if position[square].name == 'Pawn' and position[square].color == 'white':
                            if position[square].enPassantMove != 0:
                                legalMoves.append(position[square].square[0] + str(3))

        if self.color == 'white':
            if int(self.square[1]) == 5:
                possiblePawnsEP = [str(chr(ord(self.square[0]) - 1)) + str(5), str(chr(ord(self.square[0]) + 1)) + str(5)]
                print("possible for " + self.square + ' ' + str(possiblePawnsEP))
                for square in possiblePawnsEP:
                    if square in position:
                        if position[square].name == 'Pawn' and position[square].color == 'black':
                            if position[square].enPassantMove != 0:
                                legalMoves.append(position[square].square[0] + str(6))
        return legalMoves

    def getLegalMoves(self, position):

        if self.color == 'black':
            pawn_directions = copy.deepcopy(PAWN_DIRECTIONS)
            pawn_captures = copy.deepcopy(PAWN_CAPTURES)

            for i in range(0, len(pawn_directions)):
                pawn_directions[i][1] = min(pawn_directions[i][1], - pawn_directions[i][1])
            for i in range(0, len(pawn_captures)):
                pawn_captures[i][1] = min(pawn_captures[i][1], - pawn_captures[i][1])
            if self.square[1] != '7':
                self.moveDistance = 1

            return self.enPassant(position) + super().getLegalMoves(position, pawn_directions, self.moveDistance, pawn_captures, self.captureDistance)
        else:
            if self.square[1] != '2':
                self.moveDistance = 1
            return self.enPassant(position) + super().getLegalMoves(position, PAWN_DIRECTIONS, self.moveDistance, PAWN_CAPTURES, self.captureDistance)

