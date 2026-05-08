import json
import customtkinter as ctk
from config.paths import SETTINGS_FILE


def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"theme": "Dark"}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def apply_theme(theme):
    ctk.set_appearance_mode(theme)
