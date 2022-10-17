from tinydb import TinyDB


class Player:
    """Player."""

    def __init__(self, lastname, firstname, date_of_birth, gender, rating):
        """Initialise le joueur."""
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.rating: int = rating
        players: list = []

    def __str__(self):
        """Représentation de l'objet (datas du joueur) sous forme de chaîne de caractères."""
        player: str = f"Nom : {self.lastname} {self.firstname}\n Né(e) le : {self.date_of_birth}\n Genre : {self.gender}\n Rang : {self.rating}"
        return player

    def serialized_player(self):
        """Sérialise l'instance du joueur dans un dictionnaire pour insertion des datas dans la bdd)."""
        serialized_player = \
            {
                "lastname": self.lastname,
                "firstname": self.firstname,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender,
                "rating": self.rating
            }
        return serialized_player


##################################### test

print("Je suis dans le Player")


