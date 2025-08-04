# DECK

**DECK** est un stream deck open-source DIY basé sur un écran tactile TFT LCD et un microcontrôleur ESP32, permettant de déclencher des actions personnalisées sur un ordinateur via une application Python. Idéal pour les streamers, développeurs ou toute personne souhaitant automatiser des tâches grâce à un panneau tactile personnalisable.

---

## 🚀 Présentation

- **Interface tactile** : écran TFT avec boutons interactifs, personnalisables (labels, couleurs, actions…)
- **Communication série** : l’ESP32 communique avec le PC via USB (port série)
- **Application Python** : reçoit les commandes et exécute les actions associées (raccourcis clavier, lancement de logiciels, scripts, etc.)
- **Extensible & DIY** : modifiez facilement le firmware ou l’application PC pour ajouter de nouvelles fonctionnalités

---

## 🏗️ Architecture

- **ESP32** : gère l’affichage et la détection tactile, envoie les événements boutons au PC
- **PC** : l’application Python écoute le port série, mappe chaque bouton à une action personnalisée

---

## ✨ Fonctionnalités principales

- Interface tactile interactive (affichage dynamique des boutons)
- Personnalisation complète des boutons (label, couleur, action)
- Communication série bidirectionnelle (ESP32 ↔ Python)
- Application Python extensible (ajout facile de nouvelles actions)
- Réactivité et faible latence pour une expérience fluide

---

## 🛠️ Technologies utilisées

- **Firmware ESP32** :  
  - C++ (Arduino framework)
  - [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI)
  - TouchScreen
  - Serial

- **Application PC** :  
  - Python 3.10+
  - PySerial
  - OS, subprocess
  - (optionnel : Pygame, Pystray, Pillow, PyWin32 pour interface graphique avancée)

---

## ⚡ Installation

### Côté ESP32

1. **Ouvrir le firmware**  
   Ouvre le dossier `/firmware/` dans l’IDE Arduino ou PlatformIO.

2. **Installer les bibliothèques nécessaires**  
   - `TFT_eSPI`
   - `Adafruit_GFX`
   - (et autres selon le code)

3. **Flasher le code**  
   Branche l’ESP32 en USB et téléverse le firmware.

### Côté PC (Python)

1. **Installer Python 3.10+**  
   [Télécharger Python](https://www.python.org/downloads/)

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```