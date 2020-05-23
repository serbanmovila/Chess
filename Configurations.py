ROWS = 8
COLUMNS = 8
SQUARE_SIZE = 64
COLOR_LIGHT = '#C0A684'
COLOR_DARK = '#835F42'

WHITE = '#FFFFFF'

ROWS_LABELS = list(i for i in range(ROWS))
COLUMNS_LABELS = list(chr(i) for i in range(65, 65 + COLUMNS))

START_POSITION = {
    "A8": "r", "B8": "n", "C8": "b", "D8": "q", "E8": "k", "F8": "b", "G8": "n", "H8": "r",
    "A7": "p", "B7": "p", "C7": "p", "D7": "p", "E7": "p", "F7": "p", "G7": "p", "H7": "p",
    "A2": "P", "B2": "P", "C2": "P", "D2": "P", "E2": "P", "F2": "P", "G2": "P", "H2": "P",
    "A1": "R", "B1": "N", "C1": "B", "D1": "Q", "E1": "K", "F1": "B", "G1": "N", "H1": "R"
}

ROOK_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
BISHOP_DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
KNIGHT_DIRECTIONS = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
PAWN_DIRECTIONS = [[0, 1]]
PAWN_CAPTURES = [[-1, 1], [1, 1]]
