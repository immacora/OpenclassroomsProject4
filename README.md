# OpenclassroomsProject4
Développez un programme logiciel en Python

Programme autonome développé en Python pour gérer, hors ligne, des tournois d'échecs selon l'algorithme "suisse" d'appariements et produire les rapports de ces tournois.

## Prérequis :
    - python 3.10.7
    - pip
    - pyinputplus
    - pandas 
    - tinyDB
    - flake8

## Installation
    - Créez l’environnement virtuel du projet : py -m venv .venv
        - Activez l’environnement virtuel : .venv\Scripts\activate
        - Installer les modules : pip install -r requirements.txt

## Contenu
    - Un répertoire data (données des tables players, tournaments et players_standings_grid de tinydb)
    - Un répertoire flake8_rapport contenant le fichier HTML généré par flake8
    - Le répertoire swiss_chess_manager contenant les répertoires models, views et controllers
    - Le fichier swiss_chess_manager.py permettant d'exécuter l'application
    - Le fichier requirements
    - Le fichier flake8
    - Le fichier README
    Le programme propose l'export (facultatif) des rapports consultés vers un répertoire reports.

## Utilisation
### Remarques générales
    Le logiciel comporte un menu principal, le MENU SWISS CHESS MANAGER, qui propose 3 sous-menus :
    - MENU JOUEURS : section dédiée à l'ajout et la modification des joueurs de la base de données du programme.
    - MENU TOURNOIS : section dédiée à la gestion d'un tournoi d'échecs selon le système suisse.
    Elle permet de gérer 1 tournoi à la fois et fonctionne par états.
    - MENU RAPPORTS : section dédiée à l'affichage des joueurs (ordre alphabétique/classement) et des tournois.
    Elle permet d'afficher la liste des tournois puis celle des joueurs, tours et matchs du tournoi sélectionné.

### Déroulement d'un tournoi

    1- Exécutez le programme depuis la console :
        Pour afficher le MENU SWISS CHESS MANAGER, saisir : py swiss_chess_manager.py

    2- Choisir un sous-menu :
        2.1 MENU JOUEURS :
            - Créer un nouveau joueur
            - Modifier la fiche d'un joueur
            - Retourner au menu principal
        2.2 MENU TOURNOIS :
            - Créer un tournoi (8 joueurs et 4 tours par défaut)
            - Gérer le tournoi en cours (appariements, tours, résultats, clôture du tournoi)
        2.3 MENU RAPPORTS :
            - Afficher la liste des joueurs :
                * Ordre alphabétique
                * Classement
            - Afficher la liste des tournois :
                - Afficher le détail d'un tournoi de la liste :
                    * Liste de ses joueurs
                    * Liste de ses tours
                    * Liste de ses matchs

    3- Générer 1 nouveau rapport flake8 (exemple) :
        Pour générer le rapport, saisir : flake8 --format=html --htmldir=flake8_rapport
