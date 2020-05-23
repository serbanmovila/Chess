from Board import *
from Configurations import *
from Piece import *
from Exceptions import *

class Game():

    def __init__(self, parent):
        self.parent = parent
        self.createGame()

    def createGame(self):
        self.board = Board(self.parent)
        self.positionNotation = START_POSITION
        self.position = self.getInitialPosition()
        self.turn = 'white'
        self.selectedPiece = None
        self.fullMoveCount = 0
        self.halfMoveCount = 0
        self.board.canvas.bind("<Button-1>", self.onClickEvent)

    def getInitialPosition(self):
        position = {}
        for i in START_POSITION:
            if START_POSITION[i] == 'Q':
                position[i] = Queen('white', i)
            elif START_POSITION[i] == 'q':
                position[i] = Queen('black', i)
            elif START_POSITION[i] == 'K':
                position[i] = King('white', i)
            elif START_POSITION[i] == 'k':
                position[i] = King('black', i)
            elif START_POSITION[i] == 'R':
                position[i] = Rook('white', i)
            elif START_POSITION[i] == 'r':
                position[i] = Rook('black', i)
            elif START_POSITION[i] == 'B':
                position[i] = Bishop('white', i)
            elif START_POSITION[i] == 'b':
                position[i] = Bishop('black', i)
            elif START_POSITION[i] == 'N':
                position[i] = Knight('white', i)
            elif START_POSITION[i] == 'n':
                position[i] = Knight('black', i)
            elif START_POSITION[i] == 'P':
                position[i] = Pawn('white', i)
            elif START_POSITION[i] == 'p':
                position[i] = Pawn('black', i)
        return position

    def onClickEvent(self, event):
        selectedSquare = self.getClickedSquare(event)
        if selectedSquare in self.position:
            print(self.position[selectedSquare].getLegalMoves(self.position))

        # selects friendly piece to move
        if selectedSquare in self.position and self.selectedPiece is None and self.turn == self.position[selectedSquare].color:
            self.selectedPiece = selectedSquare

        # selects square to move the selected piece
        if self.selectedPiece is not None:
            # selects another piece
            if selectedSquare in self.position and self.turn == self.position[selectedSquare].color:
                self.selectedPiece = selectedSquare
            else:
                self.makeMove(self.selectedPiece, selectedSquare)
                self.selectedPiece = None

    def makeMove(self, selectedPiece, selectedSquare):

        if self.isCheckmate(self.position, self.turn):
            print("Checkmate!")
            return

        if self.isStalemate(self.position, self.turn):
            print("Stalemate!")
            return

        if self.isLegalMove(selectedPiece, selectedSquare):
            self.updatePosition(selectedPiece, selectedSquare)
            self.updateTurn()

    def isLegalMove(self, selectedPiece, selectedSquare):
        if selectedSquare not in self.position[selectedPiece].getLegalMoves(self.position):
            return False

        else:
            if self.isPinned(self.position, selectedPiece):
                return False

            newPos = copy.deepcopy(self.position)
            if selectedSquare in self.position[selectedPiece].getLegalMoves(self.position):
                newPos[selectedSquare] = self.position[selectedPiece]
                del newPos[selectedPiece]

            if self.isInCheck(self.position, self.turn) is False and self.isInCheck(newPos, self.turn):
                return False

            if self.isInCheck(self.position, self.turn) and self.isInCheck(newPos, self.turn):
                return False

            return True

    def getClickedSquare(self, event):
        clickedCol = chr(65 + event.x // SQUARE_SIZE)
        clickedRow = ROWS - event.y // SQUARE_SIZE
        square = str(str(clickedCol) + str(clickedRow))
        return square

    def updatePosition(self, selectedPiece, selectedSquare):

        if self.position[selectedPiece].name == 'King' and self.position[selectedPiece].castles(selectedSquare):
            print("castles")
            self.castles(selectedSquare)

        self.updateEnPassant(selectedPiece, selectedSquare)

        self.position[selectedSquare] = self.position[selectedPiece]
        self.position.pop(selectedPiece)
        self.position[selectedSquare].square = selectedSquare
        self.position[selectedSquare].moveCount += 1

        # print(selectedSquare)
        # self.checkPawnPromotion(selectedSquare)

        self.halfMoveCount += 1
        if self.turn == 'black':
            self.fullMoveCount += 1

        self.positionNotation[selectedSquare] = self.positionNotation[selectedPiece]
        self.positionNotation.pop(selectedPiece)
        self.board.canvas.delete(ALL)
        self.board.drawBoard()
        self.board.drawAllPieces(self.positionNotation)

    def updateTurn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def isInCheck(self, position, color):

        for piece in position:
            if position[piece].__class__.__name__ == 'King' and position[piece].color == color:
                king = piece

        for piece in position:
            if position[piece].color != color:
                if king in position[piece].getLegalMoves(position):
                    return True
        return False

    def isPinned(self, position, piece):
        if position[piece].__class__.__name__ == 'King':
            return False

        newPos = copy.deepcopy(self.position)
        del newPos[piece]
        if self.isInCheck(self.position, self.turn) is False and self.isInCheck(newPos, self.turn):
            return True
        return False

    def getAllLegalMoves(self, position, color):
        legalMoves = []
        for piece in position:
            if position[piece].color == color:
                for move in position[piece].getLegalMoves(position):
                    if self.isLegalMove(position[piece].square, move):
                        legalMoves.append((position[piece].square, move))
        return legalMoves

    def hasLegalMoves(self, position, color):
        for piece in position:
            if position[piece].color == color:
                for move in position[piece].getLegalMoves(position):
                    if self.isLegalMove(position[piece].square, move):
                        return True
        return False

    def isCheckmate(self, position, color):
        if self.hasLegalMoves(position, color) is False:
            if self.isInCheck(position, color):
                return True
        return False

    def isStalemate(self, position, color):
        if self.hasLegalMoves(position, color) is False:
            if self.isInCheck(position, color) is False:
                return True
        return False

    def castles(self, selectedSquare):
        if selectedSquare == 'G1':
            self.position['F1'] = self.position['H1']
            self.position.pop('H1')
            self.position['F1'].square = 'F1'
            self.position['F1'].moveCount += 1
            self.positionNotation['F1'] = self.positionNotation['H1']
            self.positionNotation.pop('H1')

        if selectedSquare == 'C1':
            self.position['D1'] = self.position['A1']
            self.position.pop('A1')
            self.position['D1'].square = 'D1'
            self.position['D1'].moveCount += 1
            self.positionNotation['D1'] = self.positionNotation['A1']
            self.positionNotation.pop('A1')

        if selectedSquare == 'G8':
            self.position['F8'] = self.position['H8']
            self.position.pop('H8')
            self.position['F8'].square = 'F8'
            self.position['F8'].moveCount += 1
            self.positionNotation['F8'] = self.positionNotation['H8']
            self.positionNotation.pop('H8')

        if selectedSquare == 'C8':
            self.position['D8'] = self.position['A8']
            self.position.pop('A8')
            self.position['D8'].square = 'D8'
            self.position['D8'].moveCount += 1
            self.positionNotation['D8'] = self.positionNotation['A8']
            self.positionNotation.pop('A8')

    def isValidEnPassant(self, selectedPiece, selectedSquare):
        if self.position[selectedPiece].name == 'Pawn' and selectedSquare not in self.position and selectedPiece[0] != selectedSquare[0]:
            return True
        return False

    def updateEnPassant(self, selectedPiece, selectedSquare):
        if self.isValidEnPassant(selectedPiece, selectedSquare):
            print("it is")
            if self.turn == 'white':
                self.position.pop(selectedSquare[0] + str(5))
                self.positionNotation.pop(selectedSquare[0] + str(5))
            else:
                self.position.pop(selectedSquare[0] + str(4))
                self.positionNotation.pop(selectedSquare[0] + str(4))

        for piece in self.position:
            if self.position[piece].name == 'Pawn':
                self.position[piece].enPassantMove = 0

        if self.turn == 'white':
            if self.position[selectedPiece].name == 'Pawn':
                if selectedPiece[1] == '2' and selectedSquare[1] == '4':
                    self.position[selectedPiece].enPassantMove = self.halfMoveCount + 1

        if self.turn == 'black':
            if self.position[selectedPiece].name == 'Pawn':
                if selectedPiece[1] == '7' and selectedSquare[1] == '5':
                    self.position[selectedPiece].enPassantMove = self.halfMoveCount + 1

    # def checkPawnPromotion(self, piece):
    #     if self.position[piece].name == 'Pawn' and (int(piece[1]) == 1 or int(piece[1]) == ROWS):
    #         self.promotePawn(piece)
    #
    # def choosePromotedPiece(self, event):
    #     clickedRow = event.y // SQUARE_SIZE
    #     return clickedRow
    #
    # def promotePawn(self, pawn):
    #     pieces = ['q', 'r', 'n', 'b']
    #     if int(pawn[1]) == ROWS:
    #         for piece in pieces:
    #             piece = piece.upper()
    #
    #     self.board.drawPromotionList(pieces, pawn)
    #     self.board.promotion.bind('<Button-1>', self.choosePromotedPiece)



def main():
    root = Tk()
    root.title("Chess")
    newGame = Game(root)
    root.mainloop()


if __name__ == '__main__':
    main()
