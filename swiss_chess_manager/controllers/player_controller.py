from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.views.player_view import PlayerView


class PlayerController:
    """PlayerController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    @staticmethod
    def edit_player():
        """Modifie la fiche d'un joueur.

        Initialise l'id cherché et le document correspondant.
        Affiche un message d'erreur si l'id n'existe pas ou modifie et affiche le joueur.
        """
        player_id = PlayerView.ask_player_id()
        db_serialized_player = PlayerModel.get_player_by_id(player_id)
        if db_serialized_player is None:
            print("ERREUR: L'identifiant saisi n'existe pas")
        else:
            player = PlayerModel.unserialize_player(db_serialized_player)
            field_to_update = PlayerView.field_to_update(player, player_id)
            if field_to_update == "Prénom":
                label = "lastname"
                field_to_update = PlayerView.lastname()
            elif field_to_update == "Nom":
                label = "firstname"
                field_to_update = PlayerView.firstname()
            elif field_to_update == "Date de naissance":
                label = "date_of_birth"
                field_to_update = PlayerView.date_of_birth().strftime('%Y-%m-%d')
            elif field_to_update == "Genre":
                label = "gender"
                field_to_update = PlayerView.gender()
            elif field_to_update == "Classement":
                label = "rating"
                field_to_update = PlayerView.rating()
            elif field_to_update == "Quitter la modification":
                return
            else:
                print("ERREUR: La modification du joueur a échoué")
                return
            PlayerModel.update_player(label, field_to_update, player_id)
            updated_player = PlayerModel.unserialize_player(PlayerModel.get_player_by_id(player_id))
            print(f"\nVous avez modifié le joueur n° {player_id}:\n {updated_player}")

    @staticmethod
    def show_players():
        """Affiche la liste des joueurs par ordre alphabétique ou classement.

        Initialise la liste des joueurs et le type de tri.
        Retourne le rapport de la liste des joueurs triée ou False.
        """
        players = PlayerModel.get_all_players()
        sort = PlayerView.ask_sort()
        if len(players) == 0:
            print("ERREUR: Aucun joueur n'a été trouvé dans la table players")
            return False
        else:
            report = PlayerView.display_sorted_df(sort, players)
            return report

    def add_new_player(self):
        """Créer un joueur.

        Initialise le joueur.
        Formate la datetime.
        Crée l'objet joueur.
        Sauvegarde le joueur.
        Affiche le joueur créé et retourne son id ou affiche un message d'erreur.
        """
        player_input: dict = PlayerView.player_input(self.view)
        player_input["date_of_birth"] = player_input["date_of_birth"].strftime('%Y-%m-%d')
        player = PlayerModel(player_input["lastname"],
                             player_input["firstname"],
                             player_input["date_of_birth"],
                             player_input["gender"],
                             player_input["rating"])
        saved_player = player.save_player()

        if saved_player is not None:
            print(f"\nVous avez créé le joueur n° {saved_player}:\n {player}")
            return saved_player
        else:
            print("L'enregistrement du joueur n'a pas été effectué")
