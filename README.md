# Mini projet Docker : générer des biographies de personnages inspirées d’images de référence grâce à des LLMs.

## Description
Ce projet prendra la forme de deux containers interagissant ensemble pour former une seule et même application. Pour ce faire, nous utiliserons docker compose un outil de composition des conteneurs simple d’utilisation.

## Sommaire
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Licence](#licence)

------------------- Création de l'application Flask ------------------------


## Installation
1. sur le terminal, se placer dans le dossier du projet

 ''' Terminal
    py -3 -m venv .venv                # environnement virtuel
    .venv\Scripts\activate             # activation de l'environnement
    python -m pip install Flask        # installation de Flask

2) création du fichier principal projetcards.py

    utilisation de la fonction app.route()

    http://127.0.0.1:5000/

    http://127.0.0.1:5000/galerie

    http://127.0.0.1:5000/new_personnage

    utilisation de la fonction render_templates()

3) fichier index.html

    utilisation de la fonction url_for(), avec l'affichage d'images sans utiliser de variable :

        - un lien qui redirige vers la route Flask nommée /galerie ("img/galerie.jpg")

        - un lien qui redirige vers la route Flask nommée /new_personnage (img/ajoutcards.jpg)
    
4) création de deux pages : galerie.html et new_personnage.html

    galerie : bouton de retour à la page d'accueil
                
              affiche toutes les images se trouvant dans le dossier uploaded_images

    new_personnage : bouton de retour à la page d'accueil

                     formulaire pour récupérer un fichier auprès de l'utilisateur

------------------- conteneurisation de l'application Flask  ------------------------



docker build -t projectcard .

docker run -v C:\Users\Utilisateur\Bureau\code\dockeexs:/python-docker -p 5000:5000 projectcard