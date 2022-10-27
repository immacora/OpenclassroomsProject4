import pyinputplus as pyip


class MenuView:
    """Menu."""

    def __init__(self):
        pass

    @staticmethod
    def display_main_menu():
        """Affiche le menu principal."""
        menu = pyip.inputMenu(
            choices=["Joueurs", "Tournois", "Rapports", "Quitter"],
            prompt="\n----- SWISS CHESS MANAGER MENU -----\n", numbered=True)
        return menu

    @staticmethod
    def display_players_menu():
        menu = pyip.inputMenu(
            choices=["Créer un nouveau joueur", "Modifier la fiche d'un joueur", "Afficher la liste des joueurs", "Retourner au menu principal"],
            prompt="\n----- MENU JOUEURS -----\n", numbered=True)
        return menu

    @staticmethod
    def display_tournaments_menu():
        menu = pyip.inputMenu(
            choices=["Créer un nouveau tournoi", "Afficher un rapport", "Retourner au menu principal"],
            prompt="\n----- MENU TOURNOIS -----\n", numbered=True)
        return menu

    @staticmethod
    def display_report_menu():
        menu = pyip.inputMenu(
            choices=["Afficher un rapport", "Retourner au menu principal"],
            prompt="\n----- MENU RAPPORTS -----\n", numbered=True)
        return menu

    @staticmethod
    def ask_user_option():
        return pyip.inputChoice(prompt="\nSaisir 'S' pour sortir et revenir au menu principal ou 'R' pour recommencer", choices=["S", "R"])
