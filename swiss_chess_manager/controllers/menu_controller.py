from swiss_chess_manager.models import constants
from swiss_chess_manager.models.menu_model import Menu
from swiss_chess_manager.views.menu_view import MenuView
from swiss_chess_manager.controllers.my_exceptions import is_int_exception


class MenuController:
    """MenuController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def display_menu(self):
        """Affiche le menu actif, demande la saisie d'une option à l'utilisateur et retourne la valeur saisie."""
        display_menu = Menu.__str__(self.model)
        print(display_menu)
        user_option_str = MenuView.ask_user_option(self.view)
        return user_option_str

    def find_selected_option(self, option):
        """Compare le titre du menu actif du modèle à ceux du fichier de constantes,
        Sélectionne le menu à afficher selon le numéro d'option choisi par l'utilisateur
        ATTENTION LES CONSTANTES NE SONT PAS LIEES"""
        active_menu_title = Menu.get_menu_title(self.model)
        user_option_int = option
        if active_menu_title == constants.MAIN_MENU[0]:
            if user_option_int == 1:
                menu = Menu(constants.PLAYERS_MENU)
                view = MenuView()
                MenuController(menu, view).run_interactive_menu()
            elif user_option_int == 2:
                menu = Menu(constants.TOURNAMENTS_MENU)
                view = MenuView()
                MenuController(menu, view).run_interactive_menu()
            elif user_option_int == 3:
                exit()
            else:
                print("ERREUR: Mettre à jour les constantes de menu")
        elif active_menu_title == constants.PLAYERS_MENU[0]:
            if user_option_int == 1:
                print("Créer un nouveau joueur (saisir exit() pour quitter ou yyyy pour revenir au menu principal)")
            elif user_option_int == 2:
                print("option 2 : Modifier les données d'un joueur (saisir exit() pour quitter ou yyyy pour revenir au menu principal)")
            elif user_option_int == 3:
                print("option 3 : Afficher un rapport (saisir exit() pour quitter ou yyyy pour revenir au menu principal)")
            elif user_option_int == 4:
                self.run_swiss_chess_manager()
            else:
                print("ERREUR: Mettre à jour les constantes de menu")
        elif active_menu_title == constants.TOURNAMENTS_MENU[0]:
            if user_option_int == 1:
                print("option 1 : Créer un nouveau tournoi (saisir exit() pour quitter ou yyyy pour revenir au menu principal)")
            elif user_option_int == 2:
                print("option 2 : Afficher un rapport (saisir exit() pour quitter ou yyyy pour revenir au menu principal)")
            elif user_option_int == 3:
                self.run_swiss_chess_manager()
            else:
                print("ERREUR: Mettre à jour les constantes de menu")
        else:
            print("ERREUR DU PROGRAMME : Le menu actif n'a pas été reconnu. Saisir exit() pour quitter")

    def run_interactive_menu(self):
        """Affiche le menu interactif, récupère le numéro de menu saisi par l'utilisateur et le convertit en entier,
        Récupère la liste des n° d'options du menu,
        Vérifie si l'utilisateur a saisi un entier ou un numéro qui ne se trouve pas dans la liste des n° d'options du menu (récursif),
        Appelle la fonction de recherche du menu demandé"""

        user_option_str = self.display_menu()
        user_option_int = is_int_exception(user_option_str)
        menu_options_numbers = Menu.get_options_numbers(self.model)

        if not user_option_int:
            return self.run_interactive_menu()
        elif user_option_int not in menu_options_numbers:
            print("ERREUR: Vous devez saisir un numéro du menu")
            return self.run_interactive_menu()
        else:
            self.find_selected_option(user_option_int)

    def run_swiss_chess_manager(self):
        """Initialise les variables modèle (paramètre = constante MAIN_MENU), vue et controller,
         Lance le programme avec le controlleur (affiche le menu principal."""
        menu = Menu(constants.MAIN_MENU)
        view = MenuView()
        MenuController(menu, view).run_interactive_menu()
