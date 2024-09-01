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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Para poder revertir el movimiento
        self.whiteToMove = not self.whiteToMove #Cambiar de jugador
        #Modificar la posición del rey si se mueve
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)


    '''
    Eliminar el último movimiento
    '''

    def undoMove(self):
        if len(self.moveLog) != 0: #Estar seguro de que hay un movimiento que eliminar
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Cambiar de turno
            #Cambiar la posición del rey si es necesario
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    Todos los movimientos considerados jaque
    '''
    def getValidMoves(self):
        #1.)Generar todos los movimientos posibles
        moves = self.getAllPossibleMoves()
        #2.) Por cada movimiento, hacer hacer el movimiento
        for i in range(len(moves)-1, -1, -1): #Cuando elimino un elemento de la lista, vuelvo atrás en esa misma lista
            self.makeMove(moves[i])
            #3.) Generar todos los movimientos del oponente
            #4.) Para cada uno de los movimientos del oponente, ver si estos atacan a mi rey
            self.whiteToMove = not self.whiteToMove #Cambiar turno
            if self.inCheck():
                moves.remove(moves[i])  #5.) Si los movimientos atacan a mi rey, no son movimientos válidos
            self.whiteToMove = not self.whiteToMove #Cambiar turno
            self.undoMove()
        if len(moves) == 0: #Jaque mate o tablas
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    '''
    Determinar si el jugador está en jaque
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determinar si el jugador puede atacar el cuadrado r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #Cambiar el turno
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #Cambiar turnos
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #Cuadrado bajo ataque
                self.whiteToMove = not self.whiteToMove #Cambiar turnos
                return True
        return False

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
            if self.board[r+1][c] == "--": #1 solo movimiento
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--": #2 Movimientos de peón
                    moves.append(Move((r, c), (r + 2, c), self.board))
            #Capturas de peón
            if c-1 >= 0: #Capturar a la iizquierda
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7: #Capturar a la derecha
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    '''
    Coger todos los movimientos de la torre y añadirlos a una lista
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #Arriba, abajo, izquierda, derecha
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #En el tablero
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #Espacio vacío válido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Pieza enemiga válida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Pieza amiga inválida
                        break
                else: #Fin de tablero
                    break

    '''
   Coger todos los movimientos de la Knight y añadirlos a una lista
   '''
    def getKnightMoves(self, r, c, moves):
        KnightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in KnightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Vacío o pieeza enemiga
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
   Coger todos los movimientos de la Bishop y añadirlos a una lista
   '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 direcciones
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #El alfil puede moverse como máximo 7 posiciones
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #Si está en el tablero
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #Espacio vacío válido
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Pieza enemiga válida
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #Pieza amiga inválida
                        break
                else: #Fuera de tablero
                    break

    '''
   Coger todos los movimientos de la Queen y añadirlos a una lista
   '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
   Coger todos los movimientos de el King y añadirlos a una lista
   '''
    def getKingMoves(self, r, c, moves):
        KingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + KingMoves[i][0]
            endCol = c + KingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Vacío o pieza enemiga
                    moves.append(Move((r, c), (endRow, endCol), self.board))

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




