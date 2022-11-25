from swiss_chess_manager.models import db_functions


class Round:
    """Tour (ronde)."""

    TOURNAMENTS_TABLE = db_functions.tournaments_table()

    def __init__(self, round_number, round_name, matches_number, matches=None, round_player_exempt_id=0, start_datetime="", end_datetime="",
                 closed=False):
        """Initialise le tour."""
        self.round_number: int = round_number
        self.round_name: str = round_name
        self.matches_number: int = matches_number
        self.matches: list = matches
        self.round_player_exempt_id: int = round_player_exempt_id
        self.start_datetime: str = start_datetime
        self.end_datetime: str = end_datetime
        self.closed = closed

    @staticmethod
    def unserialize_round(serialized_round):
        """Convertit le tour sérialisé en instance."""
        unserialize_round = Round(
            round_number=serialized_round["round_number"],
            round_name=serialized_round["round_name"],
            matches_number=serialized_round["matches_number"],
            matches=serialized_round["matches"],
            round_player_exempt_id=serialized_round["round_player_exempt_id"],
            start_datetime=serialized_round["start_datetime"],
            end_datetime=serialized_round["end_datetime"],
            closed=serialized_round["closed"]
        )
        return unserialize_round

    def __str__(self):
        """Représentation de l'objet tour (ronde) sous forme de chaîne de caractères."""
        round: str = f"Tour n° {self.round_number}\n " \
                     f"Nom : {self.round_name}\n " \
                     f"Nombre de matchs : {self.matches_number}\n " \
                     f"Liste des matchs : {self.matches}\n " \
                     f"Date et heure de début : {self.start_datetime}\n " \
                     f"Date et heure de fin : {self.end_datetime}\n " \
                     f"Archivé : {self.closed}"
        return round

    @staticmethod
    def serialize_rounds(rounds):
        """Sérialise la liste des instances des joueurs de la grille."""
        serialized_rounds = []
        for round in rounds:
            serialized_round = Round.serialize_round(round)
            serialized_rounds.append(serialized_round)
        return serialized_rounds

    def serialize_round(self):
        """Sérialise l'instance du tour dans un dictionnaire."""
        serialized_round: dict = {
            "round_number": self.round_number,
            "round_name": self.round_name,
            "matches_number": self.matches_number,
            "matches": self.matches,
            "round_player_exempt_id": self.round_player_exempt_id,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "closed": self.closed
        }
        return serialized_round


