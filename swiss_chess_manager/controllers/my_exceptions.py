"""Gestion personnalisée des erreurs"""


def is_int(text: str):
    """ Essaie de convertir le texte en int et renvoie le chiffre,
    Renvoie False si la valeur n'est pas un entier"""
    try:
        text_int = int(text)
        return text_int
    except ValueError:
        print("ERREUR: Vous devez rentrer un chiffre")
        return False
