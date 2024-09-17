import requests
import socket
import numpy as np
import cv2


deneyap_ip = '192.168.2.239'
kamera_port = 80


url = f'http://{deneyap_ip}:{kamera_port}/capture'


def get_img():
    resp = requests.get(url)
    if resp.status_code == 200:
        img_data = np.frombuffer(resp.content, dtype=np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        return True, img


# tcp part
client_socket: socket


def start_socket():
    c = 0
    global client_socket
    while (c < 10):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (deneyap_ip, 65000)
        try:
            client_socket.connect(server_address)
            return
        except Exception as e:
            c += 1
            print(e)


def send_data(msg: str):
    msg = msg + '\n'
    client_socket.sendall(msg.encode())