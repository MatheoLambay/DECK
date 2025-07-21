from button import Button
import pygame

class dropDown:
    def __init__(self,screen,x,y,text,content,mode):
        self.screen = screen
        self.content = content
        self.x = x
        self.y = y

        data_font = pygame.font.Font("freesansbold.ttf", 20)
        self.data_text = data_font.render(text, True, (255,255,255))
        self.Rect = self.data_text.get_rect(topleft=(x,y))
        
        self.btns = []
        x = self.Rect.bottomleft[0]
        y = self.Rect.bottomleft[1] + 10
        for i in self.content:
            new_btn = Button(self.screen,x,y,i,"white",20)
            self.btns.append(new_btn)
            x = new_btn.rect.topright[0] + 10

        self.current_option = self.btns[self.content.index(mode)]
    

    def draw(self):
        self.screen.blit(self.data_text, self.Rect)
       
        for i in self.btns:
            i.draw()
            if i == self.current_option:
                i.text_color = "green"
            else:
                i.text_color = "white"

    def detect(self):
        for i in self.btns:
            if i.detect():
                self.current_option = i
            
