import pyinputplus as pyip


class MenuView:
    """Menu."""

    def __init__(self):
        pass

    @staticmethod
    def display_main_menu():
        """Affiche le menu principal et retourne le sous-menu choisi."""
        submenu = pyip.inputMenu(
            choices=["Joueurs", "Tournois", "Quitter"],
            prompt="\n----- SWISS CHESS MANAGER MENU -----\n", numbered=True)
        return submenu

    @staticmethod
    def display_players_menu():
        """Affiche le sous-menu players et retourne l'option choisie."""
        submenu_option = pyip.inputMenu(
            choices=["Créer un nouveau joueur", "Modifier la fiche d'un joueur", "Afficher la liste des joueurs", "Retourner au menu principal"],
            prompt="\n----- MENU JOUEURS -----\n", numbered=True)
        return submenu_option

    @staticmethod
    def display_tournaments_menu():
        """Affiche le sous-menu tournois et retourne l'option choisie."""
        submenu_option = pyip.inputMenu(
            choices=["Créer un tournoi", "Accéder au tournoi en cours", "Retourner au menu principal"],
            prompt="\n----- MENU TOURNOIS -----\n", numbered=True)
        return submenu_option

    @staticmethod
    def player_action_choice():
        """Propose de revenir au menu principal ou de recommencer l'action et retourne le choix."""
        return pyip.inputChoice(
            prompt="\nSaisir 'S' pour sortir et revenir au menu principal ou 'R' pour recommencer\n",
            choices=["S", "R"]
        )

    @staticmethod
    def tournament_action_choice():
        """Propose de revenir au menu principal ou de lancer le tournoi et retourne le choix."""
        return pyip.inputChoice(
            prompt="\nSaisir 'S' pour sortir et revenir au menu principal ou 'T' pour lancer le tournoi\n",
            choices=["S", "T"]
        )
