"""
Esta clase guarda toda la información del estado de la partida y también es la responsable de determinar cuales son los movimientos válidos
"""

class GameState():
    def __init__(self):
        #El tablero es un 8*8 2d, cada elemento de la lista tiene 2 letras.
        #La primera letra representa el color de la pieza "b" o "w"
        #La segunda letra representa el tipo de pieza "K", "Q", "R", "B", "N" o "P"
        #"--" - representa el espacio en blanco entre piezas
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteMove = True
        self.moveLog = []
