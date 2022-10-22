import pyinputplus as pyip


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
        """Demande la saisie (vérifiée) d'un id à l'utilisateur et le retourne."""
        id_choice: int = pyip.inputNum(prompt="Saisir l'identifiant du joueur à modifier: ", min=1)
        return id_choice

    @staticmethod
    def field_to_update(player, doc_id):
        """Affiche le joueur à modifier,
        Demande à l'utilisateur la saisie (vérifiée) d'une option de champ à modifier et le retourne."""
        print(f"Vous allez modifier le joueur n° {doc_id}:\n {player}")
        field_to_update = pyip.inputMenu(choices=["Prénom", "Nom", "Date de naissance", "Genre", "Classement", "Quitter la modification"], prompt="Saisir le numéro correspondant au champ à modifier:\n", numbered=True)
        return field_to_update

    def player_input(self):
        """Demande à l'utilisateur de saisir les renseignements nécessaires à la création de la fiche du joueur et vérifie les saisies à l'aide du module pyinputplus
        Renvoie le dictionnaire des datas."""
        print("Créer un nouveau joueur: ")
        lastname = self.lastname_input()
        firstname = self.lastname_input()
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
