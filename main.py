import random
from src.game_logic import GameState
from src.ai_agent import get_best_move  # Importar IA
from src.constants import WIDTH, HEIGHT, WHITE, BLACK, BOARD_SIZE
from src.gui import KnightEnergyGUI


def main():
    # 1. Selecciona la dificultad para la IA ('PRINCIPIANTE', 'AMATEUR', 'EXPERTO')
    # Cambia este valor para probar las profundidades (2, 4 o 6)
    DIFICULTAD = None
    
    game = GameState()
    gui = KnightEnergyGUI(game.white_pos, game.black_pos)

    DIFICULTAD = gui.main_menu()
    
    print("=== ESTADO INICIAL DEL TABLERO ===")
    game.print_board_terminal()

    white_moves = game.get_valid_moves('WHITE')    
    print(f"Movimientos válidos iniciales para el caballo blanco en {game.white_pos}: {white_moves}\n")

    turnos_jugados = 0
    
    # Bucle hasta que el juego termine (por falta de estrellas o encierro/energía)
    if DIFICULTAD:
        while not game.is_terminal_state():
            turnos_jugados += 1
            
            # 1. Revisar penalización (si no tiene energía, pierde turno y puntos)
            if game.check_energy_penalty():
                print(f"Turno {turnos_jugados}: Penalización aplicada por falta de energía.")
                game.print_board_terminal()
                continue
                
            # 2. Obtener movimientos del jugador actual
            movimientos = game.get_valid_moves(game.current_turn)
            
            if movimientos:
                if game.current_turn == 'WHITE':
                    # Usa Minimax para decidir el mejor movimiento
                    print(f"Turno {turnos_jugados} [WHITE - IA ({DIFICULTAD})]: Pensando...")
                    movimiento_elegido = get_best_move(game, DIFICULTAD)
                    
                    # Si Minimax no devuelve nada, usamos un fallback al azar
                    if movimiento_elegido is None:
                        movimiento_elegido = random.choice(movimientos)
                else:
                    # El rival (BLACK - Humano simulado) sigue eligiendo al azar
                    print(f"Turno {turnos_jugados} [BLACK - Humano (Simulado)]: Moviendo aleatorio...")
                    movimiento_elegido = None
                    while not movimiento_elegido or movimiento_elegido != game.black_pos or movimiento_elegido not in movimientos:
                        movimiento_elegido = gui.white.position
                
                # Ejecutar el movimiento en el juego real
                game.make_move(movimiento_elegido)
                gui.update_player_position(game.current_turn, movimiento_elegido[0], movimiento_elegido[1])
                game.print_board_terminal()
            else:
                # Si tiene energía pero está encerrado (no tiene movimientos en L libres), pasa el turno
                print(f"Turno {turnos_jugados} [{game.current_turn}]: Encerrado sin movimientos válidos. Pasa turno.")
                if game.current_turn == 'WHITE':
                    game.current_turn = 'BLACK'
                else:
                    game.current_turn = 'WHITE'

    # --- CUANDO EL JUEGO TERMINA ---
    print(f"\n======================================")
    print(f"Juego terminado después de {turnos_jugados} turnos.")
    print(f"======================================")
    game.print_board_terminal()
    
    ganador = game.get_winner()
    print(f"El ganador es -> {ganador} \n")

if __name__ == "__main__":
    gui = KnightEnergyGUI()
    dificultad = gui.main_menu()
    if dificultad:
        print(f"Iniciando juego en modo {dificultad}...")
        gui.run_game(dificultad)