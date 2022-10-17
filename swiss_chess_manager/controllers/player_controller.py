from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.models.player_model import Player
from swiss_chess_manager.controllers.my_exceptions import is_int_exception
import datetime


class PlayerController:
    """PlayerController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def add_new_player(self):
        """Créer un nouveau joueur (fonctionnalité de l'option 1 PLAYERS_MENU):
        Demande la création du player à la vue,
        Formate la data datetime->str(annee-mois-jour)
        Crée l'objet player et l'affiche

        Appelle la fonction d'ajout dans la bdd (modèle Player)

        ."""
        player_input: dict = PlayerView.player_input(self.view)
        player_input["date_of_birth"] = player_input["date_of_birth"].strftime('%Y-%m-%d')
        player = Player(player_input["lastname"], player_input["firstname"], player_input["date_of_birth"], player_input["gender"], player_input["rating"])
        print(f"Vous avez créé le joueur \n {player}")
