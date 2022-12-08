import pandas as pd
import pyinputplus as pyip


class PlayerView:
    """Player view."""

    def __init__(self):
        pass

    @staticmethod
    def lastname():
        """Saisie du prénom du joueur."""
        return pyip.inputStr(
            prompt="Saisir le prénom du joueur (en lettres uniquement): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def firstname():
        """Saisie du nom du joueur."""
        return pyip.inputStr(
            prompt="Saisir le nom du joueur (en lettres uniquement): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def date_of_birth():
        """Saisie de la date de naissance du joueur."""
        return pyip.inputDate(prompt="Saisir la date de naissance du joueur au format (YYYY/MM/DD): ")

    @staticmethod
    def gender():
        """Saisie du genre du joueur."""
        return pyip.inputChoice(prompt="Saisir le genre du joueur (M : Masculin, F : Féminin): ", choices=["M", "F"])

    @staticmethod
    def rating():
        """Saisie du classement du joueur(de 799: plancher ELO rapide à 3500: plafond ordi)."""
        return pyip.inputNum(prompt="Saisir le classement du joueur (entre 799 et 3500): ", min=799, max=3500)

    @staticmethod
    def ask_player_id():
        """Saisie d'un id de joueur."""
        player_id: int = pyip.inputNum(prompt="\nSaisir l'identifiant du joueur à modifier: ", min=1)
        return player_id

    @staticmethod
    def field_to_update(player, doc_id):
        """Saisie d'une option de champ de la fiche joueur à modifier."""
        print(f"\nVous allez modifier le joueur n° {doc_id}:\n {player}")
        field_to_update = pyip.inputMenu(
            choices=["Prénom", "Nom", "Date de naissance", "Genre", "Classement", "Quitter la modification"],
            prompt="\nSaisir le numéro correspondant au champ à modifier:\n", numbered=True
        )
        return field_to_update

    @staticmethod
    def ask_sort():
        """Saisie du type de tri (alphabétique ou classement)."""
        sort = pyip.inputMenu(
            choices=["Ordre alphabétique", "Classement"],
            prompt="\nAfficher les joueurs par:\n", numbered=True
        )
        return sort

    @staticmethod
    def display_sorted_df(sort, players):
        """Affiche le dataframe des joueurs (ordre alphabétique/classement) et retourne la version de tri demandée."""
        players_df = pd.DataFrame(players)
        players_df.rename(
            columns={"lastname": "Prénom", "firstname": "Nom", "date_of_birth": "Date de naissance", "gender": "Genre",
                     "rating": "Classement", "player_id": "Identifiant"}, inplace=True)
        players_df = players_df.reindex(
            columns=["Identifiant", "Nom", "Prénom", "Date de naissance", "Genre", "Classement"]
        )
        players_df.set_index("Identifiant", inplace=True)
        if sort == "Ordre alphabétique":
            sorted_df = players_df.sort_values(by=["Nom"])
            print(f"Liste des joueurs triée par ordre alphabétique:\n{sorted_df}")
            return sorted_df
        elif sort == "Classement":
            sorted_df = players_df.sort_values(by=["Classement"], ascending=False)
            print(f"Liste des joueurs triée par classement:\n{sorted_df}")
            return sorted_df
        else:
            print("ERREUR: L'affichage a échoué")

    def player_input(self):
        """Saisie vérifiée de la fiche du joueur par l'utilisateur et renvoi du dictionnaire des datas."""
        print("\nCréer un nouveau joueur: ")
        lastname = self.lastname()
        firstname = self.firstname()
        date_of_birth = self.date_of_birth()
        gender = self.gender()
        rating = self.rating()
        player_input: dict = {
            "lastname": lastname,
            "firstname": firstname,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "rating": rating
        }
        return player_input
