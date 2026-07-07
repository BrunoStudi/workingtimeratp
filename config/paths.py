import sys
from pathlib import Path

# ================= RESSOURCES EMBARQUÉES =================
def resource_path(relative_path):
    """Chemin pour les fichiers embarqués avec PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent

    return str(Path(base_path) / relative_path)


# ================= DONNÉES UTILISATEUR =================
APP_DATA_DIR = Path.home() / "AppData" / "Local" / "WorkingTimeRatp"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR = APP_DATA_DIR / "data"
CONFIG_DIR = APP_DATA_DIR / "config"

DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

DEPANNAGE_FILE = DATA_DIR / "depannage.json"
MATERIELS_FILE = DATA_DIR / "materiels.json"
CONSOMMABLES_FILE = DATA_DIR / "consommables.jsonl"
DATA_FILE = DATA_DIR / "data.jsonl"
DATA_IA = DATA_DIR / "data_ia.csv"
USER_FILE = DATA_DIR / "user.json"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
DASHBOARD_CONFIG_FILE = CONFIG_DIR / "dashboard_config.json"