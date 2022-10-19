from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.models.player_model import Player


class PlayerController:
    """PlayerController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def add_new_player(self):
        """Créer un nouveau joueur (fonctionnalité de l'option 1 PLAYERS_MENU):
        Demande la création du joueur à la vue,
        Formate la data datetime->str(annee-mois-jour),
        Crée l'objet joueur, l'insère en base et affiche le joueur créé ou un message d'erreur,
        Affiche le menu PLAYERS_MENU."""
        player_input: dict = PlayerView.player_input()
        player_input["date_of_birth"] = player_input["date_of_birth"].strftime('%Y-%m-%d')
        player = Player(player_input["lastname"], player_input["firstname"], player_input["date_of_birth"], player_input["gender"], player_input["rating"])
        try:
            player.insert_player()
            print(f"Vous avez créé le joueur :\n {player}")
        except RuntimeError:
            print("ERREUR: L'enregistrement du joueur a échoué")

        print("#######################FIN DU PROGRAMME DANS player_controller, add_new_player", "ajouter l'appel à la fonction de retour au menu")
