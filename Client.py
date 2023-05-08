import pickle
import socket
import Codage
import select


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connecté au serveur:", self.host, "sur le port:", self.port)
            return True
        except:
            print("Connection échoué.")
            return False

    def communicate(self, chosen_file):
        try:
            files_list = self.client_socket.recv(1024).decode()
            print(chosen_file)

            self.client_socket.send(chosen_file.encode())
            while True:
                code_table = self.client_socket.recv(1024)
                obj = pickle.loads(code_table)
                print("Test 1")
                compressed_data = self.client_socket.recv(1024).decode()
                print("Test 3", compressed_data)
                d_compress_file = Codage.decompressData(compressed_data, obj[0])

                file = open("newFile.txt", "w")

                file.write(d_compress_file)

                file.close()
        except Exception as e:
            print(f"Error occurred during communication with the server: {str(e)}")
            self.client_socket.close()
