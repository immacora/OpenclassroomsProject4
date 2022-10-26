import pyinputplus as pyip
import pandas as pd


class PlayerView:
    """Joueur."""

    def __init__(self):
        """Initialise la vue Joueur."""
        pass

    @staticmethod
    def lastname_input():
        return pyip.inputStr(prompt="Saisir le prénom du joueur (chiffres interdits): ", blank=False, blockRegexes="0123456789")

    @staticmethod
    def firstname_input():
        return pyip.inputStr(prompt="Saisir le nom du joueur (chiffres interdits): ", blank=False, blockRegexes="0123456789")

    @staticmethod
    def date_of_birth_input():
        return pyip.inputDate(prompt="Saisir la date de naissance du joueur au format (YYYY/MM/DD): ")

    @staticmethod
    def gender_input():
        return pyip.inputChoice(prompt="Saisir le genre du joueur (M : Masculin, F : Féminin): ", choices=["M", "F"])

    @staticmethod
    def rating_input():
        return pyip.inputNum(prompt="Saisir le classement du joueur (0 ou un nombre entier positif): ", min=0)

    @staticmethod
    def player_id_input():
        """Demande la saisie d'un id à l'utilisateur et le retourne."""
        player_id: int = pyip.inputNum(prompt="\nSaisir l'identifiant du joueur à modifier: ", min=1)
        return player_id

    @staticmethod
    def field_to_update(player, doc_id):
        """Affiche le joueur à modifier,
        Demande à l'utilisateur la saisie d'une option de champ à modifier et le retourne."""
        print(f"\nVous allez modifier le joueur n° {doc_id}:\n {player}")
        field_to_update = pyip.inputMenu(choices=["Prénom", "Nom", "Date de naissance", "Genre", "Classement", "Quitter la modification"], prompt="\nSaisir le numéro correspondant au champ à modifier:\n", numbered=True)
        return field_to_update

    @staticmethod
    def list_sort(players_list):
        """Demande à l'utilisateur de choisir le type de tri et affiche la liste des joueurs triés par ordre alphabétique ou classement."""
        sort = pyip.inputChoice(prompt="\nAfficher les joueurs par ordre alphabétique: 1 ou classement: 2", choices=["1", "2"])
        players_table = pd.DataFrame(players_list)
        players_table.rename(columns={"lastname": "Prénom", "firstname": "Nom", "date_of_birth": "Date de naissance", "gender": "Genre", "rating": "Classement", "player_id": "Identifiant"}, inplace=True)
        players_table = players_table.reindex(columns=["Identifiant", "Nom", "Prénom", "Date de naissance", "Genre", "Classement"])
        players_table.set_index("Identifiant", inplace=True)
        if sort == "1":
            sorted_list = players_table.sort_values(by=["Nom"])
            print(f"\nListe des joueurs triée par ordre alphabétique:\n{sorted_list}")
        elif sort == "2":
            sorted_list = players_table.sort_values(by=["Classement"], ascending=False)
            print(f"\nListe des joueurs triée par classement:\n{sorted_list}")
        else:
            print("ERREUR: L'affichage a échoué")

    def player_input(self):
        """Saisie vérifiée de la fiche du joueur par utilisateur et renvoi du dictionnaire des datas."""
        print("\nCréer un nouveau joueur: ")
        lastname = self.lastname_input()
        firstname = self.firstname_input()
        date_of_birth = self.date_of_birth_input()
        gender = self.gender_input()
        rating = self.rating_input()
        player_input: dict = {
            "lastname": lastname,
            "firstname": firstname,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "rating": rating
        }
        return player_input
