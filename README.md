# Mini projet Docker : générer des biographies de personnages inspirées d’images de référence grâce à des LLMs.

## Description
Ce projet prendra la forme de deux containers interagissant ensemble pour former une seule et même application. Pour ce faire, nous utiliserons docker compose un outil de composition des conteneurs simple d’utilisation.

## Sommaire
---------- Création de l'application Flask --------------
- [Installation](#installation)
- [Création du fichier principal projetcards](#creation-du-fichier-principal-projetcards)
- [Création du fichier index](#creation-du-fichier-index)
- [Création de deux pages](#creation-de-deux-pages)

---------- Conteneurisation de l'application Flask  -----
- [Création de fichiers](#creation-de-fichiers)
- [Construction de l'image initiale](#construction-de-l-image-initiale)
- [Mapping de volume](#mapping-de-volume)
- [Installation de l'image sur Docker Hub](#installation-de-l-image-sur-Docker-Hub)

---------- docker compose  ------------------------------
- [Création d'un second container](#création-d-un-secondcontainer)
- [Ollama](#ollama)


------------------- Création de l'application Flask ------------------------

## Installation
1. sur le terminal, se placer dans le dossier du projet  
&emsp;&emsp;py -3 -m venv .venv&emsp;&emsp;# environnement virtuel  
&emsp;&emsp;.venv\Scripts\activate&emsp;# activation de l'environnement  
&emsp;&emsp;python -m pip install Flask &emsp;# installation de Flask  

## Création du fichier principal projetcards
&emsp;utilisation de la fonction app.route()  
&emsp;&emsp;http://127.0.0.1:5000/  
&emsp;&emsp;http://127.0.0.1:5000/galerie  
&emsp;&emsp;http://127.0.0.1:5000/new_personnage

&emsp;utilisation de la fonction render_templates()

## Création du fichier index
&emsp;Utilisation de la fonction url_for(), avec l'affichage d'images sans utiliser de variable :  
&emsp;&emsp;- Un lien qui redirige vers la route Flask nommée /galerie ("img/galerie.jpg").  
&emsp;&emsp;- Un lien qui redirige vers la route Flask nommée /new_personnage (img/ajoutcards.jpg).
    
## Création de deux pages
&emsp;galerie :  
&emsp;&emsp;Bouton de retour à la page d'accueil.  
&emsp;&emsp;Affiche toutes les images se trouvant dans le dossier uploaded_images.

&emsp;new_personnage :  
&emsp;&emsp;Bouton de retour à la page d'accueil.  
&emsp;&emsp;Formulaire pour récupérer un fichier auprès de l'utilisateur.


------------------- Conteneurisation de l'application Flask  ------------------------

## Création de fichiers   
&emsp;requirements.txt : fichier des dépendances  
&emsp;Dockerfile : fichier pour la construction de l'image  

## Construction de l'image initiale  
&emsp;Ouvrir Docker Desktop  
```Bash 
docker build -t projetcards .  
docker images  
```  

## Mapping de volume
&emsp;Lancement du container en utilisant mapping de volume (-v) :
```Bash 
docker run -v cheminAbsoluJusqua/dockeexs:/python-docker -p 5000:5000 projetcards 
```  

## Installation de l'image sur Docker Hub
```Bash 
docker login
docker tag projetcards monpseudo/projetcards:latest
docker images
docker push monpseudo/projetcards:latest
docker pull monpseudo/projetcards:latest
```  

------------------- docker compose  ------------------------

## Création d'un second container  
&emsp;Création d'un fichier docker-compose.yml   
&emsp;Création d'une connexion avec le conteneur PostgreSQL  
&emsp;Création de la base de données "pokemons"  
&emsp;Conservation des données de la base (création d'un Volume)  
&emsp;Stockage du hash des images  

## Ollama
&emsp;

------------------- accès sur le web  ------------------------
### acccès base de données sur le web :
localhost:8080, remplir les champs avec : postgresql, db, pokemon, password, myapp  

### accès application sur le web :
localhost:5050  
