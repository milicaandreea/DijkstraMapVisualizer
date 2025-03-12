import pygame
from dijkstra import calculate_distance,dijkstra
import threading

class MapVisualizer:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.window_width = 1200
        self.window_height = 800
        self.screen = None
        self.running = True
        self.selected_nodes = []
        self.path = None

        # Zoom și deplasare
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Dimensiuni și spațiere butoane
        button_size = 50
        margin = 10
        center_x = self.window_width - 4 * button_size  # Coordonata X centrală
        center_y = self.window_height - 3 * button_size  # Coordonata Y centrală

        # Poziționarea butoanelor
        self.buttons = {
            "zoom_in": pygame.Rect(center_x, center_y, button_size, button_size),  # +
            "zoom_out": pygame.Rect(center_x + button_size + margin, center_y, button_size, button_size),  # -
            "left": pygame.Rect(center_x - button_size - margin, center_y, button_size, button_size),  # Stânga
            "right": pygame.Rect(center_x + 2 * (button_size + margin), center_y, button_size, button_size),  # Dreapta
            "down": pygame.Rect(center_x + button_size // 2, center_y + button_size + margin, button_size, button_size),  # Jos
            "up": pygame.Rect(center_x + button_size // 2, center_y - button_size - margin, button_size, button_size),  # Sus
        }

        self._initialize_pygame()
        self.render_static()

    def draw_buttons(self):
        """
        Desenează butoanele pentru zoom și deplasare, cu aliniere perfectă a textului.
        """
        button_color = (255, 255, 255)
        font = pygame.font.SysFont("arial", 30)  # Font compatibil Unicode

        # Desenează fiecare buton
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, button_color, rect)  # Fundal buton
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Contur negru

        # Simboluri pentru butoane (aliniate central)
        symbols = {
            "zoom_in": "+",
            "zoom_out": "-",
            "up": "↑",
            "down": "↓",
            "left": "←",
            "right": "→",
        }

        for name, rect in self.buttons.items():
            text_surface = font.render(symbols[name], True, (0, 0, 0))  # Desenează textul
            text_rect = text_surface.get_rect(center=rect.center)  # Centrează textul în buton
            self.screen.blit(text_surface, text_rect)  # Afișează textul pe buton

    def _initialize_pygame(self):
        """
        Initializeaza fereastra pygame si parametrii initiali.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Dijkstra - Harta Luxembourg")
        
        # Calcul limite si scalare
        min_x = min(x for x, _ in self.nodes.values())
        min_y = min(y for _, y in self.nodes.values())
        max_x = max(x for x, _ in self.nodes.values())
        max_y = max(y for _, y in self.nodes.values())
        
        self.scale_x = self.window_width / (max_x - min_x)
        self.scale_y = self.window_height / (max_y - min_y)
        self.scale = min(self.scale_x, self.scale_y)
        self.min_x = min_x
        self.min_y = min_y

    def transform_coords(self, coords):
        """
        Transformă coordonatele reale în coordonate pe ecran, aplicând zoom și deplasare.
        """
        x, y = coords
        transformed_x = (x - self.min_x) * self.scale * self.zoom_level + self.offset_x
        transformed_y = (y - self.min_y) * self.scale * self.zoom_level + self.offset_y
        return int(transformed_x), int(transformed_y)

    def find_closest_node(self, click_pos):
        """
        Gaseste nodul cel mai apropiat de pozitia unde s-a dat click.
        """
        closest_node = None
        min_distance = float('inf')
        real_x = click_pos[0] / self.scale + self.min_x
        real_y = click_pos[1] / self.scale + self.min_y

        for node_id, position in self.nodes.items():
            distance = calculate_distance((real_x, real_y), position)
            if distance < min_distance:
                min_distance = distance
                closest_node = node_id
        return closest_node

    def render_static(self):
        """
        Deseneaza fundalul si muchiile o singura data pentru performanta.
        """
        self.background = pygame.Surface((self.window_width, self.window_height))
        self.background.fill((255, 255, 255))

        # Deseneaza muchiile
        for u, v, _ in self.edges:
            pygame.draw.line(self.background, (200, 200, 200),
                            self.transform_coords(self.nodes[u]),
                            self.transform_coords(self.nodes[v]), 1)

        # Deseneaza nodurile
        for node_id, pos in self.nodes.items():
            pygame.draw.circle(self.background, (0, 0, 255), self.transform_coords(pos), 2)

    def render(self):
        """
        Desenează harta completă (fundal, muchii, noduri, drum minim) în ordinea corectă.
        """
        self.screen.fill((200, 255, 200))  # Fundal verde foarte deschis

        # 1. Desenează muchiile (arcele)
        for u, v, _ in self.edges:
            pygame.draw.line(self.screen, (200, 200, 200),  # Gri deschis pentru muchii
                            self.transform_coords(self.nodes[u]),
                            self.transform_coords(self.nodes[v]), 1)

        # 2. Desenează nodurile (verde închis)
        for node_id, pos in self.nodes.items():
            pygame.draw.circle(self.screen, (0, 100, 0), self.transform_coords(pos), 2)

        # 3. Evidențiază nodurile selectate (albastru)
        for i, node_id in enumerate(self.selected_nodes):
            pygame.draw.circle(self.screen, (0, 0, 255), self.transform_coords(self.nodes[node_id]), 5)

        # 4. Desenează drumul minim (albastru deschis)
        if self.path:
            self.draw_path(self.path)

        # 5. Desenează butoanele (deasupra tuturor)
        self.draw_buttons()

        pygame.display.flip()

    def repaint(self):
        """
        Reface complet desenul grafic.
        """
        self.render()

    def run(self):
        """
        Rulează fereastra și procesează evenimentele.
        """
        def compute_path():
            start_node, end_node = self.selected_nodes
            path, total_distance = dijkstra(self.nodes, self.edges, start_node, end_node)
            self.set_path(path)

        while self.running:
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Detectează click pe butoane
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.buttons["zoom_in"].collidepoint(mouse_pos):
                        self.zoom_level *= 1.1  # Zoom in
                    elif self.buttons["zoom_out"].collidepoint(mouse_pos):
                        self.zoom_level /= 1.1  # Zoom out
                    elif self.buttons["up"].collidepoint(mouse_pos):
                        self.offset_y += 50  # Deplasare în sus
                    elif self.buttons["down"].collidepoint(mouse_pos):
                        self.offset_y -= 50  # Deplasare în jos
                    elif self.buttons["left"].collidepoint(mouse_pos):
                        self.offset_x += 50  # Deplasare la stânga
                    elif self.buttons["right"].collidepoint(mouse_pos):
                        self.offset_x -= 50  # Deplasare la dreapta

                    # Detectează click pentru selectarea nodurilor
                    elif len(self.selected_nodes) < 2:
                        closest_node = self.find_closest_node(mouse_pos)
                        if closest_node is not None:
                            self.selected_nodes.append(closest_node)

            # Calculează drumul minim când sunt selectate 2 noduri
            if len(self.selected_nodes) == 2 and not hasattr(self, 'path_thread'):
                self.path_thread = threading.Thread(target=compute_path)
                self.path_thread.start()

            pygame.time.delay(10)  # Mică pauză pentru performanță

    def draw_path(self, path):
        """
        Desenează drumul minim, aplicând zoom și deplasare.
        """
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            pygame.draw.line(self.screen, (255, 0, 0),
                            self.transform_coords(self.nodes[u]),
                            self.transform_coords(self.nodes[v]), 3)

    def set_path(self, path):
        """
        Seteaza drumul minim pentru afisare si coloreaza-l.
        """
        self.path = path
        self.repaint()

    def close(self):
        """
        Inchide fereastra pygame.
        """
        pygame.quit()
