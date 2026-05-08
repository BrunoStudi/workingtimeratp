import customtkinter as ctk
import json

from utils.page_lang import PageLang
from config.paths import USER_FILE


# ------------ Classe Principale Profile -------------
class PageProfil(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.lang_util = PageLang(app)
        self.app = app

        # ================= HEADER =================
        self.header = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color="#1E5CC4",
            height=60
        )
        self.header.pack(fill="x", padx=5, pady=5)
        self.header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(
            self.header,
            text=self.lang_util.t("mon_profil"),
            font=("Roboto", 24),
            text_color="white"
        )
        self.header_label.pack(expand=True)

        # ---------- Conteneur principal --------------
        self.main_container = ctk.CTkFrame(
            self,
            border_width=1,
            border_color=("gray68", "gray30"),
            fg_color=("gray75", "gray20"),
        )
        self.main_container.pack(fill="x", expand=True, padx=50, pady=(5,5))

        # ---------------- Configuration grille ----------------
        self.main_container.grid_columnconfigure((0, 1), weight=1)
        self.main_container.grid_rowconfigure((1, 2), weight=1)

        self.info_title = ctk.CTkLabel(
             self.main_container,
             text=self.lang_util.t("mes_informations"),
             font=("Roboto", 14, "bold"),
             text_color="white",
             fg_color="black",
             corner_radius=20,
             padx= 8,
             pady=5
        )
        self.info_title.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=15,
            pady=(10, 20)
        )

        self.load_user()  # récupère infos utilisateur si existantes

        # ------ Variables pour la création des
        # cartes avec appel de la focntion pour la creation de cartes 
        prenom = self.app.user_name or "Non défini"
        role = self.app.user_role or "Non défini"
        nom = self.app.user_lastname or "Non défini"
        team = self.app.user_team or "Non défini"

        self.create_info_card(1, 0, "Prénom", prenom)
        self.create_info_card(1, 1, "Nom", nom)
        self.create_info_card(2, 0, "Grade", role)
        self.create_info_card(2, 1, "Equipe", team)

        self.btn_edit = ctk.CTkButton(
            self.main_container,
            text=self.lang_util.t("modifier_information"),
            command=self.open_edit_popup
        )
        self.btn_edit.grid(row=3, column=0, columnspan=2, pady=20)

    # --------- Charger les données utilisateur -------------
    def load_user(self):
        if USER_FILE.exists():
            try:
                with open(USER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.app.user_name = data.get("prenom")
                    self.app.user_role = data.get("role")
                    self.app.user_lastname = data.get("nom")
                    self.app.user_team = data.get("equipe")
                        
            except:
                self.app.user_name = None
                self.app.user_role = None
                self.app.user_lastname = None
                self.app.user_team = None

    # ----------- Fonction pour création de cartes ------------
    def create_info_card(self, row, col, title, value):
        card = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color=("gray85", "gray25"),
            border_width=1
        )
        card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 12),
            text_color="gray"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 16, "bold")
        ).pack(pady=(0, 10))

    def open_edit_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Modifier profil")
        self.center_popup(popup, 400, 380)
        popup.transient(self)
        popup.grab_set()
        popup.lift()
        popup.focus_force()
        popup.resizable(False, False)

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Prénom ---
        ctk.CTkLabel(frame, text="Prénom").pack(anchor="w", padx=5)
        prenom_entry = ctk.CTkEntry(frame)
        prenom_entry.pack(fill="x", pady=5, padx=5)
        prenom_entry.insert(0, self.app.user_name or "")

        # --- Nom ---
        ctk.CTkLabel(frame, text="Nom").pack(anchor="w", padx=5)
        nom_entry = ctk.CTkEntry(frame)
        nom_entry.pack(fill="x", pady=5, padx=5)
        nom_entry.insert(0, self.app.user_lastname or "")

        # --- Grade (dropdown) ---
        ctk.CTkLabel(frame, text="Grade").pack(anchor="w", padx=5)
        grade_var = ctk.StringVar(value=self.app.user_role or "Inconnu")

        grades = ["Opérateur", "Technicien", "Technicien Superieur", "Manager", "Bureau Technique", "Service Informatique"]
        grade_menu = ctk.CTkOptionMenu(frame, values=grades, variable=grade_var)
        grade_menu.pack(fill="x", pady=5, padx=5)

        # --- Équipe (dropdown) ---
        ctk.CTkLabel(frame, text="Équipe").pack(anchor="w", padx=5)
        equipe_var = ctk.StringVar(value=self.app.user_team or "Inconnue")

        equipes = ["EK1", "EK11", "EK2", "EK3", "EK4", "EK5", "EK7", "EN31", "EN32"]
        equipe_menu = ctk.CTkOptionMenu(frame, values=equipes, variable=equipe_var)
        equipe_menu.pack(fill="x", pady=5, padx=5)

        def save():
            data = {
                "prenom": prenom_entry.get(),
                "nom": nom_entry.get(),
                "role": grade_var.get(),
                "equipe": equipe_var.get()
            }

            try:
                with open(USER_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print("Erreur sauvegarde :", e)

            # refresh affichage
            self.load_user()
            self.refresh_cards()

            popup.destroy()

        ctk.CTkButton(frame, text="Enregistrer", command=save).pack(pady=20)

    def refresh_cards(self):
        # Détruire les anciennes cards
        for widget in self.main_container.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        prenom = self.app.user_name or "Non défini"
        role = self.app.user_role or "Non défini"
        nom = self.app.user_lastname or "Non défini"
        team = self.app.user_team or "Non définie"

        self.create_info_card(1, 0, "Prénom", prenom)
        self.create_info_card(1, 1, "Nom", nom)
        self.create_info_card(2, 0, "Grade", role)
        self.create_info_card(2, 1, "Équipe", team)

    def center_popup(self, popup, width, height):
        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        popup.geometry(f"{width}x{height}+{x}+{y}")

    # ================= RAFRAÎCHISSEMENT LANGUE =================
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("mon_profil"))
        self.info_title.configure(text=self.lang_util.t("mes_informations"))
        self.btn_edit.configure(text=self.lang_util.t("modifier_information"))