import pyinputplus as pyip
import pandas as pd


class PlayerView:
    """Joueur."""

    def __init__(self):
        pass

    @staticmethod
    def lastname():
        """Demande la saisie du prénom du joueur et le retourne."""
        return pyip.inputStr(
            prompt="Saisir le prénom du joueur (en lettres uniquement): ",
            blank=False, blockRegexes=[r"[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]"]
        )

    @staticmethod
    def firstname():
        """Demande la saisie du nom du joueur et le retourne."""
        return pyip.inputStr(
            prompt="Saisir le nom du joueur (en lettres uniquement): ",
            blank=False, blockRegexes=[r"[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]"]
        )

    @staticmethod
    def date_of_birth():
        """Demande la saisie de la date de naissance du joueur et la retourne."""
        return pyip.inputDate(prompt="Saisir la date de naissance du joueur au format (YYYY/MM/DD): ")

    @staticmethod
    def gender():
        """Demande la saisie du genre du joueur et le retourne."""
        return pyip.inputChoice(prompt="Saisir le genre du joueur (M : Masculin, F : Féminin): ", choices=["M", "F"])

    @staticmethod
    def rating():
        """Demande la saisie du classement du joueur (entre 1000 et 3500) et le retourne."""
        return pyip.inputNum(prompt="Saisir le classement du joueur (entre 1000 et 3500): ", min=1000, max=3500)

    @staticmethod
    def ask_player_id():
        """Demande la saisie de l'id du joueur cherché et le retourne."""
        player_id: int = pyip.inputNum(prompt="\nSaisir l'identifiant du joueur à modifier: ", min=1)
        return player_id

    @staticmethod
    def field_to_update(player, doc_id):
        """Demande la saisie d'une option de champ de la fiche joueur à modifier et le retourne."""
        print(f"\nVous allez modifier le joueur n° {doc_id}:\n {player}")
        field_to_update = pyip.inputMenu(
            choices=["Prénom", "Nom", "Date de naissance", "Genre", "Classement", "Quitter la modification"],
            prompt="\nSaisir le numéro correspondant au champ à modifier:\n", numbered=True
        )
        return field_to_update

    @staticmethod
    def list_sort(players_list):
        """Affiche la liste des joueurs par ordre alphabétique ou classement.

        Initialise le type de tri.
        Initialise le dataframe.
        Renomme les colonnes du dataframe.
        Réorganise les colonnes du dataframe.
        Remplace la colonne d'index du dataframe par celle des identifiants des joueurs.
        Effectue le tri du dataframe selon le type de tri demandé.
        Affiche le dataframe trié et le retourne (pour export).
        """
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
            return sorted_list
        elif sort == "2":
            sorted_list = players_table.sort_values(by=["Classement"], ascending=False)
            print(f"\nListe des joueurs triée par classement:\n{sorted_list}")
            return sorted_list
        else:
            print("ERREUR: L'affichage a échoué")

    @staticmethod
    def report_request():
        """Retourne la demande de sauvegarde (booléen)."""
        return pyip.inputYesNo(prompt="\nVoulez-vous sauvegarder le rapport 'Y' (yes) / 'N' (no) ?\n", yesVal="Y", noVal="N")

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
