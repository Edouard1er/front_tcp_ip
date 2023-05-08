import socket
import pickle
import Codage
import os
from flask import Flask, render_template, request, json, abort, send_from_directory


from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

compress_directory = os.getenv('COMPRESS_DIRECTORY')
ready_directory = os.getenv('READY_DIRECTORY')
# Créer un socket pour la communication avec le serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def compressClient(selection):

    # Définir l'adresse IP et le port d'écoute du serveur
    HOST = '127.0.0.1'
    PORT = 8000

    # Se connecter au serveur
    client_socket.connect((HOST, PORT))

    # Récupérer la liste des fichiers disponibles depuis le serveur
    fichier_str = client_socket.recv(1024).decode()
    
    # Envoyer la sélection au serveur
    client_socket.send(selection.encode())
    # Récupérer la liste des fichiers disponibles depuis le serveur
    compressFile = client_socket.recv(1024).decode()
    
    # Ouvrir le fichier en mode écriture
    filename_compress = selection.split(".")
    fichier = open(compress_directory + "/" + filename_compress[0] + "_compress." + filename_compress[1], "w")
    # Écrire le texte dans le fichier
    fichier.write(compressFile)
    # Fermer le fichier
    fichier.close()


    print("CLient compress file", compressFile)


def decompressClient(filename):
    filename_compress = filename.split(".")
    compressFile = filename_compress[0] + "_compress." + filename_compress[1]
    # Ouvrir le fichier en mode lecture
    fichier = open(compress_directory + "/" + compressFile, "r")

    # Lire le contenu du fichier avec la méthode read()
    contenu = fichier.read()

    # Fermer le fichier
    fichier.close()

    print(contenu)

    #recuperer codeTable
    codeTable = pickle.loads(client_socket.recv(1024))

    print("codeTable Client", codeTable)

    #Decompress data
    decompressedFile = Codage.decompressData(contenu, codeTable[0])
    
    fichierReady = open(ready_directory + "/" + filename, "w")
    # Écrire le texte dans le fichier
    fichierReady.write(decompressedFile)
    # Fermer le fichier
    fichierReady.close()
    
    print("decompressedFile Client", decompressedFile)
    client_socket.close()
    
    return send_from_directory(ready_directory, filename, as_attachment=True)

    
def closeConnection():
    # Fermer la connexion avec le serveur
    client_socket.close()
    