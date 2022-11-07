from swiss_chess_manager.models import db_functions


class TournamentModel:
    """Tournament."""

    TOURNAMENTS_TABLE = db_functions.tournaments_table()

    def __init__(self, name, location, start_date, end_date, players, rounds_number, cadence, description,
                 closed=False):
        """Initialise le tournois."""
        self.name: str = name
        self.location: str = location
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.players: list = players
        self.rounds_number: int = rounds_number
        self.cadence: float = cadence
        self.description = description


        ########## CALCUL SELON NB ROUNDS/TOURS #############
        self.matchs_number: int  # . Chaque match consiste en une paire de joueurs avec un champ de résultats pour chaque joueur.
        ####################################################

        ########## LISTE DES RONDES/TOURS/ROUNDS (Rapport???)#############
        self.rounds: list  # Tournées/Tours(list) : liste des instances rondes. / Les matchs multiples???? doivent être stockés sous forme de liste sur l'instance du tour. / Chaque tour(round) est une liste de matchs
        ####################################################

        self.closed = closed

    @staticmethod
    def get_tournament_by_id(tournament_id):
        """Cherche le tournoi sérialisé de la db par son id et le retourne."""
        db_serialized_tournament = TournamentModel.TOURNAMENTS_TABLE.get(doc_id=tournament_id)
        return db_serialized_tournament

    @staticmethod
    def get_open_tournament():
        """Cherche le tournoi en cours retourne son id."""
        tournament_query = db_functions.Query()
        open_tournament = TournamentModel.TOURNAMENTS_TABLE.get(tournament_query.closed == False)#ATTENTION NE FONCTIONNE PAS AVEC le type booléen (is)
        if open_tournament:
            return open_tournament.doc_id

    @staticmethod
    def get_all_tournaments():
        """Initialise la liste des tournois avec leur id et la retourne."""
        tournaments = db_functions.get_all_documents(TournamentModel.TOURNAMENTS_TABLE.all(), "tournament_id")
        return tournaments

    @staticmethod
    def unserialize_tournament(serialized_tournament):
        """Convertit le tournoi sérialisé en instance."""
        unserialized_tournament = TournamentModel(
            name=serialized_tournament["name"],
            location=serialized_tournament["location"],
            start_date=serialized_tournament["start_date"],
            end_date=serialized_tournament["end_date"],
            players=serialized_tournament["players"],
            rounds_number=serialized_tournament["rounds_number"],
            cadence=serialized_tournament["cadence"],
            description=serialized_tournament["description"],
            closed=serialized_tournament["closed"]
        )
        return unserialized_tournament

    @staticmethod
    def close_tournament(tournament_id):
        """Cloturer le tournoi."""
        TournamentModel.TOURNAMENTS_TABLE.update({"closed": True}, doc_ids=[tournament_id])

    def __str__(self):
        """Représentation de l'objet tournoi sous forme de chaîne de caractères."""
        tournament: str = f"Nom : {self.name}\n " \
                          f"Lieu : {self.location}\n " \
                          f"Date de début : {self.start_date}\n " \
                          f"Date de fin : {self.end_date}\n " \
                          f"Joueurs : {self.players}\n " \
                          f"Nombre de tours : {self.rounds_number}\n " \
                          f"Cadence : {self.cadence}\n " \
                          f"Description : {self.description}\n " \
                          f"Archivé : {self.closed}"
        return tournament

    def serialize_tournament(self):
        """Sérialise l'instance du joueur dans un dictionnaire."""
        serialized_tournament: dict = {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": self.players,
            "rounds_number": self.rounds_number,
            "cadence": self.cadence,
            "description": self.description,
            "closed": self.closed
        }
        return serialized_tournament

    def save_tournament(self):
        """Insère le tournoi dans la table tournaments et retourne son id."""
        tournament_id: int = TournamentModel.TOURNAMENTS_TABLE.insert(self.serialize_tournament())
        return tournament_id
