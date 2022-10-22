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
        player_input: dict = PlayerView.player_input(self.view)
        player_input["date_of_birth"] = player_input["date_of_birth"].strftime('%Y-%m-%d')
        player = Player(player_input["lastname"], player_input["firstname"], player_input["date_of_birth"], player_input["gender"], player_input["rating"])
        try:
            player.save_player()
            print(f"Vous avez créé le joueur n° {player.player_id}:\n {player}")
        except RuntimeError:
            print("ERREUR: L'enregistrement du joueur a échoué")
        print("#######################FIN DU PROGRAMME DANS player_controller, add_new_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")

    def edit_player(self):
        """Modifier la fiche d'un joueur (fonctionnalité de l'option 2 PLAYERS_MENU):
        Demande l'identifiant du joueur à la vue,
        Demande la fiche sérialisée du joueur cherché par l'id,
        Affiche un message d'erreur puis le menu PLAYERS_MENU si le joueur n'existe pas,
        Désérialise la fiche sérialisée du joueur reçue de la bdd,
        Affiche l'objet joueur et demande à l'utilisateur de choisir le champ à modifier,
        Modifie le champ sélectionné puis affiche le joueur modifié
        Affiche le menu PLAYERS_MENU."""
        player_id_input = PlayerView.player_id_input()
        db_serialized_player = Player.get_player_by_id(player_id_input)
        if db_serialized_player is None:
            print("ERREUR: L'identifiant saisi n'existe pas")
            print("#######################FIN DU PROGRAMME DANS player_controller, edit_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
        else:
            player = Player.unserialize_player(db_serialized_player)
            field_to_update = PlayerView.field_to_update(player, Player.DOC_ID)
            if field_to_update == "Prénom":
                label = "lastname"
                field_to_update = PlayerView.lastname_input()
                Player.update_player(label, field_to_update, Player.DOC_ID)
            elif field_to_update == "Nom":
                label = "firstname"
                field_to_update = PlayerView.firstname_input()
                Player.update_player(label, field_to_update, Player.DOC_ID)
            elif field_to_update == "Date de naissance":
                label = "date_of_birth"
                field_to_update = PlayerView.date_of_birth_input().strftime('%Y-%m-%d')
                Player.update_player(label, field_to_update, Player.DOC_ID)
            elif field_to_update == "Genre":
                label = "gender"
                field_to_update = PlayerView.gender_input()
                Player.update_player(label, field_to_update, Player.DOC_ID)
            elif field_to_update == "Classement":
                label = "rating"
                field_to_update = PlayerView.rating_input()
                Player.update_player(label, field_to_update, Player.DOC_ID)
            elif field_to_update == "Quitter la modification":
                print("#######################FIN DU PROGRAMME DANS player_controller, edit_player",
                      "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
            else:
                print("ERREUR: La modification du joueur a échoué")
                print("#######################FIN DU PROGRAMME DANS player_controller, edit_player",
                      "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
            updated_player = Player.unserialize_player(Player.get_player_by_id(Player.DOC_ID))
            print(f"Vous avez modifié le joueur n° {Player.DOC_ID}:\n {updated_player}")
        print("#######################FIN DU PROGRAMME DANS player_controller, edit_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")

