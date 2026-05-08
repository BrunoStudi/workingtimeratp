import customtkinter as ctk
import json
import os

from PIL import Image
from ui.page_saisie import PageSaisie
from ui.page_historique import PageHistorique
from ui.page_organes import PageOrganes
from ui.page_accueil import PageAccueil
from ui.page_parametres import PageParams
from ui.page_apropos import PageApropos
from ui.page_depannage import PageDepannage
from ui.page_consommables import PageConsommables
from ui.page_profil import PageProfil
from utils.settings import load_settings, apply_theme
from utils.page_lang import PageLang
from config.paths import DATA_FILE, USER_FILE


# ----------------- Fonctions utilitaires -----------------
# Chargement / creation des données Organes
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except:
            return {}
    return {}

def save_data(entry):
    with open(DATA_FILE, "a", encoding="utf-8") as f:  
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def load_all_entries():
    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    pass
    return entries

# Suppression des données
def delete_all_entries():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

# ----------------- Classe Dashboard -----------------
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        settings = load_settings()
        self.lang = settings.get("lang", "francais")
        self.lang_util = PageLang(self)
        apply_theme(settings.get("theme", "Dark"))

        self.title("Journées de travail RATP - Application Agent v1.27.23")
        self.geometry("1180x850")

        icon_path = os.path.join("ui", "assets", "train.ico")
        self.iconbitmap(icon_path)

        # --- Initialisation des infos utilisateur ---
        self.user_name = None
        self.user_lastname = None
        self.user_role = "Opérateur"  # valeur par défaut
        self.user_team = None
        self.load_user_data()  # récupère prénom et rôle si existants

        if not self.user_name:
            self.ask_user_name()

        # ==== Sidebar ====
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        # ---- Logo dans la sidebar ----
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("ui/assets/logo_ratp.png"),
                dark_image=Image.open("ui/assets/logo_ratp.png"),
                size=(150, 105)
            )
            ctk.CTkLabel(self.sidebar, image=logo_image, text="").pack(pady=40)
        except:
            ctk.CTkLabel(self.sidebar, text="").pack(pady=40)

        # Boutons menu
        self.btn_accueil=ctk.CTkButton(self.sidebar, text=self.lang_util.t("accueil"), command=self.show_accueil)
        self.btn_accueil.pack(pady=10)
        self.btn_saisie=ctk.CTkButton(self.sidebar, text=self.lang_util.t("saisie"), command=self.show_saisie)
        self.btn_saisie.pack(pady=10)
        self.btn_historique=ctk.CTkButton(self.sidebar, text=self.lang_util.t("historique"), command=self.show_historique)
        self.btn_historique.pack(pady=10)
        self.btn_organes=ctk.CTkButton(self.sidebar, text=self.lang_util.t("organes"), command=self.show_organes)
        self.btn_organes.pack(pady=10)
        self.btn_depann=ctk.CTkButton(self.sidebar, text=self.lang_util.t("depannage"), command=self.show_depannage)
        self.btn_depann.pack(pady=10)
        self.btn_conso=ctk.CTkButton(self.sidebar, text=self.lang_util.t("consommables"), command=self.show_consommables)
        self.btn_conso.pack(pady=10)
        self.btn_profil=ctk.CTkButton(self.sidebar, text=self.lang_util.t("profil"), command=self.show_profil)
        self.btn_profil.pack(pady=10)
        self.btn_params=ctk.CTkButton(self.sidebar, text=self.lang_util.t("parametres"), command=self.show_params)
        self.btn_params.pack(pady=10)
        self.btn_apropos=ctk.CTkButton(self.sidebar, text=self.lang_util.t("a_propos"), command=self.show_apropos)
        self.btn_apropos.pack(pady=10)

        # Zone principale
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Pages
        self.pages = {
            "accueil": PageAccueil(self.main_frame, self),
            "saisie": PageSaisie(self.main_frame, self),
            "historique": PageHistorique(self.main_frame, self),
            "organes": PageOrganes(self.main_frame, self),
            "depann": PageDepannage(self.main_frame,self),
            "conso": PageConsommables(self.main_frame, self),
            "profil": PageProfil(self.main_frame, self),
            "paramètres" : PageParams(self.main_frame, self),
            "apropos" : PageApropos(self.main_frame, self)
        }

        self.refresh_language()

        # Page par défaut
        self.show_accueil()

        for page in self.pages.values():
            if hasattr(page, "refresh_language"):
                page.refresh_language()


    # ----------------- Navigation -----------------
    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(fill="both", expand=True)

    def show_accueil(self):
        self.pages["accueil"].refresh()  # <-- Rafraîchir les totaux
        self.show_page("accueil")

    def show_saisie(self):
        self.pages["saisie"].refresh_materiels()  # <-- recharge dropdown organes
        self.show_page("saisie")

    def show_historique(self):
        self.pages["historique"].refresh()
        self.show_page("historique")

    def show_organes(self):
        self.show_page("organes")

    def show_depannage(self):
        self.show_page("depann")
        self.pages["depann"].refresh_materiels()

    def show_consommables(self):
        self.show_page("conso")

    def show_profil(self):
        self.show_page("profil")

    def show_params(self):
        self.show_page("paramètres")

    def show_apropos(self):
        self.show_page("apropos")

    # ------------------ Méthode utilitaire : centrer un popup --------------
    def center_popup(self, popup):
        """
        Centre le CTkToplevel `popup` par rapport à la fenêtre principale.
        Appeler après popup.update_idletasks().
        """
        # Forcer mise à jour géométrie
        self.update_idletasks()
        popup.update_idletasks()

        parent_win = self.winfo_toplevel()
        parent_x = parent_win.winfo_rootx()
        parent_y = parent_win.winfo_rooty()
        parent_w = parent_win.winfo_width()
        parent_h = parent_win.winfo_height()

        popup_w = popup.winfo_width()
        popup_h = popup.winfo_height()
        if popup_w <= 1:
            popup_w = popup.winfo_reqwidth()
        if popup_h <= 1:
            popup_h = popup.winfo_reqheight()

        x = parent_x + max(0, (parent_w // 2) - (popup_w // 2))
        y = parent_y + max(0, (parent_h // 2) - (popup_h // 2))

        popup.geometry(f"+{x}+{y}")

    # ----------------- Prénom utilisateur -----------------
    def load_user_data(self):
        if USER_FILE.exists():
            try:
                with open(USER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_name = data.get("prenom")
                    self.user_lastname = data.get("nom")
                    self.user_role = data.get("role", "Opérateur")  # valeur par défaut
                    self.user_team = data.get("equipe")
            except:
                self.user_name = None
                self.user_lastname = None
                self.user_role = "Opérateur"
                self.user_team = None

    # Fonction demande du prénom
    def ask_user_name(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Bienvenue !")
        popup.iconbitmap("ui/assets/train.ico")
        popup.geometry("400x300")
        popup.grab_set()
        popup.resizable(False, False)

        popup.update_idletasks()
        self.center_popup(popup)

        header = ctk.CTkFrame(popup, fg_color="#1E5CC4", height=60)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Bienvenue Agent", font=("Roboto", 18), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(popup, text="Veuillez entrer votre prénom :", font=("Roboto", 14)).pack(pady=(20,5))
        entry = ctk.CTkEntry(popup, width=200, font=("Roboto", 14))
        entry.pack(pady=5)
        entry.focus()

        ctk.CTkLabel(popup, text="Sélectionnez votre rôle :", font=("Roboto", 14)).pack(pady=(10,5))

        # Variable rôle
        role_var = ctk.StringVar(value="Opérateur")  # valeur par défaut

        # Radio boutons exclusifs
        ctk.CTkRadioButton(popup, text="Opérateur", variable=role_var, value="Opérateur").pack(pady=2)
        ctk.CTkRadioButton(popup, text="Technicien", variable=role_var, value="Technicien").pack(pady=2)
        ctk.CTkRadioButton(popup, text="Technicien supérieur", variable=role_var, value="Technicien Superieur").pack(pady=2)

        def valider():
            USER_FILE.parent.mkdir(parents=True, exist_ok=True)

            name = entry.get().strip()
            self.user_name = name if name else "Utilisateur"
            self.user_role = role_var.get()  # <- ici on récupère le rôle sélectionné
            with open(USER_FILE, "w", encoding="utf-8") as f:
                json.dump({"prenom": self.user_name, "nom": "", "role": self.user_role, "equipe": ""}, f, ensure_ascii=False, indent=4)
            popup.destroy()

            # --- Actualisation de la page Accueil si déjà créée ---
            if "accueil" in getattr(self, "pages", {}):
                accueil_page = self.pages["accueil"]
                # Mettre à jour le label prénom
                accueil_page.greeting_label.configure(text=f"Bonjour {self.user_name} !")
                # Mettre à jour le badge rôle
                color_badge = "#0024F3" if self.user_role == "Opérateur" else "#ACACAC"
                accueil_page.badge_role.configure(text=self.user_role.upper(), fg_color=color_badge)
                # Rafraîchir les HV
                accueil_page.refresh()

        btn = ctk.CTkButton(popup, text="Valider", command=valider)
        btn.pack(pady=15)
        popup.bind("<Return>", lambda e: valider())

    def refresh_language(self):
        self.lang_util = PageLang(self)

        self.btn_accueil.configure(text=self.lang_util.t("accueil"))
        self.btn_saisie.configure(text=self.lang_util.t("saisie"))
        self.btn_historique.configure(text=self.lang_util.t("historique"))
        self.btn_organes.configure(text=self.lang_util.t("organes"))
        self.btn_depann.configure(text=self.lang_util.t("depannage"))
        self.btn_conso.configure(text=self.lang_util.t("consommables"))
        self.btn_profil.configure(text=self.lang_util.t("profil"))
        self.btn_params.configure(text=self.lang_util.t("parametres"))
        self.btn_apropos.configure(text=self.lang_util.t("a_propos"))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = Dashboard()
    app.mainloop()
