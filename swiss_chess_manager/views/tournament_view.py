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


""" Test
print(6)
#blockRegexes=r"^[0-9]{5}$"
listejtournois = [tournoi1, tournoi2, tournoi3]"""

"""

    @staticmethod
    def field_to_update(player, doc_id):
        #Affiche le joueur à modifier,
        #Demande à l'utilisateur la saisie d'une option de champ à modifier et le retourne.#

        print(f"\nVous allez modifier le joueur n° {doc_id}:\n {player}")
        field_to_update = pyip.inputMenu(
            choices=["Prénom", "Nom", "Date de naissance", "Genre", "Classement", "Quitter la modification"],
            prompt="\nSaisir le numéro correspondant au champ à modifier:\n", numbered=True
        )
        return field_to_update

    @staticmethod
    def list_sort(players_list):
        #Demande à l'utilisateur de choisir le type de tri
        #Formate le dataframe,
        #Affiche la liste des joueurs triés selon le type choisi (alphabétique ou classement).#

        sort = pyip.inputChoice(
            prompt="\nAfficher les joueurs par ordre alphabétique: 1 ou classement: 2", choices=["1", "2"]
        )

        players_table = pd.DataFrame(players_list)
        players_table.rename(
            columns={"lastname": "Prénom", "firstname": "Nom", "date_of_birth": "Date de naissance", "gender": "Genre",
                     "rating": "Classement", "player_id": "Identifiant"}, inplace=True)
        players_table = players_table.reindex(
            columns=["Identifiant", "Nom", "Prénom", "Date de naissance", "Genre", "Classement"]
        )
        players_table.set_index("Identifiant", inplace=True)

        if sort == "1":
            sorted_list = players_table.sort_values(by=["Nom"])
            print(f"\nListe des joueurs triée par ordre alphabétique:\n{sorted_list}")
        elif sort == "2":
            sorted_list = players_table.sort_values(by=["Classement"], ascending=False)
            print(f"\nListe des joueurs triée par classement:\n{sorted_list}")
        else:
            print("ERREUR: L'affichage a échoué")"""
