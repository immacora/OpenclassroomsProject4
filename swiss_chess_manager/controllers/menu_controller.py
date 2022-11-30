from swiss_chess_manager.controllers.player_controller import PlayerController
from swiss_chess_manager.controllers.tournament_controller import TournamentController
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.views.menu_view import MenuView
from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.views.tournament_view import TournamentView
from swiss_chess_manager.controllers import functions


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

        Initialise la fonction du contrôleur concerné.
        Initialise l'action choisie par l'utilisateur.
        Exécute le choix
        MENU JOUEURS :
            Boucle sur l'action (ajouter ou modifier un joueur, afficher la liste des joueurs)
            Retourne au menu principal (R: recommencer / S: sortir).
        MENU TOURNOIS :
            Lance un tournoi, gère le tournoi en cours ou affiche les tournois.
        Affiche le menu principal.
        """
        if submenu_option == "Créer un nouveau joueur":
            PlayerController(PlayerModel, PlayerView).add_new_player()
            restart = MenuView.ask_to_restart()
            while restart == "Y":
                PlayerController(PlayerModel, PlayerView).add_new_player()
                restart = MenuView.ask_to_restart()
        elif submenu_option == "Modifier la fiche d'un joueur":
            PlayerController(PlayerModel, PlayerView).edit_player()
            restart = MenuView.ask_to_restart()
            while restart == "Y":
                PlayerController(PlayerModel, PlayerView).edit_player()
                restart = MenuView.ask_to_restart()
        elif submenu_option == "Afficher la liste des joueurs":
            report = PlayerController(PlayerModel, PlayerView).show_players()
            if report is not False:
                functions.save_report(report)
        elif submenu_option == "Lancer un tournoi":
            TournamentController(TournamentModel, TournamentView).start_tournament()
        elif submenu_option == "Gérer le tournoi en cours":
            TournamentController(TournamentModel, TournamentView).manage_current_tournament()
        elif submenu_option == "Afficher les tournois":
            report = TournamentController(TournamentModel, TournamentView).show_tournaments()
            if report is not False:
                functions.save_report(report)
                tournament_id = MenuView.ask_tournament_id()
                if isinstance(tournament_id, int):
                    while tournament_id not in report.index.values:
                        print("L'identifiant choisi ne correspond à aucun tournoi")
                        tournament_id = MenuView.ask_tournament_id()
                    tournament = TournamentModel.unserialize_tournament(
                        TournamentModel.get_tournament_by_id(tournament_id)
                    )
                    tournament_display_option = TournamentView.ask_tournament_display_option()
                    if tournament_display_option == "Liste de tous les joueurs du tournoi":
                        tournament_players_id = tournament.players
                        report = TournamentController(TournamentModel, TournamentView).show_tournament_players(
                            tournament_players_id
                        )
                        functions.save_report(report)
                        restart = MenuView.ask_to_restart()
                        while restart == "Y":
                            report = TournamentController(TournamentModel, TournamentView).show_tournament_players(
                                tournament_players_id
                            )
                            functions.save_report(report)
                            restart = MenuView.ask_to_restart()
                    elif tournament_display_option == "Liste de tous les tours du tournoi":
                        tournament_rounds = tournament.rounds
                        if len(tournament_rounds) == 0:
                            print("Pour afficher les tours du tournoi, lancez l'appariement des joueurs "
                                  "depuis le MENU TOURNOIS - Gérer le tournoi en cours")
                        else:
                            report = TournamentController(TournamentModel, TournamentView)\
                                .show_rounds(tournament_rounds)
                            if report is not False:
                                functions.save_report(report)
                    elif tournament_display_option == "Liste de tous les matchs du tournoi":
                        tournament_rounds = tournament.rounds
                        if len(tournament_rounds) == 0:
                            print(
                                "Pour afficher les matchs du tournoi, lancez l'appariement des joueurs "
                                "depuis le MENU TOURNOIS - Gérer le tournoi en cours")
                        else:
                            tournament = tournament.serialize_tournament()
                            tournament_rounds = tournament["rounds"]
                            round_1 = tournament_rounds[0]
                            if len(round_1["matches"]) == 0:
                                print(
                                    "Aucun match n'a encore été joué. Pour afficher les matchs du tournoi, "
                                    "lancez le premier tour depuis le MENU TOURNOIS - Gérer le tournoi en cours")
                            else:
                                report = TournamentController(TournamentModel, TournamentView)\
                                    .show_matches(tournament_rounds)
                                if report is not False:
                                    functions.save_report(report)
                MenuController.run_menu()
            else:
                MenuController.run_menu()
        else:
            print("ERREUR: La requête a échoué (retour au menu principal)")
        MenuController.run_menu()
