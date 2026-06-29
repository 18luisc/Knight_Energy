from src.constants import BOARD_SIZE
import math
from src.constants import MOVE_COST

def heuristic_evaluation(game_state):
    """
    Función de utilidad heurística (temporal).
    Evalúa qué tan buena es la posición actual para el caballo Blanco (IA).
    """

    # Tenemos en cuenta si vamos ganando o no con los Puntos 
    score_diff = game_state.white_points - game_state.black_points

    # Si la energía del caballo blanco es menor a 3, le da prioridad a buscar rayos.
    weight_energy = 5
    if game_state.white_energy < 3:
        weight_energy = 20
    energy_diff = game_state.white_energy - game_state.black_energy

    # Buscamos la estrella más cercana usando Distancia Manhattan

    min_dist_score = math.inf  #Inicializamoss vlaor de distancia mínima
    
    white_r, white_c = game_state.white_pos

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = game_state.board[r][c]
            if cell is not None and cell[0] == "STAR":
                star_value = cell[1]
                # Distancia Manhattan: |x1 - x2| + |y1 - y2|
                dist = abs(game_state.white_pos[0] - r) + abs(game_state.white_pos[1] - c)

                # Las estrellas de mayor valor deben ser prioritarias pareciendo más cercanas
                distance_score = dist- (star_value * 0.5)
                if distance_score < min_dist_score:
                    min_dist_score = distance_score
            
    # Si ya no quedan estrellas, anulamos el cálculo de distancia
    if min_dist_score == math.inf:
        min_dist_score = 0
    
    # Por ahora coloquemoslo así. Más puntos y energía es bueno. Más distancia es malo.
    return (score_diff * 30) + (energy_diff * weight_energy) - (min_dist_score * 4)

def minimax(game_state, depth, alpha, beta, is_maximizing):
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
            evaluacion =  pass_turn(game_state, depth, alpha, beta)
            return evaluacion, None

        for move in valid_moves:
            # Simular el movimiento en una copia del tablero
            clon_estado = game_state.clone()
            clon_estado.make_move(move)
            
            # Evaluar recursivamente el movimiento del oponente (MIN)
            evaluacion, _ = minimax(clon_estado, depth - 1, alpha, beta, False)
            
            if evaluacion > max_eval:
                max_eval = evaluacion
                best_move = move

            # Mini poda alpha-beta
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break 

                
        return max_eval, best_move

    else:
        min_eval = math.inf
        best_move = None
        # Obtener movimientos válidos para el Humano (BLACK)
        valid_moves = game_state.get_valid_moves('BLACK')
        
        if not valid_moves:
            evaluacion =  pass_turn(game_state, depth, alpha, beta)
            return evaluacion, None

        for move in valid_moves:
            # Simular el movimiento en una copia del tablero
            clon_estado = game_state.clone()
            clon_estado.make_move(move)
            
            # Evaluar recursivamente el movimiento de la máquina (MAX)
            evaluacion, _ = minimax(clon_estado, depth - 1, alpha, beta, True)
            
            if evaluacion < min_eval:
                min_eval = evaluacion
                best_move = move

            # Mini poda alpha-beta
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break 

                
        return min_eval, best_move

def pass_turn(game_state, depth, alpha, beta):
    clon_estado = game_state.clone()
    current_turn = clon_estado.current_turn
    clon_estado.current_turn = 'BLACK' if current_turn == 'WHITE' else 'WHITE'
    evaluacion, _ = minimax(clon_estado, depth - 1, alpha, beta, False)

    return evaluacion, None

    
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
    
    depth = depth_limits.get(difficulty.upper(), 4)
    # La máquina siempre busca maximizar ('WHITE')
    # Iniciamos el Minimax con Alfa en -Infinito y Beta en +Infinito
    _, move = minimax(game_state, depth, -math.inf, math.inf, True)
    return move