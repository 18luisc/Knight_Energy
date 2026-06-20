from src.game_logic import GameState

if __name__ == "__main__":
    game_state = GameState()
    game_state.display_state()

    movimientos_blanco = game_state.get_valid_moves('White')
    print(f"Movimientos válidos para el blanco en {game_state.white_pos}: {movimientos_blanco}")

    movimientos_negro = game_state.get_valid_moves('Black')
    print(f"Movimientos válidos para el negro en {game_state.black_pos}: {movimientos_negro}")