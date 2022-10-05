"""Gestion des erreurs"""

def to_integer(answer_str):
    """Renvoie None si la valeur n'est pas un entier"""
    try:
        value = int(answer_str)
        return value
    except ValueError:
        print ("ERREUR: Vous devez rentrer un chiffre")
