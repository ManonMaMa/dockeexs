# Mini projet Docker : générer des biographies de personnages inspirées d’images de référence grâce à des LLMs.

## Description
Ce projet prendra la forme de deux containers interagissant ensemble pour former une seule et même application. Pour ce faire, nous utiliserons docker compose un outil de composition des conteneurs simple d’utilisation.

## Sommaire
- [Installation](#installation)
- [création du fichier principal projetcards](#création-du-fichier-principal-projetcards)
- [fichier index](#fichier-index)
- [création de deux pages](#création-de-deux-pages)

------------------- Création de l'application Flask ------------------------


## Installation
1. sur le terminal, se placer dans le dossier du projet  
&emsp;&emsp;py -3 -m venv .venv&emsp;&emsp;# environnement virtuel  
&emsp;&emsp;.venv\Scripts\activate&emsp;# activation de l'environnement  
&emsp;&emsp;python -m pip install Flask &emsp;# installation de Flask  

## création du fichier principal projetcards
&emsp;utilisation de la fonction app.route()  
&emsp;&emsp;http://127.0.0.1:5000/  
&emsp;&emsp;http://127.0.0.1:5000/galerie  
&emsp;&emsp;http://127.0.0.1:5000/new_personnage

&emsp;utilisation de la fonction render_templates()

## fichier index
&emsp;utilisation de la fonction url_for(), avec l'affichage d'images sans utiliser de variable :  
&emsp;&emsp;- un lien qui redirige vers la route Flask nommée /galerie ("img/galerie.jpg")  
&emsp;&emsp;- un lien qui redirige vers la route Flask nommée /new_personnage (img/ajoutcards.jpg)
    
## création de deux pages
&emsp;galerie :  
&emsp;&emsp;bouton de retour à la page d'accueil  
&emsp;&emsp;affiche toutes les images se trouvant dans le dossier uploaded_images

&emsp;new_personnage :  
&emsp;&emsp;bouton de retour à la page d'accueil  
&emsp;&emsp;formulaire pour récupérer un fichier auprès de l'utilisateur


------------------- conteneurisation de l'application Flask  ------------------------



docker build -t projectcard .

docker run -v C:\Users\Utilisateur\Bureau\code\dockeexs:/python-docker -p 5000:5000 projectcard