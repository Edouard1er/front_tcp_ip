import socket
import os
from Service import Service
import Codage
import pickle

# Créer un socket pour la communication avec les clients
serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Définir le port d'écoute et le nombre maximum de connexions en attente
HOST = '127.0.0.1'
PORT = 8000
MAX_CONN = 5

# Associer le socket au port et commencer à écouter les connexions entrantes
serveur_socket.bind((HOST, PORT))
serveur_socket.listen(MAX_CONN)

print(f"Serveur en attente de connexion sur {HOST}:{PORT}...")

while True:
    # Attendre une nouvelle connexion
    client_socket, addr = serveur_socket.accept()

    print(f"Connexion établie avec {addr[0]}:{addr[1]}")

    # Récupérer la liste des fichiers disponibles dans le répertoire courant
    fichier_dir = os.listdir('.')
    fichiers = [f for f in fichier_dir if os.path.isfile(f)]

    # Convertir la liste des fichiers en une chaîne de caractères séparée par des virgules
    fichier_str = ','.join(fichiers)

    # Envoyer la liste des fichiers au client
    client_socket.send(fichier_str.encode())
    
    # Récupérer la liste des fichiers disponibles depuis le serveur
    fichier_str = client_socket.recv(1024).decode()
    
    codageHuffman = Codage.HuffmanCode(fichier_str)
    compress = Codage.compressFile(codageHuffman.get_huffman_dict(), fichier_str)
    
    
    # Envoyer compression au client
    client_socket.send(compress.encode())
    
    codeTable = pickle.dumps(codageHuffman.get_huffman_list())
    # Envoyer codeTable au client
    client_socket.send(codeTable)
    

    # Fermer la connexion avec le client
    client_socket.close()
