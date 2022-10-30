from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.views.tournament_view import TournamentView


class TournamentController:
    """TournamentController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def create_tournament(self):
        """Créer un tournoi (fonctionnalité de l'option 1 MENU TOURNOIS):
        Initialise le tournoi,
        Formate les datas datetime->str(annee-mois-jour),
        Crée l'objet tournoi, l'insère en base et affiche le tournoi créé ou un message d'erreur."""
        tournament_input: dict = TournamentView.tournament_input(self.view)
        tournament_input["start_date"] = tournament_input["start_date"].strftime('%Y-%m-%d')
        tournament_input["end_date"] = tournament_input["end_date"].strftime('%Y-%m-%d')
        tournament = TournamentModel(tournament_input["name"], tournament_input["location"], tournament_input["start_date"], tournament_input["end_date"], tournament_input["players"], tournament_input["rounds_number"], tournament_input["cadence"], tournament_input["description"])
        try:
            saved_tournament = tournament.save_tournament()
            print(f"\nVous avez créé le tournoi n° {saved_tournament}:\n {tournament}")
        except RuntimeError:
            print("ERREUR: L'enregistrement du tournoi a échoué")

    def run_tournament(self):
        """Lancer un tournoi créé."""
        print("####################### FIN DU PROGRAMME DANS tournament_controller, run_tournament")





"""Afficher un rapport concernant les tournois (fonctionnalité de l'option 2 TOURNAMENTS_MENU) :
    -> Liste de tous les tournois
    -> Liste de tous les joueurs d'un tournoi :
        -> par ordre alphabétique
        -> par classement
    -> Liste de tous les tours d'un tournoi
    -> Liste de tous les matchs d'un tournoi.."""


""" READ-ME A CORRIGER ###################
    - Créer un nouveau tournoi (8 joueurs et 4 tours par défaut)
        - Créer 1 tour (ou "ronde") : générer les paires de joueurs (par ordinateur pour le premier tour).
        - Afficher l'appariement des joueurs dans le tour
        - Jouer le tour (Gagner/Perdre 1 match = aléatoire)
        - Saisir les résultats des matchs du tour lorsqu'il est terminé (à la main)
        - Afficher le classement (mis à jour) des joueurs dans le tournoi
        - Générer les paires de joueurs suivantes à l'aide de l'algorithme suisse 
        - Jouer les tours suivants à l'identique jusqu'à la fin des tours
        - Afficher le résulat final
    - Afficher un rapport
    - Retourner au menu principal"""