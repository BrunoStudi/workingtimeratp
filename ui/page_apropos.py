import customtkinter as ctk

from pathlib import Path
from utils.page_lang import PageLang
from config.paths import resource_path

CHANGELOG_FILE = Path(resource_path("CHANGELOG.md"))

class PageApropos(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.lang_util = PageLang(app)

        # ================= HEADER =================
        header = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color="#1E5CC4",
            height=60
        )
        header.pack(fill="x", padx=5, pady=5)
        header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(
            header,
            text=self.lang_util.t("a_propos"),
            font=("Roboto", 24),
            text_color="white"
        )
        self.header_label.pack(expand=True)

        # ================= CONTENEUR =================
        container = ctk.CTkFrame(
            self,
            fg_color=("gray95", "gray20"),
            corner_radius=10
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # largeur max du texte (évite coupure)
        WRAP = 700

        # ================= BARRE HAUTE CONTENEUR =================
        top_bar = ctk.CTkFrame(container, fg_color="transparent")
        top_bar.pack(fill="x", padx=10, pady=(10, 0))

        btn_changelog = ctk.CTkButton(
            top_bar,
            text="Changelog",
            width=120,
            command=self.show_changelog
        )
        btn_changelog.pack(side="right")

        # ================= 1 Nom + version =================
        self._section_title(container, "Journées de travail RATP - Application agent")
        self._section_text(container, "Version 1.27.24")

        # ================= 2 Description =================
        self._section_title(container, "Description")
        self._section_text(
            container,
            "Cette application permet de suivre le temps de travail quotidien, "
            "de saisir ses interventions pour les entrer plus tard dans Magellan "
            "ainsi que le cumul des heures variables (HV), conformément aux règles "
            "internes de gestion du temps.",
            WRAP
        )

        # ================= 3 Fonctionnalités =================
        self._section_title(container, "Fonctionnalités principales")
        self._section_list(
            container,
            [
                "Saisie du temps de travail journalier",
                "Calcul automatique des heures variables",
                "Suivi des cumuls avec plafonds",
                "Recherche de consommables",
                "Procédure de dépannage des cartes"
            ]
        )

        # ================= 4 Règles de calcul =================
        self._section_title(container, "Règles de calcul")
        self._section_text(
            container,
            "Les heures variables sont calculées à partir du dépassement de la "
            "durée journalière de référence (7h34). "
            "Un plafond journalier et un plafond global sont appliqués.",
            WRAP
        )

        # ================= 5 Avertissement =================
        self._section_title(container, "Avertissement")
        self._section_text(
            container,
            "Les données affichées sont fournies à titre indicatif.\n"
            "Elles ne remplacent en aucun cas les outils officiels de gestion du temps.",
            WRAP
        )

        # ================= 6 Données =================
        self._section_title(container, "Données & confidentialité")
        self._section_text(
            container,
            "Les données sont stockées localement sur l’ordinateur de l’utilisateur.\n"
            "Aucune information n’est transmise ou collectée à distance.",
            WRAP
        )

        # ================= 7 Auteur =================
        self._section_title(container, "Auteur")
        self._section_text(
            container,
            "Développé par : Bruno Carrière - Equipe EK1 - AME\nProjet personnel – 2026 : Python\nTous droits réservés.",
            WRAP
        )

    def show_changelog(self):
        win = ctk.CTkToplevel(self)
        win.title("Changelog")

        width = 600
        height = 500

        # Forcer le calcul des dimensions de la fenêtre parente
        self.app.update_idletasks()

        parent_x = self.app.winfo_x()
        parent_y = self.app.winfo_y()
        parent_width = self.app.winfo_width()
        parent_height = self.app.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        win.geometry(f"{width}x{height}+{x}+{y}")

        win.transient(self.app)
        win.grab_set()

        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        textbox = ctk.CTkTextbox(frame, wrap="word")
        textbox.pack(fill="both", expand=True)

        if CHANGELOG_FILE.exists() and CHANGELOG_FILE.stat().st_size > 0:
            with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
                textbox.insert("1.0", f.read())
        else:
            textbox.insert("1.0", "Aucun changelog disponible.")

        textbox.configure(state="disabled")

    # ================= MÉTHODES UTILITAIRES =================

    def _section_title(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=("TkDefaultFont", 16, "bold")
        ).pack(anchor="w", pady=(15, 5), padx=15)

    def _section_text(self, parent, text, wraplength=700):
        ctk.CTkLabel(
            parent,
            text=text,
            wraplength=wraplength,
            justify="left"
        ).pack(anchor="w", padx=25)

    def _section_list(self, parent, items):
        for item in items:
            ctk.CTkLabel(
                parent,
                text=f"• {item}",
                justify="left"
            ).pack(anchor="w", padx=35)

    # ================= RAFRAÎCHISSEMENT LANGUE =================
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("a_propos"))
