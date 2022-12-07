"""Module de fonctions d'échange avec la base de données."""
import os

from tinydb import TinyDB, Query


def db_connect():
    """Retourne la connexion à la base de données."""
    repertoire_courant = os.getcwd()
    db_path = os.path.join(repertoire_courant, "data", "db.json")
    db = TinyDB(db_path)
    return db


def players_table():
    """Retourne la table des joueurs."""
    db = db_connect()
    return db.table("players")


def tournaments_table():
    """Retourne la table des tournois."""
    db = db_connect()
    return db.table("tournaments")


def players_standings_grid_table():
    """Retourne la table des joueurs de grille des scores du tournoi."""
    db = db_connect()
    return db.table("players_standings_grid")


def get_all_documents(db_documents, document_id):
    """Charge le contenu de la table donnée en paramètre et insère l'id de chaque document dans la liste renvoyée."""
    documents: list = []
    for document in db_documents:
        document[document_id] = document.doc_id
        documents.append(document)
    return documents


def query():
    """Retourne l'objet requête."""
    return Query()
