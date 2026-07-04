import random
import copy
from src.constants import BOARD_SIZE, INITIAL_ENERGY, PENALTY_POINTS, MOVE_COST

class GameState:
    # Inicializa el estado del juego.
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Player status
        self.white_points = 0
        self.white_energy = INITIAL_ENERGY
        self.white_pos = None
        
        self.black_points = 0
        self.black_energy = INITIAL_ENERGY
        self.black_pos = None

        # The game is always started by the machine (white horse)
        self.current_turn = 'WHITE' 
        self.num_turns = 0

        self.stars = []
        self.energies = []
        
        self._initialize_board()
    
    # Genera las posiciones iniciales de los caballos, los puntos y la energia.
    def _initialize_board(self):
        # Generate all possible board coordinates (0,0) to (7,7)
        all_coordinates = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
        random.shuffle(all_coordinates)

        # Assign the knights
        self.white_pos = all_coordinates.pop()
        self.black_pos = all_coordinates.pop()

        # Assign the stars (points)
        star_values = [2, 3, 4, 5, 6, 8, 9]
        for val in star_values:
            r, c = all_coordinates.pop()
            self.board[r][c] = ("STAR", val)
            self.stars.append(((c,r), val))

        # Assign the rays (energy)
        energy_values = [2, 3, 4, 5] 
        for val in energy_values:
            r, c = all_coordinates.pop()
            self.board[r][c] = ("ENERGY", val)
            self.energies.append(((c,r), val))

    # Retorna una lista de coordenadas (fila, columna) con los movimientos
    # validos para el jugador ('White' o 'Black').
    def get_valid_moves(self, player_color):
        # Determine the current position of the horse that is going to move
        current_pos = self.white_pos if player_color == 'WHITE' else self.black_pos
        if not current_pos: return []

        row, col = current_pos
        
        # Define the new possible moves with the 8 "L" movement combinations
        possible_moves = [
            (row-2, col-1), (row-2, col+1),  # Two up, one left/right
            (row-1, col-2), (row-1, col+2),  # One up, two left/right
            (row+1, col-2), (row+1, col+2),  # One down, two left/right
            (row+2, col-1), (row+2, col+1)   # Two down, one left/right
        ]
        
        valid_moves = []
        
        # Calculate the new positions and filter the ones that go off the board
        for new_row, new_col in possible_moves:
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                # Se debe evitar que un caballo caiga en la casilla donde esta el otro caballo
                if (new_row, new_col) != self.white_pos and (new_row, new_col) != self.black_pos:
                    valid_moves.append((new_row, new_col))
                
        return valid_moves
    
    def is_move_valid(self, player_color, move):
        return move in self.get_valid_moves(player_color)

    def check_energy_penalty(self):
        if self.current_turn == 'WHITE' and self.white_energy < MOVE_COST:
            self.white_points -= PENALTY_POINTS
            self.current_turn = 'BLACK'
            return True
        elif self.current_turn == 'BLACK' and self.black_energy < MOVE_COST:
            self.black_points -= PENALTY_POINTS
            self.current_turn = 'WHITE'
            return True
        return False

    # Ejecuta el movimiento del jugador actual a la nueva posición (new_pos).
    # Actualiza el tablero, la energía, los puntos y cambia el turno.
    def make_move(self, new_pos):
        self.num_turns += 1
        new_row, new_col = new_pos
        
        # Charge the cost of the movement
        if self.current_turn == 'WHITE':
            self.white_energy -= MOVE_COST
        else:
            self.black_energy -= MOVE_COST
            
        # Check what is in the destination cell before overwriting it
        dest_value = self.board[new_row][new_col]
        
        if dest_value is not None:
            type, value = dest_value
            if type == "STAR":
                if self.current_turn == 'WHITE': self.white_points += value
                else: 
                    self.black_points += value
            elif type == "ENERGY":
                if self.current_turn == 'WHITE': self.white_energy += value
                else: 
                    self.black_energy += value
                
            # Cleaned the cell because the resource was consumed
            self.board[new_row][new_col] = None
        
        # Place the horse letter in the new position and change the turn
        if self.current_turn == 'WHITE':
            self.white_pos = new_pos
            self.current_turn = 'BLACK'
        else:
            self.black_pos = new_pos
            self.current_turn = 'WHITE'


    # Reglas de finalización: Cuando no queden casillas con puntos o
    # cuando ninguno de los jugadores pueda realizar movimientos
    def is_terminal_state(self):
        # Condition 1
        remaining_points = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell = self.board[row][col]

                if cell is not None and cell[0] == "STAR":
                    remaining_points += 1
                    
        if remaining_points == 0:
            return True # Game over
            
        # Condition 2
        # A player can move if they have energy (>=1) and valid cells to jump to
        white_moves = self.get_valid_moves('WHITE')
        black_moves = self.get_valid_moves('BLACK')
        
        white_can_move = len(white_moves) > 0 and self.white_energy >= MOVE_COST
        black_can_move = len(black_moves) > 0 and self.black_energy >= MOVE_COST
        
        if not white_can_move and not black_can_move:
            return True # Game over
            
        return False

    def get_winner(self):
        if self.white_points > self.black_points:
            return "WHITE"
        elif self.black_points > self.white_points:
            return "BLACK"
        else:
            return "EMPATE"

    def clone(self):
        """Retorna una copia profunda e independiente del estado actual del juego"""
        return copy.deepcopy(self)