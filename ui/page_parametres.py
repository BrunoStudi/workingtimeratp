import customtkinter as ctk

from utils.page_lang import PageLang
from utils.settings import apply_theme, load_settings, save_settings


HEADER_COLOR = "#1E5CC4"
AVAILABLE_LANGUAGES = ("francais", "english")
DEFAULT_THEME = "Dark"


class PageParams(ctk.CTkFrame):
    """Page de paramètres de l'application."""

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.lang_util = PageLang(app)

        settings = load_settings()

        self.theme_var = ctk.StringVar(
            value=settings.get("theme", DEFAULT_THEME)
        )
        self.lang_var = ctk.StringVar(
            value=self.app.lang
        )

        self._create_header()
        self._create_theme_section()
        self._create_language_section()

        self.update_switch_text()

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _create_header(self):
        self.header = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color=HEADER_COLOR,
            height=60,
        )
        self.header.pack(
            fill="x",
            padx=5,
            pady=5,
        )

        self.header_label = ctk.CTkLabel(
            self.header,
            text=self.lang_util.t("parametres_application"),
            font=("Roboto", 24),
            text_color="white",
        )
        self.header_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

    def _create_theme_section(self):
        self.frame_theme = ctk.CTkFrame(
            self,
            width=200,
            height=80,
            border_width=1,
            border_color=("gray70", "gray25"),
        )
        self.frame_theme.pack(
            pady=(140, 20),
            padx=20,
        )
        self.frame_theme.pack_propagate(False)

        self.theme_label = ctk.CTkLabel(
            self.frame_theme,
            text=self.lang_util.t("apparence_du_theme"),
            font=("Roboto", 18),
        )
        self.theme_label.pack(
            pady=(5, 15),
        )

        self.switch_theme = ctk.CTkSwitch(
            self.frame_theme,
            text=self.lang_util.t("mode_clair"),
            variable=self.theme_var,
            onvalue="Light",
            offvalue="Dark",
            command=self.on_theme_change,
        )
        self.switch_theme.pack()

    def _create_language_section(self):
        self.frame_lang = ctk.CTkFrame(
            self,
            width=200,
            height=80,
            border_width=1,
            border_color=("gray70", "gray25"),
        )
        self.frame_lang.pack(
            pady=40,
            padx=40,
        )
        self.frame_lang.pack_propagate(False)

        self.lang_label = ctk.CTkLabel(
            self.frame_lang,
            text=self.lang_util.t("langue"),
            font=("Roboto", 16),
        )
        self.lang_label.pack(
            expand=True,
            pady=(0, 3),
        )

        self.lang_menu = ctk.CTkOptionMenu(
            self.frame_lang,
            values=list(AVAILABLE_LANGUAGES),
            variable=self.lang_var,
            command=self.change_language,
        )
        self.lang_menu.pack(
            pady=(0, 15),
            expand=True,
        )

    # ------------------------------------------------------------------
    # Thème
    # ------------------------------------------------------------------

    def on_theme_change(self):
        theme = self.theme_var.get()

        apply_theme(theme)
        self._save_setting(
            "theme",
            theme,
        )

        self.update_switch_text()

    def update_switch_text(self):
        translation_key = (
            "mode_clair"
            if self.theme_var.get() == "Light"
            else "mode_sombre"
        )

        self.switch_theme.configure(
            text=self.lang_util.t(translation_key)
        )

    # ------------------------------------------------------------------
    # Langue
    # ------------------------------------------------------------------

    def change_language(self, value):
        self.app.lang = value
        self._save_setting(
            "lang",
            value,
        )

        self._refresh_application_language()

    def _refresh_application_language(self):
        # Rafraîchit chaque page disposant d'une méthode dédiée.
        for page in self.app.pages.values():
            if hasattr(page, "refresh_language"):
                page.refresh_language()

        # Dans la version d'origine, ce test se trouvait dans la boucle.
        # Un seul appel suffit pour rafraîchir l'interface principale.
        if hasattr(self.app, "refresh_language"):
            self.app.refresh_language()

        # Conservé pour garantir le rafraîchissement de cette page même
        # si elle n'est pas présente dans app.pages.
        self.refresh_language()

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------

    @staticmethod
    def _save_setting(key, value):
        settings = load_settings()
        settings[key] = value
        save_settings(settings)

    # ------------------------------------------------------------------
    # Rafraîchissement des traductions
    # ------------------------------------------------------------------

    def refresh_language(self):
        self.lang_util = PageLang(self.app)

        self.header_label.configure(
            text=self.lang_util.t("parametres_application")
        )
        self.theme_label.configure(
            text=self.lang_util.t("apparence_du_theme")
        )
        self.lang_label.configure(
            text=self.lang_util.t("langue")
        )

        self.update_switch_text()
