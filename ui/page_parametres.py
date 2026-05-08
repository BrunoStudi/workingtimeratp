import customtkinter as ctk

from utils.settings import load_settings, apply_theme, save_settings
from utils.page_lang import PageLang

class PageParams(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Création de l'utilitaire de traduction
        self.lang_util = PageLang(app)

        # --- Header ---
        self.header = ctk.CTkFrame(self, border_width=1, border_color="blue", fg_color="#1E5CC4", height=60)
        self.header.pack(fill="x", padx=5, pady=5)

        self.header_label = ctk.CTkLabel(
            self.header, 
            text=self.lang_util.t("parametres_application"), 
            font=("Roboto", 24), 
            text_color="white"
        )
        self.header_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Bloc thème ---
        self.frame_theme = ctk.CTkFrame(self, width=200, height=80, border_width=1, border_color=("gray70", "gray25"))
        self.frame_theme.pack(pady=(140, 20), padx=20)
        self.frame_theme.pack_propagate(False)

        self.theme_label = ctk.CTkLabel(
            self.frame_theme,
            text=self.lang_util.t("apparence_du_theme"),
            font=("Roboto", 18)
        )
        self.theme_label.pack(pady=(5,15))

        self.theme_var = ctk.StringVar(value=load_settings().get("theme", "Dark"))

        self.switch_theme = ctk.CTkSwitch(
            self.frame_theme,
            text=self.lang_util.t("mode_clair"),  # texte initial
            variable=self.theme_var,
            onvalue="Light",
            offvalue="Dark",
            command=self.on_theme_change
        )
        self.switch_theme.pack()

        self.update_switch_text()

        # --- Bloc langue ---
        self.frame_lang = ctk.CTkFrame(self, width=200, height=80, border_width=1, border_color=("gray70", "gray25"))
        self.frame_lang.pack(pady=40, padx=40)
        self.frame_lang.pack_propagate(False)

        self.lang_label = ctk.CTkLabel(
            self.frame_lang,
            text=self.lang_util.t("langue"),
            font=("Roboto", 16)
        )
        self.lang_label.pack(expand=True, pady=(0,3))

        self.lang_var = ctk.StringVar(value=self.app.lang)
        self.lang_menu = ctk.CTkOptionMenu(
            self.frame_lang, 
            values=["francais", "english"], 
            variable=self.lang_var, 
            command=self.change_language
        )
        self.lang_menu.pack(pady=(0,15), expand=True)

    # --- Thème ---
    def on_theme_change(self):
        theme = self.theme_var.get()
        apply_theme(theme)

        settings = load_settings()
        settings["theme"] = theme
        save_settings(settings)

        self.update_switch_text()

    def update_switch_text(self):
        if self.theme_var.get() == "Light":
            self.switch_theme.configure(text=self.lang_util.t("mode_clair"))
        else:
            self.switch_theme.configure(text=self.lang_util.t("mode_sombre"))

    # --- Langue ---
    def change_language(self, value):
        self.app.lang = value

        # Sauvegarde dans les settings
        settings = load_settings()
        settings["lang"] = value
        save_settings(settings)
        
        # Rafraîchir toutes les pages
        for page in self.app.pages.values():
            if hasattr(page, "refresh_language"):
                page.refresh_language()
            if hasattr(self.app, "refresh_language"):
                self.app.refresh_language()
        self.refresh_language()  # rafraîchir cette page

    # --- Rafraîchir textes de la page ---
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("parametres_application"))
        self.theme_label.configure(text=self.lang_util.t("apparence_du_theme"))
        self.lang_label.configure(text=self.lang_util.t("langue"))
        self.update_switch_text()
