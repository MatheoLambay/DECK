import pygame 
from dropdown import dropDown
from button import Button
import json
from inputBox import InputBox

class Edit(dropDown):
    def __init__(self,screen,command,name,color,mode,data):
        self.screen = screen
        self.command = command
        self.name = name
        self.data = data

        self.rect = pygame.Rect(30,30,300,500)
        self.rect_color = color

        self.dropdown = dropDown(screen,self.rect.topright[0],self.rect.topright[1],"OPTIONS:",("TOUCHE","MACRO","COLOR"),mode)

        self.save_btn = Button(self.screen,self.rect.bottomleft[0],self.rect.bottomleft[1],"SAVE","white",30)
        self.back_btn = Button(self.screen,self.save_btn.rect.topright[0]+10,self.save_btn.rect.topright[1],"BACK","white",30)

        self.btn_touche = Button(self.screen,0,0,"Edit key","white",40,)
        self.edit_touche = False
        self.btn_macro = Button(self.screen,0,0,"Edit Sequence","white",40)
        self.edit_macro = False
        self.macro_sequence = []
        self.rect_macro_sequence = []

        self.color = ("GREEN","RED","BLUE")

        self.dropdown_macro = dropDown(self.screen,0,0,"+ :",("TEXT","ACTION","DELETE"),"TEXT")
        self.dropdown_color = dropDown(self.screen,0,0,"Select : ",self.color,color.upper())
        self.input_box = InputBox(self.screen,400,400,200,30)

        if mode == "MACRO":
            self.macro_sequence = command

        self.editing = None
        self.clicked = False
        
        

    def open(self, screen):
        self.screen.fill("#222831")

    def close(self):
        pass

    def update(self, event, manager,key):
        self.screen.fill("#222831")
        pygame.draw.rect(self.screen,self.rect_color,self.rect)

        self.dropdown.draw()
        self.dropdown.detect()
        
        self.sep_rect = pygame.Rect(self.dropdown.Rect[0],self.dropdown.Rect[1]+50,300,10)
        pygame.draw.rect(self.screen,"white",self.sep_rect)

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

        if self.dropdown.current_option.text == "COLOR":
            self.draw_color()

        """back button"""
        self.back_btn.draw()
        if self.back_btn.detect():
            manager.pop_menu()

        """save button"""
        self.save_btn.draw()
        if self.save_btn.detect():
            if self.dropdown.current_option.text == "TOUCHE":
                self.data[self.name]["key"] = self.command
                self.data[self.name]["mode"] = "TOUCHE"
                

            if self.dropdown.current_option.text == "MACRO":
                self.data[self.name]["key"] = self.macro_sequence
                self.data[self.name]["mode"] = "MACRO"

            self.data[self.name]["color"] = self.rect_color
            with open("config.json","w") as w:
                json.dump(self.data, w, indent=4)
            manager.pop_menu()
            
    """set rect color"""
    def draw_color(self):
        self.dropdown_color.x = self.dropdown.Rect[0]
        self.dropdown_color.y = self.dropdown.Rect[1]+70
        self.dropdown_color.draw()
        self.dropdown_color.detect()
        self.rect_color = self.dropdown_color.current_option.text.lower()
        
          
    def draw_touch(self,key):
        
        data_text = self.data_font.render(str(self.command), True, (255,255,255))
        textRect = data_text.get_rect(center=(self.rect.center[0],self.rect.center[1]))
        self.screen.blit(data_text, textRect)

        self.btn_touche.x = self.dropdown.Rect[0]
        self.btn_touche.y = self.dropdown.Rect[1]+70

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
        
        self.dropdown_macro.x = self.dropdown.Rect[0]
        self.dropdown_macro.y = self.dropdown.Rect[1]+70
        self.dropdown_macro.draw()
        self.dropdown_macro.detect()

        if self.dropdown_macro.current_option.text == "TEXT":
            self.input_box.rect.x = self.dropdown_macro.Rect.bottomleft[0]
            self.input_box.rect.y = self.dropdown_macro.Rect.bottomleft[1]+40

            self.input_box.update()
            self.input_box.draw()
            result = self.input_box.handle_text_input(key)
            if  result != None:
                if self.editing == None:
                    self.macro_sequence.append(result)
                else:
                    self.macro_sequence[self.editing] = result
                    
                    self.editing = None
                self.input_box.reset()

        if self.dropdown_macro.current_option.text == "ACTION":
            data_text = self.data_font.render("Press Key...", True, (255,255,255))
            textRect = data_text.get_rect(topleft=(self.dropdown_macro.Rect.bottomleft[0],self.dropdown_macro.Rect.bottomleft[1]+40))
            self.screen.blit(data_text, textRect)
            if key != None:
                if self.editing == None:
                    self.macro_sequence.append(key)
                    
                else:
                    self.macro_sequence[self.editing] = key
                    self.editing = None
                    
        
        if self.dropdown_macro.current_option.text == "DELETE":
            if self.editing != None:
                self.macro_sequence.pop(self.editing)
                self.editing = None

   

        x = self.sep_rect.topright[0]
        y = self.sep_rect.topright[1]
        rect = pygame.Rect((x,y,198,25))
        self.rect_macro_sequence = []
        for i,j in enumerate(self.macro_sequence):
            # print(i, self.editing)
            if self.editing == i:
                
                self.rect_macro_sequence.append(pygame.draw.rect(self.screen,"green",rect,width=1))
            else :
                self.rect_macro_sequence.append(pygame.draw.rect(self.screen,"white",rect,width=1))
            data_text = self.data_font.render(str(i+1) + ": " + j, True, (255,255,255))
            textRect = data_text.get_rect(topleft=(rect.topleft[0],rect.topleft[1]))
            self.screen.blit(data_text, textRect)
            
            x = rect.bottomleft[0]
            y = rect.bottomleft[1]
            rect = pygame.Rect((x,y,198,25))


        for i in range(len(self.rect_macro_sequence)):
          
            
            pos = pygame.mouse.get_pos()
            if self.rect_macro_sequence[i].collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                   
                    self.editing = i
                    # print(self.editing)
                    self.clicked = True
			
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
