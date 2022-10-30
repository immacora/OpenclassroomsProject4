from swiss_chess_manager.controllers.player_controller import PlayerController
from swiss_chess_manager.controllers.tournament_controller import TournamentController
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.views.menu_view import MenuView
from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.views.tournament_view import TournamentView


class MenuController:
    """MenuController."""

    def __init__(self):
        pass

    @staticmethod
    def run_menu():
        """Lancer le menu.

        Lance le menu principal avec retour du sous-menu.
        Initialise l'option du sous-menu.
        Dirige vers l'option de sous-menu choisie ou boucle.
        """
        submenu = MenuView.display_main_menu()
        submenu_option = ""
        if submenu == "Joueurs":
            submenu_option = MenuView.display_players_menu()
        elif submenu == "Tournois":
            submenu_option = MenuView.display_tournaments_menu()
        elif submenu == "Quitter":
            exit()
        else:
            print("ERREUR: L'affichage du menu a échoué")

        if submenu_option == "Retourner au menu principal":
            MenuController.run_menu()
        else:
            MenuController.run_submenu_function(submenu_option)

    @staticmethod
    def run_submenu_function(submenu_option):
        """Exécute la fonction liée à l'option sélectionnée.

        Appelle la fonction du contrôleur concerné.
        Initialise le choix d'action de l'utilisateur.
        Boucle sur l'action ou retourne au menu principal selon le choix(R: recommencer / T: tournoi / S: sortir).
        """
        if submenu_option == "Créer un nouveau joueur":
            PlayerController(PlayerModel, PlayerView).add_new_player()
            player_menu_action = MenuView.player_action_choice()
            while player_menu_action == "R":
                PlayerController(PlayerModel, PlayerView).add_new_player()
                player_menu_action = MenuView.player_action_choice()
        elif submenu_option == "Modifier la fiche d'un joueur":
            PlayerController(PlayerModel, PlayerView).edit_player()
            player_menu_action = MenuView.player_action_choice()
            while player_menu_action == "R":
                PlayerController(PlayerModel, PlayerView).edit_player()
                player_menu_action = MenuView.player_action_choice()
        elif submenu_option == "Afficher la liste des joueurs":
            PlayerController(PlayerModel, PlayerView).show_players_list()
            player_menu_action = MenuView.player_action_choice()
            while player_menu_action == "R":
                PlayerController(PlayerModel, PlayerView).show_players_list()
                player_menu_action = MenuView.player_action_choice()

        ################TODO####################
        elif submenu_option == "Créer un tournoi":
            TournamentController(TournamentModel, TournamentView).create_tournament()
            tournament_menu_action = MenuView.tournament_action_choice()
            if tournament_menu_action == "T":
                TournamentController(TournamentModel, TournamentView).run_tournament()

            else:
                print("ERREUR: La requête a échoué")
        elif submenu_option == "Accéder au tournoi en cours":
            print("####################### FIN DU PROGRAMME DANS menu_controller, run_submenu_function")
        else:
            print("ERREUR: La requête a échoué (retour au menu principal)")
        MenuController.run_menu()
