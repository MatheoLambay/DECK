import pygame
import json
import serial
import keyboard
from serial.tools.list_ports import comports
from edit import Edit
from button import Button
import time
import os
import sys

class mainMenu:
    def __init__(self,screen):
        self.screen = screen
        self.back_button = Button(self.screen,1000,800,"CLOSE",(0,0,0),64,"bottomright")
        
        # # Pour récupérer le dossier utilisateur, cross-platform
        # user_dir = os.path.expanduser("~")  

        # # Chemin où on sauvegarde la config modifiable
        # save_dir = os.path.join(user_dir, ".matheo_deck")
        # os.makedirs(save_dir, exist_ok=True)

        # self.config_save_path = os.path.join(save_dir, "config.json")

        # # Pour lire la config incluse dans l'app (lecture seule)
        # if getattr(sys, 'frozen', False):
        #     base_dir = sys._MEIPASS
        # else:
        #     base_dir = os.path.dirname(os.path.abspath(__file__))

        # self.config_default_path = os.path.join(base_dir, "config.json")

        # # Chargement de la config : si un fichier modifié existe, on charge celui-là,
        # # sinon on charge celui par défaut dans l'exe
        # if os.path.exists(self.config_save_path):
        #     with open(self.config_save_path, "r") as f:
        #         self.data = json.load(f)
        # else:
        #     with open(self.config_default_path, "r") as f:
        #         self.data = json.load(f)
        with open('config.json', "r") as f:
            self.data = json.load(f)

                
        

        self.rectangles = [
            Rectangle(self.screen,10,10,200,380,"btn1",self.data["btn1"]["key"],self.data["btn1"]["mode"]),
            Rectangle(self.screen,220,10,200,380,"btn2",self.data["btn2"]["key"],self.data["btn2"]["mode"]),
            Rectangle(self.screen,430,10,200,380,"btn3",self.data["btn3"]["key"],self.data["btn3"]["mode"]),
            Rectangle(self.screen,10,400,200,380,"btn4",self.data["btn4"]["key"],self.data["btn4"]["mode"]),
            Rectangle(self.screen,220,400,200,380,"btn5",self.data["btn5"]["key"],self.data["btn5"]["mode"]),
            Rectangle(self.screen,430,400,200,380,"btn6",self.data["btn6"]["key"],self.data["btn6"]["mode"])
        ]
        self.btns = ("btn1","btn2","btn3","btn4","btn5","btn6",)

        # self.current_rectangle = None
        self.edit_rect = pygame.Rect(650,100,300,500)

        self.save_button = Button(self.screen,self.edit_rect.midbottom[0],self.edit_rect.midbottom[1]-40,"Save",(0,0,0),30,"center")
        
        self.ser = None
        self.ser_connected = False

        self.last_try_time = 0
        self.retry_interval = 2  

        

    def detect_serial(self):
        now = time.time()
        if now - self.last_try_time < self.retry_interval:
            return False
        self.last_try_time = now

        look_ports = comports()
        for p in look_ports:
            if "CP210" in p.description:
                try:
                    self.ser = serial.Serial(str(p.device), 115200, timeout=0)
                    self.ser_connected = True
                    return True
                except serial.SerialException as e:
                    print(f"Erreur d'ouverture du port {p.device}: {e}")
                    self.ser_connected = False
                    self.ser = None
                    return False
        self.ser_connected = False
        self.ser = None
        return False
            
                
    def open(self, screen):
        screen.fill((255,255,255))
        
    def close(self):
        pass

    def update(self, event, manager,key):
        self.screen.fill("#222831")
       

        if not self.ser_connected:
            # Tente la détection
            self.detect_serial()

            # Affiche "DECK not detected"
            data_font = pygame.font.Font("freesansbold.ttf", 30)
            data_text = data_font.render("DECK not detected", True, (255,255,255))
            textRect = data_text.get_rect(center=(500,400))
            self.screen.blit(data_text, textRect)

        else:

            pygame.draw.rect(self.screen,"grey",self.edit_rect)

            for i in self.rectangles:
                i.mode = self.data[i.name]["mode"]
                i.command = self.data[i.name]["key"]
                if(i.detect()):
                    manager.push_menu(Edit(self.screen,i.command,i.name,i.mode,self.data))

            for i in self.rectangles:
                i.draw()
                     
            try:
                if self.ser.in_waiting > 0:
                    
                    ligne = self.ser.readline().decode('utf-8').strip()
                    if ligne in self.btns:
                        if self.rectangles[self.btns.index(ligne)].mode == "TOUCHE":
                            keyboard.press_and_release(self.rectangles[self.btns.index(ligne)].command)
                        elif self.rectangles[self.btns.index(ligne)].mode == "MACRO":
                            for i in self.rectangles[self.btns.index(ligne)].command:
                                keyboard.press_and_release(i)
                    # if ligne == "btn1":
                    #     index = 0
                    #     keyboard.press_and_release(self.rectangles[0].command)
                    # elif ligne == "btn2":
                    #     keyboard.press_and_release(self.rectangles[1].command)
                    # elif ligne == "btn3":
                    #     keyboard.press_and_release(self.rectangles[2].command)
                    # elif ligne == "btn4":
                    #     keyboard.press_and_release(self.rectangles[3].command)
                    # elif ligne == "btn5":
                    #     keyboard.press_and_release(self.rectangles[4].command)
                    # elif ligne == "btn6":
                    #     keyboard.press_and_release(self.rectangles[5].command)

                    


            except serial.SerialException as e:
                print(f"Erreur port série détectée : {e}")
                try:
                    self.ser.close()
                except Exception:
                    pass
                self.ser = None
                self.ser_connected = False
                    
           
            
             












class Rectangle:
    def __init__(self,screen,x,y,l,h,name,command,mode):
        self.screen = screen
        self.command = command
        self.mode = mode
        self.name = name
        self.rect = pygame.Rect(x,y,l,h)

    def draw(self):
        
        pygame.draw.rect(self.screen,"green",self.rect)
        data_font = pygame.font.Font("freesansbold.ttf", 20)

     
        data_text = data_font.render("Mode : " + self.mode , True, (0,0,0))
        textRect = data_text.get_rect(center=(self.rect.midtop[0],self.rect.midtop[1]+30))
        self.screen.blit(data_text, textRect)

        data_text = data_font.render(str(self.command),True,(0,0,0))
        textRect = data_text.get_rect(center = (self.rect.center[0],self.rect.center[1])) 
        self.screen.blit(data_text, textRect)


    def detect(self):
     
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
                
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action