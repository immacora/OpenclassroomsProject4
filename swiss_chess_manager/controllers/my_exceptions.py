"""Gestion personnalisée des erreurs"""


def is_int_exception(text: str):
    """Tente de convertir le texte en int et renvoie le chiffre,
    Renvoie False si la valeur n'est pas un entier"""
    try:
        text_int = int(text)
        return text_int
    except ValueError:
        print("ERREUR: Vous devez saisir un chiffre")
        return False