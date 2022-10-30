"""Module de fonctions communes aux controllers."""
import os
from datetime import datetime


def save_report(report):
    date = datetime.now()
    date = date.strftime('%Y-%m-%d-%H-%M-%S')
    csv_name = f"report_{date}.csv"
    repertoire_courant = os.getcwd()
    report_path = os.path.join(repertoire_courant, "reports", csv_name)
    report.to_csv(report_path)
