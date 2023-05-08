from flask import Flask, render_template, request, json, abort, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from Client import Client

from controllers import files

app = Flask(__name__)

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET'])
def home():
    projectName = "Projet TCP-IP"
    fileList = files.get_file_list()
    client = Client('localhost', 6666)
    isConnected = client.connect()

    if isConnected:
        client.communicate()
    else:
        print("Error occurred during connection")
    return render_template('home.html', projectName=projectName, fileList=fileList)

@app.route('/process_files', methods=['POST'])
def process_files():
    response = {
        "code": 200,
        "data":[],
        "message": "OK"
    }
    if not request.json:
            abort(400)
    try:
        _json = request.json
        fileList = _json["file-list"]
        #Traitement
        
        response["data"] = fileList
        return json.dumps(response), 200
    except Exception as e:
            response["code"]="500"
            response["message"]="Error processing"
            return json.dumps(response), 500
    


@app.route('/download_file/<path:filename>')
def download_file(filename):
    file_path = 'static/files'
    return  send_from_directory(file_path, filename, as_attachment=True)

@app.route('/terminer', methods=['POST'])
def terminer():
    response = {
        "code": 200,
        "data":[],
        "message": "OK"
    }
    if not request.json:
            abort(400)
    try:
        _json = request.json
        fileList = _json["file-list"]
        #Traitement
        
        return json.dumps(response), 200
    except Exception as e:
            response["code"]="500"
            response["message"]="Error processing"
            return json.dumps(response), 500
        
if __name__ == '__main__':
    app.run(debug=True)
