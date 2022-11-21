from swiss_chess_manager.models.tournament_model import TournamentModel, Round, PlayerStandingsGrid
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

    @staticmethod
    def impair(players):
        if len(players) % 2 == 0:
            return False
        else:
            return True

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
                print(f"Vous avez créé le tournoi n° {saved_tournament_id}")
                return saved_tournament_id
            except RuntimeError:
                print("ERREUR: L'enregistrement du tournoi a échoué, veuillez relancer le programme.")
                exit()

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
              "Sélectionnez le joueur dans la liste qui s'affiche ou créez le. "
              "Attention, cette saisie sera définitive.")
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

    @staticmethod
    def get_tournament_players(tournament_players_id):
        """Initialise le dictionnaire des joueurs du tournoi avec leur id (PlayerModel) et le retourne."""
        tournament_players = []
        for tournament_player_id in tournament_players_id:
            tournament_player = PlayerModel.get_player_by_id(tournament_player_id)
            tournament_player["player_id"] = tournament_player_id
            tournament_players.append(tournament_player)
        return tournament_players

    def create_rounds(self, rounds_number, players):
        """Crée la liste des instances tours (rondes) du tournoi.

        Initialise le compteur, la liste des tours, le joueur exempté si la liste est impaire, le dataframe des joueurs
        triés par Classement (si classement identique->nom), la liste triée des id des joueurs et le booléen impair.
        Si la liste des id de joueurs est impaire, initialise l'id du joueur exempté.
        Crée une instance de tour par numéro de tour (n° et nom de tour + nb de matchs pour le premier tour)
        Retourne le joueur exempté du tour, la liste des instances de tours
        et la liste des id de joueurs triés par classement.
        """
        count: int = 0
        rounds: list = []
        round_player_exempt_id: int = 0
        tournament_players_df = self.show_tournament_players(players, sort="Classement")
        sorted_tournament_players_id: list = list(tournament_players_df.index.values)
        impair: bool = self.impair(sorted_tournament_players_id)

        if impair:
            round_player_exempt_id = sorted_tournament_players_id[-1]

        for round_number in range(0, rounds_number):
            count += 1
            if count == 1:
                matches_number = len(players) // 2
            else:
                matches_number = None
            round = Round(
                round_number=count,
                round_name=f"Round {count}",
                matches_number=matches_number,
                matches=[]
            )
            rounds.append(round)
        return round_player_exempt_id, rounds, sorted_tournament_players_id

    def extract_exempted_player(self, players_standings_grid):
        """Extrait le joueur exempté de la liste des joueurs du round et retourne le joueur et la liste paire."""
        for player in players_standings_grid:
            if player['exempted_round'] == 1:
                players_standings_grid.remove(player)
                return player, players_standings_grid

    def create_round_opponent(self, players_standings_grid):
        """Crée l'appariement des joueurs d'un tour selon le système suisse.

        Initialise le nombre de matchs, le booléen impair, le joueur exempté et la liste paire,
        les listes de joueurs par niveau, la liste des paires de joueurs et le compteur.
        Extrait le joueur exempté et la liste paire le cas échéant.
        Divise les joueurs en deux moitiés, une supérieure et une inférieure.
        Assigne l'adversaire du round à chaque joueur et crée les couples de joueurs par force
         (boucle sur les 1ers joueurs de chaque liste).
        Assigne l'adversaire du round.
        Ajoute le couple joueur exempté-description.
        Retourne la liste des joueurs mise à jour des adversaires du tour.
        """
        matches_number = len(players_standings_grid) // 2
        impair: bool = self.impair(players_standings_grid)
        exempted_player = None
        even_players = players_standings_grid
        strong_players = []
        week_players = []
        updated_opponents_players = []
        count = 0

        if impair:
            extract_exempted_player = self.extract_exempted_player(players_standings_grid)
            exempted_player = extract_exempted_player[0]
            even_players = extract_exempted_player[1]

        for player in even_players:
            count += 1
            if count <= matches_number:
                strong_players.append(player)
            else:
                week_players.append(player)

        for match_number in range(0, matches_number):
            player_1 = strong_players[0]
            player_1_id = player_1["player_id"]
            player_1_rounds_opponents = player_1["rounds_opponents"]
            player_2 = week_players[0]
            player_2_id = player_2["player_id"]
            player_2_rounds_opponents = player_2["rounds_opponents"]
            player_1_rounds_opponents.append(player_2_id)
            player_2_rounds_opponents.append(player_1_id)
            strong_players.remove(strong_players[0])
            week_players.remove(week_players[0])
            updated_opponents_players.append(player_1)
            updated_opponents_players.append(player_2)

        if impair:
            exempted_player_rounds_opponents = exempted_player["rounds_opponents"]
            exempted_player_rounds_opponents.append(0)
            updated_opponents_players.append(exempted_player)

        return updated_opponents_players

    def create_tournament(self):
        """Créer un tournoi.

        Initialise le tournoi.
        Formate les data, crée la liste des joueurs, celle des tours, et la grille de scores.
        Crée le tournoi.
        Propose de sauvegarder le tournoi (Y) ou de modifier un champ (N):
            Si oui (Y) : Sauvegarde le tournoi et initialise l'id du tournoi sauvegardé.
            Si non (N) : Tant que l'id n'existe pas, propose de quitter le programme
            ou de modifier un champ et boucle sur la sauvegarde
        Retourne l'id du tournoi créé.
        """
        tournament_input: dict = TournamentView.tournament_input(self.view)

        tournament_input["start_date"] = tournament_input["start_date"].strftime('%Y-%m-%d')
        tournament_input["end_date"] = tournament_input["end_date"].strftime('%Y-%m-%d')

        tournament_players = self.create_tournament_players(tournament_input["players"])
        tournament_input["players"] = tournament_players

        tournament_input["rounds"] = []

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
                print(
                    f"\nVous avez lancé le tournoi n° {tournament_id}:\n {tournament}\n"
                    f"Vous pouvez maintenant y accéder depuis le MENU TOURNOIS - Gérer le tournoi en cours")
            else:
                print("ERREUR: Le lancement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    @staticmethod
    def get_open_round(tournament):
        """Retourne le tour (ronde) en cours."""
        rounds = tournament.rounds
        for open_round in rounds:
            if open_round.closed is False:
                return open_round

    def create_players_standings_grid(self, created_rounds, saved_tournament_id):
        """Crée les joueurs de la grille des scores du tournoi.

        Initialise l'id du joueur exempté du premier tour, la liste des id des joueurs triés par classement,
        la liste triée des joueurs du tournoi cherchés par id, le compteur et la liste des joueurs de la grille.
        Crée la liste des joueurs de la grille triés par place dans le tournoi
        (place, nom complet, scores, exempté, adversaires, id)
        Crée la liste des joueurs appariés pour le tour avec gestion du joueur impair pour les joueurs de la grille.
        Crée l'objet joueur de la grille et la liste des objets joueurs de la grille.
        Retourne la liste des objets joueurs de la grille.
        """
        round_player_exempt_id = created_rounds[0]
        sorted_tournament_players_id = created_rounds[2]
        sorted_tournament_players: list = self.get_tournament_players(sorted_tournament_players_id)
        count = 0
        players_standings_grid: list = []

        for tournament_player in sorted_tournament_players:
            count += 1
            player_rank = count
            player_name = f"{tournament_player['firstname']} {tournament_player['lastname']}"
            rounds_scores = 0
            if tournament_player["player_id"] == round_player_exempt_id:
                exempted_round = 1
            else:
                exempted_round = 0
            player_id = int(tournament_player["player_id"])

            player_standings_grid = {
                "player_rank": player_rank,
                "player_name": player_name,
                "rounds_scores": rounds_scores,
                "exempted_round": exempted_round,
                "rounds_opponents": [],
                "player_id": player_id,
                "saved_tournament_id": saved_tournament_id
            }
            players_standings_grid.append(player_standings_grid)

        updated_opponents_players = self.create_round_opponent(players_standings_grid)
        players_standings_grid = []

        for updated_opponents_player in updated_opponents_players:
            player_standings_grid = PlayerStandingsGrid(
                updated_opponents_player["player_rank"],
                updated_opponents_player["player_name"],
                updated_opponents_player["rounds_scores"],
                updated_opponents_player["exempted_round"],
                updated_opponents_player["rounds_opponents"],
                updated_opponents_player["player_id"],
                updated_opponents_player["saved_tournament_id"]
            )
            players_standings_grid.append(player_standings_grid)

        return players_standings_grid

    def manage_current_tournament(self):
        """Gérer le tournoi en cours.

        Initialise l'id du tournoi en cours.
        S'il en existe un :
            Initialise l'objet tournoi et l'affiche.
            Initialise le tour en cours.
            Si aucun tour n'existe (premier tour):
                Affiche "tour 1".
                Selon le choix, retourne au menu ou crée l'appariement du premier tour
                avec la liste des tours à lancer et la liste des joueurs appariés de la grille des scores (sauvegardés).
                Affiche l'appariement des joueurs.
                Lance le tour ou retourne au menu selon le choix.
            Si tous les tours sont fermés, propose de clôturer le tournoi (tournoi + joueurs de la grille) ou de retourner au menu.
            Sinon (autres tours):
                Affiche le tour en cours


                Lance le tour ou retourne au menu selon le choix.

        Sinon :
            Affiche un message demandant de créer un tournoi.
        """
        tournament_id = TournamentModel.get_open_tournament()
        if tournament_id:
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            print(f"Vous gérez le tournoi n° {tournament_id}:\n {tournament}\n")

            open_round = self.get_open_round(tournament)
            if not open_round and len(tournament.rounds) == 0:
                print(f"Vous gérez le tour n° 1:\n")
                pairing = TournamentView.ask_for_pairing()
                if pairing == "Y":
                    created_rounds = self.create_rounds(tournament.rounds_number, tournament.players)
                    rounds = created_rounds[1]
                    serialized_rounds = []
                    for round in rounds:
                        serialized_round = Round.serialize_round(round)
                        serialized_rounds.append(serialized_round)
                        tournament.update_tournament("rounds", serialized_rounds, tournament_id)

                    players_standings_grid = self.create_players_standings_grid(created_rounds, tournament_id)
                    PlayerStandingsGrid.save_players_standings_grid(players_standings_grid)
                    serialized_player_standings_grid = PlayerStandingsGrid.serialize_players_standings_grid(
                        players_standings_grid
                    )

                    self.show_pairing(serialized_player_standings_grid, tournament)

                    print(
                        f"\nVous avez créé l'appariement du tour n° 1:\n"
                        f"Vous pouvez maintenant le consulter et lancer le tour depuis le MENU TOURNOIS - Gérer le tournoi en cours")

            elif not open_round:
                print("Tous les tours ont été joués.")
                close_tournament = TournamentView.ask_close_tournament()
                if close_tournament == "Y":
                    TournamentModel.close_tournament(tournament_id)
                    ##################### FONCTION A CREER(param=liste d'id)
                    #PlayerStandingsGrid.close_players_standings_grid(players_standings_grid_ids)
            else:
                print(f"Vous gérez le tour n° {open_round.round_number}:\n {open_round}\n")
                
                # Récupérer la grille et afficher le PAIRING

                #récupère les joueurs de la grille SOUS FORME DE DICO POUR LE DATAFRAME
                players_standings_grid = PlayerStandingsGrid.get_open_players_standings_grid()
                #print("get_open_players_standings_grid", players_standings_grid)

                self.show_pairing(players_standings_grid, tournament)

                print("show_pairing")
                ################################

                
                # Demander de lancer le tour
                play_round = TournamentView.ask_play_round()
                if play_round == "Y":
                    print("Créer la fonction : self.start_round(open_round)")


        else:
            print("Il n'existe aucun tournoi en cours, vous devez en lancer un nouveau.")

    def show_tournaments(self):
        """Afficher la liste des tournois de la table tournaments.

        Initialise la liste des tournois.
        Si aucun tournoi n'a été récupéré, affiche un message d'erreur.
        Sinon : Retourne le dataframe des tournois.
        """
        tournaments = TournamentModel.get_all_tournaments()
        if len(tournaments) == 0:
            print("ERREUR: Aucun tournoi n'a été trouvé dans la table tournaments")
            return False
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

    def show_tournament_players(self, tournament_players_id, sort=""):
        """Afficher la liste des joueurs d'un tournoi par ordre alphabétique ou classement.

        Initialise le type de tri.
        Crée la liste des joueurs.
        Retourne le rapport de la liste des joueurs triée.
        """
        if sort == "":
            sort = PlayerView.ask_sort()
        tournament_players = self.get_tournament_players(tournament_players_id)
        report = TournamentView.display_sorted_players_df(sort, tournament_players)
        return report

    @staticmethod
    def show_rounds(rounds):
        """Afficher la liste des tours."""
        report = TournamentView.display_rounds(rounds)
        if len(report) == 0:
            print("ERREUR: L'affichage a échoué")
            return False
        else:
            return report

    @staticmethod
    def show_pairing(players_standings_grid, tournament):
        """Afficher l'appariement d'un tour

        Initialise le nom du tournoi, le nom et le n° du tour en cours,
        la liste des appariements, celle des doublons et le compteur.
        Cherche le tour ouvert.
        Double-boucle sur les joueurs de la grille pour construire la liste des appariements
        et initialiser le nom de l'adversaire du joueur dans chaque dictionnaire de joueur.
        Supprime les doublons de la liste.
        Prépare la liste des joueurs pour le dataframe.
        Initialise le rapport d'affichage de l'appariement, propose sa sauvegarde et le retourne.
        """
        tournament_name = tournament.name
        current_round_name = ""
        current_round_number = 0
        pairing = []
        pairing_df = []
        players_double = []
        count = 0

        for round in tournament.rounds:
            if round.closed == False:
                current_round_name = round.round_name
                current_round_number = round.round_number
                break
        if current_round_number == 0:
            current_round_name = "Round 1"
            current_round_number = 1

        for player in players_standings_grid:
            round_opponent_id = player["rounds_opponents"][current_round_number-1]
            if player["exempted_round"] == 1:
                player["round_opponent_name"] = "Exempté"
                pairing.append(player)
            else:
                for opponent in players_standings_grid:
                    if round_opponent_id == opponent["player_id"]:
                        player["round_opponent_name"] = opponent["player_name"]
                        pairing.append(player)
                        players_double.append(opponent["player_id"])
                        break
        for player in pairing:
            if player["player_id"] in players_double:
                pairing.remove(player)
        for player in pairing:
            count += 1
            player_df = {"Match": count,
                         "Joueur 1": player["player_name"],
                         "Joueur 2": player["round_opponent_name"]
                         }
            pairing_df.append(player_df)
        pairing = [tournament_name, current_round_name, pairing_df]
        report = TournamentView.display_pairing(pairing)
        if len(report) == 0:
            print("ERREUR: L'affichage a échoué")
            return False
        else:
            functions.save_report(report)
            return report


    """"@staticmethod
    def show_round(round):
        #Afficher le détail d'un tour.
        report = TournamentView.display_rounds(round)
        if len(report) == 0:
            print("ERREUR: L'affichage a échoué")
            return False
        else:
            return report"""
