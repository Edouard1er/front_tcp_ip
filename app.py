from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from controllers import files

app = Flask(__name__)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    projectName = "Projet TCP-IP"
    fileList = files.getFiles()
    return render_template('home.html', projectName=projectName)

if __name__ == '__main__':
    app.run(debug=True)
