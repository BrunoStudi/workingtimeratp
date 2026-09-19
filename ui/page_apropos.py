import customtkinter as ctk

from pathlib import Path

from config.paths import resource_path
from utils.page_lang import PageLang


CHANGELOG_FILE = Path(resource_path("CHANGELOG.md"))

APP_VERSION = "1.49.44"
CONTENT_WRAP = 760
CHANGELOG_WIDTH = 900
CHANGELOG_HEIGHT = 600

FEATURES = (
    (
        "⏱ Temps de travail",
        "Saisie et suivi du temps de travail journalier.",
    ),
    (
        "📈 Heures variables",
        "Calcul automatique et suivi du cumul des HV.",
    ),
    (
        "🛠 Interventions",
        "Saisie des interventions pour report ultérieur dans Magellan.",
    ),
    (
        "📦 Consommables",
        "Recherche des articles et suivi des quantités STOE / VG.",
    ),
    (
        "🛠️ Dépannage",
        "Consultation, création, modification et suppression de procédures avec photos, "
        "base collaborative EK1 et synchronisation automatique entre les postes.",
    ),
    (
        "🔗 Raccourcis",
        "Accès rapide aux principaux outils et liens métier.",
    ),
)

TECHNOLOGIES = (
    "Python",
    "CustomTkinter",
    "Tkinter",
    "JSON",
    "OpenPyXL",
    "Pillow",
)


