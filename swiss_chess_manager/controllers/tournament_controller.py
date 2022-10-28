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
