# pyrefly: ignore [missing-import]
import pygame
import sys
from src.constants import WIDTH, HEIGHT, WHITE, BLACK, BOARD_SIZE
from src.game_logic import *
from src.ai_agent import get_best_move  # Importar IA
import queue
import threading
import random


class cellGUI:
    def __init__(self, rect, col, row):
        self.rect = rect
        self.row = row
        self.col = col

# Player piece containint the Pygame surface and rect
class playerPiece:
    def __init__(self, image_path, col, row, sq_size, board_x = 0, board_y = 0):
        self.surface = pygame.image.load(image_path).convert_alpha()
        self.surface = pygame.transform.smoothscale(self.surface, (sq_size, sq_size))
        self.rect = self.surface.get_rect()
        self.sq_size = sq_size
        self.position = (col, row)

        # Position chess piece
        self.update_grid_position(col, row, board_x, board_y)
    
    def update_grid_position(self, col, row, board_x, board_y):
        sq_size = self.sq_size
        """Calculate the pixel center of the grid square and snap the piece's rect center to it."""
        pixel_x = board_x + (col * sq_size) + (sq_size // 2)
        pixel_y = board_y + (row * sq_size) + (sq_size // 2)
        self.rect.center = (pixel_x, pixel_y)


class specialSquare:
    def __init__(self, type, value, col, row, sq_size, board_x, board_y, font):
        image_path = "star.png" if type == "STAR" else "ray.png"
        self.surface = pygame.image.load(image_path).convert_alpha()
        self.surface = pygame.transform.smoothscale(self.surface, (sq_size, sq_size))
        self.rect = self.surface.get_rect()

        pixel_x = board_x + (col * sq_size) + (sq_size // 2)
        pixel_y = board_y + (row * sq_size) + (sq_size // 2)
        self.rect.center = (pixel_x, pixel_y + 2)

        width = self.surface.get_width()
        height = self.surface.get_height()

        cx = width
        cy = 0

        # Draw value
        val_surf = font.render(str(value), True, (0, 0, 0),)
        val_rect = val_surf.get_rect(center=(cx - 6, cy + 5))
        self.surface.blit(val_surf, val_rect)

        self.position = (col, row)
        self.visible = True

    
    def not_visible(self):
        self.visible = False
    
class KnightEnergyGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Knight Energy")
        self.clock = pygame.time.Clock()

        # Fuentes
        self.font_title = pygame.font.SysFont('georgia', 65, bold=True)
        self.font_subtitle = pygame.font.SysFont('georgia', 14)
        self.font_button = pygame.font.SysFont('georgia', 18, bold=True)
        self.font_info = pygame.font.SysFont('segoeuisymbol, segoeuiemoji, arial', 14)
        self.font_panel = pygame.font.SysFont('georgia', 16, bold=True)
        
        # Estado inicial
        self.running = True
        self.dificultad_seleccionada = None
        
        # Ajuste de tamaño y posición de botones
        btn_width, btn_height = 270, 55
        
        base_y = 280
        espaciado = 75
        self.botones = {
            'PRINCIPIANTE': pygame.Rect(WIDTH//2 - btn_width//2, base_y, btn_width, btn_height),
            'AMATEUR':      pygame.Rect(WIDTH//2 - btn_width//2, base_y + espaciado, btn_width, btn_height),
            'EXPERTO':      pygame.Rect(WIDTH//2 - btn_width//2, base_y + espaciado * 2, btn_width, btn_height)
        }

        # Paleta de colores 
        self.color_bg = (246, 240, 228)       # Crema estilo papel
        self.color_text_dark = (40, 30, 20)   # Café casi negro
        self.color_gold = (156, 114, 56)      # Bronce/Oro mate
        self.color_btn = (235, 225, 210)      # Crema claro
        self.color_btn_hover = (250, 243, 230)# Crema mas brillante
        self.color_shadow = (205, 195, 180)   # Sombra del botón

        # Colores del tablero
        self.color_board_light = (193, 154, 107) # Madera clara
        self.color_board_dark = (101, 67, 33)    # Madera oscura

        # Casillas de tablero
        self.cells = []
        self.special_sqs = []

        # Fondo para el menú
        try:
            img_menu = pygame.image.load("background0.png").convert()
            self.bg_menu = pygame.transform.scale(img_menu, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_menu = None

        # Fondo para el tablero
        try:
            img_board = pygame.image.load("background6.png").convert() 
            self.bg_board = pygame.transform.scale(img_board, (WIDTH, HEIGHT))
        except FileNotFoundError:
            self.bg_board = None
        
        # Game logic
        self.game = GameState()
        
        # Imagenes de caballos
        sq_size = int(HEIGHT * 0.75) // 8
        board_size = sq_size * 8  
        self.board_x = WIDTH // 2 - board_size // 2
        self.board_y = HEIGHT // 2 - board_size // 2

        init_black_pos = self.game.black_pos
        init_white_pos = self.game.white_pos

        print(f"White player starts at {init_white_pos}")
        print(f"Black player starts at {init_black_pos}")

        self.black = playerPiece("black.png", init_black_pos[1], init_black_pos[0], sq_size, self.board_x, self.board_y)
        self.white = playerPiece("white.png", init_white_pos[1], init_white_pos[0], sq_size, self.board_x, self.board_y)

        for (col, row), val in self.game.stars:
            self.special_sqs.append(specialSquare("STAR", val, col, row, sq_size, self.board_x, self.board_y, self.font_info))
        
        for (col, row), val in self.game.energies:
            self.special_sqs.append(specialSquare("ENERGY", val, col, row, sq_size, self.board_x, self.board_y, self.font_info))



    def draw_text_centered(self, text, font, color, y, shadow=False):
        """Función auxiliar para centrar textos fácilmente"""
        if shadow:
            # Dibuja una sombra sutil desplazada 3 píxeles
            shadow_surf = font.render(text, True, (220, 210, 195))
            self.screen.blit(shadow_surf, (WIDTH//2 - shadow_surf.get_width()//2 + 3, y + 3))
            
        surf = font.render(text, True, color)
        self.screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))

    def draw_text_at(self, text, font, color, cx, cy):
        """Función auxiliar para centrar textos en coordenadas X e Y específicas"""
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(cx, cy))
        self.screen.blit(surf, rect)

    def draw_player_info(self, title, subtitle, points, energy, x, y):
        """Dibuja el texto sobre los paneles con la información del jugador"""

        self.draw_text_at(title, self.font_panel, self.color_text_dark, x, y + 40)
        self.draw_text_at(subtitle, self.font_panel, self.color_text_dark, x, y + 65)

        # Textos de estadísticas
        points_text = f"PUNTOS: {points} ★"
        energy_text = f"ENERGÍA: {energy} ⚡"
        
        self.draw_text_at(points_text, self.font_info, self.color_text_dark, x, y + 105)
        self.draw_text_at(energy_text, self.font_info, self.color_text_dark, x, y + 135)
    
    def update_player_position(self, player, col, row):
        self.game.make_move((row, col))
        self.game.print_board_terminal()
        if player == "BLACK":
            self.black.update_grid_position(col, row, self.board_x, self.board_y)
        else:
            self.white.update_grid_position(col, row, self.board_x, self.board_y)


    def main_menu(self):
        while self.running and self.dificultad_seleccionada is None:

            if self.bg_menu:
                self.screen.blit(self.bg_menu, (0, 0))
            else:
                self.screen.fill(self.color_bg)
            # Textos Superiores
            self.draw_text_centered("S E L E C C I O N A   D I F I C U L T A D", self.font_subtitle, self.color_text_dark, 40)

            # Título en dos líneas
            self.draw_text_centered("KNIGHT", self.font_title, self.color_gold, 70, shadow=True)
            self.draw_text_centered("ENERGY", self.font_title, self.color_gold, 140, shadow=True)
            
            # Subtítulo con caracteres Unicode
            info_text = "★ 7 CASILLAS DE PUNTOS   |   ⚡ 4 CASILLAS DE ENERGÍA"
            self.draw_text_centered(info_text, self.font_info, (0, 0, 0), 235)
            
            # Gestionar Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic izquierdo
                        for diff, rect in self.botones.items():
                            if rect.collidepoint(event.pos):
                                self.dificultad_seleccionada = diff

            # Dibujar Botones
            mouse_pos = pygame.mouse.get_pos()

            radio_borde = self.botones['PRINCIPIANTE'].height // 2

            for diff, rect in self.botones.items():
                is_hover = rect.collidepoint(mouse_pos)

                # 1. Dibujar sombra (desplazada hacia abajo)
                shadow_rect = rect.copy()
                shadow_rect.y += 4
                pygame.draw.rect(self.screen, self.color_shadow, shadow_rect, border_radius=radio_borde)

                # 2. Dibujar botón principal
                current_color = self.color_btn_hover if is_hover else self.color_btn
                display_rect = rect.copy()
                
                # Efecto de "clic" (el botón baja si mantienes presionado)
                if is_hover and pygame.mouse.get_pressed()[0]:
                    display_rect.y += 3
                    
                pygame.draw.rect(self.screen, current_color, display_rect, border_radius=radio_borde)
                
                # 3. Dibujar borde sutil
                pygame.draw.rect(self.screen, (215, 205, 190), display_rect, width=2, border_radius=radio_borde)
                
                # 4. Texto del botón
                text_color = self.color_gold if is_hover else self.color_text_dark
                text_surf = self.font_button.render(diff, True, text_color)
                self.screen.blit(text_surf, (display_rect.centerx - text_surf.get_width()//2, 
                                             display_rect.centery - text_surf.get_height()//2))

            pygame.display.flip()
            self.clock.tick(60)
        
        return self.dificultad_seleccionada

    # Draw background boad
    def create_board_surface(self):
        # 1. Setup sizes
        board_size = BOARD_SIZE
        sq_size = int(HEIGHT * 0.75) // 8
        board_x = self.board_x
        board_y = self.board_y

        # 2. Create a blank surface the size of the whole screen
        # (or just the size of the board, but whole-screen is easier for positioning)
        bg_surface = pygame.Surface((WIDTH, HEIGHT))

        # 3. Draw the background on our temporary surface
        if self.bg_board:
            bg_surface.blit(self.bg_board, (0, 0))
        else:
            bg_surface.fill(self.color_bg)

        # 4. Draw Board Borders on the surface
        border_rect = pygame.Rect(board_x - 6, board_y - 6, board_size + 12, board_size + 12)
        pygame.draw.rect(bg_surface, self.color_gold, border_rect, width=6, border_radius=4)
        pygame.draw.rect(bg_surface, self.color_text_dark, border_rect, width=2, border_radius=4)

        # 5. Draw the 8x8 Grid AND build the cell logic list ONCE
        self.cells = [] # Clear it just in case
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(board_x + col * sq_size, board_y + row * sq_size, sq_size, sq_size)
                
                color = self.color_board_light if (row + col) % 2 == 0 else self.color_board_dark
                pygame.draw.rect(bg_surface, color, rect)
                
                # Keep track of cells
                self.cells.append(cellGUI(rect, col, row))
                
        return bg_surface
    
        
    def run_game(self, dificultad):
        # Variables de estado del juego
        self.game_started = False
        game = self.game
        maquina_pts, maquina_en = game.white_points, game.white_energy
        jugador_pts, jugador_en = game.black_points, game.black_energy
        self.current_turn = game.current_turn

        board_background = self.create_board_surface()
        
        # Queue for AI movements
        self.ai_queue = queue.Queue() #
        self.ai_thinking = False
        self.ai_timer = 0       # Tracks when the AI is allowed to move
        self.ai_cooldown = 1000  # Delay in milliseconds (1.5 seconds)

        self.game.print_board_terminal()
        
        warning_msg = ""
        warning_timer = 0

        while self.running and not self.game.is_terminal_state():
            maquina_pts, maquina_en = game.white_points, game.white_energy
            jugador_pts, jugador_en = game.black_points, game.black_energy
            
            current_time = pygame.time.get_ticks()

            penalty = game.check_energy_penalty()
            if penalty:
                warning_msg = "¡Penalización por energía! Turno perdido."
                warning_timer = current_time + 2500
            else:
                movimientos = game.get_valid_moves(game.current_turn)
                if not movimientos:
                    jugador_actual = "MÁQUINA" if game.current_turn == 'WHITE' else "JUGADOR"
                    warning_msg = f"¡Sin movimientos! {jugador_actual} pasa turno."
                    warning_timer = current_time + 2500
                    game.current_turn = 'BLACK' if game.current_turn == 'WHITE' else 'WHITE'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic izquierdo
                        self.game_started = True
                        print("Game Started")
                        for cell in self.cells:
                            rect = cell.rect
                            row = cell.row
                            col = cell.col
                            move = (row, col)
                            if rect.collidepoint(event.pos) and not penalty and game.current_turn == "BLACK":
                                if game.is_move_valid("BLACK", move):
                                    print(f"Moving to ({col}, {row})")
                                    self.ai_timer = 0
                                    self.update_player_position("BLACK", col, row)
                                else:
                                    warning_msg = "¡Movimiento inválido! El caballo se mueve en 'L'."
                                    warning_timer = current_time + 1500
                                
                
            if game.current_turn == "WHITE" and self.game_started:
                
                if self.ai_timer == 0:
                    self.ai_timer = current_time + self.ai_cooldown
                if current_time >= self.ai_timer:
                    if not self.ai_thinking:
                        print("AI thinking")
                        self.ai_thinking = True
                        # Start the AI calculation in the BACKGROUND so the GUI doesn't freeze
                        threading.Thread(
                            target=lambda q: q.put(get_best_move(game, dificultad)), 
                            args=(self.ai_queue,), 
                            daemon=True
                        ).start()

                # Check if the AI thread has finished and sent a move down the bridge
                try:
                    ai_move = self.ai_queue.get_nowait() # Non-blocking check
                    print(f"AI MOVE: {ai_move}")
                    if ai_move:
                        self.update_player_position("WHITE", ai_move[1], ai_move[0])
                    else:
                        # Fallback
                        movs = game.get_valid_moves("WHITE")
                        if movs:
                            mov = random.choice(movs)
                            self.update_player_position("WHITE", mov[1], mov[0])

                    self.ai_thinking = False
                    self.ai_timer = 0

                except queue.Empty:
                    pass
            

            # Dibujar tablero fijo
            self.screen.blit(board_background, (0, 0))
            
            # 2. Dibujar Información Lateral
            # Panel Izquierdo (Máquina)
            self.draw_player_info("MÁQUINA", "(BLANCA)", maquina_pts, maquina_en, 
                                x=110, y=HEIGHT//2 - 65)
            
            # Panel Derecho (Jugador)
            self.draw_player_info("JUGADOR", "(NEGRA)", jugador_pts, jugador_en, 
                                x=WIDTH - 110, y=HEIGHT//2 - 65)
            

            # Figuras de jugadores
            self.screen.blit(self.black.surface, self.black.rect)
            self.screen.blit(self.white.surface, self.white.rect)

            # Estrellas y energías
            for square in self.special_sqs:
                black_pos = (game.black_pos[1], game.black_pos[0])
                white_pos = (game.white_pos[1], game.white_pos[0])
                if black_pos == square.position or white_pos == square.position:
                    square.not_visible()

                if square.visible:
                    self.screen.blit(square.surface, square.rect)
            
            # Dibujar mensaje de advertencia si está activo
            if warning_timer > current_time:
                # Fondo para el texto de advertencia para que resalte
                padding_x, padding_y = 20, 10
                text_surf = self.font_button.render(warning_msg, True, (200, 30, 30))
                bg_rect = text_surf.get_rect(center=(WIDTH//2, 40))
                bg_rect.inflate_ip(padding_x, padding_y)
                pygame.draw.rect(self.screen, self.color_btn, bg_rect, border_radius=10)
                pygame.draw.rect(self.screen, self.color_gold, bg_rect, width=2, border_radius=10)
                self.screen.blit(text_surf, (bg_rect.x + padding_x//2, bg_rect.y + padding_y//2))
        
            pygame.display.flip()
            self.clock.tick(60)

        # Si el bucle termina y el juego está en estado terminal, mostrar pantalla de Game Over
        if self.game.is_terminal_state() and self.running:
            self.show_game_over()

    def show_game_over(self):
        ganador = self.game.get_winner()
        texto_ganador = f"¡GANADOR: MÁQUINA (BLANCA)!" if ganador == "WHITE" else (f"¡GANADOR: JUGADOR (NEGRA)!" if ganador == "BLACK" else "¡EMPATE!")
        
        # Overlay oscuro semitransparente
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(self.color_text_dark)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.screen.blit(overlay, (0, 0))

            # Usar las fuentes del menú
            self.draw_text_centered("JUEGO TERMINADO", self.font_title, self.color_gold, HEIGHT//2 - 60, shadow=True)
            self.draw_text_centered(texto_ganador, self.font_subtitle, self.color_btn, HEIGHT//2 + 20)
            self.draw_text_centered("Haz clic para salir", self.font_info, self.color_btn_hover, HEIGHT//2 + 70)

            pygame.display.flip()
            self.clock.tick(60)
    
        

if __name__ == "__main__":
    gui = KnightEnergyGUI((0,0), (0,1))
    dificultad = gui.main_menu()
    if dificultad:
        print(f"Iniciando juego en modo {dificultad}...")
        gui.run_game(dificultad)

