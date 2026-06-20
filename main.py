from src.game_logic import GameState

if __name__ == "__main__":
    game_state = GameState()
    game_state.display_state()

    white_moves = game_state.get_valid_moves('White')
    print(f"Movimientos válidos para el caballo blanco en {game_state.white_pos}: {white_moves}")
    
    # Para probar voy a elegir el primer movimiento de la lista
    if white_moves:
        selected_move = white_moves[0]
        print(f"\nCaballo Blanco a la posición: {selected_move}")
        game_state.make_move(selected_move)
        game_state.display_state()
    else:
        print("El caballo blanco no tiene movimientos válidoS.")


