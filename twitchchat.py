import socket
import re


class TwitchChat:
    def __init__(self, host='irc.chat.twitch.tv', port=6667, nick='', token='', channel=''):
        self.host = host
        self.port = port
        self.nick = nick
        self.token = token
        self.channel = channel
        self.last_message = None
   
    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nick}\n".encode('utf-8'))
        self.sock.send("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
        
    
    def read(self):
        while 1:
            resp = self.sock.recv(2048).decode('utf-8')
    
            if resp.startswith('@'):
                try:
                    tags, content = resp.split(' ', 1)
                    tag_dict = dict(tag.split('=') for tag in tags[1:].split(';'))

                    color = tag_dict.get('color', '')  # peut être vide
                    display_name = tag_dict.get('display-name', '')

                    match = re.search(r'PRIVMSG #[^ ]+ :(.*)', content)
                    if match:
                        message = match.group(1)

                        # Si pas de couleur définie, on affiche "None"
                        hex_color = color if color else "None"

                        return  f"{hex_color} | {display_name} | {message}"
                except Exception as e:
                    print(f"Erreur: {e}")
            return None
        