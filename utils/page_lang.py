import customtkinter as ctk

from utils.translations import TRANSLATIONS

class PageLang:
    def __init__(self, app):
        self.app = app

    def t(self, key: str) -> str:
        # récupère la langue depuis l'application
        lang = getattr(self.app, "lang", "francais")
        return TRANSLATIONS.get(lang, {}).get(key, key)
