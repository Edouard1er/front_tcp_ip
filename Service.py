import os
import Codage
import pickle

from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

directory_file = os.getenv('FILE_DIRECTORY')


class Service:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.reader = client_socket.makefile('r')
        self.writer = client_socket.makefile('w')

    def handle_client(self):
        files = os.listdir(directory_file)
        self.writer.write('Liste des fichiers disponibles:\n')
        for file in files:
            self.writer.write(f'- {file}\n')
        self.writer.flush()

        filename = self.client_socket.recv(1024).decode("utf8")

        if filename in files:
            huffman_code = Codage.HuffmanCode(filename)
            compress = Codage.compressFile(huffman_code.get_huffman_dict(), filename)

            data = pickle.dumps(huffman_code.get_huffman_list())
            self.client_socket.send(data)
            self.writer.write(f'{compress}')
            self.client_socket.send(compress.encode("utf8"))
        else:
            self.writer.write(f'Le fichier {filename} n\'existe pas\n')

        self.reader.close()
        self.writer.close()
        self.client_socket.close()
