from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new_personnage")
def new_personnage():
    return render_template('new_personnage.html')

@app.route("/galerie")
def galerie():
    return render_template('galerie.html')

if __name__ == '__main__':
    app.run(debug = True)

