import pygame 
from dropdown import dropDown
from button import Button
import json

class Edit(dropDown):
    def __init__(self,screen,command,name,mode,data):
        self.screen = screen
        self.command = command
        self.name = name
      
        self.data = data

        self.rect = pygame.Rect(30,30,300,500)

        self.dropdown = dropDown(screen,self.rect.topright[0],self.rect.topright[1],"MODE :",("TOUCHE","MACRO"),mode)

        self.save_btn = Button(self.screen,self.rect.bottomleft[0],self.rect.bottomleft[1],"SAVE","white",30)

        self.btn_touche = Button(self.screen,0,0,"Edit key","white",40,)
        self.edit_touche = False
        self.btn_macro = Button(self.screen,0,0,"New Sequence","white",40)
        self.edit_macro = False
        self.macro_sequence = []
        

    def open(self, screen):
        self.screen.fill((0,0,0))

    def close(self):
        pass

    def update(self, event, manager,key):
        self.screen.fill("#222831")
        pygame.draw.rect(self.screen,"green",self.rect)

        self.dropdown.draw()
        self.dropdown.detect()

        pygame.draw.rect(self.screen,"white",(self.dropdown.Rect[0],self.dropdown.Rect[1]+50,300,10))

        self.data_font = pygame.font.Font("freesansbold.ttf", 20)
        data_text = self.data_font.render("Mode : " + self.dropdown.current_option.text , True, (255,255,255))
        textRect = data_text.get_rect(center=(self.rect.midtop[0],self.rect.midtop[1]+30))
        self.screen.blit(data_text, textRect)


        if self.dropdown.current_option.text == "TOUCHE":
            self.draw_touch(key)
            self.edit_macro = False

        if self.dropdown.current_option.text == "MACRO":
           self.draw_macro(key)
           self.edit_touche = False

        self.save_btn.draw()
        if self.save_btn.detect():
            if self.dropdown.current_option.text == "TOUCHE":
                self.data[self.name]["key"] = self.command
                self.data[self.name]["mode"] = "TOUCHE"
                

            if self.dropdown.current_option.text == "MACRO":
                self.data[self.name]["key"] = self.macro_sequence
                self.data[self.name]["mode"] = "MACRO"

            
            with open("config.json","w") as w:
                json.dump(self.data, w, indent=4)
            manager.pop_menu()
            
            
          
        
    def draw_touch(self,key):
        
        data_text = self.data_font.render(str(self.command), True, (255,255,255))
        textRect = data_text.get_rect(center=(self.rect.center[0],self.rect.center[1]))
        self.screen.blit(data_text, textRect)

        self.btn_touche.rect.x = self.dropdown.Rect[0]+20
        self.btn_touche.rect.y = self.dropdown.Rect[1]+70

        self.btn_touche.draw()
        if self.btn_touche.detect():
            
            self.edit_touche = True

        if self.edit_touche:
            self.btn_touche.text = "Select Key..."
            if key != None:
                self.command = key
                self.edit_touche = False
        else:
            self.btn_touche.text = "Edit key"


    def draw_macro(self,key):
        self.btn_macro.rect.x = self.dropdown.Rect[0]+20
        self.btn_macro.rect.y = self.dropdown.Rect[1]+70
        
        self.btn_macro.draw()
        if self.btn_macro.detect():
            self.edit_macro = True
        
        if self.edit_macro:
            self.btn_macro.text = "Select Key..."
            x = self.btn_macro.rect.bottomleft[0]
            y = self.btn_macro.rect.bottomleft[1] + 10
            rect = pygame.Rect((x,y,200,25))

            for i,j in enumerate(self.macro_sequence):
                
                pygame.draw.rect(self.screen,"white",rect,width=1)

                data_text = self.data_font.render(str(i+1) + ": " + j, True, (255,255,255))
                textRect = data_text.get_rect(topleft=(rect.topleft[0],rect.topleft[1]))
                self.screen.blit(data_text, textRect)
                
                x = rect.bottomleft[0]
                y = rect.bottomleft[1]
                rect = pygame.Rect((x,y,200,25))

            if key != None:
                self.macro_sequence.append(key)


        else:
            self.edit_touche = "New Sequence"
        
