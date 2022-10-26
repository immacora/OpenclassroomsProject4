import os

from tinydb import TinyDB, Query, where


class PlayerModel:
    """Player."""

    repertoire_courant = os.getcwd()
    db_path = os.path.join(repertoire_courant, "data", "db.json")
    DB = TinyDB(db_path)
    PLAYERS_TABLE = DB.table("players")
    # USER = Query()

    def __init__(self, lastname, firstname, date_of_birth, gender, rating):
        """Initialise le joueur, la bdd."""
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.rating: int = rating

    def __str__(self):
        """Représentation de l'objet (datas du joueur) sous forme de chaîne de caractères."""
        player: str = f"Prénom : {self.lastname}\n Nom : {self.firstname}\n Date de naissance : {self.date_of_birth}\n Genre : {self.gender}\n Classement : {self.rating}"
        return player

    def serialize_player(self):
        """Sérialise l'instance du joueur dans un dictionnaire pour insertion des datas dans la db."""
        serialized_player: dict = {"lastname": self.lastname, "firstname": self.firstname, "date_of_birth": self.date_of_birth, "gender": self.gender, "rating": self.rating}
        return serialized_player

    def save_player(self):
        """Insère le joueur dans la base de données et retourne son id."""
        player_id: int = PlayerModel.PLAYERS_TABLE.insert(self.serialize_player())
        return player_id

    @staticmethod
    def get_player_by_id(player_id):
        """Cherche le joueur sérialisé de la bdd par son id et le retourne."""
        db_serialized_player = PlayerModel.PLAYERS_TABLE.get(doc_id=player_id)
        return db_serialized_player

    @staticmethod
    def unserialize_player(serialized_player):
        """Convertit le joueur sérialisé en instance."""
        unserialized_player = PlayerModel(lastname=serialized_player["lastname"], firstname=serialized_player["firstname"], date_of_birth=serialized_player["date_of_birth"], gender=serialized_player["gender"], rating=serialized_player["rating"])
        return unserialized_player

    @staticmethod
    def update_player(label, field_to_update, player_id):
        """Met à jour la fiche du joueur sélectionné."""
        PlayerModel.PLAYERS_TABLE.update({label: field_to_update}, doc_ids=[player_id])

    @staticmethod
    def get_all_players():
        """Charge le contenu de la PLAYERS_TABLE et insère l'id de chaque document de la liste renvoyée."""
        players = PlayerModel.PLAYERS_TABLE.all()
        players_list = []
        for player in players:
            player["player_id"] = player.doc_id
            players_list.append(player)
        return players_list
