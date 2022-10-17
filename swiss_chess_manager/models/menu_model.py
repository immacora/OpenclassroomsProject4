class Menu:
    """Menu."""

    def __init__(self, menu: list):
        """Initialise le menu (constante reçue en paramètre)."""
        self.menu = menu

    def __str__(self):
        """Représentation de l'objet sous forme de chaîne de caractères (retourne le titre et les options de la constante menu)."""
        str_options = ""
        for option in self.get_menu_options():
            option_number = str(option[0])
            option_title = option[1]
            str_option = option_number + " : " + option_title
            str_options += str_option
        str_menu = self.get_menu_title() + str_options
        return str_menu

    def get_menu_title(self):
        menu_title = self.menu[0]
        return menu_title

    def get_menu_options(self):
        menu_options = self.menu[1]
        return menu_options

    def get_options_numbers(self):
        """Retourne la liste des numéros d'option du menu à comparer au choix de l'utilisateur."""
        options_numbers = []
        for option in self.get_menu_options():
            option_number = option[0]
            options_numbers.append(option_number)
        return options_numbers

    def get_options_title(self):
        """Retourne la liste des titres d'option du menu à comparer au choix de l'utilisateur."""
        options_title = []
        for title in self.get_menu_options():
            option_title = title[1]
            options_title.append(option_title)
        return options_title
