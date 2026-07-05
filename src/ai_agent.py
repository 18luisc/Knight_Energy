from src.constants import BOARD_SIZE, MOVE_COST
import math


def heuristic_evaluation(game_state, difficulty):
    """
    Función de evaluación heurística que calcula una puntuación basada en:
    - Diferencia de puntos entre jugadores
    - Diferencia de energía entre jugadores
    - Movilidad (número de movimientos válidos)
    - Distancia a las estrellas y su valor
    - Ventaja posicional basada en la distancia a las estrellas
    """

    # Calcular diferencia de puntos (ventaja de la IA WHITE vs jugador BLACK)
    score_diff = game_state.white_points - game_state.black_points
    
    # Calcular diferencia de energía (recurso crítico en el juego)
    energy_diff = game_state.white_energy - game_state.black_energy

    # Calcular movilidad: ventaja en número de movimientos disponibles
    white_moves = len(game_state.get_valid_moves("WHITE"))
    black_moves = len(game_state.get_valid_moves("BLACK"))
    mobility = white_moves - black_moves

    # Obtener posiciones actuales de ambos jugadores
    white_r, white_c = game_state.white_pos
    black_r, black_c = game_state.black_pos

    # Inicializar variables para evaluación de estrellas
    min_dist_score = math.inf  # Distancia mínima ponderada a estrellas
    best_star = 0              # Mejor puntuación de estrella para WHITE
    advantage = 0              # Ventaja posicional acumulada

    # Evaluar todas las celdas del tablero en busca de estrellas
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = game_state.board[r][c]

            # Omitir celdas vacías
            if cell is None:
                continue

            # Omitir celdas que no sean estrellas
            if cell[0] != "STAR":
                continue

            # Extraer el valor de la estrella
            value = cell[1]

            # Calcular distancia Manhattan desde cada jugador a la estrella
            white_dist = abs(white_r - r) + abs(white_c - c)
            black_dist = abs(black_r - r) + abs(black_c - c)

            # Calcular score de distancia (penaliza a WHITE si está lejos)
            distance_score = white_dist - (value * 0.5)

            # Actualizar la distancia mínima encontrada
            if distance_score < min_dist_score:
                min_dist_score = distance_score

            # Calcular score de la estrella (valor - distancia de WHITE)
            star_score = value * 5 - white_dist

            # Actualizar la mejor oportunidad de estrella
            if star_score > best_star:
                best_star = star_score

            # Calcular ventaja posicional: BLACK más lejano = mejor para WHITE
            advantage += (black_dist - white_dist) * value


    # Si no hay estrellas en el tablero, neutralizar el score
    if min_dist_score == math.inf:
        min_dist_score = 0

    # Nivel PRINCIPIANTE: enfoque simple en puntos y energía
    if difficulty == "PRINCIPIANTE":
        return (
            score_diff * 30          # Diferencia de puntos es primordial
            + energy_diff * 5        # Pequeña consideración de energía
            - min_dist_score * 4     # Evitar alejarse demasiado de estrellas
        )

    # Nivel AMATEUR: balance entre puntos, energía y oportunidades de estrellas
    elif difficulty == "AMATEUR":
        return (
            score_diff * 35          # Mayor énfasis en puntos
            + energy_diff * 10       # Energía más importante
            + best_star * 3          # Buscar las mejores estrellas
            + mobility * 2           # Movilidad como factor secundario
            - min_dist_score * 2     # Considerar distancia a estrellas
        )

    # Nivel EXPERTO: análisis profundo con todos los factores
    else:
        # Penalización por falta crítica de energía
        energy_penalty = 0
        if game_state.white_energy <= 2:
            energy_penalty = -40  # Penalización severa si energía es crítica

        return (
            score_diff * 40          # Máximo peso en diferencia de puntos
            + energy_diff * 15       # Energía es crítica en dificultad alta
            + best_star * 5          # Prioritario alcanzar las mejores estrellas
            + mobility * 5           # Libertad de movimiento es importante
            + advantage              # Ventaja posicional acumulada
            - min_dist_score         # Considerar todas las distancias
            + energy_penalty         # Aplicar penalización si es necesaria
        )


