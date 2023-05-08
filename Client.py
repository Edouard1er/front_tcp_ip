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

    def communicate(self):
        try:
            
            ready = select.select([self.client_socket], [], [], 1)
            if ready[0]:
                files_list = self.client_socket.recv(1024).decode()
                print(files_list)

                chosen_file = "test.txt"
                self.client_socket.send(chosen_file.encode())
                while True:
                    code_table = self.client_socket.recv(1024)
                    obj = pickle.loads(code_table)
                    print("Test 1")
                    compressed_data = self.client_socket.recv(1024).decode()
                    print("Test 3",compressed_data)
                    d_compress_file = Codage.decompressData(compressed_data, obj[0])
                    
                    file = open("newFile.txt", "w")

                    file.write(d_compress_file)

                    file.close()
        except Exception as e:
            print(f"Error occurred during communication with the server: {str(e)}")
            self.client_socket.close()


