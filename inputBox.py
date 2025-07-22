import pygame

class InputBox:
    def __init__(self, screen, x, y, w, h, text=''):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, 48)
        self.txt_surface = self.font.render(self.text, True, 'white')
        self.active = False
        self.clicked = False
        self.black = (0, 0, 0)

    def detect_click(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def update(self):
        # activation via détection de clic (sans event)
        self.active = True
        # if self.detect_click():
        #     self.active = not self.active  # toggle on click

        width = max(200, self.txt_surface.get_width() + 20)
        self.rect.w = width

    def handle_keyboard(self):
        keys = pygame.key.get_pressed()  # utile si tu veux utiliser des touches fixes (optionnel)

    def handle_text_input(self, key_str):
        if key_str is None:
            return None
        if not self.active:
            return None
        print(key_str)
        if key_str == "return" or key_str == "ENTER":
            return self.text
        elif key_str == "backspace":
            self.text = self.text[:-1]
        elif len(key_str) == 1:
            self.text += key_str
        self.txt_surface = self.font.render(self.text, True, "white")



    def draw(self):
        text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
        self.screen.blit(self.txt_surface, (self.rect.x + 10, text_y))
        pygame.draw.rect(self.screen, 'white', self.rect, 2 if not self.active else 4)


    def get(self):
        return self.text
