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
    - Un répertoire data (données des tables players et tournaments de tinydb)
    - Un répertoire flake8_rapport #################################
    - Un répertoire reports (rapports exportés depuis l'application)
    - Le répertoire swiss_chess_manager contenant le code de l'application (les 3 répertoires : models, views, controllers)
    - Le fichier swiss_chess_manager.py permettant d'exécuter l'application
    - Le fichier requirements
    - Un fichier .flake8###########################
    - Le fichier README

## Utilisation
### Remarques générales
    Le logiciel comporte un menu principal, le MENU SWISS CHESS MANAGER, qui propose 2 sous-menus : MENU JOUEURS et MENU TOURNOIS.

    Le MENU JOUEURS est une section dédiée à l'ajout, la modification et l'affichage des joueurs contenus dans la base de données du programme. Elle permet également d'exporter des rapports : Affichage de la liste des joueurs (par ordre alphabétique ou classement).

    Le MENU TOURNOIS est une section dédiée à la gestion d'un tournoi d'échecs selon le système suisse et son affichage. Elle permet également d'exporter des rapports : Affichage de la liste des tournois, de la fiche détaillée d'un tournoi, sa liste des joueurs (par ordre alphabétique ou classement), celle de ses tours et celle de ses matchs).

### Déroulement d'un tournoi

    1- Exécutez le programme depuis la console :
        Pour afficher le MENU SWISS CHESS MANAGER, saisir : python swiss_chess_manager.py

    2- Choisir un sous-menu :
        2.1 MENU JOUEURS :
            - Créer un nouveau joueur
            - Modifier la fiche d'un joueur
            - Afficher la liste des joueurs (par ordre alphabétique ou classement)
            - Retourner au menu principal
        2.2 MENU TOURNOIS :
            - Lancer un tournoi (créer un tournoi : 8 joueurs et 4 tours par défaut)
            - Gérer le tournoi en cours (créer les tours, les appariements, saisir les résultats, clôturer le tournoi)
            - Afficher les tournois (afficher la liste des tournois, le détail d'un tournoi : la liste de ses joueurs, celle de ses tours et de ses matchs)

    3- Consulter les rapports (fonctionnalité ajoutée à titre d'exemple pour l'amélioration souhaitée) :
        Les rapports produits au cours d'un tournoi ou depuis le menu joueurs peuvent être exportés en csv (dataframes bruts et nommés par date).
        Ils sont consultables depuis le dossier reports après l'arrêt du programme.

    4- Générer 1 nouveau rapport flake8 (exemple)
