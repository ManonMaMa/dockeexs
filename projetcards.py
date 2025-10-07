import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import imagehash
import requests
import json
import base64
import config


# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Création de l'application Flask (on indique que ce fichier est le fichier principal).
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier.

# Gestion des fichiers uploadés (images envoyées par un formulaire).
app.config["UPLOAD_FOLDER"] = config.IMG_FOLDER                    # Indique à Flask le chemin pour faire les sauvegardes.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
database = SQLAlchemy(app)


# Définition de la route principale : http://127.0.0.1:5050/
@app.route("/")                             
def index():
    return render_template('index.html')        # fonction de Flask qui va chercher index.html dans le dossier templates/


# Définition d'une route : http://127.0.0.1:5050/galerie
@app.route("/galerie")
def display_galerie():
    try:
        # Récupérer tous les utilisateurs dans la table Pokemon et les renvoyer dans une liste.
        pokemons = Pokemon.query.all()
        is_not_empty = len(pokemons) > 0

        return render_template('galerie.html', liste_pokemons = pokemons, is_not_empty=is_not_empty)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Gestion des erreurs.


# Définition d'une route : http://127.0.0.1:5050/new_personnage
@app.route('/new_personnage', methods=['GET', 'POST'])
def upload_file():
    # Vérifier que l'on récupère les données d'un formulaire.
    if request.method == 'POST':
        # Si request.files ne contient pas de fichier (aucun fichier n'a été transmis), ne fait rien et recharge la page.
        if 'file' not in request.files:
            return render_template('new_personnage.html')

        file = request.files['file']        # Variable file qui récupère le fichier 'file' envoyé par l'utilisateur.
        # Si le nom du fichier est vide, ne fait rien et recharge la page.
        if file.filename == '':
            return render_template('new_personnage.html')

        # Si l'extension est correcte, traite l'image; sinon, ne fait rien et recharge la page.
        elif is_file_allowed(file.filename):
            save_file(file)
            return render_template('new_personnage.html')

    return render_template('new_personnage.html')


# Exemple de modèle.
class Pokemon(database.Model):
    __tablename__ = 'pokemons'
    id = database.Column(database.Integer, primary_key=True)
    image_pokemon = database.Column(database.String(80), unique=True, nullable=False)
    hash_image = database.Column(database.String(1000), unique=True, nullable=False)
    nom_pokemon = database.Column(database.String(40), nullable=False)
    description_pokemon = database.Column(database.String(400), nullable=False)


# Vérifier que le nom du fichier à une extension qui se trouve dans ALLOWED_EXTENSIONS.
def is_file_allowed(filename):
    # Divise le nom du fichier en liste en séparant par le caractère "point".
    # [1] : prend la deuxième partie.
    # Transforme l’extension en minuscules.
    # Return true si l'extension se trouve dans ALLOWED_EXTENSIONS, false sinon.
    return filename.split('.')[1].lower() in config.ALLOWED_EXTENSIONS


def save_file(file):
    """Enregistre le fichier donné dans le dossier d'images, puis crée un nom et une description pour l'image si elle n'est pas déjà dans la base de données."""
    filename = secure_filename(file.filename)                           # Nettoie le nom du fichier pour enlever les caractères dangereux ou les espaces.
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)      # Indique quel chemin prendre jusqu'au fichier filename.

    file.save(filepath)                 # Sauvegarde le fichier à l'endroit indiqué.

    img = Image.open(filepath)
    hash_image = str(imagehash.average_hash(img))
    hash_pokemon = database.session.execute(database.select(Pokemon).filter_by(hash_image=hash_image)).scalar_one_or_none()

    if hash_pokemon is None:
        infos_pokemon = get_image_description(filepath)
        add_pokemon(filename, hash_image, infos_pokemon["nom"], infos_pokemon["description"])


def add_pokemon(image_pokemon, hash_image_test, nom_pokemon, description_pokemon):
    new_pokemon = Pokemon(image_pokemon= 'uploaded_images/' + image_pokemon, hash_image=hash_image_test, nom_pokemon=nom_pokemon, description_pokemon=description_pokemon)
    database.session.add(new_pokemon)
    database.session.commit()


def get_image_description(image_path):
    # Lit et encode l'image.
    base64_image = encode_image_to_base64(image_path)
    image_type = "png"
    if image_path.endswith(".jpg"):
        image_type = "jpeg"
    elif image_path.endswith(".png"):
        image_type = "png"

    data_url = f"data:image/{image_type};base64,{base64_image}"

    response = requests.post(
      url="https://openrouter.ai/api/v1/chat/completions",

      headers={
        "Authorization": f"Bearer {config.OPENROUTER_KEY_2}"
      },

      data=json.dumps({
        "model": "meta-llama/llama-4-scout:free",
        "messages": [
          {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Voici l'image d'un nouveau pokémon. En partant de l'image, crée un nom pour ce pokémon et renvoie-moi UNIQUEMENT ce nom."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
            ]
          }
        ]
      })
    )

    app.logger.info(f"response nom -------> {response}")
    response = response.json()
    app.logger.info(f"response nom -------> {response}")
    nom = response["choices"][0]["message"]["content"]

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {config.OPENROUTER_KEY_2}"
        },

        data=json.dumps({
            "model": "meta-llama/llama-4-scout:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Voici l'image d'un nouveau pokémon qui s'appelle {nom}. Crée une description de 200 à 300 caractères pour ce pokémon et renvoie-moi UNIQUEMENT cette description."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ]
        })
    )

    response = response.json()
    description = response["choices"][0]["message"]["content"]
    return {"nom": nom, "description": description}


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

