import pyinputplus as pyip
import pandas as pd


class TournamentView:
    """Tournoi."""

    def __init__(self):
        pass

    @staticmethod
    def name():
        """Demande la saisie du du nom du tournoi et le retourne."""
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
    def end_date():
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
        else:
            print(players_number)
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
        rounds_number_input: int = pyip.inputNum(
            prompt="Saisir le nombre de rondes ou valider (4 par défaut)\n",
            blank=True, min=1
        )
        if isinstance(rounds_number_input, int):
            rounds_number = rounds_number_input
        else:
            print(rounds_number)
        return rounds_number

    @staticmethod
    def cadence():
        """Demande la saisie du type de contrôle du temps du tournoi (bullet, blitz ou coup rapide) et le retourne."""
        cadence = pyip.inputMenu(
            choices=["Bullet", "Blitz", "Coup rapide"],
            prompt="\nSaisir le numéro correspondant à la cadence du tournoi:\n", numbered=True
        )
        return cadence

    @staticmethod
    def description():
        """Demande la saisie (facultative) des remarques générales sur le tournoi et les retourne."""
        return pyip.inputStr(
            prompt="Saisir les remarques générales sur le tournoi (caractères spéciaux interdits):\n",
            blank=True,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def field_to_edit():
        """Retourne le champ à modifier ou la demande d'annulation."""
        return pyip.inputMenu(
            choices=["Nom", "Lieu", "Date de début", "Date de fin", "Nombre de tours", "Cadence",
                     "Description", "Annuler et quitter le programme"],
            prompt="\nSaisir un numéro pour corriger les données du tournoi ou quitter le programme :\n", numbered=True
        )

    @staticmethod
    def ask_save_tournament():
        """Retourne la réponse à la demande de sauvegarde des données dans le tournoi."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder ce tournoi ? "
                   "Saisir 'N' (no) pour modifier un champ (liste des joueurs exclue) ou 'Y' (yes) pour sauvegarder "
                   "(Attention, aucune modification ne pourra être effectuée ensuite.)\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_save_player_tournament():
        """Retourne la réponse à la demande d'enregistrement du joueur dans le tournoi."""
        return pyip.inputYesNo(
            prompt="\nConfirmer l'enregistrement du joueur dans le tournoi :\n"
                   "Saisir 'N' (no) pour revenir à la saisie ou 'Y' (yes) pour sauvegarder "
                   "(Attention, la liste des joueurs du tournoi ne sera plus modifiable)\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_close_tournament():
        """Retourne la réponse à la demande de cloture du tournoi."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous cloturer le tournoi ? "
                   "(Attention, aucune modification ne pourra être effectuée ensuite) 'Y' (yes) / 'N' (no) ?\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_tournament_player_id():
        """Retourne la réponse à la demande de saisie de l'id du joueur à inclure dans le tournoi."""
        tournament_player_id: int = pyip.inputNum(
            prompt="\nSaisir l'identifiant du joueur à inclure dans le tournoi: ", min=1
        )
        return tournament_player_id

    @staticmethod
    def select_tournament_player():
        """Retourne la réponse à la demande de sélection ou création du joueur."""
        return pyip.inputChoice(
            prompt="Saisir 'S' pour sélectionner un joueur dans la liste, ou 'C' pour créer un joueur.\n",
            choices=["S", "C"]
        )

    @staticmethod
    def display_tournaments(tournaments):
        """Affiche la liste des tournois.

        Initialise le dataframe.
        Modifie les options d'affichage du dataframe.
        Renomme les colonnes à afficher.
        Remplace la colonne d'index par celle des identifiants.
        Retourne le dataframe.
        """
        tournaments_df = pd.DataFrame(tournaments)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        tournaments_df.rename(
            columns={
                "name": "Nom",
                "location": "Lieu",
                "start_date": "Date de début",
                "end_date": "Date de fin",
                "players": "Joueurs",
                "rounds_number": "Nombre de tours",
                "cadence": "Cadence",
                "description": "Description",
                "closed": "Archivé",
                "tournament_id": "Identifiant"
            },
            inplace=True)
        tournaments_df.set_index("Identifiant", inplace=True)
        print(f"\nListe de tous les tournois :\n{tournaments_df}")
        return tournaments_df

    @staticmethod
    def display_tournament_card(tournament_id, tournament):
        """Affiche le tournoi sélectionné.

        Initialise la fiche du tournoi.
        Renomme les colonnes à afficher.
        Affiche le tournoi.
        """
        tournament_se = pd.Series(tournament)
        tournament_se.index = ["Nom", "Lieu", "Date de début", "Date de fin", "Joueurs", "Nombre de tours", "Cadence", "Description", "Archivé"]
        print(f"\nTournoi n° {tournament_id}:\n{tournament_se}")
        return tournament_se

    @staticmethod
    def ask_tournament_display_option():
        """Affiche les options d'affichage de détail du tournoi et retourne l'option choisie."""
        tournament_display_option = pyip.inputMenu(
            choices=[
                "Liste de tous les joueurs du tournoi",
                "Liste de tous les tours du tournoi",
                "Liste de tous les matchs du tournoi"],
            prompt="Afficher le rapport :\n", numbered=True)
        return tournament_display_option


    ####################################################
    """@staticmethod
    def display_tournament_players(tournament_players):
        #Affiche les joueurs du tournoi.

        #Initialise le dataframe.



        #Renomme les colonnes à afficher.
        #Remplace la colonne d'index par celle des identifiants.
        #Retourne le dataframe.
        
        tournament_players_df = pd.DataFrame(tournament_players)
        tournament_players_df.rename(
            columns={
                "name": "Nom",
                "location": "Lieu",
                "start_date": "Date de début",
                "end_date": "Date de fin",
                "players": "Joueurs",
                "rounds_number": "Nombre de tours",
                "cadence": "Cadence",
                "description": "Description",
                "closed": "Archivé",
                "tournament_id": "Identifiant"
            },
            inplace=True)
        tournament_players_df.set_index("Identifiant", inplace=True)
        print(f"\nListe de tous les joueurs du tournoi :\n{tournament_players_df}")
        return tournament_players_df"""
    ##################################################################

    def tournament_input(self):
        """Demande la saisie de la fiche du tournoi et renvoie le dictionnaire des datas."""
        print("\nCréer un nouveau tournoi: ")
        name = self.name()
        location = self.location()
        start_date = self.start_date()
        end_date = self.end_date()
        players_number = self.players_number()
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
