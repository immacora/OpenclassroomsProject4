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
    - Un répertoire documentation ##################################
    - Un répertoire flake8_rapport #################################
    - Un répertoire reports (rapports exportés depuis l'application)
    - Le répertoire swiss_chess_manager contenant le code de l'application (les 3 répertoires : models, views, controllers)
    - Le fichier swiss_chess_manager.py permettant d'exécuter l'application
    - Un fichier .flake8###########################
    - Le fichier README
    - Le fichier requirements

## Utilisation

    1- Lancement du programme :
        - Exécutez le programme depuis la console : saisir python swiss_chess_manager.py 

    2- Choix d'une option de menu :
        Le menu principal propose 2 sous-menus qui donnent accès aux fonctionnalités suivantes :
        2.1 MENU JOUEURS :
            - Créer un nouveau joueur
            - Modifier les données d'un joueur
            - Afficher la liste des joueurs par ordre alphabétique ou classement (permet d'exporter un rapport)
            - Retourner au menu principal
        2.2 MENU TOURNOIS :
            - Créer un tournoi (8 joueurs et 4 tours par défaut)

##########################
                - Créer 1 tour (générer les paires de joueurs)
                - Afficher l'appariement des joueurs dans le tour
                - Saisir les résultats des matchs du tour lorsqu'il est terminé (Gagner/Perdre 1 match = aléatoire)
                - Afficher le classement (mis à jour) des joueurs dans le tournoi
                - Jouer les tours suivants à l'identique
                - Afficher le résulat final
            - Accéder au tournoi en cours
            - Retourner au menu principal

    3- Rapports (fonctionnalité ajoutée à titre d'exemple pour l'amélioration souhaitée):
        Les rapports produits au cours d'un tournoi ou depuis le menu joueurs peuvent être exportés en csv.
        Ils seront consultables depuis le dossier reports une fois le programme terminé.
        Proposés à titre d'exemple, les fichiers contiennent les données brutes uniquement et sont nommés par date uniquement.  

    4- Générer 1 nouveau rapport flake8 (exemple)
