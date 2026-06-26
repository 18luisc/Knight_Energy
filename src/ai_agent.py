import math
from src.constants import MOVE_COST

def heuristic_evaluation(game_state):
    """
    Función de utilidad heurística (temporal).
    Evalúa qué tan buena es la posición actual para el caballo Blanco (IA).
    """
    # Una heurística básica: mis puntos menos los puntos del oponente
    score_diff = game_state.white_points - game_state.black_points
    energy_diff = game_state.white_energy - game_state.black_energy
    
    # Podemos ponderar estos valores
    return (score_diff * 10) + (energy_diff * 2)

def minimax(game_state, depth, is_maximizing):
    """
    Algoritmo Minimax para decisiones imperfectas.
    """
    # Caso base: profundidad alcanzada o estado terminal (fin del juego)
    if depth == 0 or game_state.is_terminal_state():
        return heuristic_evaluation(game_state), None

    # Manejar penalizaciones por falta de energía antes de expandir nodos
    game_state.check_energy_penalty()

    if is_maximizing:
        max_eval = -math.inf
        best_move = None
        # Obtener movimientos válidos para la IA (WHITE)
        valid_moves = game_state.get_valid_moves('WHITE')
        
        # Si no hay movimientos posibles pero el juego no ha terminado, pasa el turno
        if not valid_moves:
            clon_estado = game_state.clone()
            clon_estado.current_turn = 'BLACK'
            evaluacion, _ = minimax(clon_estado, depth - 1, False)
            return evaluacion, None

        for move in valid_moves:
            # Simular el movimiento en una copia del tablero
            clon_estado = game_state.clone()
            clon_estado.make_move(move)
            
            # Evaluar recursivamente el movimiento del oponente (MIN)
            evaluacion, _ = minimax(clon_estado, depth - 1, False)
            
            if evaluacion > max_eval:
                max_eval = evaluacion
                best_move = move
                
        return max_eval, best_move

    else:
        min_eval = math.inf
        best_move = None
        # Obtener movimientos válidos para el Humano (BLACK)
        valid_moves = game_state.get_valid_moves('BLACK')
        
        if not valid_moves:
            clon_estado = game_state.clone()
            clon_estado.current_turn = 'WHITE'
            evaluacion, _ = minimax(clon_estado, depth - 1, True)
            return evaluacion, None

        for move in valid_moves:
            # Simular el movimiento en una copia del tablero
            clon_estado = game_state.clone()
            clon_estado.make_move(move)
            
            # Evaluar recursivamente el movimiento de la máquina (MAX)
            evaluacion, _ = minimax(clon_estado, depth - 1, True)
            
            if evaluacion < min_eval:
                min_eval = evaluacion
                best_move = move
                
        return min_eval, best_move

def get_best_move(game_state, difficulty):
    """
    Punto de entrada que define la profundidad límite según el nivel seleccionado.
    Dificultades: 'PRINCIPIANTE' (2), 'AMATEUR' (4), 'EXPERTO' (6)
    """
    depth_limits = {
        'PRINCIPIANTE': 2,
        'AMATEUR': 4,
        'EXPERTO': 6
    }
    
    depth = depth_limits.get(difficulty.upper(), 2)
    # La máquina siempre busca maximizar ('WHITE')
    _, move = minimax(game_state, depth, True)
    return move