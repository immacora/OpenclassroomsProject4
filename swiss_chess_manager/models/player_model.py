from swiss_chess_manager.models import db_functions


class PlayerModel:
    """Player."""

    PLAYERS_TABLE = db_functions.players_table()

    def __init__(self, lastname, firstname, date_of_birth, gender, rating):
        """Initialise le joueur."""
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.rating: int = rating

    @staticmethod
    def get_player_by_id(player_id):
        """Cherche le joueur sérialisé de la db par son id et le retourne."""
        db_serialized_player = PlayerModel.PLAYERS_TABLE.get(doc_id=player_id)
        return db_serialized_player

    @staticmethod
    def get_all_players():
        """Initialise la liste des joueurs avec leur id et la retourne."""
        players = db_functions.get_all_documents(PlayerModel.PLAYERS_TABLE.all(), "player_id")
        return players

    @staticmethod
    def update_player(label, field_to_update, player_id):
        """Met à jour la fiche du joueur sélectionné."""
        PlayerModel.PLAYERS_TABLE.update({label: field_to_update}, doc_ids=[player_id])

    @staticmethod
    def unserialize_player(serialized_player):
        """Convertit le joueur sérialisé en instance."""
        unserialized_player = PlayerModel(
            lastname=serialized_player["lastname"],
            firstname=serialized_player["firstname"],
            date_of_birth=serialized_player["date_of_birth"],
            gender=serialized_player["gender"],
            rating=serialized_player["rating"]
        )
        return unserialized_player

    def __str__(self):
        """Représentation de l'objet joueur sous forme de chaîne de caractères."""
        player: str = f"Prénom : {self.lastname}\n " \
                      f"Nom : {self.firstname}\n " \
                      f"Date de naissance : {self.date_of_birth}\n " \
                      f"Genre : {self.gender}\n " \
                      f"Classement : {self.rating} "
        return player

    def serialize_player(self):
        """Sérialise l'instance du joueur dans un dictionnaire."""
        serialized_player: dict = {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "rating": self.rating
        }
        return serialized_player

    def save_player(self):
        """Insère le joueur dans la table players s'il n'existe pas, et retourne son id."""
        if self.player_exist(self.serialize_player()):
            print("ERREUR: Le joueur existe déjà dans la base de données")
        else:
            player_id: int = PlayerModel.PLAYERS_TABLE.insert(self.serialize_player())
            return player_id

    def player_exist(self, serialized_player):
        """Vérifie l'existance du joueur à insérer dans la db.

         Correspondance : nom complet et date de naissance
         Retourne True si c'est un doublon.
         """
        doublon = False
        players = self.get_all_players()
        for player in players:
            if (serialized_player["lastname"] == player["lastname"]) and (serialized_player["firstname"] == player["firstname"]) and (serialized_player["date_of_birth"] == player["date_of_birth"]):
                doublon = True
        return doublon
