from datetime import datetime
from operator import attrgetter, itemgetter

from swiss_chess_manager.controllers.player_controller import PlayerController
from swiss_chess_manager.models.player_model import PlayerModel
from swiss_chess_manager.models.tournament_model import TournamentModel, Round, PlayerStandingsGrid
from swiss_chess_manager.views.player_view import PlayerView
from swiss_chess_manager.views.tournament_view import TournamentView


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
    def get_tournament_players(tournament_players_id):
        """Initialise le dictionnaire des joueurs du tournoi avec leur id (PlayerModel) et le retourne."""
        tournament_players = []
        for tournament_player_id in tournament_players_id:
            tournament_player = PlayerModel.get_player_by_id(tournament_player_id)
            tournament_player["player_id"] = tournament_player_id
            tournament_players.append(tournament_player)
        return tournament_players

    @staticmethod
    def save_tournament(tournament):
        """Sauvegarde le tournoi, l'affiche et retourne son id ou affiche un message d'erreur et quitte le programme."""
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

    @staticmethod
    def check_player_id(players_df, tournament_players):
        """Vérifie l'id du joueur avant enregistrement dans la liste des joueurs du tournoi (retourne l'id ou False)."""
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

    @staticmethod
    def check_rounds_opponents_id(player_1_rounds_opponents, week_players):
        """Retourne le 1er joueur de la liste des week_players exclu de la liste des adversaires du joueur 1."""
        for week_player in week_players:
            if week_player.player_id not in player_1_rounds_opponents:
                player_2 = week_player
                return player_2

    @staticmethod
    def convert_player_score(score):
        """Attribue la valeur de score requise (gagnant = 1, Perdant = 0, Nul = 0.5) en float."""
        if score == "Gagnant":
            score = float(1)
        elif score == "Perdant":
            score = float(0)
        elif score == "Match nul":
            score = float(0.5)
        return score

    @staticmethod
    def set_player_2_score(player_1_score):
        """Attribue le score au joueur 2 selon celui du joueur 1."""
        player_2_score = None
        if player_1_score == float(1):
            player_2_score = float(0)
        elif player_1_score == float(0):
            player_2_score = float(1)
        elif player_1_score == float(0.5):
            player_2_score = float(0.5)
        return player_2_score

    @staticmethod
    def create_players_standings_grid(tournament_id):
        """Crée les joueurs de la grille des scores triés par place dans le tournoi pour le 1er tour
        et retourne la liste de leurs id."""
        count = 0
        tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
        players_standings_grid: list = []

        for tournament_player in tournament.players:
            count += 1
            player_rank = count
            player_id = tournament_player
            tournament_score: float = 0.0

            player = PlayerModel.get_player_by_id(player_id)
            player_name = f"{player['firstname']} {player['lastname']}"

            round_1 = tournament.rounds[0]

            if round_1.round_player_exempt_id == player_id:
                exempted = True
            else:
                exempted = False

            player_standings_grid = PlayerStandingsGrid(
                player_rank=player_rank,
                player_name=player_name,
                tournament_score=tournament_score,
                exempted=exempted,
                rounds_opponents=[],
                player_id=player_id,
                tournament_id=tournament_id
            )
            players_standings_grid.append(player_standings_grid)

        players_standings_grid_id = PlayerStandingsGrid.save_players_standings_grid(players_standings_grid)

        return players_standings_grid_id

    @staticmethod
    def show_tournaments():
        """Demande l'affichage de la liste des tournois et retourne le dataframe ou affiche un message d'erreur."""
        tournaments = TournamentModel.get_all_tournaments()
        if len(tournaments) == 0:
            print("ERREUR: Aucun tournoi n'a été trouvé dans la table tournaments")
            return False
        else:
            tournament_df = TournamentView.display_tournaments(tournaments)
            return tournament_df

    @staticmethod
    def check_report(report):
        """Retourne False si le rapport est vide."""
        if len(report) == 0:
            print("ERREUR: L'affichage a échoué")
            return False
        else:
            return report

    def show_rounds(self, rounds):
        """Demande l'affichage de la liste des tours et la retourne."""
        tournament_rounds = Round.serialize_rounds(rounds)
        report = self.check_report(TournamentView.display_rounds(tournament_rounds))
        return report

    def show_pairing(self, tournament_round, tournament_id):
        """Demande l'affichage de l'appariement d'un tour et le retourne (Remplace l'id du joueur par son nom
        ou "Exempté" et construit chaque couple de joueurs par numéro de match ("Exempté" -> n°0)."""
        round_name = tournament_round["round_name"]
        matches = tournament_round["matches"]
        pairing = []
        count = 0

        for match in matches:
            player_1 = match[0]
            player_2 = match[1]

            player_standings_grid_1 = PlayerStandingsGrid.get_player_standings_grid(
                PlayerStandingsGrid.get_player_standings_grid_id(player_1[0], tournament_id)
            )
            player_1_name = player_standings_grid_1["player_name"]

            if player_2[0] == "Exempté":
                player_2_name = "Exempté"
                couple_id = 0
            else:
                count += 1

                player_standings_grid_2 = PlayerStandingsGrid.get_player_standings_grid(
                    PlayerStandingsGrid.get_player_standings_grid_id(player_2[0], tournament_id)
                )
                player_2_name = player_standings_grid_2["player_name"]
                couple_id = count

            couple = couple_id, player_1_name, player_2_name
            pairing.append(couple)

        report = self.check_report(TournamentView.display_pairing(round_name, pairing))
        return report

    def show_tournament_results(self, tournament_id, sort=""):
        """Demande l'affichage des résultats du tournoi par ordre alphabétique ou classement."""
        if sort == "":
            sort = TournamentView.ask_sort()
        players_standings_grid = PlayerStandingsGrid.get_tournament_players_standings_grid(tournament_id)
        report = self.check_report(TournamentView.display_tournament_results(sort, players_standings_grid))
        return report

    def show_round_results(self, current_round_name, tournament_id):
        """Demande l'affichage des résultats du tour (Boucle sur les tours puis les matchs
        pour construire le dataframe."""
        tournament = TournamentModel.get_tournament_by_id(tournament_id)
        tournament_rounds = tournament["rounds"]
        tournament_players = tournament["players"]
        round_player_exempt_name = "aucun"
        matches = []
        players = []
        impair: bool = self.impair(tournament_players)

        for tournament_round in tournament_rounds:
            if tournament_round["round_name"] == current_round_name:
                matches = tournament_round["matches"]
                if impair:
                    round_player_exempt_id = tournament_round["round_player_exempt_id"]
                    round_player_exempt_name = PlayerStandingsGrid.get_player_standings_grid_name(
                        round_player_exempt_id, tournament_id
                    )

        for match_players in matches:
            for match_player in match_players:
                if isinstance(match_player[0], int):
                    player_id = match_player[0]
                    round_score = match_player[1]
                    player_standings_grid = PlayerStandingsGrid.get_player_standings_grid(
                        PlayerStandingsGrid.get_player_standings_grid_id(player_id, tournament_id)
                    )
                    player = {
                        "Placement": player_standings_grid["player_rank"],
                        "Nom": player_standings_grid["player_name"],
                        "Joueur n°": player_standings_grid["player_id"],
                        "Score du tour": round_score,
                        "Score": player_standings_grid["tournament_score"]
                    }
                    players.append(player)

        report = self.check_report(
            TournamentView.display_round_results(current_round_name, players, round_player_exempt_name))
        return report

    def show_matches(self, tournament_rounds, tournament_id):
        """Demande l'affichage de la liste de tous les matchs d'un tournoi (Boucle sur les tours puis les matchs
        pour construire le dataframe)."""
        round_matches = []

        for tournament_round in tournament_rounds:
            round_name = tournament_round["round_name"]
            for match in tournament_round["matches"]:
                player_1 = match[0]
                player_1_id = player_1[0]
                player_1_score = player_1[1]
                player_1_name = PlayerStandingsGrid.get_player_standings_grid_name(player_1_id, tournament_id)

                player_2 = match[1]
                player_2_id = player_2[0]
                if player_2_id == "Exempté":
                    player_2_name = "Exempté"
                    player_2_score = ""
                else:
                    player_2_name = PlayerStandingsGrid.get_player_standings_grid_name(player_2_id, tournament_id)
                    player_2_score = player_2[1]

                round_match = {
                    "Nom du tour": round_name,
                    "Joueur 1": player_1_name,
                    "Score joueur 1": player_1_score,
                    "Joueur 2": player_2_name,
                    "Score joueur 2": player_2_score
                }
                round_matches.append(round_match)

        report = self.check_report(TournamentView.display_matches(round_matches))
        return report

    def sorted_round_players(self, tournament_id, round_number):
        """Crée la liste triée des joueurs avec le joueur exempté si la liste est impaire et la retourne."""
        sorted_round_players = PlayerStandingsGrid.unserialize_players_standings_grid(
            PlayerStandingsGrid.get_tournament_players_standings_grid(tournament_id)
        )
        tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
        tournament_rounds = tournament.rounds
        impair: bool = self.impair(sorted_round_players)

        if round_number != 1:
            sorted_round_players.sort(key=attrgetter("player_rank"))
            if impair:
                sorted_round_players.sort(key=attrgetter("player_rank"), reverse=True)
                for sorted_round_player in sorted_round_players:
                    if sorted_round_player.exempted is False:
                        sorted_round_player.exempted = True
                        PlayerStandingsGrid.update_player_standings_grid(
                            "exempted", True, sorted_round_player.player_id, tournament_id
                        )
                        for tournament_round in tournament_rounds:
                            if tournament_round.round_number == round_number:
                                tournament_round.round_player_exempt_id = sorted_round_player.player_id
                                field_to_update = tournament.rounds
                                field_to_update = Round.serialize_rounds(field_to_update)
                                tournament.update_tournament("rounds", field_to_update, tournament_id)
                                break
                        break
                sorted_round_players.sort(key=attrgetter("player_rank"))

        return sorted_round_players

    def create_tournament_players(self, players_number):
        """Crée la liste des joueurs du tournoi et la retourne."""
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

    def create_rounds(self, tournament, tournament_id):
        """Crée la liste des instances tours (rondes) du tournoi et la liste des id de joueurs triés par classement."""
        count: int = 0
        rounds: list = []
        first_round_player_exempt_id = 0
        sorted_tournament_players_id = []

        tournament_players = self.get_tournament_players(tournament.players)
        sorted_tournament_players = sorted(tournament_players, key=itemgetter("rating"), reverse=True)
        TournamentView.display_db_players_by_rating(sorted_tournament_players)

        for sorted_tournament_player in sorted_tournament_players:
            sorted_tournament_players_id.append(sorted_tournament_player["player_id"])

        impair: bool = self.impair(sorted_tournament_players_id)
        if impair:
            first_round_player_exempt_id = sorted_tournament_players_id[-1]

        for round_number in range(0, tournament.rounds_number):
            count += 1
            if count == 1:
                matches_number = len(tournament.players) // 2
                round_player_exempt_id = first_round_player_exempt_id
            else:
                matches_number = None
                round_player_exempt_id = None
            tournament_round = Round(
                round_number=count,
                round_name=f"Round {count}",
                matches_number=matches_number,
                round_player_exempt_id=round_player_exempt_id,
                matches=[]
            )
            rounds.append(tournament_round)
        serialized_rounds = Round.serialize_rounds(rounds)
        tournament.update_tournament("rounds", serialized_rounds, tournament_id)
        tournament.update_tournament("players", sorted_tournament_players_id, tournament_id)

    def create_tournament(self):
        """Crée un tournoi, propose sa modification (sauf joueurs), sa sauvegarde (ou abandon) et retourne son id."""
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
        """Lancer un tournoi s'il en existe un."""
        open_tournament = TournamentModel.get_open_tournament()
        if open_tournament:
            print("Un tournoi est déjà en cours, vous devez le clôturer avant d'en créer un nouveau.")
        else:
            tournament_id = self.create_tournament()
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            if tournament.closed is False:
                print(
                    f"\nVous avez créé le tournoi n° {tournament_id}:\n {tournament}\n"
                    f"Vous pouvez maintenant y accéder depuis le MENU TOURNOIS - Gérer le tournoi en cours")
            else:
                print("ERREUR: Le lancement du tournoi a échoué, veuillez relancer le programme.")
                exit()

    def create_match_pairing(self, tournament_id, round_number):
        """Crée l'appariement des joueurs d'un tour selon le système suisse.

        Récupère le joueur exempté du round en cours dans le tournoi,
        l'apparie avec "Exempté" et met à jour la liste de ses adversaires.
        Extrait le joueur exempté de la liste le cas échéant.
        Divise les joueurs en deux moitiés (une supérieure, une inférieure).
        Crée l'appariement des joueurs par force avec adversaires différents (+ maj. liste) sauf pour le dernier match
        (cas du nb de joueurs non optimisé pour le nb de tours), crée les matchs du tour, met à jour la liste des tours.
        """
        round_player_exempt_id = None
        sorted_round_players = self.sorted_round_players(tournament_id, round_number)
        strong_players = []
        week_players = []
        matches_number = len(sorted_round_players) // 2
        matches_pairing = []
        count = 0

        tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
        tournament_rounds = tournament.rounds

        for tournament_round in tournament_rounds:
            if tournament_round.round_number == round_number:
                round_player_exempt_id = tournament_round.round_player_exempt_id
                break

        if round_player_exempt_id:
            for round_player in sorted_round_players:
                if round_player.player_id == round_player_exempt_id:
                    exempted_round_player_rounds_opponents = round_player.rounds_opponents
                    match_pairing = [round_player_exempt_id, 0.0], ["Exempté"]
                    matches_pairing.append(match_pairing)
                    exempted_round_player_rounds_opponents.append("Exempté")
                    PlayerStandingsGrid.update_player_standings_grid(
                        "rounds_opponents", exempted_round_player_rounds_opponents,
                        round_player_exempt_id, tournament_id
                    )
                    sorted_round_players.remove(round_player)

        for player in sorted_round_players:
            count += 1
            if count <= matches_number:
                strong_players.append(player)
            else:
                week_players.append(player)

        for match_number in range(0, matches_number):
            player_1 = strong_players[0]
            player_1_id = player_1.player_id
            player_1_rounds_opponents = player_1.rounds_opponents

            player_2 = self.check_rounds_opponents_id(player_1_rounds_opponents, week_players)
            if player_2 is None:
                player_2 = week_players[0]

            player_2_id = player_2.player_id
            player_2_rounds_opponents = player_2.rounds_opponents

            player_1_rounds_opponents.append(player_2_id)
            player_2_rounds_opponents.append(player_1_id)

            PlayerStandingsGrid.update_player_standings_grid(
                "rounds_opponents", player_1_rounds_opponents, player_1_id, tournament_id
            )
            PlayerStandingsGrid.update_player_standings_grid(
                "rounds_opponents", player_2_rounds_opponents, player_2_id, tournament_id
            )

            match_pairing = [player_1_id, 0.0], [player_2_id, 0.0]
            matches_pairing.append(match_pairing)

            strong_players.remove(player_1)
            week_players.remove(player_2)

        for tournament_round in tournament_rounds:
            if tournament_round.round_number == round_number:
                tournament_round.matches = matches_pairing
                tournament_round.matches_number = matches_number
                field_to_update = tournament.rounds
                field_to_update = Round.serialize_rounds(field_to_update)
                tournament.update_tournament("rounds", field_to_update, tournament_id)
                break

    def start_round(self, open_round, tournament_id):
        """Lancer le tour en cours.

        Construit la liste des paires de joueurs du tour en cours (+exempté), demande le score obtenu,
        enregistre les résultats dans les joueurs de la grille de scores et met à jour le round du tournoi.
        Affiche les résultat du tour.
        Trie la liste d'objets players par score descendant puis placement dans le tournoi.
        Boucle sur les valeurs du dataframe pour enregistrer le nouveau placement des joueurs.
        Si le n° du tour en cours est différent du dernier tour, crée l'appariement des joueurs pour le prochain tour.
        """
        tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
        last_round = tournament.rounds_number
        tournament_rounds = tournament.rounds

        current_round_number = open_round.round_number
        current_round_name = open_round.round_name
        pairing_matches = open_round.matches

        round_matches = []
        players_round_score = []
        start_datetime = datetime.now()
        TournamentView.ask_close_round()
        end_datetime = datetime.now()
        count = 0

        for match in pairing_matches:
            player_1 = match[0]
            player_2 = match[1]

            player_standings_grid_1 = PlayerStandingsGrid.get_player_standings_grid(
                PlayerStandingsGrid.get_player_standings_grid_id(player_1[0], tournament_id)
            )
            player_1_name = player_standings_grid_1["player_name"]

            if player_2[0] == "Exempté":
                player_1_score = TournamentView.ask_exempted_score(player_1_name)
                player_standings_grid_1_tournament_score = player_standings_grid_1["tournament_score"] + player_1_score
                PlayerStandingsGrid.update_player_standings_grid(
                    "tournament_score", player_standings_grid_1_tournament_score, player_1[0], tournament_id
                )
                player_2_score = None
            else:
                player_standings_grid_2 = PlayerStandingsGrid.get_player_standings_grid(
                    PlayerStandingsGrid.get_player_standings_grid_id(player_2[0], tournament_id)
                )

                player_1_score = self.convert_player_score(TournamentView.ask_score(player_1_name))
                player_2_score = self.set_player_2_score(player_1_score)

                player_standings_grid_1_tournament_score = player_standings_grid_1["tournament_score"] + player_1_score
                PlayerStandingsGrid.update_player_standings_grid(
                    "tournament_score", player_standings_grid_1_tournament_score, player_1[0], tournament_id
                )
                player_standings_grid_2_tournament_score = player_standings_grid_2["tournament_score"] + player_2_score
                PlayerStandingsGrid.update_player_standings_grid(
                    "tournament_score", player_standings_grid_2_tournament_score, player_2[0], tournament_id
                )

            match = [player_1[0], player_1_score], [player_2[0], player_2_score]
            round_matches.append(match)

            players_round_score.append([player_1[0], player_1_score])
            players_round_score.append([player_2[0], player_2_score])

        for tournament_round in tournament_rounds:
            if tournament_round.round_name == current_round_name:
                tournament_round.matches = round_matches
                tournament_round.start_datetime = start_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                tournament_round.end_datetime = end_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                tournament_round.closed = True

        field_to_update = tournament.rounds
        field_to_update = Round.serialize_rounds(field_to_update)
        tournament.update_tournament("rounds", field_to_update, tournament_id)

        self.show_round_results(current_round_name, tournament_id)

        round_players = PlayerStandingsGrid.unserialize_players_standings_grid(
            PlayerStandingsGrid.get_tournament_players_standings_grid(tournament_id)
        )

        sorted_round_players_by_rank = sorted(round_players, key=attrgetter("player_rank"))
        sorted_round_players = sorted(sorted_round_players_by_rank, key=attrgetter("tournament_score"), reverse=True)

        for sorted_round_player in sorted_round_players:
            count += 1
            player_id = sorted_round_player.player_id
            PlayerStandingsGrid.update_player_standings_grid("player_rank", count, player_id, tournament_id)

        if current_round_number != last_round:
            open_round = TournamentModel.get_open_round(tournament_id)
            current_round_number = open_round.round_number
            self.create_match_pairing(tournament_id, current_round_number)

    def manage_current_tournament(self):
        """Gérer le tournoi en cours.

        S'il en existe un :
            Initialise l'objet tournoi et l'affiche.
            Initialise le tour en cours.
            Si aucun tour n'existe (premier tour):
                Affiche "tour 1".
                Retourne au menu ou
                crée la liste des tours, trie la liste des id de joueurs par classement pour le 1er tour, maj le tournoi
                crée la liste des joueurs de la grille des scores (classés par place d'après la liste du tournoi maj)
                crée l'appariement des joueurs et retourne au menu.
            Si tous les tours sont fermés, propose de clôturer le tournoi (tournoi + joueurs de la grille)
            ou de retourner au menu.
            Sinon :
                Affiche le tour en cours et son appariement.
                Tant que tous les tours n'ont pas été joués, lance le tour et génère l'appariement suivant
                ou retourne au menu selon le choix.
        Sinon :
            Affiche un message demandant de créer un tournoi.
        """
        tournament_id = TournamentModel.get_open_tournament()
        if tournament_id:
            tournament = TournamentModel.unserialize_tournament(TournamentModel.get_tournament_by_id(tournament_id))
            print(f"Vous gérez le tournoi n° {tournament_id}:\n {tournament}\n")

            open_round = TournamentModel.get_open_round(tournament_id)
            if not open_round and len(tournament.rounds) == 0:
                round_number = 1
                print(f"\nVous gérez le tour n° {round_number}:\n")
                pairing = TournamentView.ask_for_pairing()
                if pairing == "Y":
                    self.create_rounds(tournament, tournament_id)
                    self.create_players_standings_grid(tournament_id)
                    self.create_match_pairing(tournament_id, round_number)

                    print(
                        f"\nVous avez créé l'appariement du tour n° 1:\n"
                        f"Vous pouvez maintenant le consulter et lancer le tour depuis le MENU TOURNOIS - "
                        f"Gérer le tournoi en cours")

            elif not open_round:
                print("Tous les tours ont été joués.")
                close_tournament = TournamentView.ask_close_tournament()
                if close_tournament == "Y":
                    TournamentModel.close_tournament(tournament_id)
                    PlayerStandingsGrid.close_players_standings_grid()
                    print("Le tournoi a été clôturé. Vous pouvez relancer le programme et en créer un nouveau.")
                    exit()
            else:
                last_round = tournament.rounds_number
                active_round_number = open_round.round_number

                while active_round_number != (last_round + 1):
                    print(f"Vous gérez le tour n° {active_round_number}:\n {open_round}\n")
                    self.show_tournament_results(tournament_id, sort="Placement")
                    serialized_round = Round.serialize_round(open_round)

                    self.show_pairing(serialized_round, tournament_id)
                    play_round = TournamentView.ask_play_round()
                    if play_round == "Y":
                        self.start_round(open_round, tournament_id)
                        open_round = TournamentModel.get_open_round(tournament_id)
                        active_round_number += 1
                    else:
                        exit()
                self.show_tournament_results(tournament_id, sort="Placement")
                print("Tous les tours ont été joués.")
                close_tournament = TournamentView.ask_close_tournament()
                if close_tournament == "Y":
                    TournamentModel.close_tournament(tournament_id)
                    PlayerStandingsGrid.close_players_standings_grid()
                    print("Le tournoi a été clôturé. Vous pouvez relancer le programme et en créer un nouveau.")
                    exit()
        else:
            print("Il n'existe aucun tournoi en cours, vous devez en créer un nouveau.")
