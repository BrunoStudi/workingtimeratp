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
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=("gray95", "gray20"),
            corner_radius=10
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        WRAP = 760

        # ================= HERO =================
        hero = ctk.CTkFrame(
            container,
            corner_radius=15,
            fg_color=("white", "#181818"),
            border_width=1,
            border_color=("gray80", "gray30")
        )
        hero.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            hero,
            text="🚇",
            font=("Segoe UI Emoji", 42)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            hero,
            text="Journées de travail RATP",
            font=("Roboto", 26, "bold")
        ).pack()

        ctk.CTkLabel(
            hero,
            text="Application agent",
            font=("Roboto", 14),
            text_color=("gray40", "gray70")
        ).pack(pady=(2, 10))

        version_label = ctk.CTkLabel(
            hero,
            text="Version 1.41.43",
            font=("Roboto", 11, "bold"),
            text_color="white",
            fg_color="#1E5CC4",
            corner_radius=20,
            padx=14,
            pady=5
        )
        version_label.pack(pady=(0, 20))

        # ================= BARRE ACTION =================
        top_bar = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        top_bar.pack(fill="x", padx=15, pady=(5, 5))

        btn_changelog = ctk.CTkButton(
            top_bar,
            text="📋 Voir le changelog",
            width=150,
            command=self.show_changelog
        )
        btn_changelog.pack(side="right")

        # ================= À PROPOS =================
        self._section_title(container, "📖 À propos")

        self._section_text(
            container,
            "Cette application regroupe plusieurs outils utiles au quotidien afin de "
            "faciliter le suivi du temps de travail, la saisie des interventions, "
            "la consultation des consommables et l'accès aux procédures de dépannage.",
            WRAP
        )

        # ================= FONCTIONNALITÉS =================
        self._section_title(container, "✨ Fonctionnalités principales")

        features_frame = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        features_frame.pack(fill="x", padx=15, pady=(5, 10))

        features_frame.grid_columnconfigure((0, 1), weight=1)

        features = [
            (
                "⏱ Temps de travail",
                "Saisie et suivi du temps de travail journalier."
            ),
            (
                "📈 Heures variables",
                "Calcul automatique et suivi du cumul des HV."
            ),
            (
                "🛠 Interventions",
                "Saisie des interventions pour report ultérieur dans Magellan."
            ),
            (
                "📦 Consommables",
                "Recherche des articles et suivi des quantités STOE / VG."
            ),
            (
                "🔧 Dépannage",
                "Accès aux procédures et aides de dépannage des cartes."
            ),
            (
                "🔗 Raccourcis",
                "Accès rapide aux principaux outils et liens métier."
            )
        ]

        for index, (title, description) in enumerate(features):
            row = index // 2
            column = index % 2

            card = ctk.CTkFrame(
                features_frame,
                corner_radius=10,
                border_width=1,
                border_color=("gray80", "gray30"),
                fg_color=("white", "#202020")
            )
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=6,
                pady=6
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Roboto", 14, "bold")
            ).pack(
                anchor="w",
                padx=15,
                pady=(12, 4)
            )

            ctk.CTkLabel(
                card,
                text=description,
                wraplength=320,
                justify="left",
                text_color=("gray35", "gray70")
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 12)
            )

        # ================= TECHNOLOGIES =================
        self._section_title(container, "🧰 Technologies")

        badges_frame = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        badges_frame.pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        technologies = [
            "Python",
            "CustomTkinter",
            "Tkinter",
            "JSON",
            "OpenPyXL",
            "Pillow"
        ]

        for tech in technologies:
            badge = ctk.CTkLabel(
                badges_frame,
                text=tech,
                font=("Roboto", 11, "bold"),
                fg_color=("gray80", "gray30"),
                corner_radius=15,
                padx=12,
                pady=5
            )
            badge.pack(
                side="left",
                padx=(0, 7)
            )

        # ================= RÈGLES DE CALCUL =================
        self._section_title(container, "⏲ Règles de calcul")

        self._section_text(
            container,
            "Les heures variables sont calculées à partir du dépassement de la "
            "durée journalière de référence de 7h34. "
            "Un plafond journalier et un plafond global sont appliqués.",
            WRAP
        )

        # ================= AVERTISSEMENT =================
        warning_frame = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color=("#FFF4D6", "#3A321F"),
            border_width=1,
            border_color=("#E1B955", "#806A32")
        )
        warning_frame.pack(
            fill="x",
            padx=15,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            warning_frame,
            text="⚠ Avertissement",
            font=("Roboto", 14, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 4)
        )

        ctk.CTkLabel(
            warning_frame,
            text=(
                "Les données affichées sont fournies à titre indicatif. "
                "Elles ne remplacent en aucun cas les outils officiels "
                "de gestion du temps."
            ),
            wraplength=WRAP,
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # ================= CONFIDENTIALITÉ =================
        privacy_frame = ctk.CTkFrame(
            container,
            corner_radius=10,
            border_width=1,
            border_color=("gray80", "gray30"),
            fg_color=("white", "#202020")
        )
        privacy_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            privacy_frame,
            text="🔒 Données & confidentialité",
            font=("Roboto", 14, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 4)
        )

        ctk.CTkLabel(
            privacy_frame,
            text=(
                "Les données utilisateur sont stockées localement sur le poste de travail. "
                "Aucune information personnelle n'est collectée ou transmise à distance."
            ),
            wraplength=WRAP,
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # ================= AUTEUR =================
        author_frame = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color=("#1E5CC4", "#1E5CC4")
        )
        author_frame.pack(
            fill="x",
            padx=15,
            pady=(10, 20)
        )

        ctk.CTkLabel(
            author_frame,
            text="👨‍💻 Développement",
            font=("Roboto", 16, "bold"),
            text_color="white"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
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
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

    def show_changelog(self):
        win = ctk.CTkToplevel(self)
        win.title("Changelog")

        width = 900
        height = 600

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

        container = ctk.CTkScrollableFrame(
            win,
            fg_color=("gray95", "gray15")
        )
        container.pack(fill="both", expand=True, padx=10, pady=10)

        if not CHANGELOG_FILE.exists():
            ctk.CTkLabel(
                container,
                text="Aucun changelog disponible."
            ).pack(pady=20)
            return

        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            text = line.strip()

            if not text:
                ctk.CTkFrame(
                    container,
                    height=8,
                    fg_color="transparent"
                ).pack()
                continue

            # Titre principal
            if text.startswith("# "):
                ctk.CTkLabel(
                    container,
                    text=text[2:],
                    font=("Roboto", 24, "bold"),
                    text_color="#1E5CC4"
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=(15, 8)
                )

            # Titre niveau 2
            elif text.startswith("## "):
                ctk.CTkLabel(
                    container,
                    text=text[3:],
                    font=("Roboto", 19, "bold"),
                    text_color="#1E5CC4"
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=(18, 6)
                )

            # Titre niveau 3
            elif text.startswith("### "):
                ctk.CTkLabel(
                    container,
                    text=text[4:],
                    font=("Roboto", 15, "bold")
                ).pack(
                    anchor="w",
                    padx=30,
                    pady=(12, 4)
                )

            # Séparateur
            elif text == "---":
                ctk.CTkFrame(
                    container,
                    height=1,
                    fg_color=("gray70", "gray35")
                ).pack(
                    fill="x",
                    padx=15,
                    pady=10
                )

            # Liste
            elif text.startswith("- "):
                ctk.CTkLabel(
                    container,
                    text="• " + text[2:],
                    font=("Roboto", 12),
                    justify="left",
                    wraplength=780
                ).pack(
                    anchor="w",
                    padx=40,
                    pady=2
                )

            # Citation
            elif text.startswith("> "):
                quote_frame = ctk.CTkFrame(
                    container,
                    fg_color=("gray90", "gray22"),
                    corner_radius=8
                )
                quote_frame.pack(
                    fill="x",
                    padx=25,
                    pady=5
                )

                ctk.CTkLabel(
                    quote_frame,
                    text=text[2:],
                    font=("Roboto", 12, "italic"),
                    justify="left",
                    wraplength=750
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=10
                )

            # Texte normal
            else:
                cleaned = (
                    text
                    .replace("**", "")
                    .replace("`", "")
                )

                ctk.CTkLabel(
                    container,
                    text=cleaned,
                    font=("Roboto", 12),
                    justify="left",
                    wraplength=780
                ).pack(
                    anchor="w",
                    padx=30,
                    pady=2
                )

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
