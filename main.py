import json

import customtkinter as ctk
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
from config.paths import DATA_FILE, USER_FILE, resource_path


APP_TITLE = "Journées de travail RATP - Application Agent v1.49.44"
WINDOW_SIZE = "1180x850"
HEADER_COLOR = "#1E5CC4"
DEFAULT_LANGUAGE = "francais"
DEFAULT_THEME = "Dark"
DEFAULT_ROLE = "Opérateur"

SIDEBAR_BUTTONS = (
    ("btn_accueil", "accueil", "show_accueil"),
    ("btn_saisie", "saisie", "show_saisie"),
    ("btn_historique", "historique", "show_historique"),
    ("btn_organes", "organes", "show_organes"),
    ("btn_depann", "depannage", "show_depannage"),
    ("btn_conso", "consommables", "show_consommables"),
    ("btn_profil", "profil", "show_profil"),
    ("btn_params", "parametres", "show_params"),
    ("btn_apropos", "a_propos", "show_apropos"),
)


# ----------------- Fonctions utilitaires -----------------
# Chargement / creation des données Organes
def load_data():
    """Charge DATA_FILE comme JSON classique."""
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            content = file.read().strip()
        return json.loads(content) if content else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(entry):
    """Ajoute une intervention au fichier JSONL."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_all_entries():
    entries = []
    if not DATA_FILE.exists():
        return entries

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []

    return entries


def delete_all_entries():
    try:
        if DATA_FILE.exists():
            DATA_FILE.unlink()
    except OSError as error:
        print(f"Erreur suppression : {error}")


# ----------------- Classe Dashboard -----------------
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._initialize_settings()
        self._configure_window()
        self._initialize_user()
        self._create_sidebar()
        self._create_main_frame()
        self._create_pages()

        self.refresh_language()
        self.show_accueil()

        for page in self.pages.values():
            if hasattr(page, "refresh_language"):
                page.refresh_language()

    def _initialize_settings(self):
        settings = load_settings()
        self.lang = settings.get("lang", DEFAULT_LANGUAGE)
        self.lang_util = PageLang(self)
        apply_theme(settings.get("theme", DEFAULT_THEME))

    def _configure_window(self):
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        try:
            self.iconbitmap(resource_path("ui/assets/train.ico"))
        except Exception:
            pass

    def _initialize_user(self):
        self.user_name = None
        self.user_lastname = None
        self.user_role = DEFAULT_ROLE
        self.user_team = None
        self.load_user_data()

        if not self.user_name:
            self.ask_user_name()

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self._create_sidebar_logo()
        self._create_sidebar_buttons()

    def _create_sidebar_logo(self):
        try:
            logo = resource_path("ui/assets/logo_ratp.png")
            logo_image = ctk.CTkImage(
                light_image=Image.open(logo),
                dark_image=Image.open(logo),
                size=(150, 105),
            )
            ctk.CTkLabel(
                self.sidebar,
                image=logo_image,
                text="",
            ).pack(pady=40)
        except (OSError, ValueError):
            ctk.CTkLabel(self.sidebar, text="").pack(pady=40)

    def _create_sidebar_buttons(self):
        for attribute, translation_key, command_name in SIDEBAR_BUTTONS:
            button = ctk.CTkButton(
                self.sidebar,
                text=self.lang_util.t(translation_key),
                command=getattr(self, command_name),
            )
            button.pack(pady=10)
            setattr(self, attribute, button)

    def _create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

    def _create_pages(self):
        self.pages = {
            "accueil": PageAccueil(self.main_frame, self),
            "saisie": PageSaisie(self.main_frame, self),
            "historique": PageHistorique(self.main_frame, self),
            "organes": PageOrganes(self.main_frame, self),
            "depann": PageDepannage(self.main_frame, self),
            "conso": PageConsommables(self.main_frame, self),
            "profil": PageProfil(self.main_frame, self),
            "paramètres": PageParams(self.main_frame, self),
            "apropos": PageApropos(self.main_frame, self),
        }

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
        if not USER_FILE.exists():
            return

        try:
            with USER_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.user_name = data.get("prenom")
            self.user_lastname = data.get("nom")
            self.user_role = data.get("role", DEFAULT_ROLE)
            self.user_team = data.get("equipe")
        except (json.JSONDecodeError, OSError):
            self.user_name = None
            self.user_lastname = None
            self.user_role = DEFAULT_ROLE
            self.user_team = None

    # Fonction demande du prénom
    def ask_user_name(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Bienvenue !")
        popup.iconbitmap(resource_path("ui/assets/train.ico"))
        popup.geometry("400x300")
        popup.grab_set()
        popup.resizable(False, False)
        popup.update_idletasks()
        self.center_popup(popup)

        header = ctk.CTkFrame(popup, fg_color=HEADER_COLOR, height=60)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Bienvenue Agent", font=("Roboto", 18), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(popup, text="Veuillez entrer votre prénom :", font=("Roboto", 14)).pack(pady=(20,5))
        entry = ctk.CTkEntry(popup, width=200, font=("Roboto", 14))
        entry.pack(pady=5)
        entry.focus()
        ctk.CTkLabel(popup, text="Sélectionnez votre rôle :", font=("Roboto", 14)).pack(pady=(10,5))

        # Variable rôle
        role_var = ctk.StringVar(value=DEFAULT_ROLE)  # valeur par défaut

        # Radio boutons exclusifs
        ctk.CTkRadioButton(popup, text="Opérateur", variable=role_var, value="Opérateur").pack(pady=2)
        ctk.CTkRadioButton(popup, text="Technicien", variable=role_var, value="Technicien").pack(pady=2)
        ctk.CTkRadioButton(popup, text="Technicien supérieur", variable=role_var, value="Technicien Superieur").pack(pady=2)

        # Valider les données
        def valider():
            USER_FILE.parent.mkdir(parents=True, exist_ok=True)
            name = entry.get().strip()
            self.user_name = name if name else "Utilisateur"
            self.user_role = role_var.get()  # <- ici on récupère le rôle sélectionné
            with USER_FILE.open("w", encoding="utf-8") as file:
                json.dump(
                    {
                        "prenom": self.user_name,
                        "nom": "",
                        "role": self.user_role,
                        "equipe": "",
                    },
                    file,
                    ensure_ascii=False,
                    indent=4,
                )
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

    # Rafraichissement de la langue
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
