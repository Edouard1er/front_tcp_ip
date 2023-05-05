from flask import Flask, render_template
from controllers import files

app = Flask(__name__)

@app.route('/')
def home():
    projectName = "Projet TCP-IP"
    fileList = files.getFiles()
    return render_template('home.html', projectName=projectName)
