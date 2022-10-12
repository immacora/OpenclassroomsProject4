from swiss_chess_manager.models import constants
from swiss_chess_manager.models.menu_model import Menu
from swiss_chess_manager.views.menu_view import MenuView
from swiss_chess_manager.controllers.my_exceptions import is_int


class MenuController:
    """MenuController."""

    def __init__(self, model, view):
        """Initialise le modèle et la vue."""
        self.model = model
        self.view = view

    def run_interactive_menu(self):
        """Affiche le menu du modèle et récupère ses options,
        Demande la saisie d'une option à l'utilisateur via la vue,
        Vérifie le type et la correspondance des numéros d'option (si pb : fonction recursive s'appelle, sinon :)
        Retourne le choix de l'utilisateur///OU DIRIGE VERS LE MENU CHOISI."""
        display_menu = Menu.str_menu(self.model)
        print(display_menu)
        menu_options_numbers = Menu.get_options_numbers(self.model)

        user_option_str = MenuView.ask_user_option(self.view)

        user_option_int = is_int(user_option_str)

        if not user_option_int:
            return self.run_interactive_menu()
        elif user_option_int not in menu_options_numbers:
            print("ERREUR: Vous devez saisir un chiffre du menu")
            return self.run_interactive_menu()
        else:
            print("Diriger vers le menu choisi :" + str(user_option_int))
            return user_option_int





"""def run_swiss_chess_manager(self):
    Lance le programme
    pass"""
