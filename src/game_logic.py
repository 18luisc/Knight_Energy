import random
from .constants import BOARD_SIZE, INITIAL_ENERGY, PENALTY_POINTS, MOVE_COST

class GameState:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # Estado de los jugadores: [Puntos, Energía, (Fila, Columna)]
        # El blanco (Máquina) inicia 
        self.p1_white = [0, INITIAL_ENERGY, None] 
        self.p2_black = [0, INITIAL_ENERGY, None]
        
        self.turn = "WHITE" # "WHITE" o "BLACK" 
        self.game_over = False
        
        self._initialize_board()

    def _initialize_board(self):
        """Genera las posiciones aleatorias sin solapamiento"""
        # 1. Crear todas las posiciones posibles del tablero (0,0) a (7,7)
        all_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        random.shuffle(all_positions)
        
        # 2. Ubicar caballos 
        self.p1_white[2] = all_positions.pop()
        self.p2_black[2] = all_positions.pop()
        
        # 3. Ubicar las 7 casillas con puntos (Estrellas) [cite: 7, 10, 38]
        # Guardamos tuplas (TIPO, VALOR) -> ("STAR", valor)
        star_values = [2, 3, 4, 5, 6, 8, 9] 
        for val in star_values:
            r, c = all_positions.pop()
            self.board[r][c] = ("STAR", val)
            
        # 4. Ubicar las 4 casillas de energía (Rayos) 
        energy_values = [2, 3, 4, 5] 
        for val in energy_values:
            r, c = all_positions.pop()
            self.board[r][c] = ("ENERGY", val)

    def get_valid_moves(self, player_pos):
        """Devuelve los movimientos en L válidos desde una posición"""
        r, c = player_pos
        # Las 8 posibles combinaciones de la L del caballo 
        possible_moves = [
            (r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2),
            (r+1, c-2), (r+1, c+2), (r+2, c-1), (r+2, c+1)
        ]
        # Filtrar que estén dentro del tablero
        valid = [(nr, nc) for nr, nc in possible_moves if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE]
        return valid

    def print_board_terminal(self):
        """Muestra una representación visual del tablero en la consola para pruebas"""
        p1_pos = self.p1_white[2]
        p2_pos = self.p2_black[2]
        
        print("\n--- TABLERO DE KNIGHT ENERGY ---")
        print(f"Caballo Blanco (IA): Puntos={self.p1_white[0]}, Energía={self.p1_white[1]} | Pos={p1_pos}")
        print(f"Caballo Negro (User): Puntos={self.p2_black[0]}, Energía={self.p2_black[1]} | Pos={p2_pos}")
        print("-" * 33)
        
        for r in range(BOARD_SIZE):
            row_str = "|"
            for c in range(BOARD_SIZE):
                if (r, c) == p1_pos:
                    row_str += " 🦄W |"  # Caballo Blanco
                elif (r, c) == p2_pos:
                    row_str += " 🐴B |"  # Caballo Negro
                elif self.board[r][c] is not None:
                    tipo, val = self.board[r][c]
                    if tipo == "STAR":
                        row_str += f" S{val} |"  # Estrella + Valor
                    elif tipo == "ENERGY":
                        row_str += f" E{val} |"  # Energía + Valor
                else:
                    row_str += "    |"  # Casilla vacía
            print(row_str)
            print("-" * 33)