import customtkinter as ctk
import json
import webbrowser
import os
import json
import shutil
import uuid

from pathlib import Path
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from PIL import Image
from utils.page_lang import PageLang
from datetime import date, datetime
from tkinter import Menu
from config.paths import DATA_FILE, DASHBOARD_CONFIG_FILE, resource_path, SHORTCUTS_FILE, SHORTCUTS_ICONS_DIR, APP_DATA_DIR

# -- Constantes --
ENV_FILE = APP_DATA_DIR / "workingtime.dat"
load_dotenv(ENV_FILE)

MAX_JOURNEE = 454           # 7h34 en minutes
MAX_HV_PAR_JOUR = 50        # max HV par jour
URL_KEY = os.getenv("URL_KEY")

if not URL_KEY:
    raise ValueError("URL_KEY absente du fichier .env")

FERNET = Fernet(URL_KEY.encode("utf-8"))

class PageAccueil(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.custom_shortcuts = self.load_custom_shortcuts()

        # ------------------ Partie flag HV -------------------
        self.last_reset_date = None
        if DASHBOARD_CONFIG_FILE.exists():
            try:
                with open(DASHBOARD_CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    date_str = config.get("last_reset")
                    if date_str:
                        self.last_reset_date = datetime.fromisoformat(date_str).date()
            except:
                self.last_reset_date = None

        # Création de l'utilitaire de traduction
        self.lang_util = PageLang(app)

        # --- Header bleu ---
        header_frame = ctk.CTkFrame(self, border_width=1, border_color="blue", fg_color="#1E5CC4", height=80)
        header_frame.pack(fill="x", padx=5, pady=5)

        # Conteneur du titre
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.place(relx=0.5, rely=0.5, anchor="center")

        # Titre
        self.title_label = ctk.CTkLabel(title_container, text=self.lang_util.t("mon_dashboard_ratp"),
                                   font=("Roboto", 24), text_color="white")
        self.title_label.pack(pady=(0,5))

        # Sous titre
        self.subtitle_label = ctk.CTkLabel(title_container,
                                      text=self.lang_util.t("La Régie Autonome des Transports Parisiens"),
                                      font=("Roboto", 12), text_color="white")
        self.subtitle_label.pack()

        # --- Contour autour du message Bonjour prénom + badge ---
        greeting_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=2,
            border_color=("gray68", "gray30"),
            fg_color=("gray75", "gray20")
        )
        greeting_frame.pack(pady=(30,30), padx=20)

        # Frame horizontale pour prénom + badge
        frame_h = ctk.CTkFrame(greeting_frame, fg_color="transparent")
        frame_h.pack(padx=15, pady=10)

        # Prénom
        self.greeting_label = ctk.CTkLabel(
            frame_h,
            text=self.lang_util.t(f"Bonjour {self.app.user_name}"),
            font=("Roboto", 20)
        )
        self.greeting_label.pack(side="left")

        # Badge rôle
        role = getattr(self.app, "user_role", "Opérateur")  # valeur par défaut
        role_config = {
            "Opérateur": {"color": "#0066DB", "label": "Opérateur"},
            "Technicien": {"color": "#009E1A", "label": "Tech"},
            "Technicien Superieur": {"color": "#FF9900", "label": "Tech sup"},
            "Manager": {"color": "#FF0000", "label": "Manager" },
            "Bureau Technique": {"color": "#BB00AB", "label": "BT"},
            "Service Informatique": {"color": "#000000", "label": "SI"}
        }

        config = role_config.get(role, {"color": "#444444", "label": role})
        color_badge = config["color"]
        badge_text = config["label"]

        self.badge_role = ctk.CTkLabel(
            frame_h,
            text=badge_text,
            font=("Roboto", 12, "bold"),
            text_color="white",
            fg_color=color_badge,
            corner_radius=50,
            width=120,
            height=24
        )
        self.badge_role.pack(side="left", padx=(10,0))

        # ================= CADRE DATE ET HEURE =================

        self.datetime_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=2,
            border_color=("gray68", "gray30"),
            fg_color=("gray75", "gray20")
        )
        self.datetime_frame.pack(
            pady=(8, 30),
            padx=20
        )

        self.date_label = ctk.CTkLabel(
            self.datetime_frame,
            text="",
            font=("Roboto", 14, "bold")
        )
        self.date_label.pack(
            padx=20,
            pady=(10, 2)
        )

        self.time_label = ctk.CTkLabel(
            self.datetime_frame,
            text="",
            font=("Roboto", 16, "bold")
        )
        self.time_label.pack(
            padx=20,
            pady=(2, 10)
        )

        self.update_datetime()

        # --- Zone affichage icones raccourcis ---
        # --- Conteneur pleine largeur des icones ---
        self.icon_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            border_width=2,
            border_color=("gray68", "gray30"),
            fg_color=("gray75", "gray20")
            )
        self.icon_frame.pack(pady=(0,30), padx=20, fill="x")

        # --- Badge "Mes raccourcis" ---
        self.shortcuts_label = ctk.CTkLabel(
            self.icon_frame,
            text=self.lang_util.t("mes_raccourcis"),
            font=("Roboto", 14, "bold"),
            text_color="white",
            fg_color="black",
            corner_radius=20,
            padx=15,
            pady=5
        )

        self.shortcuts_label.grid(
            row=0,
            column=0,
            columnspan=6,
            pady=(10, 5),
            padx=(10, 0),
            sticky="w"
        )

        # Raccourcis personnalisés
        self.custom_shortcuts_frame = ctk.CTkFrame(
            self.icon_frame,
            fg_color="transparent"
        )

        self.custom_shortcuts_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            sticky="w",
            padx=(10, 0),
            pady=(10, 5)
        )

        # Bouton ajout
        self.add_shortcut_button = ctk.CTkButton(
            self.icon_frame,
            text="Ajouter un raccourci",
            command=self.open_add_shortcut_modal,
            width=180
        )

        self.add_shortcut_button.grid(
            row=3,
            column=0,
            columnspan=6,
            pady=(5, 10)
        )

        self.refresh_custom_shortcuts()

        # Centrer les 6 colonnes
        self.icon_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5),
            weight=1
        )

        # --- Fonction pour la création d'un icone ---
        def create_icon(col, image_path, url, text):
            try:
                img = Image.open(resource_path(image_path))
                img = img.resize((50, 50))
                icon = ctk.CTkImage(img, size=(50, 50))
            except:
                icon = None  # fallback si image absente

            btn = ctk.CTkButton(
                self.icon_frame,
                image=icon,
                text=text,
                compound="top",
                command=lambda u=url: self.open_link(self.decrypt_url(u)),
                width=100,
                height=80,
                fg_color="black"
            )
            btn.grid(row=1, column=col, padx=20, pady=10)
            btn.image = icon  # IMPORTANT (sinon disparaît)

        # --- Tableau d'icones à créer dans le conteneur ---
        icons = [
            (0, "ui/assets/icons/selftime.jpg", "gAAAAABqTJ7ts4lj09jPUHVuJKNhQTtRLQFwb-W6qKFRhiaDE7OHwAXwPsbyfLQd7ZQy-9_zYMGZFtHoOUqEUC_8_Wmn-tiTcR7syjs2PqbDmYMhkUmz69g=", "Selftime"),
            (1, "ui/assets/icons/magellan.png", "gAAAAABqTJ7tdtOI2MBSYSIWHzQp9A3ziA8fgzs1P1M0SXkCNjbUyJad7cEleJPiVAluwLhkk0jzX8RylO5ddj3jZL3VHJUHer0T8RnziDdMRMBNNQmn9WllNcimAU7beccZtwGDMI9Q-Br79iBh4rGH1YxykWjqwvFYAkQassoOWsEHV93X8JE=", "Magellan Mobi"),
            (2, "ui/assets/icons/magellan.png", "gAAAAABqTJ7tJu9H69MJlF_-7r6Lf4A4M99lKHSMKPubWM46qPK-lK2Y_RFALGri3FBPdukINQIJ_9Rtvx7-_qdmGk0VKA9bGlvrfHhVZhFl0s_CtFbyUI401g650rYWlIdf7drR7hUHEoIxa8c91Nju88VfrSSDlidChYfE3nf3VJ_9ByLiPPU=", "Magellan Fixe"),
            (3, "ui/assets/icons/ihm.png", "gAAAAABqTJ7tkpAmamnbwiOFlkcnwUoTvgUp_OHFuQYbM6X-6PLahMBQ2FvPFL94QpJS2t1icp5UCdYfVkrGf6Y1B771VAh7LRZscNaufnqoqw2tQZ_oG2U-htyzaDHfwnrHnahd0DTY-Zw2oL3hgRFwpSQNxLK1vw==", "IHM"),
            (4, "ui/assets/icons/mpd.png", "gAAAAABqTJ7tKyppaGOhaVaMuBJV7N2jOYpwEtSjfaShS8u--e4cxww-pHDUVu-rEn31aJxx7W4h8Qp11-LHYu1VnnHiyk4UBBDK0zVgc_n3yasqujaCJC_gqzGvPps_t0-LUbVBERRI5HuGnEGHG0XAkjuImGBphg==", "MPD"),
            (5, "ui/assets/icons/urban.png", "gAAAAABqTJ7tUzdFxMkoXE9FvUM_jTDLMpsKr0DFZI76nanAOwf1yBfM76toQoEf4MLwWLFqVkxiZhlVIzzLboneFoBkcJJAAM0hXO5XmKD96CQOzMcLcui7ALg_m7IG67dTgO_JSXNF", "Urban AME")
        ]

        for col, img, url, text in icons:
            create_icon(col, img, url, text)

        # --- Zone affichage HV ---
        # Conteneur pleine largeur (sert juste à centrer)
        self.info_container = ctk.CTkFrame(self, fg_color="transparent")
        self.info_container.pack(pady=20, padx=20, fill="x")

        # Frame réelle limitée à 55% de la largeur du conteneur principal + effet cadre relief
        self.info_frame = ctk.CTkFrame(
            self.info_container, 
            corner_radius=10, 
            # ------------- effet relief --------------
            fg_color=("gray75", "gray20"), 
            border_width=2,border_color=("gray68", "gray30"))
            # -----------------------------------------
        self.info_frame.pack(
            pady=5,
            padx=100,
            fill="x"
        )

        # --- Labels ---
        self.label_total = ctk.CTkLabel(self.info_frame, text="", font=("Roboto", 18))
        self.label_total.pack(pady=(15, 5))

        self.label_mois = ctk.CTkLabel(self.info_frame, text="", font=("Roboto", 18))
        self.label_mois.pack(pady=(5, 5))

        self.label_saisie = ctk.CTkLabel(self.info_frame, text="", font=("Roboto", 18))
        self.label_saisie.pack(pady=(5, 5))

        self.label_hv = ctk.CTkLabel(self.info_frame, text="", font=("Roboto", 18))
        self.label_hv.pack(pady=(5, 15))

        # --- Bouton réinitialisation HV ---
        self.btn_reset_hv = ctk.CTkButton(
            self,
            text=self.lang_util.t("reset_hv"),
            command=self.reset_hv
        )
        self.btn_reset_hv.pack(pady=5)

        # Affichage initial
        self.refresh()

    # ---------------------------------------------------------------------
    # Rafraichissement du language traduit
    # ---------------------------------------------------------------------
    def refresh_language(self):
        self.lang_util = PageLang(self.app)  # recharge l'utilitaire au cas où
        # Mettre à jour tous les textes
        self.title_label.configure(text=self.lang_util.t("mon_dashboard_ratp"))
        self.subtitle_label.configure(text=self.lang_util.t("la_regie_autonome_des_transports_parisiens"))
        self.greeting_label.configure(text=f"{self.lang_util.t("bonjour")} {self.app.user_name}")
        self.btn_reset_hv.configure(text=self.lang_util.t("reset_hv"))
        self.shortcuts_label.configure(text=self.lang_util.t("mes_raccourcis"))
        self.refresh()

    # ---------------------------------------------------------------------
    # Affichage date et heure
    # ---------------------------------------------------------------------
    def update_datetime(self):
                now = datetime.now()
            
                # Jours et mois en français
                jours = [
                    "lundi", "mardi", "mercredi", "jeudi",
                    "vendredi", "samedi", "dimanche"
                ]
            
                mois = [
                    "janvier", "février", "mars", "avril",
                    "mai", "juin", "juillet", "août",
                    "septembre", "octobre", "novembre", "décembre"
                ]
            
                date_fr = (
                    f"{jours[now.weekday()]} "
                    f"{now.day} {mois[now.month - 1]} {now.year}"
                )
            
                heure = now.strftime("%H:%M:%S")
            
                self.date_label.configure(
                    text=f"{date_fr}"
                )
            
                self.time_label.configure(
                    text=f"{heure}"
                )
            
                # Mise à jour toutes les secondes
                self.after(1000, self.update_datetime)

    # ---------------------------------------------------------------------
    # Chargement icones personalisés
    # ---------------------------------------------------------------------
    def load_custom_shortcuts(self):
        if not SHORTCUTS_FILE.exists():
            return []

        try:
            with open(SHORTCUTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                return data

        except Exception as e:
            print(f"Erreur chargement raccourcis : {e}")

        return []

    # ---------------------------------------------------------------------
    # Sauvegarde des icones
    # ---------------------------------------------------------------------
    def save_custom_shortcuts(self):
        try:
            with open(SHORTCUTS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    self.custom_shortcuts,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'enregistrer les raccourcis :\n\n{e}"
            )

    # ---------------------------------------------------------------------
    # Modal pour ajout des raccourcis icones et liens
    # ---------------------------------------------------------------------
    def open_add_shortcut_modal(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter un raccourci")
        popup.geometry("500x430")
        popup.resizable(False, False)

        # Attacher la modal à la fenêtre principale
        main_window = self.winfo_toplevel()
        popup.transient(main_window)

        # Attendre que Tkinter connaisse les dimensions
        popup.update_idletasks()

        # Dimensions de la modal
        popup_width = 500
        popup_height = 430

        # Position et dimensions de la fenêtre principale
        main_x = main_window.winfo_rootx()
        main_y = main_window.winfo_rooty()
        main_width = main_window.winfo_width()
        main_height = main_window.winfo_height()

        # Calcul du centre de WorkingTimeRatp
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2

        # Positionner la modal
        popup.geometry(
            f"{popup_width}x{popup_height}+{x}+{y}"
        )

        # Modal
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(
            popup,
            text="Ajouter un raccourci",
            font=("Roboto", 20, "bold")
        ).pack(pady=(20, 20))

        # ================= NOM =================

        ctk.CTkLabel(
            popup,
            text="Nom du raccourci"
        ).pack(anchor="w", padx=40)

        name_entry = ctk.CTkEntry(
            popup,
            width=420,
            placeholder_text="Ex : Intranet"
        )
        name_entry.pack(padx=40, pady=(5, 15))

        # ================= URL =================

        ctk.CTkLabel(
            popup,
            text="Lien"
        ).pack(anchor="w", padx=40)

        url_entry = ctk.CTkEntry(
            popup,
            width=420,
            placeholder_text="https://..."
        )
        url_entry.pack(padx=40, pady=(5, 15))

        # ================= ICÔNE =================

        selected_icon = {
            "path": None
        }

        icon_label = ctk.CTkLabel(
            popup,
            text="Aucune icône sélectionnée"
        )
        icon_label.pack(pady=(5, 5))

        def choose_icon():

            path = filedialog.askopenfilename(
                parent=popup,
                title="Choisir une icône",
                filetypes=[
                    (
                        "Images",
                        "*.png *.jpg *.jpeg *.ico *.webp"
                    )
                ]
            )

            if not path:
                return

            selected_icon["path"] = path

            icon_label.configure(
                text=Path(path).name
            )

        ctk.CTkButton(
            popup,
            text="Choisir une icône",
            command=choose_icon,
            width=200
        ).pack(pady=(5, 20))

        # ================= ENREGISTRER =================

        def save():

            name = name_entry.get().strip()
            url = url_entry.get().strip()
            source_icon = selected_icon["path"]

            if not name:
                messagebox.showwarning(
                    "Nom manquant",
                    "Veuillez saisir un nom.",
                    parent=popup
                )
                return

            if not url:
                messagebox.showwarning(
                    "Lien manquant",
                    "Veuillez saisir un lien.",
                    parent=popup
                )
                return

            if not source_icon:
                messagebox.showwarning(
                    "Icône manquante",
                    "Veuillez sélectionner une icône.",
                    parent=popup
                )
                return

            # Ajouter https:// si nécessaire
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            try:
                source = Path(source_icon)

                # Nom unique pour éviter les collisions
                icon_name = (
                    f"{uuid.uuid4().hex}"
                    f"{source.suffix.lower()}"
                )

                destination = SHORTCUTS_ICONS_DIR / icon_name

                shutil.copy2(
                    source,
                    destination
                )

                shortcut = {
                    "id": uuid.uuid4().hex,
                    "name": name,
                    "url": url,
                    "icon": str(destination)
                }

                self.custom_shortcuts.append(shortcut)

                self.save_custom_shortcuts()

                popup.destroy()

                self.refresh_custom_shortcuts()

            except Exception as e:

                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'ajouter le raccourci :\n\n{e}",
                    parent=popup
                )

        buttons_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )
        buttons_frame.pack(pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="Enregistrer",
            command=save,
            width=150
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            command=popup.destroy,
            width=150,
            fg_color="#555555"
        ).pack(
            side="left",
            padx=5
        )

    def refresh_custom_shortcuts(self):
        # Supprimer uniquement les raccourcis personnalisés affichés
        for widget in self.custom_shortcuts_frame.winfo_children():
            widget.destroy()

        # Aucun raccourci personnalisé -> masquer le conteneur
        if not self.custom_shortcuts:
            self.custom_shortcuts_frame.grid_remove()
            return

        # Il y a des raccourcis -> réafficher le conteneur
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

            except Exception:
                icon = None

            button = ctk.CTkButton(
                self.custom_shortcuts_frame,
                text=name,
                image=icon,
                compound="top",
                width=100,
                height=80,
                fg_color="black",
                # hover_color="#251F1F",
                border_color="black",
                border_width=0,
                text_color="white",
                command=lambda u=url: self.open_link(u)
            )

            # Important pour conserver l'image
            button.image = icon

            # Menu contextuel
            menu = Menu(
                button,
                tearoff=0
            )

            menu.add_command(
                label="Supprimer",
                command=lambda sid=shortcut.get("id"):
                    self.delete_custom_shortcut(sid)
            )

            def show_menu(event, context_menu=menu):
                context_menu.tk_popup(
                    event.x_root,
                    event.y_root
                )

            button.bind(
                "<Button-3>",
                show_menu
            )

            row = index // 6
            column = index % 6

            button.grid(
                row=row,
                column=column,
                padx=(18, 40),
                pady=10
            )

    def delete_custom_shortcut(self, shortcut_id):
        shortcut = next(
            (
                s for s in self.custom_shortcuts
                if s.get("id") == shortcut_id
            ),
            None
        )

        if not shortcut:
            return

        confirm = messagebox.askyesno(
            "Supprimer le raccourci",
            f"Voulez-vous supprimer le raccourci :\n\n{shortcut.get('name', '')} ?"
        )

        if not confirm:
            return

        # Supprimer l'icône locale
        icon_path = shortcut.get("icon")

        if icon_path:
            try:
                path = Path(icon_path)

                if path.exists():
                    path.unlink()

            except Exception as e:
                print(f"Impossible de supprimer l'icône : {e}")

        # Supprimer le raccourci de la liste
        self.custom_shortcuts = [
            s for s in self.custom_shortcuts
            if s.get("id") != shortcut_id
        ]

        # Sauvegarder le JSON
        self.save_custom_shortcuts()

        # Rafraîchir l'affichage
        self.refresh_custom_shortcuts()

    # ---------------------------------------------------------------------
    # Calcul et affichage HV cumulées
    # ---------------------------------------------------------------------
    def refresh(self):
        if not DATA_FILE.exists():
            self.label_total.configure(text=self.lang_util.t("aucunes_donnees_enregistre"))
            self.label_hv.configure(text="")
            return

        entries = []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    entries.append(data)
                except:
                    continue

        if not entries:
            self.label_total.configure(text=self.lang_util.t("aucunes_donnees_enregistre"))
            self.label_hv.configure(text="")
            return

        # --- Total travaillé aujourd'hui ---
        today = date.today().isoformat()
        total_today = sum(
            e.get("temps_total", 0)
            for e in entries
            if e.get("jour") == today
        )
        h_today = total_today // 60
        m_today = total_today % 60
        self.label_total.configure(
            text=f"{self.lang_util.t('votre_temps_de_travail_aujourdhui')} {h_today}h{m_today:02d}"
        )

        # --- Total travaillé sur le mois en cours ---
        now = datetime.now()

        total_mois = sum(
            e.get("temps_total", 0)
            for e in entries
            if "jour" in e and
            datetime.fromisoformat(e["jour"]).month == now.month and
            datetime.fromisoformat(e["jour"]).year == now.year
        )

        # Appliquer 87% sur le total en minutes
        total_prod = int(total_mois * 0.87)

        hm = total_prod // 60
        mm = total_prod % 60

        self.label_mois.configure(
            text=f"{self.lang_util.t('temps_travaille_ce_mois')} {hm}h{mm:02d}",
            text_color="purple"
        )

        # Temps à saisir restant :
        a_saisir = sum(
            e.get("temps_total",0)
            for e in entries
            if "jour" in e and
            datetime.fromisoformat(e["jour"]).month == now.month and
            datetime.fromisoformat(e["jour"]).year == now.year and
            e.get("saisie_magellan") == False
        )

        total_saisie = int(a_saisir * 0.87)

        th_saisir = total_saisie // 60
        tm_saisir = total_saisie % 60 

        self.label_saisie.configure(
            text=f"{self.lang_util.t("temps_restant_saisie")} {th_saisir}h{tm_saisir:02d}",
            text_color="blue"
        )

       # --- Calcul HV cumulées avec plafond rôle (reset par date) ---
        cumul_hv = 0
        jours = {}

        for e in entries:
            jour_str = e.get("jour")
            if not jour_str:
                continue

            jour_date = datetime.fromisoformat(jour_str).date()

            # Ignorer les journées avant la date de reset
            if self.last_reset_date and jour_date < self.last_reset_date:
                continue

            temps = e.get("temps_total", 0)
            jours.setdefault(jour_str, 0)
            jours[jour_str] += temps


        # Plafond cumulé selon rôle
        role = getattr(self.app, "user_role", "Technicien")
        hv_max_total = 454 if role == "Technicien" else 908  # 7h34 ou 15h08

        for jour_str, total_jour in sorted(jours.items()):
            if total_jour > MAX_JOURNEE:
                hv_jour = min(total_jour - MAX_JOURNEE, MAX_HV_PAR_JOUR)
                cumul_hv += hv_jour

            if cumul_hv > hv_max_total:
                cumul_hv = hv_max_total
                break


        eh = cumul_hv // 60
        em = cumul_hv % 60

        self.label_hv.configure(
            text=f"{self.lang_util.t('vos_cumuls_hv')} {eh}h{em:02d}",
            text_color="green"
        )

    # ---- fonction appel de pages internet ----
    def open_link(self, url):
        webbrowser.open(url)

    # ---------------------------------------------------------------------
    # Bouton Réinitialiser HV
    # ---------------------------------------------------------------------
    def reset_hv(self):
        """Enregistre la date actuelle comme point de départ des HV"""
        today = date.today()
        self.last_reset_date = today

        with open(DASHBOARD_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"last_reset": today.isoformat()},
                f,
                ensure_ascii=False,
                indent=2
            )

        self.refresh()

    # Decrypter liens internets
    def decrypt_url(self, encrypted_url):
        return FERNET.decrypt(encrypted_url.encode()).decode("utf-8")

