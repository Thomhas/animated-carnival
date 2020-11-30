# This class is responsible for storing the data of the current state of the game and it will also
# be responsible for determining the valid moves and keep a log of all the moves.

class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # log the move both to be able to change the move and to have the logs
        self.moveLog.append(move)
        print(self.moveLog)
        self.whiteToMove = not self.whiteToMove

    '''
    Undo function to go back one game state
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to be undone
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # reverses the turn

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getPossibleMoves()  # this will be kept like this for now

    '''
    All moves that are possible by the moves of chess without taking checks into account
    '''

    def getPossibleMoves(self):
        moves = []
        # loops for every row
        for row in range(len(self.board)):
            # loops for every column in the row
            for col in range(self.board[row]):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.getPawnMoves(row, col, moves)
                    elif piece == 'R':
                        self.getRockMoves(row, col, moves)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, moves)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, moves)
                    elif piece == 'K':
                        self.getKingMoves(row, col, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, moves)

    '''
    FUNCTIONS FOR POSSIBLE MOVES FOR ALL THE DIFFERENT PIECES
    '''

    '''
    All the possible pawn moves
    '''

    def getPawnMoves(self, row, col, board):


class Move():

    # maps key to values
    #key : value
    ranksToRows = {'1': 7, '2': 6, '3': 5,
                   '4': 4, '5': 3, '6': 2, '7': 1, '8': 1}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    ranksToCols = {'a': 0, 'b': 1, 'c': 2,
                   'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in ranksToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        # this can be changed to feel like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
