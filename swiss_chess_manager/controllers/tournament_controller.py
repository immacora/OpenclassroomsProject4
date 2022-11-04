from swiss_chess_manager.models.tournament_model import TournamentModel
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.views.tournament_view import TournamentView


class TournamentController:
    """TournamentController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

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
        save_tournament_request = TournamentView.save_tournament_request()
        if save_tournament_request == "Y":
            try:
                saved_tournament_id: int = tournament.save_tournament()
                print(f"\nVous avez créé le tournoi n° {saved_tournament_id}:\n {tournament}")
                return saved_tournament_id
            except RuntimeError:
                print("ERREUR: L'enregistrement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    def create_tournament(self):
        """Créer un tournoi.

        Initialise le tournoi.
        Formate les datetime.
        Crée l'objet tournoi.
        Initialise l'id du tournoi sauvegardé.
        Tant que l'id n'existe pas: initialise l'action (field_to_edit), Quitte ou assigne la nouvelle valeur et boucle sur la sauvegarde
        Retourne l'id du tournoi créé ou quitte le programme
        """



        tournament_input: dict = TournamentView.tournament_input(self.view)
        tournament_input["start_date"] = tournament_input["start_date"].strftime('%Y-%m-%d')
        tournament_input["end_date"] = tournament_input["end_date"].strftime('%Y-%m-%d')



        ################ GERER LA LISTE DES JOUEURS #################
        # Initialise la liste des joueurs de la db
        #db_players = PlayerModel.get_all_players()

        # Initialise le nombre de joueurs à sélectionner
        #players_number = tournament_input["players"]

        #Initialise la liste des joueurs du tournoi
        tournament_players = []
        #Boucle sur le nombre de joueurs à sélectionner
        #for player in range(0, players_number):
            #print(player)

        #tournament_input["players"] = ["joueur n°1", "joueur n°2", "joueur n°3", "joueur n°4"]

        ################ GERER LA LISTE DES JOUEURS #################


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

            close_request = TournamentView.close_request()
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
            TournamentView.display_tournaments(tournaments)
            tournament_id = TournamentView.ask_tournament_id()
            if isinstance(tournament_id, int):
                return tournament_id
