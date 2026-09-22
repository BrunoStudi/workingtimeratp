import json
import os
import shutil
import uuid
import webbrowser

from datetime import date, datetime
from pathlib import Path
from tkinter import Menu, filedialog, messagebox

import customtkinter as ctk
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from PIL import Image

from config.paths import (
    APP_DATA_DIR,
    DASHBOARD_CONFIG_FILE,
    DATA_FILE,
    SHORTCUTS_FILE,
    SHORTCUTS_ICONS_DIR,
    resource_path,
)
from utils.page_lang import PageLang


# =============================================================================
# CONFIGURATION
# =============================================================================

ENV_FILE = APP_DATA_DIR / "workingtime.dat"
load_dotenv(ENV_FILE)

MAX_JOURNEE = 454          # 7h34 en minutes
MAX_HV_PAR_JOUR = 50       # Maximum d'HV comptabilisées par jour
PRODUCTIVE_RATIO = 0.87    # Temps productif retenu pour Magellan

# Couleurs des cartes
BORDER_COLOR = "gray72", "gray10"
FG_COLOR = "gray85", "gray30"

ROLE_CONFIG = {
    "Opérateur": {"color": "#0066DB", "label": "Opérateur"},
    "Technicien": {"color": "#009E1A", "label": "Tech"},
    "Technicien Superieur": {"color": "#FF9900", "label": "Tech sup"},
    "Manager": {"color": "#FF0000", "label": "Manager"},
    "Bureau Technique": {"color": "#BB00AB", "label": "BT"},
    "Service Informatique": {"color": "#000000", "label": "SI"},
}

DEFAULT_SHORTCUTS = (
    (
        "ui/assets/icons/selftime.jpg",
        "gAAAAABqTJ7ts4lj09jPUHVuJKNhQTtRLQFwb-W6qKFRhiaDE7OHwAXwPsbyfLQd7ZQy-9_zYMGZFtHoOUqEUC_8_Wmn-tiTcR7syjs2PqbDmYMhkUmz69g=",
        "Selftime",
    ),
    (
        "ui/assets/icons/magellan.png",
        "gAAAAABqTJ7tdtOI2MBSYSIWHzQp9A3ziA8fgzs1P1M0SXkCNjbUyJad7cEleJPiVAluwLhkk0jzX8RylO5ddj3jZL3VHJUHer0T8RnziDdMRMBNNQmn9WllNcimAU7beccZtwGDMI9Q-Br79iBh4rGH1YxykWjqwvFYAkQassoOWsEHV93X8JE=",
        "Magellan Mobi",
    ),
    (
        "ui/assets/icons/magellan.png",
        "gAAAAABqTJ7tJu9H69MJlF_-7r6Lf4A4M99lKHSMKPubWM46qPK-lK2Y_RFALGri3FBPdukINQIJ_9Rtvx7-_qdmGk0VKA9bGlvrfHhVZhFl0s_CtFbyUI401g650rYWlIdf7drR7hUHEoIxa8c91Nju88VfrSSDlidChYfE3nf3VJ_9ByLiPPU=",
        "Magellan Fixe",
    ),
    (
        "ui/assets/icons/ihm.png",
        "gAAAAABqTJ7tkpAmamnbwiOFlkcnwUoTvgUp_OHFuQYbM6X-6PLahMBQ2FvPFL94QpJS2t1icp5UCdYfVkrGf6Y1B771VAh7LRZscNaufnqoqw2tQZ_oG2U-htyzaDHfwnrHnahd0DTY-Zw2oL3hgRFwpSQNxLK1vw==",
        "IHM",
    ),
    (
        "ui/assets/icons/mpd.png",
        "gAAAAABqTJ7tKyppaGOhaVaMuBJV7N2jOYpwEtSjfaShS8u--e4cxww-pHDUVu-rEn31aJxx7W4h8Qp11-LHYu1VnnHiyk4UBBDK0zVgc_n3yasqujaCJC_gqzGvPps_t0-LUbVBERRI5HuGnEGHG0XAkjuImGBphg==",
        "MPD",
    ),
    (
        "ui/assets/icons/urban.png",
        "gAAAAABqTJ7tUzdFxMkoXE9FvUM_jTDLMpsKr0DFZI76nanAOwf1yBfM76toQoEf4MLwWLFqVkxiZhlVIzzLboneFoBkcJJAAM0hXO5XmKD96CQOzMcLcui7ALg_m7IG67dTgO_JSXNF",
        "Urban AME",
    ),
)

