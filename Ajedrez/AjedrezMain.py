"""
Drivers File. Responsable de los inputs del user y de preparar el GameState
"""

import pygame as p
from Ajedrez import AjedrezEngine

WIDTH = HEIGHT = 512 #400 es otra opcion
DIMENSION = 8 #Las dimensiones de un tablero son 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15#Para las animaciones de después
IMAGES = {}

'''
Inicializar un diccionario global de imágenes. Esto se llamará solo una vez en el main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Nota: podemos acceder a la imagen llamándola 'IMAGES['wp']

'''
La función principal para iniciar el juego
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = AjedrezEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # variable para cuando ya se ha hecho un movimiento
    loadImages() #Solo hacer esto una vez antes del bucle while
    running = True
    sqSelected = () #Ningún cuadro seleccionado
    playerClicks = [] #Mantiene la información de los clicks del jugador

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) localización del ratón
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):#Si el usuario pisa el mismo cuadrdo más de una vez
                    sqSelected = () #Desseleccionar
                    playerClicks = [] #Borrar clicks del jugador
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #Después del segundo click
                    move = AjedrezEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            #Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Eliminar cuando z está presente
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves =gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsable de todos los gráficos del game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)#Dibujamos los cuadrados del tablero
    #Más tarde se añadirá las recomendaciones subrayadas
    drawPieces(screen, gs.board)#Dibujamos las piezas del tablero


'''
Dibujar los cuadros del tablero
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Dibujar las piezas del tablero
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #Cuadro con pieza
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()


