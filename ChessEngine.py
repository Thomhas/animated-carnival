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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRockMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

    '''
    Makes the move
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # log the move both to be able to change the move and to have the logs
        self.moveLog.append(move)
        # print(self.moveLog)
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
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.getPawnMoves(row, col, moves)
                    elif piece == 'R':
                        self.getRookMoves(row, col, moves)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, moves)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, moves)
                    elif piece == 'K':
                        self.getKingMoves(row, col, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, moves)
        return moves

    '''
    FUNCTIONS FOR POSSIBLE MOVES FOR ALL THE DIFFERENT PIECES
    '''

    '''
    All the possible pawn moves
    '''

    def getPawnMoves(self, row, col, moves):
        # WHITE PAWNS
        if self.whiteToMove:
            if self.board[row-1][col] == '--':  # check if the square is empty
                moves.append(Move((row, col), (row-1, col), self.board))
                # TWO SQUARE PAWN ADVANCED
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    # upp and to the left
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    # upp and to the right
                    moves.append(Move((row, col), (row-1, col+1), self.board))
        # BLACK PAWNS
        elif not self.whiteToMove:
            if self.board[row+1][col] == '--':  # check if square in front is empty
                moves.append(Move((row, col), (row+1, col), self.board))
                # TWO SQUARE PAWN ADVANCED
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col - 1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    # down and left
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col + 1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    # down and right
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    '''
    All possible rook moves
    '''

    def getRookMoves(self, row, col, moves):
        if self.whiteToMove:
            enemyColor = 'b'
        elif not self.whiteToMove:
            enemyColor = 'w'
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # same color piece
                        break
                else:  # out of the board
                    break

    '''
    All possible bishop moves
    '''

    def getBishopMoves(self, row, col, moves):
        if self.whiteToMove:
            enemyColor = 'b'
        elif not self.whiteToMove:
            enemyColor = 'w'

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))

        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break  # friendly piece
                else:  # off the board
                    break

    def getKnightMoves(self, row, col, moves):
        if self.whiteToMove:
            enemyColor = 'b'
        elif not self.whiteToMove:
            enemyColor = 'w'

        directions = ((2, 1), (2, -1), (1, 2), (1, -2),
                      (-2, 1), (-2, -1), (-1, 2), (-1, -2))
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--':
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))

    def getKingMoves(self, row, col, moves):
        if self.whiteToMove:
            enemyColor = 'b'
        elif not self.whiteToMove:
            enemyColor = 'w'

        directions = ((0, 1), (0, -1), (-1, 1), (-1, 0),
                      (-1, -1), (1, 1), (1, 0), (1, -1))
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == '--':
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))

        if self.whiteToMove:
            self.whiteKingLocation.append(
                Move((row, col), (endRow), endCol), self.board)
        elif not self.whiteToMove:
            self.blackKingLocation.append(
                Move((row, col), (endRow), endCol), self.board)

    def getQueenMoves(self, row, col, moves):
        self.getBishopMoves
        self.getRookMoves


class Move():

    # maps key to values
    # key : value
    ranksToRows = {'0': 7, '1': 6, '2': 5,
                   '3': 4, '4': 3, '5': 2, '6': 1, '7': 1}
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

        self.MoveID = self.startRow * 1000 * self.startCol * \
            100 + self.endRow * 10 + self.endCol

    '''
    Override the equals sing
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False

    def getChessNotation(self):
        # this can be changed to feel like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
