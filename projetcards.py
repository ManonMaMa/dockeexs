from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

IMG_FOLDER = os.path.join("static")
app.config["UPLOAD_FOLDER"] = IMG_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new_personnage")
def new_personnage():
    return render_template('new_personnage.html')

@app.route("/galerie")
def galerie():
    test_list = os.listdir("static")
    test_list = ["/" + image for image in test_list]
    return render_template('galerie.html', list_test=test_list)

if __name__ == '__main__':
    app.run(debug = True)

