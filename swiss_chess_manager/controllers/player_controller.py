from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.controllers import functions


class PlayerController:
    """PlayerController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def add_new_player(self):
        """Créer un joueur.

        Initialise le joueur.
        Formate la datetime.
        Crée l'objet joueur.
        Sauvegarde le joueur.
        Affiche le joueur créé ou un message d'erreur.
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
        else:
            print("L'enregistrement du joueur n'a pas été effectué")

    def edit_player(self):
        """Modifier la fiche d'un joueur.

        Initialise l'identifiant cherché.
        Initialise le document correspondant de la table players.
        Si l'identifiant cherché n'existe pas dans la table, affiche un message d'erreur
        Sinon : Initialise l'objet joueur et le champ à modifier.
            Assigne les nouvelles valeurs
            Modifie le joueur
            Cherche le joueur modifié dans la table.
            Affiche le joueur modifié.
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

    def show_players_list(self):
        """Afficher la liste des joueurs de la table players par ordre alphabétique ou classement.

        Initialise la liste des joueurs.
        Si aucun joueur n'a été récupéré, affiche un message d'erreur.
        Sinon : Initialise le dataframe de la liste des joueurs triée.
            Initialise la demande d'export.
            Exporte le rapport si la demande est True.
        """
        players = PlayerModel.get_all_players()

        if players is None:
            print("ERREUR: Aucun joueur n'a été trouvé dans la table players")
        else:
            report = PlayerView.list_sort(players)
            report_request = PlayerView.report_request()
            if report_request == "Y":
                functions.save_report(report)
                print("Le rapport est consultable depuis le répertoire 'reports'")
