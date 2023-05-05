import os
import mimetypes

from datetime import datetime

def get_file_list():
    file_list = []
    for file_name in os.listdir('static/files'):
        file_path = os.path.join('static/files', file_name)
        if os.path.isfile(file_path):
            # Récupérer les informations sur le fichier
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            file_type = mimetypes.guess_type(file_path)[0]
            file_type = file_type.split('/')[0] if file_type else 'autre'
            file_date = datetime.fromtimestamp(file_stat.st_mtime)
            file_date_str = file_date.strftime('%d/%m/%Y %H:%M:%S')
            
            # Ajouter les informations à la liste de fichiers
            file_list.append({
                'name': file_name,
                'date': file_date_str,
                'type': file_type,
                'size': getRightFileSize(file_size)
            })
    return file_list

def getRightFileSize(file_size):
    response = "0 Byte"
    if(file_size):
        if(file_size < 1024):
            response = str(round(file_size, 2)) + " B"
        elif file_size < 1024*1024:
            response = str(round(file_size / 1024, 2)) + " KB"
        elif file_size < 1024*1024*1024:
            response = str(round(file_size / 1024 / 1024, 2)) + " MB"
        else:
            response = str(round(file_size / 1024 / 1024 / 1024 / 1024, 2)) + " GB"
        
    return response