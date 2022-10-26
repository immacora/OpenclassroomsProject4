from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.models.player_model import PlayerModel


class PlayerController:
    """PlayerController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def add_new_player(self):
        """Créer un nouveau joueur (fonctionnalité de l'option 1 PLAYERS_MENU):
        Initialise le joueur,
        Formate la data datetime->str(annee-mois-jour),
        Crée l'objet joueur, l'insère en base et affiche le joueur créé ou un message d'erreur,
        Affiche le menu PLAYERS_MENU."""
        player_input: dict = PlayerView.player_input(self.view)
        player_input["date_of_birth"] = player_input["date_of_birth"].strftime('%Y-%m-%d')
        player = PlayerModel(player_input["lastname"], player_input["firstname"], player_input["date_of_birth"], player_input["gender"], player_input["rating"])
        try:
            saved_player = player.save_player()
            print(f"\nVous avez créé le joueur n° {saved_player}:\n {player}")
        except RuntimeError:
            print("ERREUR: L'enregistrement du joueur a échoué")
        print("#######################FIN DU PROGRAMME DANS player_controller, add_new_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")

    def edit_player(self):
        """Modifier la fiche d'un joueur (fonctionnalité de l'option 2 PLAYERS_MENU):
        Initialise l'identifiant du joueur à modifier et la fiche correspondante dans la db,
        Si le numéro saisi par l'utilisateur n'existe pas : Affiche un message d'erreur puis le menu PLAYERS_MENU,
        Sinon : Initialise l'objet joueur, le label et le champ à modifier puis assigne les nouvelles valeurs et affiche le joueur modifié,
        Affiche le menu PLAYERS_MENU."""
        player_id = PlayerView.player_id_input()
        db_serialized_player = PlayerModel.get_player_by_id(player_id)
        if db_serialized_player is None:
            print("ERREUR: L'identifiant saisi n'existe pas")
            print("#######################FIN DU PROGRAMME DANS player_controller, edit_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
        else:
            player = PlayerModel.unserialize_player(db_serialized_player)
            label = ""
            field_to_update = PlayerView.field_to_update(player, player_id)
            if field_to_update == "Prénom":
                label = "lastname"
                field_to_update = PlayerView.lastname_input()
            elif field_to_update == "Nom":
                label = "firstname"
                field_to_update = PlayerView.firstname_input()
            elif field_to_update == "Date de naissance":
                label = "date_of_birth"
                field_to_update = PlayerView.date_of_birth_input().strftime('%Y-%m-%d')
            elif field_to_update == "Genre":
                label = "gender"
                field_to_update = PlayerView.gender_input()
            elif field_to_update == "Classement":
                label = "rating"
                field_to_update = PlayerView.rating_input()
            elif field_to_update == "Quitter la modification":
                print("#######################FIN DU PROGRAMME DANS player_controller, edit_player",
                      "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
            else:
                print("ERREUR: La modification du joueur a échoué")
                print("#######################FIN DU PROGRAMME DANS player_controller, edit_player",
                      "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
            PlayerModel.update_player(label, field_to_update, player_id)
            updated_player = PlayerModel.unserialize_player(PlayerModel.get_player_by_id(player_id))
            print(f"\nVous avez modifié le joueur n° {player_id}:\n {updated_player}")
        print("#######################FIN DU PROGRAMME DANS player_controller, edit_player", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")

    def show_players_list(self):
        """Afficher la liste des joueurs de la table PLAYERS_TABLE (fonctionnalité de l'option 3 PLAYERS_MENU):
        Initialise la liste des joueurs,
        Si aucun joueur n'a été récupéré : Affiche un message d'erreur puis le menu PLAYERS_MENU,
        Sinon : Affiche la liste triée
        Affiche le menu PLAYERS_MENU."""
        players_list = PlayerModel.get_all_players()
        if players_list is None:
            print("ERREUR: La requête a échoué")
            print("#######################FIN DU PROGRAMME DANS player_controller, show_players_list", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
        else:
            PlayerView.list_sort(players_list)
        print("#######################FIN DU PROGRAMME DANS player_controller, show_players_list", "ajouter l'appel à la fonction de retour au PLAYERS_MENU : Revenir au menu Joueurs")
