import random

class GameState:
    # Inicializa el estado del juego.
    def __init__(self):
        # Player Variables
        self.white_energy = 7
        self.black_energy = 7
        self.white_points = 0
        self.black_points = 0
        
        # The game is always started by the machine (white horse)
        self.current_turn = 'White' 
        
        # Horse positions (row, column)
        self.white_pos = None
        self.black_pos = None

        # Board Representation (8x8 Matrix)
        # We will use text strings to identify what is in each cell:
        # '0' = Empty
        # 'W' = White Horse, 'B' = Black Horse
        # 'P2', 'P3'... = Points (Stars)
        # 'E2', 'E3'... = Energy (Lightning Bolts)
        self.board = [['0' for _ in range(8)] for _ in range(8)]
        
        # Generate random positions when instantiating the game
        self.generate_initial_state()
    
    # Genera las posiciones iniciales de los caballos, los puntos y la energia.
    def generate_initial_state(self):
        # The initial positions of the horses, the points spaces, and the energy 
        # spaces are random and cannot be the same.

        # Generate all possible board coordinates (0,0) to (7,7)
        all_coordinates = [(row, col) for row in range(8) for col in range(8)]

        # Select 13 unique positions at random
        # (1 white + 1 black + 7 stars + 4 energy = 13)
        selected_positions = random.sample(all_coordinates, 13)

        # Assign the knights
        self.white_pos = selected_positions[0]
        self.black_pos = selected_positions[1]
        self.board[self.white_pos[0]][self.white_pos[1]] = 'W'
        self.board[self.black_pos[0]][self.black_pos[1]] = 'B'

        # Assign the stars (points)
        point_values = [2, 3, 4, 5, 6, 8, 9]

        for i, pos in enumerate(selected_positions[2:9]):
            self.board[pos[0]][pos[1]] = f'P{point_values[i]}'

        # Assign the rays (energy)
        energy_values = [2, 3, 4, 5]
        for i, pos in enumerate(selected_positions[9:13]):
            self.board[pos[0]][pos[1]] = f'E{energy_values[i]}'
        
    def __str__(self):
        # Print the board in a readable format
        board_str = ""
        for fila in self.board:
            tablero_str += " ".join(fila) + "\n"
        return tablero_str

    # Por ahora voy a imprimir el estado actual en consola
    def display_state(self):
        print(f"--- Turno de: {self.current_turn} ---")
        print(f"Blanco (Máquina): Puntos = {self.white_points}, Energía = {self.white_energy}")
        print(f"Negro (Humano):   Puntos = {self.black_points}, Energía = {self.black_energy}")
        print("-" * 35)
        for row in self.board:
            print("\t".join([str(celda).ljust(3) for celda in row]))
        print("-" * 35)

    # Retorna una lista de coordenadas (fila, columna) con los movimientos
    # validos para el jugador ('White' o 'Black').
    def get_valid_moves(self, player_color):
        # Determine the current position of the horse that is going to move
        if player_color == 'White':
            current_pos = self.white_pos
        else:
            current_pos = self.black_pos

        row, col = current_pos
        
        # Define the 8 possible combinations of a "L" movement
        move_offsets = [
            (-2, -1), (-2, 1),  # Two up, one left/right
            (-1, -2), (-1, 2),  # One up, two left/right
            (1, -2),  (1, 2),   # One down, two left/right
            (2, -1),  (2, 1)    # Two down, one left/right
        ]
        
        valid_moves = []
        
        # Calculate the new positions and filter the ones that go off the board
        for row_offset, col_offset in move_offsets:
            new_row = row + row_offset
            new_col = col + col_offset
            
            # Within the board limits (0 to 7)
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                
                # Se debe evitar que un caballo caiga en la casilla donde esta el otro caballo o no?
                if (new_row, new_col) != self.white_pos and (new_row, new_col) != self.black_pos:
                    valid_moves.append((new_row, new_col))
                
        return valid_moves

    # Ejecuta el movimiento del jugador actual a la nueva posición (new_pos).
    # Actualiza el tablero, la energía, los puntos y cambia el turno.
    def make_move(self, new_pos):
        new_row, new_col = new_pos
        
        # Identify whose turn it is and their old position
        if self.current_turn == 'White':
            old_pos = self.white_pos
            self.white_energy -= 1 
        else:
            old_pos = self.black_pos
            self.black_energy -= 1 
            
        # Check what is in the destination cell before overwriting it
        dest_value = self.board[new_row][new_col]
        
        if dest_value.startswith('P'):
            # Extract the number after the 'P'
            points_gained = int(dest_value[1:])
            if self.current_turn == 'White':
                self.white_points += points_gained
            else:
                self.black_points += points_gained
                
        elif dest_value.startswith('E'):
            # Extract the number after the 'E'
            energy_gained = int(dest_value[1:]) 
            if self.current_turn == 'White':
                self.white_energy += energy_gained
            else:
                self.black_energy += energy_gained

        # Update the board matrix (leave the old position empty)
        self.board[old_pos[0]][old_pos[1]] = '0'
        
        # Place the horse letter in the new position and change the turn
        if self.current_turn == 'White':
            self.board[new_row][new_col] = 'W'
            self.white_pos = new_pos
            self.current_turn = 'Black'
        else:
            self.board[new_row][new_col] = 'B'
            self.black_pos = new_pos
            self.current_turn = 'White'