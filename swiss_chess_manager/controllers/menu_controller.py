from swiss_chess_manager.controllers.player_controller import PlayerController
#from swiss_chess_manager.controllers.tournament_controller import TournamentController
from swiss_chess_manager.models.player_model import PlayerModel
#from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.views.menu_view import MenuView
from swiss_chess_manager.views.player_view import PlayerView
#from swiss_chess_manager.views.tournament_view import TournamentView


class MenuController:
    """MenuController."""

    def __init__(self):
        pass

    @staticmethod
    def run_menu():
        """Lancer le menu:
        Lance le menu principal, initialise le sous-menu et son option,
        Initialise l'option du sous-menu choisie par run_menu,
        Boucle si l'option est le retour au menu principal, lance le sous menu sélectionné sinon."""

        main_menu_option = MenuView.display_main_menu()
        submenu_option = ""

        if main_menu_option == "Joueurs":
            submenu_option = MenuView.display_players_menu()
        elif main_menu_option == "Tournois":
            submenu_option = MenuView.display_tournaments_menu()
        elif main_menu_option == "Rapports":
            submenu_option = MenuView.display_report_menu()
        elif main_menu_option == "Quitter":
            exit()
        else:
            print("ERREUR: L'affichage du menu a échoué")
        if submenu_option == "Retourner au menu principal":
            MenuController.run_menu()
        else:
            MenuController.run_submenu_function(submenu_option)

    @staticmethod
    def user_option():
        """Choisir l'action à exécuter:
        Initialise le choix de l'utilisateur,
        Sort et relance le menu principal (S) ou retourne le choix (R)."""

        user_option = MenuView.ask_user_option()
        if user_option == "S":
            MenuController.run_menu()
        else:
            return user_option

    @staticmethod
    def run_submenu_function(submenu_option):
        """Exécute la fonction liée à l'option sélectionnée:
        Appelle la fonction du contrôleur concerné,
        Demande un choix d'action à l'utilisateur,
        Boucle sur l'action ou retourne au menu principal selon le choix."""

        if submenu_option == "Créer un nouveau joueur":
            PlayerController(PlayerModel, PlayerView).add_new_player()
            user_option = MenuController.user_option()
            while user_option == "R":
                PlayerController(PlayerModel, PlayerView).add_new_player()
                user_option = MenuController.user_option()
        elif submenu_option == "Modifier la fiche d'un joueur":
            PlayerController(PlayerModel, PlayerView).edit_player()
            user_option = MenuController.user_option()
            while user_option == "R":
                PlayerController(PlayerModel, PlayerView).edit_player()
                user_option = MenuController.user_option()
        elif submenu_option == "Afficher la liste des joueurs":
            PlayerController(PlayerModel, PlayerView).show_players_list()
            user_option = MenuController.user_option()
            while user_option == "R":
                PlayerController(PlayerModel, PlayerView).show_players_list()
                user_option = MenuController.user_option()
        elif submenu_option == "Créer un nouveau tournoi":
            #TournamentController(TournamentModel, TournamentView).FONCTION.create_tournament()
            #user_option = MenuController.user_option()
            #while user_option == "R":
                #TournamentController(TournamentModel, TournamentView).FONCTION.create_tournament()
                #user_option = MenuController.user_option()
            print("#######################FIN DU PROGRAMME DANS menu_controller, run_submenu_function")
        elif submenu_option == "Afficher un rapport":
            print("####################### VOIR SI CONSERVER FIN DU PROGRAMME DANS menu_controller, run_submenu_function")
        else:
            print("ERREUR: La requête a échoué (retour au menu principal)")
            MenuController.run_menu()
