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
            prompt="\n----- MENU SWISS CHESS MANAGER -----\n", numbered=True)
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
            choices=["Lancer un tournoi", "Gérer le tournoi en cours", "Afficher les tournois", "Retourner au menu principal"],
            prompt="\n----- MENU TOURNOIS -----\n", numbered=True)
        return submenu_option

    @staticmethod
    def ask_to_restart():
        """Propose de recommencer l'action ou de revenir au menu principal et retourne le choix."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous relancer l'action précédente ? 'Y' (yes) "
                   "ou saisir 'N' (no) pour revenir au menu principal\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def save_report_request():
        """Propose de sauvegarder le rapport ou de revenir au menu principal et retourne le choix."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder le rapport ? Saisir 'Y' (yes) ou 'N' (no) pour revenir au menu principal\n",
            yesVal="Y", noVal="N"
        )
