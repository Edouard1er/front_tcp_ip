import socket
import threading
import os
from Service import Service


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()
        while True:
            client_socket, address = self.server.accept()
            print(f"Connection depuis l'adresse {address[0]}:{address[1]}  a été établie !")
            service = Service(client_socket)
            service.handle_client()


if __name__ == '__main__':
    server = Server("localhost", 6666)
    server.start()
