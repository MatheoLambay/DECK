import pygame

import threading
import os
import sys
import pystray
from PIL import Image, ImageDraw
import win32gui
import win32con

from menu_manager import menuManager
from mainMeny import mainMenu

def create_systray_image():
    try:
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_dir, 'logo.ico')
        return Image.open(logo_path)
    except Exception as e:
        print("Erreur chargement logo.ico, fallback cercle vert:", e)
        # Fallback cercle vert si erreur
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill="green")
        return image

def run_systray(on_show):
    icon = pystray.Icon("my_app", create_systray_image(), "Mathéo DECK")

    def on_clicked(icon, item):
        if str(item) == "Show":
            on_show()
        elif str(item) == "Quit":
            pygame.quit()
            icon.stop()

    icon.menu = pystray.Menu(
        pystray.MenuItem("Show", on_clicked),
        pystray.MenuItem("Quit", on_clicked)
    )

    threading.Thread(target=icon.run, daemon=True).start()

def show_window():
	hwnd = pygame.display.get_wm_info()["window"]
	win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
	win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
	win32gui.SetForegroundWindow(hwnd)

def hide_window():
	hwnd = pygame.display.get_wm_info()["window"]
	win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
	win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

logo_path = os.path.join(base_dir, 'logo.png')
icon_image = pygame.image.load(logo_path)

pygame.init()
pygame.font.init()
pygame.display.set_caption("Mathéo DECK")
pygame.display.set_icon(icon_image)

menu_manager = menuManager()
# Lance l'icône systray
# run_systray(show_window)

# # Au démarrage : cache la fenêtre (minimise + cache)
# hide_window()
menu_manager.push_menu(mainMenu(menu_manager.screen))




run = True
while run:
    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hide_window()
                
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
        

    current_menu = menu_manager.get_current_menu()
    if current_menu:
        current_menu.update(key,menu_manager,key)

    pygame.display.update()

pygame.quit()

