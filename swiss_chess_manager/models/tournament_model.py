from swiss_chess_manager.models import db_functions


class TournamentModel:
    """Tournament."""

    TOURNAMENTS_TABLE = db_functions.tournaments_table()

    def __init__(self, name, location, start_date, end_date, cadence, description,
                 players, rounds_number, rounds, standings_grid, closed=False):
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
        self.standings_grid: dict = standings_grid
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
    def get_all_tournaments():
        """Retourne la liste des tournois et leur id."""
        tournaments = db_functions.get_all_documents(TournamentModel.TOURNAMENTS_TABLE.all(), "tournament_id")
        return tournaments

    @staticmethod
    def unserialize_tournament(serialized_tournament):
        """Convertit le tournoi sérialisé en instance."""
        unserialized_rounds = []
        for serialized_round in serialized_tournament["rounds"]:
            unserialized_rounds.append(RoundModel.unserialize_round(serialized_round))
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
            standings_grid=serialized_tournament["standings_grid"],
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
            serialized_rounds.append(RoundModel.serialize_round(round))
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
            "standings_grid": self.standings_grid,
            "closed": self.closed
        }
        return serialized_tournament

    def save_tournament(self):
        """Insère le tournoi dans la table tournaments et retourne son id."""
        tournament_id: int = TournamentModel.TOURNAMENTS_TABLE.insert(self.serialize_tournament())
        return tournament_id


class RoundModel:
    """Tour (ronde)."""

    TOURNAMENTS_TABLE = db_functions.tournaments_table()

    def __init__(self, round_number, round_name, matchs_number, matchs=None, start_datetime="", end_datetime="",
                 closed=False):
        """Initialise le tour."""
        self.round_number: int = round_number
        self.round_name: str = round_name
        self.matchs_number: int = matchs_number
        self.matchs: list = matchs
        self.start_datetime: str = start_datetime
        self.end_datetime: str = end_datetime
        self.closed = closed

    @staticmethod
    def unserialize_round(serialized_round):
        """Convertit le tour sérialisé en instance."""
        unserialize_round = RoundModel(
            round_number=serialized_round["round_number"],
            round_name=serialized_round["round_name"],
            matchs_number=serialized_round["matchs_number"],
            matchs=serialized_round["matchs"],
            start_datetime=serialized_round["start_datetime"],
            end_datetime=serialized_round["end_datetime"],
            closed=serialized_round["closed"]
        )
        return unserialize_round

    def __str__(self):
        """Représentation de l'objet tour (ronde) sous forme de chaîne de caractères."""
        round: str = f"Tour n° {self.round_number}\n " \
                     f"Nom : {self.round_name}\n " \
                     f"Nombre de matchs : {self.matchs_number}\n " \
                     f"Liste des matchs : {self.matchs}\n " \
                     f"Date et heure de début : {self.start_datetime}\n " \
                     f"Date et heure de fin : {self.end_datetime}\n " \
                     f"Archivé : {self.closed}"
        return round

    def serialize_round(self):
        """Sérialise l'instance du tour dans un dictionnaire."""
        serialized_round: dict = {
            "round_number": self.round_number,
            "round_name": self.round_name,
            "matchs_number": self.matchs_number,
            "matchs": self.matchs,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "closed": self.closed
        }
        return serialized_round