class PageApropos(ctk.CTkFrame):
    """Page de présentation de l'application et affichage du changelog."""

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.lang_util = PageLang(app)

        self._create_header()
        self._create_content()

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _create_header(self):
        header = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color="#1E5CC4",
            height=60,
        )
        header.pack(fill="x", padx=5, pady=5)
        header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(
            header,
            text=self.lang_util.t("a_propos"),
            font=("Roboto", 24),
            text_color="white",
        )
        self.header_label.pack(expand=True)

    def _create_content(self):
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=("gray95", "gray20"),
            corner_radius=10,
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self._create_hero(container)
        self._create_action_bar(container)
        self._create_about_section(container)
        self._create_features_section(container)
        self._create_technologies_section(container)
        self._create_calculation_rules_section(container)
        self._create_warning_section(container)
        self._create_privacy_section(container)
        self._create_author_section(container)

    def _create_hero(self, parent):
        hero = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=("white", "#181818"),
            border_width=1,
            border_color=("gray80", "gray30"),
        )
        hero.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hero,
            text="🚇",
            font=("Segoe UI Emoji", 42),
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            hero,
            text="Journées de travail RATP",
            font=("Roboto", 26, "bold"),
        ).pack()

        ctk.CTkLabel(
            hero,
            text="Application agent",
            font=("Roboto", 14),
            text_color=("gray40", "gray70"),
        ).pack(pady=(2, 10))

        ctk.CTkLabel(
            hero,
            text=f"Version {APP_VERSION}",
            font=("Roboto", 11, "bold"),
            text_color="white",
            fg_color="#1E5CC4",
            corner_radius=20,
            padx=14,
            pady=5,
        ).pack(pady=(0, 20))

    def _create_action_bar(self, parent):
        top_bar = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        top_bar.pack(fill="x", padx=15, pady=(5, 5))

        ctk.CTkButton(
            top_bar,
            text="📋 Voir le changelog",
            width=150,
            command=self.show_changelog,
        ).pack(side="right")

    def _create_about_section(self, parent):
        self._section_title(parent, "📖 À propos")

        self._section_text(
            parent,
            "Cette application regroupe plusieurs outils utiles au quotidien afin de "
            "faciliter le suivi du temps de travail, la saisie des interventions, "
            "la consultation des consommables et l'accès aux procédures de dépannage.",
            CONTENT_WRAP,
        )

    def _create_features_section(self, parent):
        self._section_title(parent, "✨ Fonctionnalités principales")

        features_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        features_frame.pack(fill="x", padx=15, pady=(5, 10))
        features_frame.grid_columnconfigure((0, 1), weight=1)

        for index, (title, description) in enumerate(FEATURES):
            row, column = divmod(index, 2)

            card = ctk.CTkFrame(
                features_frame,
                corner_radius=10,
                border_width=1,
                border_color=("gray80", "gray30"),
                fg_color=("white", "#202020"),
            )
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=6,
                pady=6,
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Roboto", 14, "bold"),
            ).pack(
                anchor="w",
                padx=15,
                pady=(12, 4),
            )

            ctk.CTkLabel(
                card,
                text=description,
                wraplength=320,
                justify="left",
                text_color=("gray35", "gray70"),
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 12),
            )

    def _create_technologies_section(self, parent):
        self._section_title(parent, "🧰 Technologies")

        badges_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        badges_frame.pack(
            anchor="w",
            padx=25,
            pady=(5, 15),
        )

        for technology in TECHNOLOGIES:
            ctk.CTkLabel(
                badges_frame,
                text=technology,
                font=("Roboto", 11, "bold"),
                fg_color=("gray80", "gray30"),
                corner_radius=15,
                padx=12,
                pady=5,
            ).pack(
                side="left",
                padx=(0, 7),
            )

    def _create_calculation_rules_section(self, parent):
        self._section_title(parent, "⏲ Règles de calcul")

        self._section_text(
            parent,
            "Les heures variables sont calculées à partir du dépassement de la "
            "durée journalière de référence de 7h34. "
            "Un plafond journalier et un plafond global sont appliqués.",
            CONTENT_WRAP,
        )

    def _create_warning_section(self, parent):
        warning_frame = ctk.CTkFrame(
            parent,
            corner_radius=10,
            fg_color=("#FFF4D6", "#3A321F"),
            border_width=1,
            border_color=("#E1B955", "#806A32"),
        )
        warning_frame.pack(
            fill="x",
            padx=15,
            pady=(20, 10),
        )

        ctk.CTkLabel(
            warning_frame,
            text="⚠ Avertissement",
            font=("Roboto", 14, "bold"),
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 4),
        )

        ctk.CTkLabel(
            warning_frame,
            text=(
                "Les données affichées sont fournies à titre indicatif. "
                "Elles ne remplacent en aucun cas les outils officiels "
                "de gestion du temps."
            ),
            wraplength=CONTENT_WRAP,
            justify="left",
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12),
        )

    def _create_privacy_section(self, parent):
        privacy_frame = ctk.CTkFrame(
            parent,
            corner_radius=10,
            border_width=1,
            border_color=("gray80", "gray30"),
            fg_color=("white", "#202020"),
        )
        privacy_frame.pack(
            fill="x",
            padx=15,
            pady=10,
        )

        ctk.CTkLabel(
            privacy_frame,
            text="🔒 Données & confidentialité",
            font=("Roboto", 14, "bold"),
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 4),
        )

        ctk.CTkLabel(
            privacy_frame,
            text=(
                "Les données personnelles de l'utilisateur sont stockées localement sur le poste de travail. "
                "Les procédures de dépannage et leurs photos peuvent être synchronisées sur le partage "
                "réseau interne EK1 afin de permettre leur utilisation collaborative entre les postes. "
                "Aucune donnée personnelle n'est transmise à un service Internet externe."
            ),
            wraplength=CONTENT_WRAP,
            justify="left",
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12),
        )

    def _create_author_section(self, parent):
        author_frame = ctk.CTkFrame(
            parent,
            corner_radius=10,
            fg_color=("#1E5CC4", "#1E5CC4"),
        )
        author_frame.pack(
            fill="x",
            padx=15,
            pady=(10, 20),
        )

        ctk.CTkLabel(
            author_frame,
            text="👨‍💻 Développement",
            font=("Roboto", 16, "bold"),
            text_color="white",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5),
        )

        ctk.CTkLabel(
            author_frame,
            text=(
                "Bruno Carrière\n"
                "Équipe EK1 • AME\n"
                "Projet personnel • Python • 2026\n"
                "Tous droits réservés."
            ),
            font=("Roboto", 12),
            text_color="white",
            justify="left",
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15),
        )

    # ------------------------------------------------------------------
    # Changelog
    # ------------------------------------------------------------------

    def show_changelog(self):
        win = ctk.CTkToplevel(self)
        win.title("Changelog")

        self._center_window(
            win,
            CHANGELOG_WIDTH,
            CHANGELOG_HEIGHT,
        )

        win.transient(self.app)
        win.grab_set()

        container = ctk.CTkScrollableFrame(
            win,
            fg_color=("gray95", "gray15"),
        )
        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        if not CHANGELOG_FILE.exists():
            ctk.CTkLabel(
                container,
                text="Aucun changelog disponible.",
            ).pack(pady=20)
            return

        try:
            with CHANGELOG_FILE.open("r", encoding="utf-8") as file:
                lines = file.readlines()
        except OSError as error:
            ctk.CTkLabel(
                container,
                text=f"Impossible de lire le changelog.\n\n{error}",
            ).pack(pady=20)
            return

        self._render_changelog(container, lines)

    def _center_window(self, window, width, height):
        self.app.update_idletasks()

        parent_x = self.app.winfo_x()
        parent_y = self.app.winfo_y()
        parent_width = self.app.winfo_width()
        parent_height = self.app.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def _render_changelog(self, parent, lines):
        for line in lines:
            text = line.strip()

            if not text:
                self._create_changelog_spacing(parent)
                continue

            if text.startswith("# "):
                self._create_changelog_label(
                    parent,
                    text[2:],
                    font=("Roboto", 24, "bold"),
                    text_color="#1E5CC4",
                    padx=15,
                    pady=(15, 8),
                )
            elif text.startswith("## "):
                self._create_changelog_label(
                    parent,
                    text[3:],
                    font=("Roboto", 19, "bold"),
                    text_color="#1E5CC4",
                    padx=20,
                    pady=(18, 6),
                )
            elif text.startswith("### "):
                self._create_changelog_label(
                    parent,
                    text[4:],
                    font=("Roboto", 15, "bold"),
                    padx=30,
                    pady=(12, 4),
                )
            elif text == "---":
                self._create_changelog_separator(parent)
            elif text.startswith("- "):
                self._create_changelog_label(
                    parent,
                    "• " + text[2:],
                    font=("Roboto", 12),
                    padx=40,
                    pady=2,
                    wraplength=780,
                )
            elif text.startswith("> "):
                self._create_changelog_quote(parent, text[2:])
            else:
                cleaned = (
                    text
                    .replace("**", "")
                    .replace("`", "")
                )
                self._create_changelog_label(
                    parent,
                    cleaned,
                    font=("Roboto", 12),
                    padx=30,
                    pady=2,
                    wraplength=780,
                )

    @staticmethod
    def _create_changelog_spacing(parent):
        ctk.CTkFrame(
            parent,
            height=8,
            fg_color="transparent",
        ).pack()

    @staticmethod
    def _create_changelog_separator(parent):
        ctk.CTkFrame(
            parent,
            height=1,
            fg_color=("gray70", "gray35"),
        ).pack(
            fill="x",
            padx=15,
            pady=10,
        )

    @staticmethod
    def _create_changelog_label(
        parent,
        text,
        font,
        padx,
        pady,
        text_color=None,
        wraplength=None,
    ):
        options = {
            "text": text,
            "font": font,
            "justify": "left",
        }

        if text_color is not None:
            options["text_color"] = text_color

        if wraplength is not None:
            options["wraplength"] = wraplength

        ctk.CTkLabel(
            parent,
            **options,
        ).pack(
            anchor="w",
            padx=padx,
            pady=pady,
        )

    @staticmethod
    def _create_changelog_quote(parent, text):
        quote_frame = ctk.CTkFrame(
            parent,
            fg_color=("gray90", "gray22"),
            corner_radius=8,
        )
        quote_frame.pack(
            fill="x",
            padx=25,
            pady=5,
        )

        ctk.CTkLabel(
            quote_frame,
            text=text,
            font=("Roboto", 12, "italic"),
            justify="left",
            wraplength=750,
        ).pack(
            anchor="w",
            padx=15,
            pady=10,
        )

    # ------------------------------------------------------------------
    # Méthodes utilitaires
    # ------------------------------------------------------------------

    @staticmethod
    def _section_title(parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=("TkDefaultFont", 16, "bold"),
        ).pack(
            anchor="w",
            pady=(15, 5),
            padx=15,
        )

    @staticmethod
    def _section_text(parent, text, wraplength=700):
        ctk.CTkLabel(
            parent,
            text=text,
            wraplength=wraplength,
            justify="left",
        ).pack(
            anchor="w",
            padx=25,
        )

    @staticmethod
    def _section_list(parent, items):
        for item in items:
            ctk.CTkLabel(
                parent,
                text=f"• {item}",
                justify="left",
            ).pack(
                anchor="w",
                padx=35,
            )

    # ------------------------------------------------------------------
    # Rafraîchissement de la langue
    # ------------------------------------------------------------------

    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(
            text=self.lang_util.t("a_propos")
        )
