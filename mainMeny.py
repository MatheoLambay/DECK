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
from time import sleep

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

        self.last_time = 0
        self.interval = 100


        self.special_keys = [
            # Lettres
            "a","b","c","d","e","f","g","h","i","j","k","l","m",
            "n","o","p","q","r","s","t","u","v","w","x","y","z",

            # Chiffres
            "0","1","2","3","4","5","6","7","8","9",

            # Touches spéciales
            "enter", "return",
            "shift", "shift left", "shift right",
            "ctrl", "ctrl left", "ctrl right",
            "alt", "alt left", "alt right",
            "tab",
            "space",
            "backspace",
            "delete",
            "esc", "escape",
            "caps lock",
            "up", "down", "left", "right",
            "page up", "page down",
            "home", "end", "insert",
            "print screen",
            "scroll lock",
            "pause",
            "num lock",
            "menu",
            "windows",
            "command",
            "option",

            # Touches de fonction
            "f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12",

            # Ponctuation et symboles
            "space", "enter", "tab",
            "minus", "equal",
            "left bracket", "right bracket",
            "backslash",
            "semicolon", "apostrophe",
            "grave",        # touche "accent grave" (`)
            "comma", "dot", "slash",

            # Pavé numérique (numpad)
            "num 0", "num 1", "num 2", "num 3", "num 4", "num 5", "num 6", "num 7", "num 8", "num 9",
            "num decimal", "num divide", "num multiply", "num subtract", "num add", "num enter"
        ]




        

    def detect_serial(self):
        now = time.time()

        if now - self.last_try_time < self.retry_interval:
            return False
        self.last_try_time = now

        # Ferme proprement le port s'il est encore ouvert
        if self.ser:
            try:
                if self.ser.is_open:
                    print("🔌 Fermeture du port série précédent.")
                    self.ser.close()
            except Exception as e:
                print(f"⚠️ Erreur lors de la fermeture du port précédent : {e}")
            self.ser = None
            self.ser_connected = False

        print("🔍 Recherche de ports série...")
        look_ports = comports()

        for p in look_ports:
            desc = getattr(p, 'description', '')
            device = getattr(p, 'device', '')
            print(f"➡️ Port détecté : {desc} ({device})")

            if "CP210" in desc:
                try:
                    print(f"📡 Connexion au port {device}...")
                    self.ser = serial.Serial(device, 115200, timeout=1)
                    self.ser_connected = True
                    print(f"✅ Connecté à {device}")
                    return True
                except serial.SerialException as e:
                    print(f"❌ Erreur d'ouverture du port {device} : {e}")
                    self.ser = None
                    self.ser_connected = False
                    return False

        print("⚠️ Aucun port CP210 trouvé.")
        self.ser = None
        self.ser_connected = False
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
                    current_time = pygame.time.get_ticks()
                
                    ligne = self.ser.readline().decode('utf-8').strip()
                    if ligne in self.btns:
                        if self.rectangles[self.btns.index(ligne)].mode == "TOUCHE":
                            keyboard.press_and_release(self.rectangles[self.btns.index(ligne)].command)

                        elif self.rectangles[self.btns.index(ligne)].mode == "MACRO":
                            for i in self.rectangles[self.btns.index(ligne)].command:
                                if i in self.special_keys:
                                    keyboard.press_and_release(i)
                                    print(1)
                                    
                                else:
                                    keyboard.write(i)
                                    print(2)
                                sleep(0.1)
                        
                                        
                              
                  

                    


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