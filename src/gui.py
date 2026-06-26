# pyrefly: ignore [missing-import]
import pygame
import sys
from constants import WIDTH, HEIGHT, WHITE, BLACK, BOARD_SIZE

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

    def run_game(self, dificultad):
        
        # Variables simuladas de estado del juego
        maquina_pts, maquina_en = 25, 12
        jugador_pts, jugador_en = 30, 8
        
        # Cálculos para centrar el tablero
        # Suponemos que el tablero medirá el 75% del alto de la pantalla
        sq_size = int(HEIGHT * 0.75) // 8
        board_size = sq_size * 8  
        board_x = WIDTH // 2 - board_size // 2
        board_y = HEIGHT // 2 - board_size // 2

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            # 1. Dibujar Fondo
            if self.bg_board:
                self.screen.blit(self.bg_board, (0, 0))
            else:
                self.screen.fill(self.color_bg)

            # 2. Dibujar Información Lateral
            # Panel Izquierdo (Máquina)
            self.draw_player_info("MÁQUINA", "(BLANCA)", maquina_pts, maquina_en, 
                                   x=110, y=HEIGHT//2 - 65)
            
            # Panel Derecho (Jugador)
            self.draw_player_info("JUGADOR", "(NEGRA)", jugador_pts, jugador_en, 
                                   x=WIDTH - 110, y=HEIGHT//2 - 65)

            # 3. Dibujar Borde del Tablero
            border_rect = pygame.Rect(board_x - 6, board_y - 6, board_size + 12, board_size + 12)
            pygame.draw.rect(self.screen, self.color_gold, border_rect, width=6, border_radius=4)
            pygame.draw.rect(self.screen, self.color_text_dark, border_rect, width=2, border_radius=4) # Borde interior fino

            # 4. Dibujar Cuadrícula de 8x8
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    rect = pygame.Rect(board_x + col * sq_size, board_y + row * sq_size, sq_size, sq_size)
                    
                    # Alternar colores como en el ajedrez
                    if (row + col) % 2 == 0:
                        color = self.color_board_light
                    else:
                        color = self.color_board_dark
                        
                    pygame.draw.rect(self.screen, color, rect)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    gui = KnightEnergyGUI()
    dificultad = gui.main_menu()
    if dificultad:
        print(f"Iniciando juego en modo {dificultad}...")
        gui.run_game(dificultad)