class TournamentModel:
    """Tournament."""

    TOURNAMENTS_TABLE = db_functions.tournaments_table()

    def __init__(self, name, location, start_date, end_date, cadence, description,
                 players, rounds_number, rounds, closed=False):
        """Initialise le tournois."""
        if rounds is None:
            rounds = []
        self.name: str = name
        self.location: str = location
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.cadence: float = cadence
        self.description = description
        self.players: list = players
        self.rounds_number: int = rounds_number
        self.rounds: list = rounds
        self.closed = closed

    @staticmethod
    def get_tournament_by_id(tournament_id):
        """Retourne le tournoi cherché par id."""
        db_serialized_tournament = TournamentModel.TOURNAMENTS_TABLE.get(doc_id=tournament_id)
        return db_serialized_tournament

    @staticmethod
    def get_open_tournament():
        """Retourne l'id du tournoi en cours."""
        tournament_query = db_functions.Query()
        open_tournament = TournamentModel.TOURNAMENTS_TABLE.get(
            tournament_query.closed == False)  # ATTENTION NE FONCTIONNE PAS AVEC le type booléen (is)
        if open_tournament:
            return open_tournament.doc_id

    @staticmethod
    def update_tournament(label, field_to_update, tournament_id):
        """Met à jour la fiche du tournoi."""
        TournamentModel.TOURNAMENTS_TABLE.update({label: field_to_update}, doc_ids=[tournament_id])

    @staticmethod
    def get_all_tournaments():
        """Retourne la liste des tournois et leur id."""
        tournaments = db_functions.get_all_documents(TournamentModel.TOURNAMENTS_TABLE.all(), "tournament_id")
        return tournaments

    @staticmethod
    def unserialize_tournament(serialized_tournament):
        """Convertit le tournoi sérialisé en instance."""
        unserialized_rounds = []
        for serialized_round in serialized_tournament["rounds"]:
            unserialized_rounds.append(Round.unserialize_round(serialized_round))
        unserialized_tournament = TournamentModel(
            name=serialized_tournament["name"],
            location=serialized_tournament["location"],
            start_date=serialized_tournament["start_date"],
            end_date=serialized_tournament["end_date"],
            cadence=serialized_tournament["cadence"],
            description=serialized_tournament["description"],
            players=serialized_tournament["players"],
            rounds_number=serialized_tournament["rounds_number"],
            rounds=unserialized_rounds,
            closed=serialized_tournament["closed"]
        )
        return unserialized_tournament

    @staticmethod
    def close_tournament(tournament_id):
        """Clôture le tournoi."""
        TournamentModel.TOURNAMENTS_TABLE.update({"closed": True}, doc_ids=[tournament_id])

    def __str__(self):
        """Représentation de l'objet tournoi sous forme de chaîne de caractères."""

        tournament: str = f"Nom : {self.name}\n " \
                          f"Lieu : {self.location}\n " \
                          f"Date de début : {self.start_date}\n " \
                          f"Date de fin : {self.end_date}\n " \
                          f"Cadence : {self.cadence}\n " \
                          f"Description : {self.description}\n " \
                          f"Joueurs : {self.players}\n " \
                          f"Nombre de tours : {self.rounds_number}\n " \
                          f"Archivé : {self.closed}"
        return tournament

    def serialize_tournament(self):
        """Sérialise l'instance du tournoi dans un dictionnaire."""
        serialized_rounds = []
        for round in self.rounds:
            serialized_rounds.append(Round.serialize_round(round))
        serialized_tournament: dict = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cadence": self.cadence,
            "description": self.description,
            "players": self.players,
            "rounds_number": self.rounds_number,
            "rounds": serialized_rounds,
            "closed": self.closed
        }
        return serialized_tournament

    def save_tournament(self):
        """Insère le tournoi dans la table tournaments et retourne son id."""
        tournament_id: int = TournamentModel.TOURNAMENTS_TABLE.insert(self.serialize_tournament())
        return tournament_id


