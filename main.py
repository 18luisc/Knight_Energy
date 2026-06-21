import random
from src.game_logic import GameState

def main():
    game = GameState()
    game.print_board_terminal()

    white_moves = game.get_valid_moves('White')    
    print(f"Movimientos válidos para el caballo blanco en {game.white_pos}: {white_moves}")
    print(white_moves)

    turnos_jugados = 0
    
    # Bucle hasta que el juego termine (por falta de estrellas o encierro/energía)
    while not game.is_terminal_state():
        turnos_jugados += 1
        
        # 1. Revisar penalización (si no tiene energía, pierde turno y puntos)
        if game.check_energy_penalty():
            continue
            
        # 2. Obtener movimientos del jugador actual
        movimientos = game.get_valid_moves(game.current_turn)
        
        if movimientos:
            # Elegir un movimiento al azar
            movimiento_elegido = random.choice(movimientos)
            game.make_move(movimiento_elegido)
        else:
            # Si tiene energía pero está encerrado (no tiene movimientos), pierde turno
            if game.current_turn == 'WHITE':
                game.current_turn = 'BLACK'
            else:
                game.current_turn = 'WHITE'

    # --- CUANDO EL JUEGO TERMINA ---
    print(f"\nJuego terminado después de {turnos_jugados} turnos.")
    game.print_board_terminal()
    
    ganador = game.get_winner()
    print(f"\nEl ganador es -> {ganador} \n")


    
if __name__ == "__main__":
    main()


