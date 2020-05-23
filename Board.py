from tkinter import *
from Configurations import *

class Board():

    def __init__(self, parent):
        self.parent = parent
        self.initChessBoard()

    def initChessBoard(self):
        self.images = {}
        self.createCanvas()
        self.drawBoard()
        self.drawAllPieces(START_POSITION)

    def createCanvas(self):
        canvasWidth = COLUMNS * SQUARE_SIZE
        canvasHeight = ROWS * SQUARE_SIZE
        self.canvas = Canvas(self.parent, width = canvasWidth, height = canvasHeight)
        self.canvas.pack()


    def drawBoard(self):
        color = COLOR_DARK
        for r in range(0, ROWS):
            if color == COLOR_LIGHT:
                color = COLOR_DARK
            else:
                color = COLOR_LIGHT
            for c in range(0, COLUMNS):
                x0 = c * SQUARE_SIZE
                y0 = r * SQUARE_SIZE
                x1 = x0 + SQUARE_SIZE
                y1 = y0 + SQUARE_SIZE
                square = COLUMNS_LABELS[c] + str(ROWS-r)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=square)
                self.canvas.create_text(x0+int(SQUARE_SIZE/10),y0+int(SQUARE_SIZE/10),text=square, font=("Purisa", int(SQUARE_SIZE/10)), fill="#1F1F1F")
                if color == COLOR_LIGHT:
                    color = COLOR_DARK
                else:
                    color = COLOR_LIGHT

    def drawAllPieces(self, position):
        for square in position:
            self.drawPiece(self.canvas, position[square], square)

    def drawPiece(self, canvas, piece, position):
        if(piece.lower() == piece):
            filename = 'black_' + piece + '.png'
        else:
            filename = 'white_' + piece.lower() + '.png'

        path = 'C:\\Users\\Serban\\PycharmProjects\\ChessLicenta\\pieces\\' + filename
        x,y = self.getPieceCoordinate(position)
        if path not in self.images:
            self.images[path] = PhotoImage(file=path)
        canvas.create_image(x, y, image = self.images[path])

    def getItemNumber(self, square):
        return 16 * (ord(square[0])-ord('A')) + (8-int(square[1]))*2 + 1

    def getPieceCoordinate(self, square):
        x = SQUARE_SIZE * (ord(square[0]) - ord('A')) + SQUARE_SIZE/2
        y = SQUARE_SIZE * (COLUMNS - int(square[1])) + SQUARE_SIZE/2
        return (x,y)

    # def drawPromotionList(self, pieces, square):
    #     self.promotion = Canvas(self.parent, width = SQUARE_SIZE, height = len(pieces)*SQUARE_SIZE)
    #     self.promotion.create_rectangle(0,0, SQUARE_SIZE, len(pieces)*SQUARE_SIZE, fill=WHITE)
    #
    #     for piece in pieces:
    #         self.drawPiece(self.promotion, piece, square)
    #     self.promotion.pack()