URL_KEY = os.getenv("URL_KEY")
if not URL_KEY:
    raise ValueError("URL_KEY absente du fichier .env")

FERNET = Fernet(URL_KEY.encode("utf-8"))


class PageAccueil(ctk.CTkScrollableFrame):
    """Page d'accueil et tableau de bord de WorkingTimeRatp."""

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.lang_util = PageLang(app)
        self.custom_shortcuts = self.load_custom_shortcuts()
        self.last_reset_date = self._load_last_reset_date()

        self._create_header()
        self._create_greeting_section()
        self._create_datetime_section()
        self._create_shortcuts_section()
        self._create_worktime_section()

        self.update_datetime()
        self.refresh()

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _create_header(self):
        header_frame = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color="#1E5CC4",
            height=80,
        )
        header_frame.pack(fill="x", padx=5, pady=5)

        title_container = ctk.CTkFrame(
            header_frame,
            fg_color="transparent",
        )
        title_container.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(
            title_container,
            text=self.lang_util.t("mon_dashboard_ratp"),
            font=("Roboto", 24),
            text_color="white",
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = ctk.CTkLabel(
            title_container,
            text=self.lang_util.t("La Régie Autonome des Transports Parisiens"),
            font=("Roboto", 12),
            text_color="white",
        )
        self.subtitle_label.pack()

    def _create_greeting_section(self):
        greeting_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR,
            fg_color=FG_COLOR,
        )
        greeting_frame.pack(pady=(30, 30), padx=20)

        frame_h = ctk.CTkFrame(
            greeting_frame,
            fg_color="transparent",
        )
        frame_h.pack(padx=15, pady=10)

        self.greeting_label = ctk.CTkLabel(
            frame_h,
            text=self.lang_util.t(f"Bonjour {self.app.user_name}"),
            font=("Roboto", 20),
        )
        self.greeting_label.pack(side="left")

        role = getattr(self.app, "user_role", "Opérateur")
        role_config = ROLE_CONFIG.get(
            role,
            {"color": "#444444", "label": role},
        )

        self.badge_role = ctk.CTkLabel(
            frame_h,
            text=role_config["label"],
            font=("Roboto", 12, "bold"),
            text_color="white",
            fg_color=role_config["color"],
            corner_radius=50,
            width=120,
            height=24,
        )
        self.badge_role.pack(side="left", padx=(10, 0))

    def _create_datetime_section(self):
        self.datetime_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR,
            fg_color=FG_COLOR,
        )
        self.datetime_frame.pack(pady=(8, 30), padx=20)

        self.date_label = ctk.CTkLabel(
            self.datetime_frame,
            text="",
            font=("Roboto", 14, "bold"),
        )
        self.date_label.pack(padx=20, pady=(10, 2))

        self.time_label = ctk.CTkLabel(
            self.datetime_frame,
            text="",
            font=("Roboto", 16, "bold"),
        )
        self.time_label.pack(padx=20, pady=(2, 10))

    def _create_shortcuts_section(self):
        self.icon_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=1,
            border_color=BORDER_COLOR,
            fg_color=FG_COLOR,
        )
        self.icon_frame.pack(pady=(0, 30), padx=20, fill="x")

        self.shortcuts_label = ctk.CTkLabel(
            self.icon_frame,
            text=self.lang_util.t("mes_raccourcis"),
            font=("Roboto", 14, "bold"),
            text_color="white",
            fg_color="black",
            corner_radius=20,
            padx=15,
            pady=5,
        )
        self.shortcuts_label.grid(
            row=0,
            column=0,
            columnspan=6,
            pady=(10, 5),
            padx=(10, 0),
            sticky="w",
        )

        self.custom_shortcuts_frame = ctk.CTkFrame(
            self.icon_frame,
            fg_color="transparent",
        )
        self.custom_shortcuts_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            sticky="w",
            padx=(10, 0),
            pady=(10, 5),
        )

        self.add_shortcut_button = ctk.CTkButton(
            self.icon_frame,
            text="Ajouter un raccourci",
            command=self.open_add_shortcut_modal,
            width=180,
        )
        self.add_shortcut_button.grid(
            row=3,
            column=0,
            columnspan=6,
            pady=(5, 10),
        )

        self.icon_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5),
            weight=1,
        )

        for column, (image_path, encrypted_url, text) in enumerate(DEFAULT_SHORTCUTS):
            self._create_default_shortcut(
                column,
                image_path,
                encrypted_url,
                text,
            )

        self.refresh_custom_shortcuts()

    def _create_default_shortcut(self, column, image_path, encrypted_url, text):
        try:
            image = Image.open(resource_path(image_path))
            image = image.resize((50, 50))
            icon = ctk.CTkImage(image, size=(50, 50))
        except (OSError, ValueError):
            icon = None

        button = ctk.CTkButton(
            self.icon_frame,
            image=icon,
            text=text,
            compound="top",
            command=lambda url=encrypted_url: self.open_link(
                self.decrypt_url(url)
            ),
            width=100,
            height=80,
            fg_color="black",
        )
        button.grid(row=1, column=column, padx=20, pady=10)

        # Conserver une référence afin d'éviter la libération de l'image.
        button.image = icon

    def _create_worktime_section(self):
        self.info_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.info_container.pack(pady=20, padx=20, fill="x")

        self.info_frame = ctk.CTkFrame(
            self.info_container,
            corner_radius=10,
            fg_color=FG_COLOR,
            border_width=1,
            border_color=BORDER_COLOR,
        )
        self.info_frame.pack(
            pady=5,
            padx=100,
            fill="x",
        )

        self.label_total = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Roboto", 18),
        )
        self.label_total.pack(pady=(15, 5))

        self.label_mois = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Roboto", 18),
        )
        self.label_mois.pack(pady=(5, 5))

        self.label_saisie = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Roboto", 18),
        )
        self.label_saisie.pack(pady=(5, 5))

        self.label_hv = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Roboto", 18),
        )
        self.label_hv.pack(pady=(5, 15))

        self.btn_reset_hv = ctk.CTkButton(
            self,
            text=self.lang_util.t("reset_hv"),
            command=self.reset_hv,
        )
        self.btn_reset_hv.pack(pady=5)

    # =========================================================================
    # LANGUE
    # =========================================================================

    def refresh_language(self):
        self.lang_util = PageLang(self.app)

        self.title_label.configure(
            text=self.lang_util.t("mon_dashboard_ratp")
        )
        self.subtitle_label.configure(
            text=self.lang_util.t(
                "la_regie_autonome_des_transports_parisiens"
            )
        )
        self.greeting_label.configure(
            text=f"{self.lang_util.t('bonjour')} {self.app.user_name}"
        )
        self.btn_reset_hv.configure(
            text=self.lang_util.t("reset_hv")
        )
        self.shortcuts_label.configure(
            text=self.lang_util.t("mes_raccourcis")
        )

        self.refresh()

    # =========================================================================
    # DATE ET HEURE
    # =========================================================================

    def update_datetime(self):
        now = datetime.now()

        jours = (
            "lundi",
            "mardi",
            "mercredi",
            "jeudi",
            "vendredi",
            "samedi",
            "dimanche",
        )
        mois = (
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        )

        date_fr = (
            f"{jours[now.weekday()]} "
            f"{now.day} {mois[now.month - 1]} {now.year}"
        )

        self.date_label.configure(text=date_fr)
        self.time_label.configure(text=now.strftime("%H:%M:%S"))

        self.after(1000, self.update_datetime)

    # =========================================================================
    # RACCOURCIS PERSONNALISÉS
    # =========================================================================

    def load_custom_shortcuts(self):
        if not SHORTCUTS_FILE.exists():
            return []

        try:
            with open(SHORTCUTS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (OSError, json.JSONDecodeError) as error:
            print(f"Erreur chargement raccourcis : {error}")

        return []

    def save_custom_shortcuts(self):
        try:
            with open(SHORTCUTS_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.custom_shortcuts,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except OSError as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer les raccourcis :\n\n{error}",
            )

    def open_add_shortcut_modal(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter un raccourci")
        popup.geometry("500x430")
        popup.resizable(False, False)

        main_window = self.winfo_toplevel()
        popup.transient(main_window)
        popup.update_idletasks()

        popup_width = 500
        popup_height = 430

        main_x = main_window.winfo_rootx()
        main_y = main_window.winfo_rooty()
        main_width = main_window.winfo_width()
        main_height = main_window.winfo_height()

        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2

        popup.geometry(
            f"{popup_width}x{popup_height}+{x}+{y}"
        )
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(
            popup,
            text="Ajouter un raccourci",
            font=("Roboto", 20, "bold"),
        ).pack(pady=(20, 20))

        ctk.CTkLabel(
            popup,
            text="Nom du raccourci",
        ).pack(anchor="w", padx=40)

        name_entry = ctk.CTkEntry(
            popup,
            width=420,
            placeholder_text="Ex : Intranet",
        )
        name_entry.pack(padx=40, pady=(5, 15))

        ctk.CTkLabel(
            popup,
            text="Lien",
        ).pack(anchor="w", padx=40)

        url_entry = ctk.CTkEntry(
            popup,
            width=420,
            placeholder_text="https://...",
        )
        url_entry.pack(padx=40, pady=(5, 15))

        selected_icon = {"path": None}

        icon_label = ctk.CTkLabel(
            popup,
            text="Aucune icône sélectionnée",
        )
        icon_label.pack(pady=(5, 5))

        def choose_icon():
            path = filedialog.askopenfilename(
                parent=popup,
                title="Choisir une icône",
                filetypes=[
                    (
                        "Images",
                        "*.png *.jpg *.jpeg *.ico *.webp",
                    )
                ],
            )

            if not path:
                return

            selected_icon["path"] = path
            icon_label.configure(text=Path(path).name)

        ctk.CTkButton(
            popup,
            text="Choisir une icône",
            command=choose_icon,
            width=200,
        ).pack(pady=(5, 20))

        def save():
            name = name_entry.get().strip()
            url = url_entry.get().strip()
            source_icon = selected_icon["path"]

            if not name:
                messagebox.showwarning(
                    "Nom manquant",
                    "Veuillez saisir un nom.",
                    parent=popup,
                )
                return

            if not url:
                messagebox.showwarning(
                    "Lien manquant",
                    "Veuillez saisir un lien.",
                    parent=popup,
                )
                return

            if not source_icon:
                messagebox.showwarning(
                    "Icône manquante",
                    "Veuillez sélectionner une icône.",
                    parent=popup,
                )
                return

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            try:
                source = Path(source_icon)
                icon_name = f"{uuid.uuid4().hex}{source.suffix.lower()}"
                destination = SHORTCUTS_ICONS_DIR / icon_name

                shutil.copy2(source, destination)

                shortcut = {
                    "id": uuid.uuid4().hex,
                    "name": name,
                    "url": url,
                    "icon": str(destination),
                }

                self.custom_shortcuts.append(shortcut)
                self.save_custom_shortcuts()

                popup.destroy()
                self.refresh_custom_shortcuts()

            except (OSError, shutil.Error) as error:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'ajouter le raccourci :\n\n{error}",
                    parent=popup,
                )

        buttons_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent",
        )
        buttons_frame.pack(pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="Enregistrer",
            command=save,
            width=150,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            command=popup.destroy,
            width=150,
            fg_color="#555555",
        ).pack(side="left", padx=5)

    def refresh_custom_shortcuts(self):
        for widget in self.custom_shortcuts_frame.winfo_children():
            widget.destroy()

        if not self.custom_shortcuts:
            self.custom_shortcuts_frame.grid_remove()
            return

        self.custom_shortcuts_frame.grid()

        for index, shortcut in enumerate(self.custom_shortcuts):
            icon_path = shortcut.get("icon")
            name = shortcut.get("name", "Raccourci")
            url = shortcut.get("url", "")

            try:
                image = Image.open(icon_path)
                icon = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(50, 50),
                )
            except (OSError, ValueError, TypeError):
                icon = None

            button = ctk.CTkButton(
                self.custom_shortcuts_frame,
                text=name,
                image=icon,
                compound="top",
                width=100,
                height=80,
                fg_color="black",
                border_color="black",
                border_width=0,
                text_color="white",
                command=lambda shortcut_url=url: self.open_link(shortcut_url),
            )

            # Conserver une référence afin d'éviter la libération de l'image.
            button.image = icon

            menu = Menu(button, tearoff=0)
            menu.add_command(
                label="Supprimer",
                command=lambda shortcut_id=shortcut.get("id"):
                    self.delete_custom_shortcut(shortcut_id),
            )

            def show_menu(event, context_menu=menu):
                context_menu.tk_popup(event.x_root, event.y_root)

            button.bind("<Button-3>", show_menu)

            row = index // 6
            column = index % 6

            button.grid(
                row=row,
                column=column,
                padx=(18, 40),
                pady=10,
            )

    def delete_custom_shortcut(self, shortcut_id):
        shortcut = next(
            (
                item
                for item in self.custom_shortcuts
                if item.get("id") == shortcut_id
            ),
            None,
        )

        if not shortcut:
            return

        confirm = messagebox.askyesno(
            "Supprimer le raccourci",
            f"Voulez-vous supprimer le raccourci :\n\n"
            f"{shortcut.get('name', '')} ?",
        )

        if not confirm:
            return

        icon_path = shortcut.get("icon")

        if icon_path:
            try:
                path = Path(icon_path)
                if path.exists():
                    path.unlink()
            except OSError as error:
                print(f"Impossible de supprimer l'icône : {error}")

        self.custom_shortcuts = [
            item
            for item in self.custom_shortcuts
            if item.get("id") != shortcut_id
        ]

        self.save_custom_shortcuts()
        self.refresh_custom_shortcuts()

    # =========================================================================
    # DONNÉES DU TABLEAU DE BORD
    # =========================================================================

    def _load_last_reset_date(self):
        if not DASHBOARD_CONFIG_FILE.exists():
            return None

        try:
            with open(DASHBOARD_CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)

            date_str = config.get("last_reset")
            if date_str:
                return datetime.fromisoformat(date_str).date()

        except (OSError, json.JSONDecodeError, ValueError):
            pass

        return None

    def _load_work_entries(self):
        if not DATA_FILE.exists():
            return []

        entries = []

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        except OSError as error:
            print(f"Erreur lecture des données : {error}")

        return entries

    def refresh(self):
        entries = self._load_work_entries()

        if not entries:
            self._display_empty_state()
            return

        self._update_daily_worktime(entries)
        self._update_monthly_worktime(entries)
        self._update_magellan_remaining(entries)
        self._update_hv(entries)

    def _display_empty_state(self):
        self.label_total.configure(
            text=self.lang_util.t("aucunes_donnees_enregistre")
        )
        self.label_hv.configure(text="")

        # Le comportement historique ne modifiait pas les deux labels suivants.
        # On le conserve afin de ne pas changer le rendu existant.

    def _update_daily_worktime(self, entries):
        today = date.today().isoformat()

        total_today = sum(
            entry.get("temps_total", 0)
            for entry in entries
            if entry.get("jour") == today
        )

        hours = total_today // 60
        minutes = total_today % 60

        self.label_total.configure(
            text=(
                f"{self.lang_util.t('votre_temps_de_travail_aujourdhui')} "
                f"{hours}h{minutes:02d}"
            )
        )

    def _entries_for_current_month(self, entries):
        now = datetime.now()
        current_entries = []

        for entry in entries:
            day_str = entry.get("jour")
            if not day_str:
                continue

            try:
                entry_date = datetime.fromisoformat(day_str)
            except (TypeError, ValueError):
                continue

            if entry_date.month == now.month and entry_date.year == now.year:
                current_entries.append(entry)

        return current_entries

    def _update_monthly_worktime(self, entries):
        current_entries = self._entries_for_current_month(entries)

        total_month = sum(
            entry.get("temps_total", 0)
            for entry in current_entries
        )

        productive_total = int(total_month * PRODUCTIVE_RATIO)
        hours = productive_total // 60
        minutes = productive_total % 60

        self.label_mois.configure(
            text=(
                f"{self.lang_util.t('temps_travaille_ce_mois')} "
                f"{hours}h{minutes:02d}"
            ),
            text_color="purple",
        )

    def _update_magellan_remaining(self, entries):
        current_entries = self._entries_for_current_month(entries)

        remaining = sum(
            entry.get("temps_total", 0)
            for entry in current_entries
            if entry.get("saisie_magellan") is False
        )

        productive_remaining = int(remaining * PRODUCTIVE_RATIO)
        hours = productive_remaining // 60
        minutes = productive_remaining % 60

        self.label_saisie.configure(
            text=(
                f"{self.lang_util.t('temps_restant_saisie')} "
                f"{hours}h{minutes:02d}"
            ),
            text_color="blue",
        )

    def _update_hv(self, entries):
        cumul_hv = 0
        days = {}

        for entry in entries:
            day_str = entry.get("jour")
            if not day_str:
                continue

            try:
                day_date = datetime.fromisoformat(day_str).date()
            except (TypeError, ValueError):
                continue

            if self.last_reset_date and day_date < self.last_reset_date:
                continue

            worktime = entry.get("temps_total", 0)
            days.setdefault(day_str, 0)
            days[day_str] += worktime

        role = getattr(self.app, "user_role", "Technicien")
        hv_max_total = 454 if role == "Technicien" else 908

        for _, total_day in sorted(days.items()):
            if total_day > MAX_JOURNEE:
                hv_day = min(
                    total_day - MAX_JOURNEE,
                    MAX_HV_PAR_JOUR,
                )
                cumul_hv += hv_day

            if cumul_hv > hv_max_total:
                cumul_hv = hv_max_total
                break

        hours = cumul_hv // 60
        minutes = cumul_hv % 60

        self.label_hv.configure(
            text=(
                f"{self.lang_util.t('vos_cumuls_hv')} "
                f"{hours}h{minutes:02d}"
            ),
            text_color="green",
        )

    # =========================================================================
    # ACTIONS ET UTILITAIRES
    # =========================================================================

    def open_link(self, url):
        webbrowser.open(url)

    def reset_hv(self):
        """Enregistre la date actuelle comme nouveau point de départ des HV."""
        today = date.today()
        self.last_reset_date = today

        try:
            with open(DASHBOARD_CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    {"last_reset": today.isoformat()},
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
        except OSError as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer la réinitialisation des HV :\n\n{error}",
            )
            return

        self.refresh()

    def decrypt_url(self, encrypted_url):
        return FERNET.decrypt(
            encrypted_url.encode("utf-8")
        ).decode("utf-8")
