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
    - Créez l’environnement virtuel du projet : python3 -m venv .venv
        - Activez l’environnement virtuel
        - Installer les modules : pip install -r requirements.txt

## Contenu
    - Un répertoire data (données des tables players, tournaments et players_standings_grid de tinydb)
    - Un répertoire flake8_rapport contenant le fichier HTML généré par flake8
    - Le répertoire swiss_chess_manager contenant le code de l'application (les 3 répertoires : models, views, controllers)
    - Le fichier swiss_chess_manager.py permettant d'exécuter l'application
    - Le fichier requirements
    - Le fichier README
    - Un répertoire reports a été ajouté à titre d'exemple de la fonctionnalité d'export souhaitée pour l'avenir. Les rapports, consultables depuis le dossier répertoire après l'arrêt du programme, ne contiennent actuellement que les données brutes des dataframes générés. 

## Utilisation
### Remarques générales
    Le logiciel comporte un menu principal, le MENU SWISS CHESS MANAGER, qui propose 3 sous-menus :
    - MENU JOUEURS : section dédiée à l'ajout et la modification des joueurs de la base de données du programme.
    - MENU TOURNOIS : section dédiée à la gestion d'un tournoi d'échecs selon le système suisse. Elle permet de gérer plusieurs tournois mais 1 seul à la fois. Elle fonctionne par états gérés par sauvegarde automatique selon l'action de l'utilisateur.
    - MENU RAPPORTS : section dédiée à l'affichage des joueurs par ordre alphabétique ou classement et des tournois (liste des tournois, des tours d'un tournoi, des matchs d'un tournoi).

### Déroulement d'un tournoi

    1- Exécutez le programme depuis la console :
        Pour afficher le MENU SWISS CHESS MANAGER, saisir : python swiss_chess_manager.py

    2- Choisir un sous-menu :
        2.1 MENU JOUEURS :
            - Créer un nouveau joueur
            - Modifier la fiche d'un joueur
            - Retourner au menu principal
        2.2 MENU TOURNOIS :
            - Créer un tournoi (8 joueurs et 4 tours par défaut)
            - Gérer le tournoi en cours (créer les appariements, les tours, saisir les résultats, clôturer le tournoi)
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
