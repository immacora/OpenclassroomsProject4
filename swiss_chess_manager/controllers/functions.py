"""Module commun pour la fonction de sauvegarde."""
import os
from datetime import datetime
from swiss_chess_manager.views.menu_view import MenuView


def save_report(report):
    """Sauvegarde le rapport."""
    if MenuView.ask_save_report() == "Y":
        date = datetime.now()
        date = date.strftime('%Y-%m-%d-%H-%M-%S')
        csv_name = f"report_{date}.csv"
        repertoire_courant = os.getcwd()
        report_path = os.path.join(repertoire_courant, "reports", csv_name)
        report.to_csv(report_path)
        print("Le rapport sera consultable depuis le répertoire 'reports' après l'arrêt du programme")
