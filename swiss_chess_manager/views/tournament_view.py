import pyinputplus as pyip
import pandas as pd


class TournamentView:
    """Tournoi."""

    def __init__(self):
        pass

    @staticmethod
    def name():
        """Demande la saisie du nom du tournoi et le retourne."""
        return pyip.inputStr(
            prompt="Saisir le nom du tournoi (caractères spéciaux interdits): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def location():
        """Demande la saisie du lieu du tournoi et le retourne."""
        return pyip.inputStr(
            prompt="Saisir le lieu du tournoi (caractères spéciaux interdits): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def start_date():
        """Demande la saisie de la date de début du tournoi et la retourne."""
        return pyip.inputDate(prompt="Saisir la date de début du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def end_date():###########self ou controller pour vérif date antérieure/postérieure?????
        """Demande la saisie de la date de fin du tournoi et la retourne."""
        return pyip.inputDate(prompt="Saisir la date de fin du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def players_number():
        """Nombre de joueurs du tournoi : 8 par défaut (min 2).

        Initialise le nombre de tours à 8.
        Initialise le nombre de tours saisis par l'utilisateur.
        Si le résultat de l'input est un int, assigne la valeur saisie.
        Retourne le nombre de joueurs du tournoi
        """
        players_number = 8
        players_number_input: int = pyip.inputNum(
            prompt="Saisir le nombre de joueurs ou valider (8 par défaut)\n",
            blank=True, min=2
        )
        if isinstance(players_number_input, int):
            players_number = players_number_input
        return players_number

    @staticmethod
    def rounds_number():
        """Nombre de tours (rondes) du tournoi : 4 par défaut (min 1).

        Initialise le nombre de tours à 4.
        Initialise le nombre de tours saisis par l'utilisateur.
        Si le résultat de l'input est un int, assigne la valeur saisie.
        Retourne le nombre de tours
        """
        rounds_number = 4
        rounds_number_input: int = pyip.inputNum(prompt="Saisir le nombre de rondes ou valider (4 par défaut)\n",
                                                 blank=True, min=1)
        if isinstance(rounds_number_input, int):
            rounds_number = rounds_number_input
        return rounds_number

    @staticmethod
    def cadence():
        """Demande la saisie du type de contrôle du temps : bullet, blitz ou coup rapide."""
        cadence = pyip.inputMenu(
            choices=["Bullet", "Blitz", "Coup rapide"],
            prompt="\nSaisir le numéro correspondant à la cadence du tournoi:\n", numbered=True
        )
        return cadence

    @staticmethod
    def description():
        """Demande la saisie (facultative) des remarques générales"""
        return pyip.inputStr(
            prompt="Saisir les remarques générales sur le tournoi (caractères spéciaux interdits):\n",
            blank=True,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def save_tournament_request():
        """Retourne la demande de sauvegarde des données du tournoi."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder ces données ? "
                   "(Attention, aucune modification ne pourra être effectuée ensuite) 'Y' (yes) / 'N' (no) ?\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def field_to_edit():
        """Retourne le champ à modifier."""
        return pyip.inputMenu(
            choices=["Nom", "Lieu", "Date de début", "Date de fin", "Joueurs", "Nombre de tours", "Cadence",
                     "Description", "Annuler et quitter le programme"],
            prompt="\nSaisir un numéro pour corriger les données du tournoi ou quitter le programme :\n", numbered=True
        )

    @staticmethod
    def report_request():
        """Retourne la demande de sauvegarde (booléen)."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder le rapport 'Y' (yes) / 'N' (no) ?\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_tournament_id():
        """Demande la saisie de l'id du tournoi à afficher et le retourne."""
        tournament_id: int = pyip.inputNum(prompt="\nSaisir l'identifiant du tournoi à afficher ou valider pour revenir au menu principal: ", blank=True, min=1)
        return tournament_id

    @staticmethod
    def close_request():
        """Retourne la demande de cloture du tournoi (booléen)."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous cloturer le tournoi ? "
                   "(Attention, aucune modification ne pourra être effectuée ensuite) 'Y' (yes) / 'N' (no) ?\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def display_tournaments(tournaments):
        """Affiche la liste des tournois (Nom, lieu, date de début).

        Initialise le dataframe.
        Modifie les options d'affichage du dataframe.
        Supprime les colonnes de détail.
        Renomme ces colonnes.
        Remplace la colonne d'index par celle des identifiants.
        Retourne le dataframe.
        """
        tournaments_table = pd.DataFrame(tournaments)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        del tournaments_table["players"], tournaments_table["description"], tournaments_table["end_date"], tournaments_table["rounds_number"], tournaments_table["cadence"], tournaments_table["closed"]
        tournaments_table.rename(
            columns={"name": "Nom", "location": "Lieu", "start_date": "Date de début", "tournament_id": "Identifiant"}, inplace=True)
        tournaments_table.set_index("Identifiant", inplace=True)
        print(f"\nListe de tous les tournois :\n{tournaments_table}")
        return tournaments_table

    def tournament_input(self):
        """Demande la saisie de la fiche du tournoi et renvoie le dictionnaire des datas."""
        print("\nCréer un nouveau tournoi: ")
        name = self.name()
        location = self.location()
        start_date = self.start_date()
        end_date = self.end_date()
        players_number = self.players_number
        rounds_number = self.rounds_number()
        cadence = self.cadence()
        description = self.description()

        tournament_input: dict = {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "players": players_number,
            "rounds_number": rounds_number,
            "cadence": cadence,
            "description": description
        }
        return tournament_input
