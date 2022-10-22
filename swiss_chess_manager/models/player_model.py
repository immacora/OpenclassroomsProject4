from tinydb import TinyDB, Query


class Player:
    """Player."""

    DB_CONNECT = TinyDB("db.json")
    PLAYERS_TABLE = DB_CONNECT.table('players')
    USER = Query()
    DOC_ID = 0

    def __init__(self, lastname, firstname, date_of_birth, gender, rating):
        """Initialise le joueur, la bdd."""
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.rating: int = rating
        self.player_id: int = 0

    @staticmethod
    def get_player_by_id(player_id):
        """Cherche le joueur sérialisé de la bdd par son id et le retourne,
        Initialise l'id du document dans l'attribut de classe."""
        db_serialized_player = Player.PLAYERS_TABLE.get(doc_id=player_id)
        Player.DOC_ID = player_id
        return db_serialized_player

    @staticmethod
    def unserialize_player(serialized_player):
        """Convertit le joueur sérialisé de la bdd en instance."""
        unserialized_player = Player(lastname=serialized_player["lastname"], firstname=serialized_player["firstname"], date_of_birth=serialized_player["date_of_birth"], gender=serialized_player["gender"], rating=serialized_player["rating"])
        return unserialized_player

    @staticmethod
    def update_player(label, field_to_update, player_id):
        """Met à jour la fiche du joueur sélectionné."""
        Player.PLAYERS_TABLE.update({label: field_to_update}, doc_ids=[player_id])

    @staticmethod
    def get_all_players():
        return Player.PLAYERS_TABLE.all()

    def __str__(self):
        """Représentation de l'objet (datas du joueur) sous forme de chaîne de caractères."""
        player: str = f"Prénom : {self.lastname}\n Nom : {self.firstname}\n Né(e) le : {self.date_of_birth}\n Genre : {self.gender}\n Classement : {self.rating}"
        return player

    def serialize_player(self):
        """Sérialise l'instance du joueur dans un dictionnaire pour insertion des datas dans la bdd)."""
        serialized_player: dict = {"lastname": self.lastname, "firstname": self.firstname, "date_of_birth": self.date_of_birth, "gender": self.gender, "rating": self.rating}
        return serialized_player

    def save_player(self):
        """Insère le joueur dans la base de données et assigne l'id retourné à l'instance du joueur."""
        player_id: int = Player.PLAYERS_TABLE.insert(self.serialize_player())
        self.player_id = player_id



