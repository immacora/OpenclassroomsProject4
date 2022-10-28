import pyinputplus as pyip
import pandas as pd


class TournamentView:
    """Tournoi."""

    def __init__(self):
        pass

    @staticmethod
    def name():
        """Nom du tournoi"""
        return pyip.inputStr(
            prompt="Saisir le nom du tournoi (caractères spéciaux interdits): ",
            blank=False, blockRegexes=[r"[&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]"]
        )

    @staticmethod
    def location():
        """Lieu du tournoi"""
        return pyip.inputStr(
            prompt="Saisir le lieu du tournoi (caractères spéciaux interdits): ",
            blank=False, blockRegexes=[r"[&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]"]
        )

    @staticmethod
    def start_date():
        """Date de début du tournoi"""
        return pyip.inputDate(prompt="Saisir la date de début du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def end_date():#self ou controller pour vérif date antérieure/postérieure
        """Date de fin du tournoi"""
        return pyip.inputDate(prompt="Saisir la date de fin du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def players():
        """Liste des joueurs du tournoi"""
        ########################### DONNEES EN DUR #########################
        players = pyip.inputNum(prompt="taper un numéro pour l'instant PUIS Sélectionner les joueurs dans la liste ou les créer (8 par défaut): ")
        players = ["joueur n°1", "joueur n°2", "joueur n°3", "joueur n°4"]
        ####################################################################
        # Liste des indices correspondant aux instances du joueur stockées en mémoire.PAR DEFAUT POUR LA CREATION D'UN TOURNOI = 8
        return players

    @staticmethod
    def rounds_number():
        """Nombre de tours (rondes) du tournoi (min 4, max 100)"""
        # Nombre de tours (valeur choisie par l'organisateur = par défaut sur 4 : prompt = Nombre de tours par défaut : 4. Pour modifier, saisir un autre nombre avant de valider" valeur min = 4) / Chaque tour(round) est une liste de matchs
        return pyip.inputNum(prompt="Saisir le nombre de tours (4 minimum): ", min=4, max=100)

    @staticmethod
    def cadence():
        """Contrôle du temps : bullet, blitz ou coup rapide."""
        cadence = pyip.inputMenu(
            choices=["Bullet", "Blitz", "Coup rapide"],
            prompt="\nSaisir le numéro correspondant à la cadence du tournoi:\n", numbered=True
        )
        return cadence

    @staticmethod
    def description():
        """Remarques générales du directeur du tournoi"""
        return pyip.inputStr(
            prompt="Saisir les remarques générales sur le tournoi (caractères spéciaux interdits): ",
            blank=True,
            blockRegexes=[r"[&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]"]
        )

    def tournament_input(self):
        """Saisie vérifiée de la fiche du tournoi par l'utilisateur et renvoi du dictionnaire des datas."""

        print("\nCréer un nouveau tournoi: ")

        name = self.name()
        location = self.location()
        start_date = self.start_date()
        end_date = self.end_date()
        players = self.players()
        rounds_number = self.rounds_number()
        cadence = self.cadence()
        description = self.description()

        tournament_input: dict = {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "players": players,
            "rounds_number": rounds_number,
            "cadence": cadence,
            "description": description
        }
        return tournament_input
