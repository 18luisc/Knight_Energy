import random
from src.game_logic import GameState
from src.ai_agent import get_best_move  # Importar IA
from src.constants import WIDTH, HEIGHT, WHITE, BLACK, BOARD_SIZE
from src.gui import KnightEnergyGUI

def main():
    while True:
        gui = KnightEnergyGUI()
        dificultad = gui.main_menu()
        
        if dificultad:
            print(f"Iniciando juego en modo {dificultad}...")
            gui.run_game(dificultad)
        else:
            break

if __name__ == "__main__":
    main()