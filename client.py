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


def compressClient(selection):

    # Définir l'adresse IP et le port d'écoute du serveur
    HOST = '127.0.0.1'
    PORT = 8000
    # Créer un socket pour la communication avec le serveur
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se connecter au serveur
    client_socket.connect((HOST, PORT))

    # Récupérer la liste des fichiers disponibles depuis le serveur
    fichier_str = client_socket.recv(1024).decode()
    
    # Envoyer la sélection au serveur
    client_socket.send(selection.encode())
    # Récupérer la liste des fichiers disponibles depuis le serveur
    compressFile = client_socket.recv(1024).decode()
    
    #recuperer codeTable
    codeTable = pickle.loads(client_socket.recv(1024))

    print("codeTable Client", codeTable)

    #Decompress data
    decompressedFile = Codage.decompressData(compressFile, codeTable[0])


    print("CLient compress file", decompressedFile)
    client_socket.close()
    
    fichierReady = open(ready_directory + "/" + selection, "w")
    # Écrire le texte dans le fichier
    fichierReady.write(decompressedFile)
    # Fermer le fichier
    fichierReady.close()
    
    print("decompressedFile Client", decompressedFile)
    client_socket.close()
    
    return send_from_directory(ready_directory, selection, as_attachment=True)


# def decompressClient(filename):
    
    
    
    return send_from_directory(ready_directory, filename, as_attachment=True)

    

    