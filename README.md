# OpenclassroomsProject4
Développez un programme logiciel en Python

Programme autonome développé en Python pour gérer, hors ligne, des tournois d'échecs selon l'algorithme "suisse" d'appariements et produire les rapports de ces tournois.

## Prérequis :
    - python 3.10.7
    - pip
    - tinyDB
    - flake8

## Installation
    PyCharm (Windows, Mac ou Linux):
        - Téléchargez les fichiers du projet dans l'IDE PyCharm via VCS
        - Vérifier l'import et lancez le programme SwissChessManager.py
    Terminal Windows :
        - Accédez à l’emplacement où placer vos projets : cd Users\Username\RepertoireProjects ou créez le : mkdir RepertoireProjects
        - Déplacez-vous dans le répertoire : cd RepertoireProjects
        - Clonez le projet : git clone https://github.com/immacora/OpenclassroomsProject4.git
        - Déplacez-vous dans le répertoire : cd OpenclassroomsProject4
        - Créez l’environnement virtuel du projet : python3 -m venv .venv
        - Activez le projet : .venv\Scripts\activate
        - Installer les modules : pip install -r requirements.txt
        - Exécutez le programme : python swiss_chess_manager.py

## Utilisation

    1- Lancement du programme:
        - Initialisation des variables modèle, vue et controller du menu avec la constante MAIN_MENU en paramètre du menu.
        - Appel de la fonction de lancement du menu interactif (controlleur) pour lancer le programme 

    2- Choix d'une option de menu (fichier constants.py du dossier models):
        Le menu principal propose 2 sous-menus qui donnent accès aux fonctionnalités demandées:

        2.1 PLAYERS_MENU:
            - Créer un nouveau joueur
            - Modifier les données d'un joueur
            - Afficher un rapport
            - Retourner au menu principal
    
        2.2 TOURNAMENTS_MENU:
            - Créer un nouveau tournoi
                - Ajout de 8 joueurs (par défaut)
                - Créer 1 tour (générer les paires de joueurs)
                - Afficher l'appariement des joueurs dans le tour
                - Saisir les résultats des matchs du tour lorsqu'il est terminé (Gagner/Perdre 1 match = aléatoire)
                - Afficher le classement (mis à jour) des joueurs dans le tournoi
                - Jouer les tours suivants à l'identique
                - Afficher le résulat final
            - Afficher un rapport
            - Retourner au menu principal

    3- Générer 1 nouveau rapport flake8 (exemple)

