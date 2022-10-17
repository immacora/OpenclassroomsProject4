import pyinputplus as pyip


class PlayerView:
    """Joueur."""

    def __init__(self):
        """Initialise la vue Joueur."""
        pass

    def player_input(self):
        """Demande à l'utilisateur de saisir les renseignements nécessaires à la création de la fiche du joueur et vérifie les saisies à l'aide du module pyinputplus
        Renvoie le dictionnaire des datas."""
        print("Créer un nouveau joueur : ")
        lastname = pyip.inputStr(prompt="Saisir le prénom du joueur (chiffres interdits) : ", blank=False, blockRegexes="0123456789")
        firstname = pyip.inputStr(prompt="Saisir le nom du joueur (chiffres interdits) : ", blank=False, blockRegexes="0123456789")
        date_of_birth = pyip.inputDate(prompt="Saisir la date de naissance du joueur au format (DD/MM/YYYY) : ")
        gender = pyip.inputChoice(prompt="Saisir le genre du joueur (M : Masculin, F : Féminin) : ", choices=["M", "F"])
        rating = pyip.inputNum(prompt="Saisir le classement du joueur (0 ou un nombre entier positif) : ", min=0)
        player_input = {
            "lastname": lastname,
            "firstname": firstname,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "rating": rating
        }
        return player_input





    """def display_players_list(self):
        si j'ai un player dans ma liste
            j'affiche la liste
            alpha/rating (donnée par le controller/récup modèle def players_list"""