class PlayerStandingsGrid:
    """Joueur de la grille des scores du tournoi triés par place dans le tournoi (place, nom complet, liste des score par tour, exempté (booléen car 1 seule foi/tournoi), liste des adversaires par tour, id)."""

    PLAYERS_STANDINGS_GRID_TABLE = db_functions.players_standings_grid_table()

    def __init__(self, player_rank, player_name,
                 rounds_scores, exempted, rounds_opponents, player_id, tournament_id, closed=False):
        """Initialise le joueur de la grille."""
        self.player_rank: int = player_rank
        self.player_name: str = player_name
        self.rounds_scores: list = rounds_scores
        self.exempted: int = exempted
        self.rounds_opponents: list = rounds_opponents
        self.player_id: int = player_id
        self.tournament_id: int = tournament_id
        self.closed = closed

    @staticmethod
    def unserialize_players_standings_grid(serialized_players_standings_grid):
        """Sérialise la liste des instances des joueurs de la grille."""

        unserialized_players_standings_grid = []
        for serialized_player_standings_grid in serialized_players_standings_grid:
            unserialized_player_standings_grid = PlayerStandingsGrid.unserialize_player_standings_grid(
                serialized_player_standings_grid
            )
            unserialized_players_standings_grid.append(unserialized_player_standings_grid)
        return unserialized_players_standings_grid

    @staticmethod
    def unserialize_player_standings_grid(serialized_player_standings_grid):
        """Convertit le joueur sérialisé de la grille en instance."""
        unserialized_player_standings_grid = PlayerStandingsGrid(
            player_rank=serialized_player_standings_grid["player_rank"],
            player_name=serialized_player_standings_grid["player_name"],
            rounds_scores=serialized_player_standings_grid["rounds_scores"],
            exempted=serialized_player_standings_grid["exempted"],
            rounds_opponents=serialized_player_standings_grid["rounds_opponents"],
            player_id=serialized_player_standings_grid["player_id"],
            tournament_id=serialized_player_standings_grid["tournament_id"],
            closed=serialized_player_standings_grid["closed"]
        )
        return unserialized_player_standings_grid

    def __str__(self):
        """Représentation de l'objet joueur de la grille des scores sous forme de chaîne de caractères."""
        player_standings_grid: str = \
            f"Place du joueur dans le tournoi : {self.player_rank}\n"\
            f"Nom du joueur : {self.player_name}\n"\
            f"Scores du joueur : {self.rounds_scores}\n"\
            f"Exempté lors du tournoi : {self.exempted}\n"\
            f"Adversaires du joueur: {self.rounds_opponents}\n"\
            f"Identifiant du joueur : {self.player_id}\n"\
            f"Identifiant du tournoi : {self.tournament_id}\n"\
            f"Archivé : {self.closed}"
        return player_standings_grid

    @staticmethod
    def serialize_players_standings_grid(players_standings_grid):
        """Sérialise la liste des instances des joueurs de la grille."""

        serialized_players_standings_grid = []
        for player_standings_grid in players_standings_grid:
            serialized_player_standings_grid = PlayerStandingsGrid.serialize_player_standings_grid(
                player_standings_grid
            )
            serialized_players_standings_grid.append(serialized_player_standings_grid)
        return serialized_players_standings_grid

    def serialize_player_standings_grid(self):
        """Sérialise l'instance du joueur de la grille dans un dictionnaire."""
        serialized_player_standings_grid: dict = {
            "player_rank": self.player_rank,
            "player_name": self.player_name,
            "rounds_scores": self.rounds_scores,
            "exempted": self.exempted,
            "rounds_opponents": self.rounds_opponents,
            "player_id": self.player_id,
            "tournament_id": self.tournament_id,
            "closed": self.closed
        }
        return serialized_player_standings_grid

    @staticmethod
    def save_players_standings_grid(players_standings_grid):
        """Insère les joueurs sérialisés du tournoi dans la table players_standings_grid_table
        et retourne la liste d'id des joueurs de la grille."""
        serialized_players_standings_grid = []
        for player_standings_grid in players_standings_grid:
            serialized_player_standings_grid = PlayerStandingsGrid.serialize_player_standings_grid(
                player_standings_grid
            )
            serialized_players_standings_grid.append(serialized_player_standings_grid)

        players_standings_grid_id: int = PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.insert_multiple(
            serialized_players_standings_grid
        )
        return players_standings_grid_id

    @staticmethod
    def get_open_players_standings_grid():
        """Retourne la liste des joueurs en cours."""
        players_standings_grid_query = db_functions.Query()
        open_players_standings_grid = PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.search(players_standings_grid_query.closed == False) # ATTENTION NE FONCTIONNE PAS AVEC le type booléen (is)
        if open_players_standings_grid:
            return open_players_standings_grid

    @staticmethod
    def get_player_standings_grid_id(player_id):
        """Retourne l'id du joueur de la grille du tournoi en cours par statut et id de joueur."""
        players_standings_grid_query = db_functions.Query()
        player_standings_grid = PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.get(players_standings_grid_query.closed == False and players_standings_grid_query.player_id == player_id)
        player_standings_grid_id = player_standings_grid.doc_id
        return player_standings_grid_id

    @staticmethod
    def get_player_standings_grid(player_standings_grid_id):
        """Retourne le joueur de la grille du tournoi cherché par id."""
        serialized_player_standings_grid = PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.get(doc_id=player_standings_grid_id)
        return serialized_player_standings_grid

    @staticmethod
    def update_player_standings_grid(label, field_to_update, player_id):
        """Met à jour la fiche du joueur."""
        player_standings_grid_id = PlayerStandingsGrid.get_player_standings_grid_id(player_id)
        PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.update({label: field_to_update}, doc_ids=[player_standings_grid_id])

    @staticmethod
    def close_players_standings_grid():
        """Clôture les fiches des joueurs en cours."""
        PlayerStandingsGrid.PLAYERS_STANDINGS_GRID_TABLE.update({"closed": True})
