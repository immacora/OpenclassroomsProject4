from swiss_chess_manager.models.tournament_model import TournamentModel, RoundModel
from swiss_chess_manager.views.tournament_view import TournamentView
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.controllers.player_controller import PlayerController
from swiss_chess_manager.views.player_view import PlayerView


class TournamentController:
    """TournamentController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def check_player_id(self, players_df, tournament_players):
        """Vérifie l'id et la fiche du joueur avant enregistrement dans la liste des joueurs du tournoi.

        Initialise l'id du joueur demandé.
        Affiche un message d'erreur et redemande l'id tant qu'il n'est pas dans la liste de tous les joueurs
        ou se trouve déjà dans la liste des joueurs du tournoi.
        Initialise la fiche du joueur correspondant à l'id.
        Affiche le joueur.
        Demande la confirmation d'enregistrement du joueur dans la liste des joueurs du tournoi.
        Retourne False ou l'id vérifié si la demande de sauvegarde est True.
        """
        player_id = TournamentView.ask_tournament_player_id()
        while (player_id not in players_df.index.values) or (player_id in tournament_players):
            print("L'identifiant choisi ne correspond à aucun joueur disponible "
                  "(il n'existe pas ou se trouve déjà dans la liste des joueurs sélectionnés pour le tournoi)")
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

        Affiche un message d'information.
        Initialise le dataframe de tous les joueurs et la liste des joueurs du tournoi.
        Boucle sur le nombre de joueurs à sélectionner.
            Initialise le choix de sélection ou création du joueur.
            Si le joueur est sélectionné dans la liste :
                Initialise l'id vérifié du joueur.
                 Boucle tant que l'id est false.
                 Ajoute l'id du joueur sélectionné à la liste des joueurs du tournoi.
            Si le joueur est créé :
                Initialise l'id du joueur créé.
                 Boucle tant que l'id n'existe pas.
                 Ajoute l'id du joueur créé à la liste des joueurs du tournoi.
            Affiche la liste des joueurs du tournoi (récap).
        Retourne la liste des joueurs du tournoi.
        """
        print("Vous allez saisir la liste des joueurs du tournoi. "
              "Sélectionnez le joueur dans la liste qui s'affiche ou créez le. Attention, cette saisie sera définitive.")
        players_df = PlayerController.show_players()
        tournament_players = []
        for number in range(0, players_number):
            select_tournament_player = TournamentView.select_tournament_player()
            if select_tournament_player == "S":
                player_id = self.check_player_id(players_df, tournament_players)
                while player_id is False:
                    player_id = self.check_player_id(players_df, tournament_players)
                tournament_players.append(player_id)
            elif select_tournament_player == "C":
                player_id = PlayerController(PlayerModel, PlayerView).add_new_player()
                while player_id is None:
                    player_id = PlayerController(PlayerModel, PlayerView).add_new_player()
                tournament_players.append(player_id)
            print(f"\nListe des joueurs enregistrés dans le tournoi : {tournament_players}")
        return tournament_players

    def create_rounds(self, rounds_number, players_number):
        """Crée la liste des instances tours (rondes) du tournoi.

        Crée une instance de tour par numéro de tour (n° et nom de tour) et retourne la liste des instances de tours.
        """
        count = 0
        rounds = []
        for round_number in range(0, rounds_number):
            count += 1
            round = RoundModel(
                round_number=count,
                round_name=f"Round {count}",
                matchs_number=players_number//2
            )
            rounds.append(round)
        return rounds

    def create_tournament(self):
        """Créer un tournoi.

        Initialise le tournoi.
        Formate les datetime, crée la liste des joueurs et celle des tours.
        Crée le tournoi.
        Propose de sauvegarder le tournoi (Y) ou de modifier un champ (N):
            Si oui (Y) : Sauvegarde le tournoi et initialise l'id du tournoi sauvegardé.
            Si non (N) : Tant que l'id n'existe pas, propose la modification d'un champ et boucle sur la sauvegarde
        Retourne l'id du tournoi créé ou quitte le programme
        """
        tournament_input: dict = TournamentView.tournament_input(self.view)
        tournament_input["start_date"] = tournament_input["start_date"].strftime('%Y-%m-%d')
        tournament_input["end_date"] = tournament_input["end_date"].strftime('%Y-%m-%d')
        tournament_input["rounds"] = self.create_rounds(tournament_input["rounds_number"], tournament_input["players"])
        tournament_input["players"] = self.create_tournament_players(tournament_input["players"])
        tournament = TournamentModel(
            tournament_input["name"],
            tournament_input["location"],
            tournament_input["start_date"],
            tournament_input["end_date"],
            tournament_input["cadence"],
            tournament_input["description"],
            tournament_input["players"],
            tournament_input["rounds_number"],
            tournament_input["rounds"]
        )
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
            elif field_to_edit == "Cadence":
                new_cadence = TournamentView.cadence()
                tournament.cadence = new_cadence
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Description":
                new_description = TournamentView.description()
                tournament.description = new_description
                saved_tournament_id = self.save_tournament(tournament)
            elif field_to_edit == "Nombre de tours":
                new_rounds_number = TournamentView.rounds_number()
                tournament.rounds_number = new_rounds_number
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
                print(f"Vous avez créé le tournoi n° {saved_tournament_id}:\n")
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
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            if tournament.closed is False:
                print(f"\nVous avez lancé le tournoi n° {tournament_id}:\n {tournament}\nVous pouvez maintenant y accéder depuis le MENU TOURNOIS - Gérer le tournoi en cours")
            else:
                print("ERREUR: Le lancement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    def player_pairing(self, tournament):
        """Associe les joueurs dans le tour selon le système suisse d'appariement.

        Initialise les listes de joueurs, le compteur


        Scinde les joueurs en 2 groupes selon leur niveau.


        """
        strong_group = []
        week_group = []
        count = 0


        #rounds_number = tournament.rounds_number

        # Initialise les matchs
        match = ()
        # Initialise le statut exempt(joueur impair exempté)
        exempt = False

        # demande si le tour doit etre lancé
        play_round = TournamentView.ask_play_round()

        # ??? CONSERVER ?????Initialise et affiche le dataframe des joueurs du tournoi trié par classement.
        round_players = self.show_tournament_players(tournament.players, sort="Classement")
        print(round_players.index)

        # Affiche l'appariement des joueurs dans le tour
        # si oui
        if play_round == "Y":
            # pour chaque index dans la liste des joueurs du round.
            #for i in range(0, len(round_players.index)):

            # pour chaque id de joueur du round (dataframe) trié par classement.
            for round_player_id in round_players.index.values:

                print(round_player_id, round_players.index.values)
                count += 1
                print(count)
                # si count est inférieur à la moitié de la longueur de la liste des index (quotient de la division euclidienne)

                if count <= (len(round_players.index)//2):
                    strong_group.append(round_player_id)
                else:
                    week_group.append(round_player_id)

            print(strong_group)
            print(week_group)

            # pour chaque id de joueur du round (dataframe) trié par classement.
            #for round_player_id in round_players.index.values:
                #if index < (len(round_players.index)//2):
                #print(round_player_id, round_players.index.values)



                #for i in range(0, len(round_players.index)//2):
                    #strong_group.append(round_player_id)
                    #print(strong_group)

                #match = ()


            print(round_players.index.values)


        pairing = tournament.rounds_number
        return pairing

    def manage_current_tournament(self):
        """Gérer le tournoi en cours.

        Initialise l'id du tournoi en cours.
        S'il en existe un :
            Initialise l'objet tournoi et l'affiche.

            Trie tous les joueurs en fonction de leur classement.



            Propose de clôturer le tournoi.
        Sinon :
            Demande de créer un tournoi.
        """
        tournament_id = TournamentModel.get_open_tournament()
        if tournament_id:
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            print(f"Vous gérez le tournoi n° {tournament_id}:\n {tournament}\n")




            # Crée la liste des instances tours/rondes
            #rounds = TournamentModel.rounds


            #rounds_df = pd.DataFrame(rounds)
            #print(rounds, "rounds")
            #print(tournament.rounds_number)


            # Affiche le numéro du tour
            #print(f"Créer le tour n° {round_number}:\n")

            # Affiche l'appariement des joueurs dans le tour
            pairing = self.player_pairing(tournament)
            print(pairing)


            print("Triez tous les joueurs en fonction de leur classement.")
            print("Créer 1 tour (générer les paires de joueurs).")
            print("Afficher l'appariement des joueurs dans le tour")
            print("Saisir les résultats des matchs du tour lorsqu'il est terminé (Gagner/Perdre 1 match = aléatoire)")
            print("Afficher le classement (mis à jour) des joueurs dans le tournoi")


                # Trie le dataframe par Classement de joueur

                # Apparie les joueurs selon leur niveau

                #Crée l'instance ronde
                #round = RoundModel(round_number, round_name, start_datetime, end_datetime, name, location, start_date, end_date, players, rounds_number, cadence, description)


            #Initialise la liste des id des joueurs du tournoi
            # Initialise la liste vide des joueurs du tournoi
            #tournament_players_id = tournament.players
            #tournament_players = []
            #pour chaque id de joueur dans la liste d'id:
            #for tournament_player_id in tournament_players_id:

            #for round in len(int(tournament.rounds_number)):
            #print(type(tournament.rounds_number))
            #print(tournament.rounds_number)

            #1.	Au début du premier tour, triez tous les joueurs en fonction de leur classement."


            print(f"menu : lancer le premier tour / revenir au menu principal")


            print("Jouer les tours suivants à l'identique")
            print("Afficher le résulat final")

            #Si le dernier tour est terminé: propose de clôturer le tournoi
            x = "z"
            if x != "z":
                close_tournament = TournamentView.ask_close_tournament()
                if close_tournament == "Y":
                    TournamentModel.close_tournament(tournament_id)
        else:
            print("Il n'existe aucun tournoi en cours, vous devez en lancer un nouveau.")

    def show_tournaments(self):
        """Afficher la liste des tournois de la table tournaments.

        Initialise la liste des tournois.
        Si aucun tournoi n'a été récupéré, affiche un message d'erreur.
        Sinon : Retourne le dataframe des tournois.
        """
        tournaments = TournamentModel.get_all_tournaments()
        if tournaments is None:
            print("ERREUR: Aucun tournoi n'a été trouvé dans la table tournaments")
        else:
            tournament_df = TournamentView.display_tournaments(tournaments)
            return tournament_df

    def show_tournament(self, tournament_id):
        """Afficher le détail d'un tournoi de la table tournaments.

        Initialise le tournoi à afficher.
        Initialise la fiche du tournoi.
        Retourne la fiche.
        """
        tournament = TournamentModel.get_tournament_by_id(tournament_id)
        tournament_se = TournamentView.display_tournament_card(tournament_id, tournament)
        return tournament_se

    @staticmethod
    def show_tournament_players(tournament_players_id, sort=""):
        """Afficher la liste des joueurs d'un tournoi par ordre alphabétique ou classement.

        Initialise la liste des joueurs du tournoi.
        Initialise le type de tri.
        Retourne le rapport de la liste des joueurs triée.
        """
        tournament_players = []
        if sort == "":
            sort = PlayerView.ask_sort()
        for tournament_player_id in tournament_players_id:
            tournament_player = PlayerModel.get_player_by_id(tournament_player_id)
            tournament_player["player_id"] = tournament_player_id
            tournament_players.append(tournament_player)
        report = PlayerView.display_sorted_df(sort, tournament_players)
        return report

    @staticmethod
    def show_rounds(rounds):
        """Afficher la liste des tours d'un tournoi."""
        report = TournamentView.display_rounds(rounds)
        if report is None:
            print("ERREUR: L'affichage a échoué")
        else:
            return report
