# syntax=docker/dockerfile:1
# La ligne ci-dessus n'est pas un commentaire ordinaire,
# Elle doit être placée en premier.
# Elle est lue par Docker pour choisir la version du langage.

# Indique à Docker d'utiliser l'image de base Python.
FROM python:3.12

# Création du dossier de travail au sein du container.
WORKDIR /python-docker

# Copie le contenu du fichier requirements.txt dans le fichier requirements.txt de l'image du conteneur.
COPY requirements.txt requirements.txt
# Les bibliothèques Python, qui se trouvent dans requirements.txt, sont installées dans l’image finale.
RUN pip3 install -r requirements.txt
RUN pip django-bootstrap5

# Copie de notre répertoire locale vers le répertoire de l'image Docker.
# COPY . .  # La copie a été déplacée dans le fichier docker-compose.

# CMD : commande par défaut au démarrage du container.
# Appelle l'interpréteur Python 3 et exécute le fichier projetcards qui se trouve dans l'image.
CMD ["python3", "/app/projetcards.py"]