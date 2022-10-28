import os

from tinydb import TinyDB, Query, where


class TournamentModel:
    """Tournament."""

    repertoire_courant = os.getcwd()
    db_path = os.path.join(repertoire_courant, "data", "db.json")
    DB = TinyDB(db_path)
    TOURNAMENTS_TABLE = DB.table("tournaments")

    def __init__(self, name, location, start_date, end_date, players, rounds_number, cadence, description):
        """Initialise le tournois."""
        self.name: str = name
        self.location: str = location
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.players: list = players
        self.rounds_number: int = rounds_number
        self.cadence: float = cadence
        self.description = description

    def __str__(self):
        """Représentation de l'objet (datas du tournoi) sous forme de chaîne de caractères."""
        tournament: str = f"Nom : {self.name}\n Lieu : {self.location}\n Date de début : {self.start_date}\n Date de fin : {self.end_date}\n Joueurs : {self.players}\n Nombre de tours : {self.rounds_number}\n Cadence : {self.cadence}\n Description : {self.description}"
        return tournament

    def serialize_tournament(self):
        """Sérialise l'instance du joueur dans un dictionnaire pour insertion des datas dans la db."""
        serialized_tournament: dict = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": self.players,
            "rounds_number": self.rounds_number,
            "cadence": self.cadence,
            "description": self.description
        }
        return serialized_tournament

    def save_tournament(self):
        """Insère le tournoi dans la base de données et retourne son id."""
        tournament_id: int = TournamentModel.TOURNAMENTS_TABLE.insert(self.serialize_tournament())
        return tournament_id

    @staticmethod
    def get_tournament_by_id(tournament_id):
        """Cherche le tournoi sérialisé de la db par son id et le retourne."""
        db_serialized_tournament = TournamentModel.TOURNAMENTS_TABLE.get(doc_id=tournament_id)
        return db_serialized_tournament

    @staticmethod
    def unserialize_tournament(serialized_tournament):
        """Convertit le tournoi sérialisé en instance."""
        unserialized_player = TournamentModel(
            name=serialized_tournament["name"],
            location=serialized_tournament["location"],
            start_date=serialized_tournament["start_date"],
            end_date=serialized_tournament["end_date"],
            players=serialized_tournament["players"],
            rounds_number=serialized_tournament["rounds_number"],
            cadence=serialized_tournament["cadence"],
            description=serialized_tournament["description"]
        )
        return unserialized_player

    @staticmethod
    def get_all_tournaments():
        """Charge le contenu de la PLAYERS_TABLE et insère l'id de chaque document dans la liste renvoyée."""
        tournaments = TournamentModel.TOURNAMENTS_TABLE.all()
        tournaments_list = []
        for tournament in tournaments:
            tournament["tournament_id"] = tournament.doc_id
            tournaments_list.append(tournament)
        return tournaments_list
