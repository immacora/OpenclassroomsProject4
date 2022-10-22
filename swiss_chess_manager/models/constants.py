"""Constants. ATTENTION LES CONSTANTES MAIN_MENU, PLAYERS_MENU, TOURNAMENTS_MENU et REPORT_MENU NE SONT PAS LIEES ENTRE ELLES (cf.
menu_controller.py -> fonction find_selected_option(self, option) """

# listes de tuple (immutables) non liés
MAIN_MENU = [
    "\n----- SWISS CHESS MANAGER MENU -----\n",
    [
        (1, "Joueurs\n"),
        (2, "Tournois\n"),
        (3, "Rapports\n"),
        (4, "Quitter\n")
    ]
]

PLAYERS_MENU = [
    "\n----- MENU JOUEURS -----\n",
    [
        (1, "Créer un nouveau joueur\n"),
        (2, "Modifier la fiche d'un joueur\n"),
        (3, "Afficher la liste des joueurs\n"),
        (4, "Retourner au menu principal\n")
    ]
]

TOURNAMENTS_MENU = [
    "\n----- MENU TOURNOIS -----\n",
    [
        (1, "Créer un nouveau tournoi\n"),
        (2, "Afficher un rapport\n"),
        (3, "Retourner au menu principal\n")
    ]
]

REPORT_MENU = [
    "\n----- MENU RAPPORTS -----\n",
    [
        (1, "Afficher un rapport\n"),
        (2, "Retourner au menu principal\n")
    ]
]