def minimax(game_state, depth, alpha, beta, is_maximizing, difficulty):
    """
    Algoritmo Minimax con poda Alpha-Beta para tomar decisiones óptimas.
    Alterna entre maximizar (IA) y minimizar (jugador humano).
    """

    # ===== CASO BASE =====
    # Se detiene cuando: 1) alcanza profundidad máxima, o 2) el juego terminó
    if depth == 0 or game_state.is_terminal_state():
        return heuristic_evaluation(game_state, difficulty), None

    # Aplicar penalización si algún jugador se queda sin energía
    game_state.check_energy_penalty()

    # ===== FASE DE MAXIMIZACIÓN (turno de la IA - WHITE) =====
    if is_maximizing:
        max_eval = -math.inf  # Inicializar con valor mínimo posible
        best_move = None

        # Obtener todos los movimientos legales para WHITE (IA)
        valid_moves = game_state.get_valid_moves('WHITE')

        # Si no hay movimientos disponibles, pasar turno
        if not valid_moves:
            evaluacion = pass_turn(
                game_state,
                depth,
                alpha,
                beta,
                is_maximizing,
                difficulty
            )
            return evaluacion, None

        # Evaluar cada movimiento posible
        for move in valid_moves:
            # Crear copia del estado para simular el movimiento
            clon_estado = game_state.clone()
            clon_estado.make_move(move)

            # Recursivamente evaluar el siguiente nivel (turno del jugador)
            evaluacion, _ = minimax(
                clon_estado,
                depth - 1,
                alpha,
                beta,
                False,  # Siguiente es minimización (jugador)
                difficulty
            )

            # Actualizar el mejor movimiento encontrado
            if evaluacion > max_eval:
                max_eval = evaluacion
                best_move = move

            # Actualizar límite alfa para poda
            alpha = max(alpha, evaluacion)

            # Poda: si beta <= alfa, no hay punto en seguir explorando
            if beta <= alpha:
                break

        return max_eval, best_move

    # ===== FASE DE MINIMIZACIÓN (turno del jugador - BLACK) =====
    else:
        min_eval = math.inf   # Inicializar con valor máximo posible
        best_move = None

        # Obtener todos los movimientos legales para BLACK (jugador)
        valid_moves = game_state.get_valid_moves('BLACK')

        # Si no hay movimientos disponibles, pasar turno
        if not valid_moves:
            evaluacion = pass_turn(
                game_state,
                depth,
                alpha,
                beta,
                is_maximizing,
                difficulty
            )
            return evaluacion, None

        # Evaluar cada movimiento posible del jugador
        for move in valid_moves:
            # Crear copia del estado para simular el movimiento
            clon_estado = game_state.clone()
            clon_estado.make_move(move)

            # Recursivamente evaluar el siguiente nivel (turno de la IA)
            evaluacion, _ = minimax(
                clon_estado,
                depth - 1,
                alpha,
                beta,
                True,   # Siguiente es maximización (IA)
                difficulty
            )

            # Actualizar el movimiento que minimiza el score de la IA
            if evaluacion < min_eval:
                min_eval = evaluacion
                best_move = move

            # Actualizar límite beta para poda
            beta = min(beta, evaluacion)

            # Poda: si beta <= alfa, no hay punto en seguir explorando
            if beta <= alpha:
                break

        return min_eval, best_move


def pass_turn(game_state, depth, alpha, beta, is_maximizing, difficulty):
    """
    Maneja el caso cuando un jugador no tiene movimientos disponibles.
    Cambia el turno al otro jugador y continúa la búsqueda minimax.
    """

    # Crear copia del estado para no modificar el original
    clon_estado = game_state.clone()

    # Cambiar el turno al otro jugador
    clon_estado.current_turn = (
        'BLACK'
        if clon_estado.current_turn == 'WHITE'
        else 'WHITE'
    )

    # Continuar búsqueda con turno invertido
    evaluacion, _ = minimax(
        clon_estado,
        depth - 1,
        alpha,
        beta,
        not is_maximizing,  # Invertir turno (si era maximización, ahora es minimización)
        difficulty
    )

    return evaluacion, None


def get_best_move(game_state, difficulty):
    """
    Punto de entrada principal para obtener el mejor movimiento de la IA.
    Define la profundidad de búsqueda según el nivel de dificultad seleccionado.
    
    Dificultades y profundidades:
        - PRINCIPIANTE: profundidad 2 (búsqueda superficial, rápida)
        - AMATEUR: profundidad 4 (búsqueda moderada)
        - EXPERTO: profundidad 6 (búsqueda profunda, cálculo intensivo)
    """

    # Mapeo de dificultad a profundidad de búsqueda minimax
    depth_limits = {
        'PRINCIPIANTE': 2,
        'AMATEUR': 4,
        'EXPERTO': 6
    }

    # Obtener la profundidad correspondiente (por defecto 4 si no existe)
    depth = depth_limits.get(difficulty.upper(), 4)

    # Ejecutar minimax: la IA (WHITE) busca maximizar su evaluación
    # Inicializar alpha con -inf (peor caso) y beta con +inf (mejor caso)
    _, move = minimax(
        game_state,
        depth,
        -math.inf,      # Alpha: límite inferior para maximización
        math.inf,       # Beta: límite superior para minimización
        True,           # is_maximizing: siempre es True para la IA
        difficulty
    )

    return move