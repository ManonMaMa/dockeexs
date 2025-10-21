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
from dotenv import load_dotenv

load_dotenv()   # Ajoute les variables du fichier .env aux à l'environnement (les variables d'environnement sont accessibles par os.getenv('VARIABLE')).

# Lors du développement d'une app Flask, mettre :
#       les fichiers HTML dans un dossier templates/
#       les fichiers CSS, JS, images dans un dossier static/

# Création de l'application Flask (on indique que ce fichier est le fichier principal).
app = Flask(__name__)       # __name__ : variable spéciale de python contenant le nom de ce fichier.

# Gestion des fichiers uploadés (images envoyées par un formulaire).
app.config["UPLOAD_FOLDER"] = config.IMG_FOLDER                    # Indique à Flask le chemin pour faire les sauvegardes.
# lis dans les variables d’environnement de docker-compose.yml la valeur DATABASE_URL et l'utilise comme adresse de connexion pour SQLAlchemy dans l'application Flask
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
database = SQLAlchemy(app)


@app.route("/")     # Définition de la route principale : http://127.0.0.1:5050/
def index():
    """Retourne le fichier index.html du dossier templates/ grâce à la fonction render_template() de Flask."""
    return render_template('index.html')


@app.route("/galerie")      # Définition d'une route : http://127.0.0.1:5050/galerie
def display_galerie():
    """Retourne une page qui affiche tous les pokémons présents dans la BDD."""
    try:
        # Récupère toutes les lignes de la table "pokemons" et les transforme en une liste d'objets Pokemon.
        pokemons = Pokemon.query.all()
        is_not_empty = len(pokemons) > 0

        return render_template('galerie.html', liste_pokemons = pokemons, is_not_empty=is_not_empty)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Gestion des erreurs.


@app.route('/new_personnage', methods=['GET', 'POST'])  # Définition d'une route : http://127.0.0.1:5050/new_personnage
def upload_file():
    """Affiche une page qui permet à l'utilisateur de créer de nouveaux pokémons (et gère l'enregistrement)."""
    # Regarde si on récupère les données d'un formulaire. Si oui, enregistre le pokémon.
    if request.method == 'POST':
        # Si request.files ne contient pas de fichier (aucun fichier n'a été transmis), ne fait rien et recharge la page.
        if 'file' not in request.files:
            return render_template('new_personnage.html')

        file = request.files['file']    # Variable file qui récupère le fichier 'file' envoyé par l'utilisateur.
        # Si le nom du fichier est vide, ne fait rien et recharge la page.
        if file.filename == '':
            return render_template('new_personnage.html')

        # Si l'extension est correcte, traite l'image ; sinon, ne fait rien et recharge la page.
        elif is_file_allowed(file.filename):
            turn_file_to_pokemon(file)
            return render_template('index.html')

    return render_template('new_personnage.html')


# Définition de la classe Pokemon, qui est utilisée pour créer la table "pokemons" dans la BDD.
class Pokemon(database.Model):
    __tablename__ = 'pokemons'
    id = database.Column(database.Integer, primary_key=True)
    image_pokemon = database.Column(database.String(80), unique=True, nullable=False)
    hash_image = database.Column(database.String(1000), unique=True, nullable=False)
    nom_pokemon = database.Column(database.String(2000), nullable=False)
    description_pokemon = database.Column(database.String(2000), nullable=False)


# Vérifie que le nom du fichier donné à une extension qui se trouve dans ALLOWED_EXTENSIONS.
def is_file_allowed(filename):
    # split('.') : divise le nom du fichier en liste en séparant par le caractère "point".
    # [-1] : prend la dernière entrée de la liste.
    # lower() : transforme cette entrée (l’extension) en minuscules.
    # in : devient True si l'extension se trouve dans ALLOWED_EXTENSIONS, False sinon.
    return filename.split('.')[-1].lower() in config.ALLOWED_EXTENSIONS


def turn_file_to_pokemon(file):
    """
    Prend un fichier d'image en paramètre.

    Enregistre le fichier, crée une description par IA, et enregistre la description et l'image associées dans la BDD.
    """
    filedata = save_file(file)
    save_pokemon(filedata)


def save_file(file):
    """Enregistre le fichier donné dans le dossier d'images."""
    filename = secure_filename(file.filename)                           # Nettoie le nom du fichier pour enlever les caractères dangereux ou les espaces.
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)      # Indique quel chemin prendre jusqu'au fichier filename.

    file.save(filepath)                 # Sauvegarde le fichier à l'endroit indiqué.
    return filepath, filename


def save_pokemon(filedata):
    """
    Prends un tuple en paramètre. Le tuple doit contenir un chemin de fichier d'image, et le nom du fichier.

    Si l'image n'est pas déjà dans la base de données, crée un nom de pokémon et une description, puis enregistre le tout dans la BDD.
    """
    filepath, filename = filedata

    img = Image.open(filepath)
    hash_image = str(imagehash.average_hash(img))
    database_image = database.session.execute(database.select(Pokemon).filter_by(hash_image=hash_image)).scalar_one_or_none()

    # Si l'image n'est pas déjà dans la BDD, une nouvelle ligne peut être ajoutée.
    if database_image is None:
        infos_pokemon = get_image_description(filepath)
        add_pokemon_to_database(filename, hash_image, infos_pokemon["nom"], infos_pokemon["description"])


def add_pokemon_to_database(image_pokemon, hash_image_test, nom_pokemon, description_pokemon):
    new_pokemon = Pokemon(image_pokemon= 'uploaded_images/' + image_pokemon, hash_image=hash_image_test, nom_pokemon=nom_pokemon, description_pokemon=description_pokemon)
    database.session.add(new_pokemon)
    database.session.commit()


def get_image_description(image_path):
    """Demande à une IA de créer un nom de pokémon et une description pour ce pokémon à partir de l'image donnée en paramètre."""
    # Lit et encode l'image.
    base64_image = encode_image_to_base64(image_path)
    image_type = "png"
    if image_path.endswith(".jpg"):
        image_type = "jpeg"
    elif image_path.endswith(".png"):
        image_type = "png"

    data_url = f"data:image/{image_type};base64,{base64_image}"

    # Demande à l'IA de créer un nom pour le pokémon à partir de son image.
    name_prompt = "Voici l'image d'un nouveau pokémon. En partant de l'image, crée un nom pour ce pokémon et renvoie-moi UNIQUEMENT ce nom."
    name = get_ai_response(data_url, name_prompt)

    # Demande à l'IA de créer une description pour le pokémon à partir de son image et son nom.
    description_prompt = f"Voici l'image d'un nouveau pokémon qui s'appelle {name}. Crée une description de 200 à 300 caractères pour ce pokémon et renvoie-moi UNIQUEMENT cette description."
    description = get_ai_response(data_url, description_prompt)

    return {"nom": name, "description": description}


def get_ai_response(image_url, prompt):
    """
    Prend l'URL d'une image et un prompt en paramètre.

    Envoie l'image et le prompt à une IA et retourne la réponse de l'IA.
    """
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {os.environ.get("CLE_API")}"  # os.environ.get() est interchangeable avec os.getenv()
        },

        data=json.dumps({
            "model": "meta-llama/llama-4-scout:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
        })
    )

    response = response.json()
    return response["choices"][0]["message"]["content"]


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Lancement du serveur : mode debug et hot reload actif.
if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

