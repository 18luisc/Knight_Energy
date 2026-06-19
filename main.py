from src.game_logic import GameState

def main():
    print("Iniciando simulación del motor de juego...")
    
    # 1. Instanciamos el estado del juego (esto ejecuta la inicialización aleatoria)
    game = GameState()
    
    # 2. Imprimimos el tablero generado
    game.print_board_terminal()
    
    # 3. Probamos que el cálculo de movimientos en L funcione para el caballo blanco
    pos_blanco = game.p1_white[2]
    movimientos_validos = game.get_valid_moves(pos_blanco)
    print(f"\nMovimientos válidos en L para el Caballo Blanco desde {pos_blanco}:")
    print(movimientos_validos)

if __name__ == "__main__":
    main()