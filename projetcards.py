import os
from flask import Flask, request
from flask import render_template
from werkzeug.utils import secure_filename

# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Flask utilise la valeur de __name__ pour savoir où est le fichier principal
app = Flask(__name__)

IMG_FOLDER = os.path.join("static", "uploaded_images")
app.config["UPLOAD_FOLDER"] = IMG_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Lors d’une requête sur la route ‘/’ flask doit renvoyer la page index.html
@app.route("/")                             # défini des routes (@app.route(...))
def index():
    return render_template('index.html')

@app.route("/galerie")
def galerie():
    image_list = os.listdir("static/uploaded_images")
    image_list = ["uploaded_images/" + image for image in image_list]
    return render_template('galerie.html', liste_images=image_list)

def allowed_file(filename):
    return filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new_personnage', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('new_personnage.html')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('new_personnage.html')
        elif allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('new_personnage.html')
    return render_template('new_personnage.html')

# Lancement du serveur : mode debug et hot reload actif
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)      # démarre le serveur

# if __name__ == '__main__':
#     app.run(debug = True)


