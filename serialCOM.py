import serial
import time

class SerialCom:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # délai pour stabiliser la connexion
            print(f"Connecté au port {self.port}")
        except serial.SerialException as e:
            print(f"Erreur de connexion : {e}")
            time.sleep(1)

    
    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def send(self, data):
        if self.ser and self.ser.is_open:
            if isinstance(data, str):
                data = data.encode()  # conversion en bytes
            self.ser.write(data)
        else:
            print("Port série non ouvert")


    def readline(self):
        if self.ser and self.ser.is_open:
            msg = self.ser.readline().decode('utf-8').strip()
            if msg != "":
                return msg
            return None

        else:
            print("Port série non ouvert")
            return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Port {self.port} fermé")