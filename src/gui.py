import pygame
import sys
from src.constants import WIDTH, HEIGHT, LIGHT_BROWN, DARK_BROWN, WHITE, BLACK

class KnightEnergyGUI:
    def __init__(self):
        pygame.init()
        # Creamos la ventana (800x600 como definió tu compañero)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Knight Energy - Selección de Dificultad")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 30)
        
        # Estado inicial
        self.running = True
        self.dificultad_seleccionada = None
        
        # Definimos los botones de dificultad
        self.botones = {
            'PRINCIPIANTE': pygame.Rect(WIDTH//2 - 100, 200, 200, 50),
            'AMATEUR':      pygame.Rect(WIDTH//2 - 100, 280, 200, 50),
            'EXPERTO':      pygame.Rect(WIDTH//2 - 100, 360, 200, 50)
        }

    def main_menu(self):
        """Bucle del menú principal"""
        while self.running and self.dificultad_seleccionada is None:
            self.screen.fill((255, 243, 221)) # Color crema de nuestra estética
            
            # Dibujar Título
            title_surf = self.font_title.render("KNIGHT ENERGY", True, (60, 64, 67))
            self.screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 80))
            
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
                                print(f"Dificultad elegida: {self.dificultad_seleccionada}")

            # Dibujar Botones
            mouse_pos = pygame.mouse.get_pos()
            for diff, rect in self.botones.items():
                # Efecto Hover
                color = (217, 119, 6) if rect.collidepoint(mouse_pos) else (181, 136, 99)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                
                # Texto del botón
                text_surf = self.font_button.render(diff, True, WHITE)
                self.screen.blit(text_surf, (rect.centerx - text_surf.get_width()//2, 
                                             rect.centery - text_surf.get_height()//2))

            pygame.display.flip()
            self.clock.tick(60)
        
        return self.dificultad_seleccionada

if __name__ == "__main__":
    gui = KnightEnergyGUI()
    dificultad = gui.main_menu()
    if dificultad:
        print(f"Iniciando juego en modo {dificultad}...")
        # Aquí llamaríamos a la siguiente fase: dibujar el tablero

