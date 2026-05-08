from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DEPANNAGE_FILE = DATA_DIR  / "depannage.json"
MATERIELS_FILE = DATA_DIR / "materiels.json"
CONSOMMABLES_FILE = DATA_DIR / "consommables.jsonl"
DATA_FILE = DATA_DIR / "data.jsonl"
DATA_IA = DATA_DIR / "data_ia.csv"
USER_FILE = DATA_DIR / "user.json"

SETTINGS_FILE = DATA_DIR / "config" / "settings.json"
DASHBOARD_CONFIG_FILE = DATA_DIR / "config" / "dashboard_config.json"