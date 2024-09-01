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
            ["--", "--", "wR", "--", "--", "bB", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Para poder revertir el movimiento
        self.whiteToMove = not self.whiteToMove #Cambiar de jugador


    '''
    Eliminar el último movimiento
    '''

    def undoMove(self):
        if len(self.moveLog) != 0: #Estar seguro de que hay un movimiento que eliminar
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Cambiar de turno

    '''
    Todos los movimientos considerados jaque
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #Por ahora es sin jaque mate

    '''
    Todos los movimientos no considerados jaque
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):#Nº de filas
            for c in range(len(self.board[r])): #Nº de columnas
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #LLama a la función apropiada para mover la pieza
        return moves

    '''
    Coger todos los movimientos del peón y añadirlos a una lista
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #El peón blanco se mueve
            if self.board[r-1][c] == "--": #Se avanza un cuadrado
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #El peón avanza dos posiciones
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:#Se captura a la izquierda
                if self.board[r-1][c-1][0] == 'b': #Se captura pieza del enemigo
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #Se captura a la derecha
                if self.board[r-1][c+1][0] == 'b': #Se captura pieza del enemigo
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #Se mueve el peón negro
            pass

    '''
    Coger todos los movimientos de la torre y añadirlos a una lista
    '''
    def getRookMoves(self, r, c, moves):
        pass

    '''
   Coger todos los movimientos de la Knight y añadirlos a una lista
   '''
    def getKnightMoves(self, r, c, moves):
        pass

    '''
   Coger todos los movimientos de la Bishop y añadirlos a una lista
   '''
    def getBishopMoves(self, r, c, moves):
        pass

    '''
   Coger todos los movimientos de la Queen y añadirlos a una lista
   '''
    def getQueenMoves(self, r, c, moves):
        pass

    '''
   Coger todos los movimientos de el King y añadirlos a una lista
   '''
    def getKingMoves(self, r, c, moves):
        pass

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCalls = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCalls.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Anular los movimientos iguales
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False


    def getChessNotation(self):
        #Anotación real de ajedrez
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




