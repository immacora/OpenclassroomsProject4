"""Entry point."""

from models import constants
from models.menu_model import Menu
from controllers.menu_controller import MenuController
from views.menu_view import MenuView


def main():

    """1: Initialise les variables modèle (paramètre = constante MAIN_MENU), vue et controller."""

    menu = Menu(constants.MAIN_MENU)
    view = MenuView()
    swiss_chess_manager = MenuController(menu, view)

    """2: Lance le programme avec le controlleur (affiche le menu interactif principal)"""

    swiss_chess_manager.run_interactive_menu()


if __name__ == "__main__":
    main()
