"""I) Afficher le menu (view)"""
##########################
"""CONSTANTES : TRANSFORMER EN CLASSES"""
MAIN_MENU = {
    1: "Joueurs",
    2: "Tournois",
    3: "Quitter"
}

PLAYERS_MENU = {
    1: "Créer un nouveau joueur",
    2: "Modifier les données d'un joueur",
    3: "Afficher un rapport",
    4: "Retourner au menu principal"
}

TOURNAMENTS_MENU = {
    1: "Créer un nouveau tournoi",
    2: "Afficher un rapport",
    3: "Retourner au menu principal"
}
##########################


##########################
"""FONCTIONS SECONDAIRES"""
def menu_title():
    """Affiche le titre du menu"""
    deco = (
        "\n|####################################################|\n"
        "|                          MENU                      |\n"
        "|####################################################|\n"
    )
    print(deco)

def menu_options(menu_items):
    """Affiche les options du menu"""
    for tab, tab_title in menu_items.items():
        print(tab, ":", tab_title)

##########################

##########################
"""FONCTION PRINCIPALE"""
def display_menu():
    """Affiche le menu."""
    menu_title()
    menu_options(MAIN_MENU)

"""Appel de la fonction principale"""
display_menu()
##########################