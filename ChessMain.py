# Main driver file responsible for handeling user input and displaying the game
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # this can be useful for later animations?
IMAGES = {}  # images dictionary that will be called once, this contains all the images


def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wN',
              'bN', 'wB', 'bB', 'wK', 'bK', 'wQ', 'bQ']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            'images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))
    # Note: with this we can acces the image of a specific pieces with IMAGES['#piecename']


'''
The main driver of the code
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # variable to make sure that a move is valid

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # MOUSE handeler
            elif e.type == p.MOUSEBUTTONDOWN:
                # p.mouse.get.pos() returns the cordinates of the mouse position
                location = p.mouse.get_pos()
                # now the coordinates have to be changed into squares
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # if you select the same space a second time
                    sqSelected = ()  # deselect click
                    playerClicks = []  # remove the log of player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:  # after the second click
                    move = ChessEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board)
                    # print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()  # reset the clicks
                    playerClicks = []  # reset the clicks
            # KEY handeler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when z is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Function responsible of graphics of the current game state
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw the board (squares)
    # later could add move suggestion/piece highliting
    placePieces(screen, gs.board)  # place pieces on the right square


def drawBoard(screen):
    colors = [p.Color('gray'), p.Color('white')]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            squareColor = colors[((row+col) % 2)]
            p.draw.rect(screen, squareColor, p.Rect(
                col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def placePieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(
                    col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
