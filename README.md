Mini projet Docker : générer des biographies de personnages inspirées d’images de référence grâce à des LLMs.

Ce projet prendra la forme de deux containers interagissant ensemble pour former une seule et même application.  Pour ce faire nous utiliserons docker compose un outil de composition des conteneurs simple d’utilisation.

------------------- Création de l'application Flask ------------------------
1) installation de l'environnement :
    se placer dans le dossier du projet
    >py -3 -m venv .venv                # environnement virtuel
    >.venv\Scripts\activate             # activation de l'environnement
    >python -m pip install Flask        # installation de Flask

2) création du fichier principal projetcards.py
    http://127.0.0.1:5000/              # app.route("/")




docker build -t projectcard .

docker run -v C:\Users\Utilisateur\Bureau\code\dockeexs:/python-docker -p 5000:5000 projectcard