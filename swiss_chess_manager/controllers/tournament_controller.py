from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.views.tournament_view import TournamentView
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.controllers.player_controller import PlayerController
from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.controllers import functions


class TournamentController:
    """TournamentController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def check_player_id(self, players_df, tournament_players):
        """Vérifie l'id et la fiche du joueur avant enregistrement dans la liste des joueurs du tournoi.

        Initialise l'id du joueur demandé.
        Affiche un message d'erreur et redemande l'id tant qu'il n'est pas dans la liste de tous les joueurs ou se trouve déjà dans la liste des joueurs du tournoi.
        Initialise la fiche du joueur correspondant à l'id.
        Affiche le joueur.
        Demande la confirmation d'enregistrement du joueur dans la liste des joueurs du tournoi.
        Retourne False ou l'id vérifié si la demande de sauvegarde est True.
        """
        player_id = TournamentView.ask_tournament_player_id()
        while (player_id not in players_df.index.values) or (player_id in tournament_players):
            print("L'identifiant choisi ne correspond à aucun joueur disponible (il n'existe pas ou se trouve déjà dans la liste des joueurs sélectionnés pour le tournoi)")
            player_id = TournamentView.ask_tournament_player_id()
        player = PlayerModel.unserialize_player(PlayerModel.get_player_by_id(player_id))
        print(f"\nVous allez enregistrer le joueur n°{player_id} dans le tournoi:\n{player}")
        save_player_tournament = TournamentView.ask_save_player_tournament()
        if save_player_tournament == "Y":
            return player_id
        else:
            return False

    def create_tournament_players(self, players_number):
        """Crée la liste des joueurs du tournoi.

        Initialise le dataframe de tous les joueurs.
        Initialise la liste des joueurs du tournoi.
        Boucle sur le nombre de joueurs à sélectionner.
            Initialise l'id vérifié du joueur.
             Boucle tant que l'id est false.
             Ajoute l'id du joueur sélectionné à la liste des joueurs du tournoi.
        Retourne la liste des joueurs du tournoi.
        """
        print("Vous allez saisir la liste des joueurs du tournoi. Pour sélectionner le joueur, saisir l'identifiant correspondant dans la liste qui s'affiche ou taper ################################################################## pour créer un joueur")
        players_df = PlayerController.show_players_list()
        tournament_players = []
        for number in range(0, players_number):

            #Si selection == Yes : sélectionner le joueur ds le dataframe
            player_id = self.check_player_id(players_df, tournament_players)
            while player_id is False:
                player_id = self.check_player_id(players_df, tournament_players)
            tournament_players.append(player_id)
            #Sinon : créer le joueur
        return tournament_players

    def create_tournament(self):
        """Créer un tournoi.

        Initialise le tournoi.
        Formate les datetime.
        Initialise la liste des joueurs.
        Crée le tournoi.
        Propose de sauvegarder le tournoi (Y) ou de modifier un champ (N):
            Si oui (Y) : Sauvegarde le tournoi et initialise l'id du tournoi sauvegardé.
            Si non (N) : Tant que l'id n'existe pas, propose la modification d'un champ et boucle sur la sauvegarde
        Retourne l'id du tournoi créé ou quitte le programme
        """

        tournament_input: dict = TournamentView.tournament_input(self.view)
        tournament_input["start_date"] = tournament_input["start_date"].strftime('%Y-%m-%d')
        tournament_input["end_date"] = tournament_input["end_date"].strftime('%Y-%m-%d')
        tournament_input["players"] = self.create_tournament_players(tournament_input["players"])
        tournament = TournamentModel(
            tournament_input["name"],
            tournament_input["location"],
            tournament_input["start_date"],
            tournament_input["end_date"],
            tournament_input["players"],
            tournament_input["rounds_number"],
            tournament_input["cadence"],
            tournament_input["description"])
        saved_tournament_id = self.save_tournament(tournament)

        while saved_tournament_id is None:
            field_to_edit = TournamentView.field_to_edit()
            if field_to_edit == "Annuler et quitter le programme":
                exit()
            elif field_to_edit == "Nom":
                new_name = TournamentView.name()
                tournament.name = new_name
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Lieu":
                new_location = TournamentView.location()
                tournament.location = new_location
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Date de début":
                new_start_date = TournamentView.start_date()
                print(new_start_date)
                new_start_date = new_start_date.strftime('%Y-%m-%d')
                tournament.start_date = new_start_date
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Date de fin":
                new_end_date = TournamentView.end_date()
                new_end_date = new_end_date.strftime('%Y-%m-%d')
                tournament.end_date = new_end_date
                saved_tournament_id = self.save_tournament(tournament)
            #elif field_to_edit == "Joueurs":
                #new_players = TournamentView.players()
                #tournament.players = new_players
                #saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Nombre de tours":
                new_rounds_number = TournamentView.rounds_number()
                tournament.rounds_number = new_rounds_number
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Cadence":
                new_cadence = TournamentView.cadence()
                tournament.cadence = new_cadence
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Description":
                new_description = TournamentView.description()
                tournament.description = new_description
                saved_tournament_id = self.save_tournament(tournament)
            else:
                print("ERREUR: La création du tournoi a échoué, veuillez relancer le programme.")
                exit()
        return saved_tournament_id

    @staticmethod
    def save_tournament(tournament):
        """Sauvegarde le tournoi.

        Affiche les données saisies.
        Initialise la demande de sauvegarde des données
        Si la sauvegarde est demandée :
            Initialise l'id du tournoi sauvegardé
            Affiche le tournoi sauvegardé et retourne son id, ou affiche un message d'erreur et quitte le programme
        """
        print(f"\nVous allez créer le tournoi :\n {tournament}")
        save_tournament_request = TournamentView.ask_save_tournament()
        if save_tournament_request == "Y":
            try:
                saved_tournament_id: int = tournament.save_tournament()
                print(f"\nVous avez créé le tournoi n° {saved_tournament_id}:\n {tournament}")
                return saved_tournament_id
            except RuntimeError:
                print("ERREUR: L'enregistrement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    def start_tournament(self):
        """Lancer un tournoi.

        Initialise le tournoi en cours.
        S'il en existe un :
            Affiche un message demandant sa clôture.
        Sinon :
            Crée le tournoi et initialise son id.
            Initialise le document tournoi correspondant à cet id.
            Si le tournoi est ouvert :
                Affiche le tournoi lancé.
            Sinon quitte le programme.
        """
        open_tournament = TournamentModel.get_open_tournament()
        if open_tournament:
            print("Un tournoi est déjà en cours, vous devez le clôturer avant d'en lancer un nouveau.")
        else:
            tournament_id = self.create_tournament()
            tournament = TournamentModel.get_tournament_by_id(tournament_id)
            if tournament["closed"] is False:
                print(f"\nVous avez lancé le tournoi n° {tournament_id}:\n {tournament}\nVous pouvez maintenant y accéder depuis le MENU TOURNOIS - Rejoindre le tournoi en cours")
            else:
                print("ERREUR: Le lancement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    def manage_current_tournament(self):
        """Gérer le tournoi en cours.

        Initialise l'id du tournoi en cours.
        S'il en existe un :
            Initialise l'objet tournoi.



            Propose de clôturer le tournoi.
        Sinon :
            Demande de créer un tournoi.
        """
        tournament_id = TournamentModel.get_open_tournament()
        if tournament_id:
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            print(f"\nVous gérez le tournoi n° {tournament_id}:\n {tournament}\n")

            print(f"\nmenu : lancer le premier tour / revenir au menu principal")

            print("Triez tous les joueurs en fonction de leur classement.")
            print("Créer 1 tour (générer les paires de joueurs).")
            print("Afficher l'appariement des joueurs dans le tour")
            print("Saisir les résultats des matchs du tour lorsqu'il est terminé (Gagner/Perdre 1 match = aléatoire)")
            print("Afficher le classement (mis à jour) des joueurs dans le tournoi")
            print("Jouer les tours suivants à l'identique")
            print("Afficher le résulat final")

            close_request = TournamentView.ask_close_tournament()
            if close_request == "Y":
                TournamentModel.close_tournament(tournament_id)
        else:
            print("Il n'existe aucun tournoi en cours, vous devez en lancer un nouveau.")

    def show_tournaments_list(self):
        """Afficher la liste des tournois de la table tournaments.

        Initialise la liste des tournois.
        Si aucun tournoi n'a été récupéré, affiche un message d'erreur.
        Sinon : Affiche la liste des tournois.
            Initialise la demande de saisie de l'id du tournoi à afficher.
            Affiche le tournoi si le retour est un int.
        """
        tournaments = TournamentModel.get_all_tournaments()
        if tournaments is None:
            print("ERREUR: Aucun tournoi n'a été trouvé dans la table tournaments")
        else:
            return TournamentView.display_tournaments(tournaments)

    def show_tournament(self):
        """Afficher le détail d'un tournoi de la table tournaments.

        Initialise la demande de saisie de l'id du tournoi à afficher.
        Retourne le tournoi si la réponse est un int.
        """
        tournament_id = TournamentView.ask_tournament_id()
        if isinstance(tournament_id, int):
            return tournament_id
