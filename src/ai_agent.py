class MinimaxAgent:
    # Inicializa el agente.
    def __init__(self, difficulty='amateur'):
        if difficulty == 'principiante':
            self.max_depth = 2
        elif difficulty == 'amateur':
            self.max_depth = 4
        elif difficulty == 'experto':
            self.max_depth = 6
        else:
            self.max_depth = 4  # Default