import pygame
import sys
from constants import WIDTH, HEIGHT, WHITE, BLACK

class KnightEnergyGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Knight Energy - Selección de Dificultad")
        self.clock = pygame.time.Clock()

        # Fuentes
        self.font_title = pygame.font.SysFont('georgia', 65, bold=True)
        self.font_subtitle = pygame.font.SysFont('georgia', 14)
        self.font_button = pygame.font.SysFont('georgia', 18, bold=True)
        self.font_info = pygame.font.SysFont('segoeuisymbol, segoeuiemoji, arial', 14)
        
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

        # Imagen de fondo
        image_path = "background0.png" 
        try:
            loaded_image = pygame.image.load(image_path).convert()
            # Escalarla al tamaño de la pantalla para que encaje perfecto
            self.background_image = pygame.transform.scale(loaded_image, (WIDTH, HEIGHT))
        except FileNotFoundError:
            print(f"No se encontró la imagen '{image_path}'. Usando color sólido de respaldo.")
            self.background_image = None

    def draw_text_centered(self, text, font, color, y, shadow=False):
        """Función auxiliar para centrar textos fácilmente"""
        if shadow:
            # Dibuja una sombra sutil desplazada 3 píxeles
            shadow_surf = font.render(text, True, (220, 210, 195))
            self.screen.blit(shadow_surf, (WIDTH//2 - shadow_surf.get_width()//2 + 3, y + 3))
            
        surf = font.render(text, True, color)
        self.screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y))

    def main_menu(self):
        while self.running and self.dificultad_seleccionada is None:

            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
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

if __name__ == "__main__":
    gui = KnightEnergyGUI()
    dificultad = gui.main_menu()
    if dificultad:
        print(f"Iniciando juego en modo {dificultad}...")
        # Aquí llamaríamos a la siguiente fase: dibujar el tablero

