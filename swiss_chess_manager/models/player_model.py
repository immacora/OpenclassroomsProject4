from tinydb import TinyDB, Query


class Player:
    """Player."""
    DB_CONNECT = TinyDB("db.json")
    DB_QUERY = Query()

    def __init__(self, lastname, firstname, date_of_birth, gender, rating):
        """Initialise le joueur, la bdd."""
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.rating: int = rating
        self.player_id: int = 0

    def __str__(self):
        """Représentation de l'objet (datas du joueur) sous forme de chaîne de caractères."""
        player: str = f"Identifiant n° : {self.player_id}\n Nom : {self.lastname} {self.firstname}\n Né(e) le : {self.date_of_birth}\n Genre : {self.gender}\n Rang : {self.rating}"
        return player

    def serialize_player(self):
        """Sérialise l'instance du joueur dans un dictionnaire pour insertion des datas dans la bdd)."""
        serialized_player: dict = {"lastname": self.lastname, "firstname": self.firstname, "date_of_birth": self.date_of_birth, "gender": self.gender, "rating": self.rating}
        return serialized_player

    def insert_player(self):
        """Insère le joueur dans la base de données et assigne l'id retourné à l'instance du joueur."""
        player_id: int = Player.DB_CONNECT.insert(self.serialize_player())
        self.player_id = player_id
