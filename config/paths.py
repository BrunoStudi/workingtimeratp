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

# =========== Base de dépannage locale ====================
DEPANNAGE_FILE = DATA_DIR / "depannage.json"

# =========== Base dépannage partagée EK1 =================
DEPANNAGE_NETWORK_FILE = Path(
    r"S:\EK1\03-PARTAGE\AME\depannage.json"
)

DEPANNAGE_NETWORK_IMAGES_DIR = Path(
    r"S:\EK1\03-PARTAGE\AME\wtratp_pictures"
)

MATERIELS_FILE = DATA_DIR / "materiels.json"
CONSOMMABLES_FILE = DATA_DIR / "consommables.jsonl"
EXCEL_RESEAU = r"S:\EK1\03-PARTAGE\AME\articles-ref.xlsx"
DATA_FILE = DATA_DIR / "data.jsonl"
DATA_IA = DATA_DIR / "data_ia.csv"
USER_FILE = DATA_DIR / "user.json"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
DASHBOARD_CONFIG_FILE = CONFIG_DIR / "dashboard_config.json"

# ================= RACCOURCIS PERSONNALISÉS =================
SHORTCUTS_FILE = CONFIG_DIR / "shortcuts.json"
SHORTCUTS_ICONS_DIR = APP_DATA_DIR / "shortcuts_icons"
SHORTCUTS_ICONS_DIR.mkdir(parents=True, exist_ok=True)