import pandas as pd
import pyinputplus as pyip


class TournamentView:
    """Tournoi."""

    def __init__(self):
        pass

    @staticmethod
    def name():
        """Saisie du nom du tournoi."""
        return pyip.inputStr(
            prompt="Saisir le nom du tournoi (caractères spéciaux interdits): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def location():
        """Saisie du lieu du tournoi."""
        return pyip.inputStr(
            prompt="Saisir le lieu du tournoi (caractères spéciaux interdits): ",
            blank=False,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def start_date():
        """Saisie de la date de début du tournoi."""
        return pyip.inputDate(prompt="Saisir la date de début du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def end_date():
        """Saisie de la date de fin du tournoi."""
        return pyip.inputDate(prompt="Saisir la date de fin du tournoi au format (YYYY/MM/DD): ")

    @staticmethod
    def cadence():
        """Saisie du type de contrôle du temps du tournoi (bullet, blitz ou coup rapide)."""
        cadence = pyip.inputMenu(
            choices=["Bullet", "Blitz", "Coup rapide"],
            prompt="\nSaisir le numéro correspondant à la cadence du tournoi:\n", numbered=True
        )
        return cadence

    @staticmethod
    def description():
        """Saisie (facultative) des remarques générales sur le tournoi."""
        return pyip.inputStr(
            prompt="Saisir les remarques générales sur le tournoi (caractères spéciaux interdits):\n",
            blank=True,
            blockRegexes=[r"^[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]$"]
        )

    @staticmethod
    def players_number():
        """Saisie du nombre de joueurs du tournoi (8 par défaut, min 2)."""
        players_number = 8
        players_number_input: int = pyip.inputNum(
            prompt="Saisir le nombre de joueurs ou valider (8 par défaut)",
            blank=True, min=2
        )
        if isinstance(players_number_input, int):
            players_number = players_number_input
        else:
            print(players_number)
        return players_number

    @staticmethod
    def rounds_number():
        """Saisie du nombre de tours (rondes) du tournoi (4 par défaut, min 1)."""
        rounds_number = 4
        rounds_number_input: int = pyip.inputNum(
            prompt="Saisir le nombre de tours ou valider (4 par défaut)",
            blank=True, min=1
        )
        if isinstance(rounds_number_input, int):
            rounds_number = rounds_number_input
        else:
            print(rounds_number)
        return rounds_number

    @staticmethod
    def field_to_edit():
        """Retourne le champ à modifier ou la demande d'annulation."""
        return pyip.inputMenu(
            choices=["Nom", "Lieu", "Date de début", "Date de fin", "Nombre de tours", "Cadence",
                     "Description", "Annuler et quitter le programme"],
            prompt="\nSaisir un numéro pour corriger les données du tournoi ou quitter le programme :\n", numbered=True
        )

    @staticmethod
    def ask_save_tournament():
        """Demande de sauvegarde des données dans le tournoi."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous sauvegarder ce tournoi ? "
                   "Saisir 'N' (no) pour modifier un champ (liste des joueurs exclue) ou 'Y' (yes) pour sauvegarder "
                   "(Attention, aucune modification ne pourra être effectuée ensuite.)\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_save_player_tournament():
        """Demande d'enregistrement du joueur dans le tournoi."""
        return pyip.inputYesNo(
            prompt="\nConfirmer l'enregistrement du joueur dans le tournoi :\n"
                   "Saisir 'N' (no) pour revenir à la saisie ou 'Y' (yes) pour sauvegarder "
                   "(Attention, la liste des joueurs du tournoi ne sera plus modifiable)\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_play_round():
        """Demande de lancement du tour."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous lancer le tour (le lancement déclenchera l'horodatage) ?"
                   " Saisir 'Y' (yes) pour le lancer ou 'N' (no) pour quitter le programme\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_for_pairing():
        """Demande de création de l'appariement."""
        return pyip.inputYesNo(
            prompt="Voulez-vous créer l'appariement du tour ? "
                   "Saisir 'Y' (yes) pour le lancer ou 'N' (no) pour revenir au menu\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_close_tournament():
        """Demande de clôture du tournoi."""
        return pyip.inputYesNo(
            prompt="\nVoulez-vous clôturer le tournoi ? "
                   "(Attention, aucune modification ne pourra être effectuée ensuite) 'Y' (yes) / 'N' (no) ?\n",
            yesVal="Y", noVal="N"
        )

    @staticmethod
    def ask_sort():
        """Demande le type de tri (alphabétique ou placement)."""
        sort = pyip.inputMenu(
            choices=["Ordre alphabétique", "Placement"],
            prompt="\nAfficher les joueurs par:\n", numbered=True
        )
        return sort

    @staticmethod
    def ask_score(player_name):
        """Demande la saisie du score."""
        return pyip.inputMenu(
            choices=["Gagnant", "Perdant", "Match nul"],
            prompt=f"\nSaisir le résultat du joueur {player_name} (Attention, "
                   f"aucune modification ne pourra être effectuée ensuite):\n", numbered=True
        )

    @staticmethod
    def ask_exempted_score(player_name):
        """Demande la saisie du score du joueur exempté (de 0 à 1 selon le règlement du tournoi)."""
        return pyip.inputFloat(
            prompt=f"\nSaisir le score attribué au joueur exempté {player_name} (de 0 à 1): ", min=0, max=1
        )

    @staticmethod
    def ask_close_round():
        """Demande de clôture du tour."""
        return pyip.inputYesNo(
            prompt="\nSaisir 'Y' (yes) pour terminer le tour\n",
            yesVal="Y"
        )

    @staticmethod
    def ask_tournament_player_id():
        """Demande de saisie de l'id du joueur à inclure dans le tournoi."""
        tournament_player_id: int = pyip.inputNum(
            prompt="\nSaisir l'identifiant du joueur à inclure dans le tournoi: ", min=1
        )
        return tournament_player_id

    @staticmethod
    def select_tournament_player():
        """Demande de sélection ou de création du joueur."""
        return pyip.inputChoice(
            prompt="Saisir 'S' pour sélectionner un joueur dans la liste, ou 'C' pour créer un joueur.\n",
            choices=["S", "C"]
        )

    @staticmethod
    def display_tournaments(tournaments):
        """Affiche le dataframe de la liste des tournois (index = identifiants) et le retourne."""
        columns_names = ["name", "location", "start_date", "end_date", "cadence", "description",
                         "players", "rounds_number", "tournament_id", "closed"]
        tournaments_df = pd.DataFrame(tournaments, columns=columns_names)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        tournaments_df.rename(
            columns={
                "name": "Nom",
                "location": "Lieu",
                "start_date": "Date de début",
                "end_date": "Date de fin",
                "cadence": "Cadence",
                "description": "Description",
                "players": "Joueurs",
                "rounds_number": "Nombre de tours",
                "closed": "Archivé",
                "tournament_id": "Identifiant"
            },
            inplace=True)
        tournaments_df.set_index("Identifiant", inplace=True)
        print(f"\nListe de tous les tournois :\n{tournaments_df}")
        return tournaments_df

    @staticmethod
    def display_db_players_by_rating(sorted_tournament_players):
        """Affiche le dataframe des joueurs de la db dans le tournoi."""
        players_df = pd.DataFrame(sorted_tournament_players)
        players_df.rename(
            columns={"lastname": "Prénom", "firstname": "Nom", "date_of_birth": "Date de naissance", "gender": "Genre",
                     "rating": "Classement", "player_id": "Id"}, inplace=True)
        players_df = players_df.reindex(
            columns=["Classement", "Nom", "Prénom", "Date de naissance", "Genre", "Id"]
        )
        players_df.set_index("Classement", inplace=True)

        sorted_df = players_df.sort_values(by=["Classement"], ascending=False)
        print(f"Liste des joueurs triée par classement:\n{sorted_df}")

    @staticmethod
    def display_rounds(rounds):
        """Affiche le dataframe des tours du tournoi et le retourne (index = round_number)."""
        columns_names = ["round_number", "round_name", "matches_number", "start_datetime", "end_datetime", "closed"]
        rounds_df = pd.DataFrame(rounds, columns=columns_names)
        rounds_df.rename(
            columns={"round_number": "Numéro de tour",
                     "round_name": "Nom du tour",
                     "matches_number": "Nombre de matchs",
                     "start_datetime": "Date et heure de début",
                     "end_datetime": "Date et heure de fin",
                     "closed": "Archivé"},
            inplace=True
        )
        rounds_df.set_index("Numéro de tour", inplace=True)
        rounds_df = rounds_df.fillna(0)
        rounds_df["Nombre de matchs"] = rounds_df["Nombre de matchs"].astype(int)
        print(f"Liste des tours du tournoi:\n{rounds_df}")

        return rounds_df

    @staticmethod
    def display_pairing(round_name, pairing):
        """Affiche le dataframe de l'appariement des joueurs et le retourne (index = Match)."""
        columns_names = ["Match", "Joueur 1", "Joueur 2"]
        pairing_df = pd.DataFrame(pairing, columns=columns_names)
        pairing_df.set_index("Match", inplace=True)
        print(f"\n{round_name}, appariement :\n\n{pairing_df}")
        return pairing_df

    @staticmethod
    def display_tournament_results(sort, players_standings_grid):
        """Affiche la grille de score des joueurs du tournoi selon le tri demandé et le retourne (index = Placement)."""
        columns_names = ["player_rank", "player_name", "player_id", "tournament_score"]
        players_standings_grid_results_df = pd.DataFrame(players_standings_grid, columns=columns_names)
        players_standings_grid_results_df.rename(
            columns={
                "player_rank": "Placement",
                "player_name": "Nom",
                "player_id": "Joueur n°",
                "tournament_score": "Score"
            },
            inplace=True)
        players_standings_grid_results_df.set_index("Placement", inplace=True)
        if sort == "Ordre alphabétique":
            sorted_players_results_df = players_standings_grid_results_df.sort_values(by=["Nom"])
            print(f"Liste des joueurs triée par ordre alphabétique:\n{sorted_players_results_df}")
            return sorted_players_results_df
        elif sort == "Placement":
            sorted_players_results_df = players_standings_grid_results_df.sort_values(by=["Placement"])
            print(f"Liste des joueurs triée par placement:\n{sorted_players_results_df}")
            return sorted_players_results_df
        else:
            print("ERREUR: L'affichage a échoué")

    @staticmethod
    def display_round_results(current_round_name, players, round_player_exempt_name):
        """Affiche le dataframe des résultats du tour et le retourne (index = Placement)."""
        players_round_results_df = pd.DataFrame(players)
        players_round_results_df.set_index("Placement", inplace=True)
        sorted_players_round_results_df = players_round_results_df.sort_values(by=["Placement"])
        print(f"\n{current_round_name}, résultat (Joueur exempté : {round_player_exempt_name}) :\n"
              f"{sorted_players_round_results_df}")
        return sorted_players_round_results_df

    @staticmethod
    def display_matches(tournament_matches):
        """Affiche le dataframe des matchs du tournoi et le retourne."""
        matches_df = pd.DataFrame(tournament_matches)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        matches_df.set_index("Nom du tour", inplace=True)
        print(f"Liste des matchs du tournoi:\n{matches_df}")
        return matches_df

    @staticmethod
    def ask_tournament_display_option():
        """Demande l'option d'affichage de détail du tournoi sélectionné (joueurs, tours, match)."""
        tournament_display_option = pyip.inputMenu(
            choices=[
                "Liste des joueurs du tournoi",
                "Liste des tours du tournoi",
                "Liste des matchs du tournoi"
            ],
            prompt="Afficher le rapport :\n", numbered=True)
        return tournament_display_option

    def tournament_input(self):
        """Demande la saisie de la fiche du tournoi et renvoie le dictionnaire des datas."""
        print("\nCréer un nouveau tournoi: ")
        name = self.name()
        location = self.location()
        start_date = self.start_date()
        end_date = self.end_date()
        cadence = self.cadence()
        description = self.description()
        players_number = self.players_number()
        rounds_number = self.rounds_number()

        tournament_input: dict = {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "cadence": cadence,
            "description": description,
            "players": players_number,
            "rounds_number": rounds_number
        }
        return tournament_input
