import pyinputplus as pyip


class MenuView:
    """Menu."""

    def __init__(self):
        pass

    @staticmethod
    def display_main_menu():
        """Affiche le menu principal et retourne le sous-menu choisi."""
        submenu = pyip.inputMenu(
            choices=["Joueurs", "Tournois", "Rapports", "Quitter"],
            prompt="\n----- MENU SWISS CHESS MANAGER -----\n", numbered=True)
        return submenu

    @staticmethod
    def display_players_menu():
        """Affiche le sous-menu players et retourne l'option choisie."""
        submenu_option = pyip.inputMenu(
            choices=["Créer un nouveau joueur",
                     "Modifier la fiche d'un joueur",
                     "Retourner au menu principal"],
            prompt="\n----- MENU JOUEURS -----\n", numbered=True)
        return submenu_option

    @staticmethod
    def display_tournaments_menu():
        """Affiche le sous-menu tournois et retourne l'option choisie."""
        submenu_option = pyip.inputMenu(
            choices=["Créer un tournoi",
                     "Gérer le tournoi en cours",
                     "Retourner au menu principal"],
            prompt="\n----- MENU TOURNOIS -----\n", numbered=True)
        return submenu_option

    @staticmethod
    def display_reports_menu():
        """Affiche le sous-menu rapports et retourne l'option choisie."""
        submenu_option = pyip.inputMenu(
            choices=["Afficher la liste des joueurs",
                     "Afficher les tournois",
                     "Retourner au menu principal"],
            prompt="\n----- MENU RAPPORTS -----\n", numbered=True)
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
    def ask_save_report():
        """Propose de sauvegarder le rapport ou de revenir au menu et retourne le choix."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder le rapport ? "
                   "Saisir 'Y' (yes) ou 'N' (no).\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_tournament_id():
        """Demande la saisie de l'id du tournoi à afficher et le retourne."""
        tournament_id: int = pyip.inputNum(
            prompt="Pour afficher le détail d'un tournoi (joueurs, tours, matchs), saisir son identifiant. "
                   "Sinon, valider pour revenir au menu.\n",
            blank=True, min=1)
        return tournament_id
