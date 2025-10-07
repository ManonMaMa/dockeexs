import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import imagehash
import requests
import json

OPENROUTER_KEY = "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"


# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# création de l'application Flask (on indique que ce fichier est le fichier principal)
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier

# gestion des fichiers uploadés (images envoyées par un formulaire)
IMG_FOLDER = '/app/static/uploaded_images'                  # écriture d'un chemin lisible par tous (windows, linux, mac)
app.config["UPLOAD_FOLDER"] = IMG_FOLDER                    # indique à Flask le chemin pour faire les sauvegardes
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)



# Exemple de modèle
class Pokemon(db.Model):
    __tablename__ = 'pokemons'
    id = db.Column(db.Integer, primary_key=True)
    image_pokemon = db.Column(db.String(80), unique=True, nullable=False)
    hash_image = db.Column(db.String(1000), unique=True, nullable=False)
    nom_pokemon = db.Column(db.String(40), nullable=False)
    description_pokemon = db.Column(db.String(400), nullable=False)

# protection : liste d’extensions de fichiers autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Définition de la route principale : http://127.0.0.1:5000/
@app.route("/")                             
def index():
    return render_template('index.html')        # fonction de Flask qui va chercher index.html dans le dossier templates/

# Définition d'une route : http://127.0.0.1:5000/galerie
@app.route("/galerie")
def galerie():
    # image_list = os.listdir(IMG_FOLDER)                                     # liste tous les fichiers et sous-dossiers présents dans uploaded_images
    # image_list = ["uploaded_images/" + image for image in image_list]       # dans la liste ajoute devant chaque fichier : "uploaded_images/"
    # return render_template('galerie.html', liste_images=image_list)
    try:
        # Récupérer tous les utilisateurs dans la table Pokemon et les renvoyer dans une liste
        pokemons = Pokemon.query.all()
        return render_template('galerie.html', liste_pokemons = pokemons)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Gestion des erreurs

# vérifier que le nom du fichier à une extension qui se trouve dans ALLOWED_EXTENSIONS
def allowed_file(filename):
    # divise le nom du fichier en liste en séparant par le caractère "point"
    # [1] : prend la deuxième partie
    # transforme l’extension en minuscules
    # return true si l'extension se trouve dans ALLOWED_EXTENSIONS, false sinon
    return filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

# Définition d'une route : http://127.0.0.1:5000/new_personnage
@app.route('/new_personnage', methods=['GET', 'POST'])
def upload_file():
    # vérifier que l'on récupère les données d'un formulaire
    if request.method == 'POST':
        # si request.files est vide car 'file' n'a pas été transmis du tout
        if 'file' not in request.files:
            return render_template('index.html')
        file = request.files['file']        # variable file qui récupère le fichier 'file' envoyé par l'utilisateur
        # si le nom du fichier est vide 
        if file.filename == '':
            return render_template('index.html')
        # si l'extension est correcte
        elif allowed_file(file.filename):
            filename = secure_filename(file.filename)                           # nettoie le nom du fichier pour enlever les caractères dangereux ou les espaces.
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)      # indique quel chemin prendre jusqu'au fichier filename

            file.save(filepath)                 # sauvegarde le fichier à l'endroit indiqué
            img = Image.open(filepath)

            hash_image_test = str(imagehash.average_hash(img))

            hash_pokemon = db.session.execute(db.select(Pokemon).filter_by(hash_image=hash_image_test)).scalar_one_or_none()

            if hash_pokemon is None:
                add_pokemon(filename, hash_image_test, 'pokemon', 'ceci est un pokemon')
            return render_template('new_personnage.html')
    # s'il ne s'agit pas d'un fichier, redémarrer la page
    return render_template('new_personnage.html')

def add_pokemon(image_pokemon, hash_image_test, nom_pokemon, description_pokemon):
    new_pokemon = Pokemon(image_pokemon= 'uploaded_images/' + image_pokemon, hash_image=hash_image_test, nom_pokemon=nom_pokemon, description_pokemon=description_pokemon)
    db.session.add(new_pokemon)
    db.session.commit()

def get_image_description(image):
    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",

      headers={
        "Authorization": f"Bearer {OPENROUTER_KEY}"
      },

      data=json.dumps({
        "model": "meta-llama/llama-4-scout:free", # Optional
        "messages": [
          {
            "role": "user",
            "content": "Hello?"
          }
        ]
      })
    )

    response = response.json()
    description = response["choices"][0]["message"]["content"]
    return description


# Lancement du serveur : mode debug et hot reload actif
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

