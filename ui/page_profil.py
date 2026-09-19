import json

import customtkinter as ctk

from config.paths import USER_FILE
from utils.page_lang import PageLang


HEADER_COLOR = "#1E5CC4"
UNDEFINED_VALUE = "Non défini"

GRADES = (
    "Opérateur",
    "Technicien",
    "Technicien Superieur",
    "Manager",
    "Bureau Technique",
    "Service Informatique",
)

TEAMS = (
    "EK1",
    "EK11",
    "EK2",
    "EK3",
    "EK4",
    "EK5",
    "EK7",
    "EN31",
    "EN32",
)

EDIT_POPUP_SIZE = (400, 380)


class PageProfil(ctk.CTkFrame):
    """Affichage et modification du profil utilisateur local."""

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.lang_util = PageLang(app)

        self.load_user()

        self._create_header()
        self._create_main_container()
        self._create_profile_content()

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
        self.header.pack_propagate(False)

        self.header_label = ctk.CTkLabel(
            self.header,
            text=self.lang_util.t("mon_profil"),
            font=("Roboto", 24),
            text_color="white",
        )
        self.header_label.pack(expand=True)

    def _create_main_container(self):
        self.main_container = ctk.CTkFrame(
            self,
            border_width=1,
            border_color=("gray68", "gray30"),
            fg_color=("gray75", "gray20"),
        )
        self.main_container.pack(
            fill="x",
            expand=True,
            padx=50,
            pady=(5, 5),
        )

        self.main_container.grid_columnconfigure(
            (0, 1),
            weight=1,
        )
        self.main_container.grid_rowconfigure(
            (1, 2),
            weight=1,
        )

        self.info_title = ctk.CTkLabel(
            self.main_container,
            text=self.lang_util.t("mes_informations"),
            font=("Roboto", 14, "bold"),
            text_color="white",
            fg_color="black",
            corner_radius=20,
            padx=8,
            pady=5,
        )
        self.info_title.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=15,
            pady=(10, 20),
        )

        self.btn_edit = ctk.CTkButton(
            self.main_container,
            text=self.lang_util.t("modifier_information"),
            command=self.open_edit_popup,
        )
        self.btn_edit.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20,
        )

    def _create_profile_content(self):
        values = self._get_profile_display_values()

        self.create_info_card(
            1,
            0,
            "Prénom",
            values["prenom"],
        )
        self.create_info_card(
            1,
            1,
            "Nom",
            values["nom"],
        )
        self.create_info_card(
            2,
            0,
            "Grade",
            values["role"],
        )
        self.create_info_card(
            2,
            1,
            "Équipe",
            values["equipe"],
        )

    def create_info_card(
        self,
        row,
        col,
        title,
        value,
    ):
        card = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color=("gray85", "gray25"),
            border_width=1,
        )
        card.grid(
            row=row,
            column=col,
            padx=15,
            pady=10,
            sticky="nsew",
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 12),
            text_color="gray",
        ).pack(
            pady=(10, 5)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 16, "bold"),
        ).pack(
            pady=(0, 10)
        )

    # ------------------------------------------------------------------
    # Chargement / sauvegarde du profil
    # ------------------------------------------------------------------

    def load_user(self):
        data = self._read_user_file()

        self.app.user_name = data.get("prenom")
        self.app.user_role = data.get("role")
        self.app.user_lastname = data.get("nom")
        self.app.user_team = data.get("equipe")

    @staticmethod
    def _read_user_file():
        if not USER_FILE.exists():
            return {}

        try:
            with USER_FILE.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def _write_user_file(data):
        USER_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with USER_FILE.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def _get_profile_display_values(self):
        return {
            "prenom": self.app.user_name or UNDEFINED_VALUE,
            "nom": self.app.user_lastname or UNDEFINED_VALUE,
            "role": self.app.user_role or UNDEFINED_VALUE,
            "equipe": self.app.user_team or UNDEFINED_VALUE,
        }

    # ------------------------------------------------------------------
    # Modification du profil
    # ------------------------------------------------------------------

    def open_edit_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Modifier profil")
        self.center_popup(
            popup,
            *EDIT_POPUP_SIZE,
        )
        popup.transient(self)
        popup.grab_set()
        popup.lift()
        popup.focus_force()
        popup.resizable(
            False,
            False,
        )

        frame = ctk.CTkFrame(popup)
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        prenom_entry = self._create_text_field(
            frame,
            "Prénom",
            self.app.user_name or "",
        )
        nom_entry = self._create_text_field(
            frame,
            "Nom",
            self.app.user_lastname or "",
        )

        grade_var = ctk.StringVar(
            value=self.app.user_role or "Inconnu"
        )
        self._create_option_field(
            frame,
            "Grade",
            grade_var,
            GRADES,
        )

        equipe_var = ctk.StringVar(
            value=self.app.user_team or "Inconnue"
        )
        self._create_option_field(
            frame,
            "Équipe",
            equipe_var,
            TEAMS,
        )

        def save():
            data = {
                "prenom": prenom_entry.get(),
                "nom": nom_entry.get(),
                "role": grade_var.get(),
                "equipe": equipe_var.get(),
            }

            try:
                self._write_user_file(data)
            except OSError as error:
                print(
                    "Erreur sauvegarde :",
                    error,
                )
                return

            self.load_user()
            self.refresh_cards()
            popup.destroy()

        ctk.CTkButton(
            frame,
            text="Enregistrer",
            command=save,
        ).pack(
            pady=20
        )

    @staticmethod
    def _create_text_field(
        parent,
        label,
        value,
    ):
        ctk.CTkLabel(
            parent,
            text=label,
        ).pack(
            anchor="w",
            padx=5,
        )

        entry = ctk.CTkEntry(parent)
        entry.pack(
            fill="x",
            pady=5,
            padx=5,
        )
        entry.insert(
            0,
            value,
        )

        return entry

    @staticmethod
    def _create_option_field(
        parent,
        label,
        variable,
        values,
    ):
        ctk.CTkLabel(
            parent,
            text=label,
        ).pack(
            anchor="w",
            padx=5,
        )

        menu = ctk.CTkOptionMenu(
            parent,
            values=list(values),
            variable=variable,
        )
        menu.pack(
            fill="x",
            pady=5,
            padx=5,
        )

        return menu

    # ------------------------------------------------------------------
    # Rafraîchissement des cartes
    # ------------------------------------------------------------------

    def refresh_cards(self):
        self._destroy_info_cards()
        self._create_profile_content()

    def _destroy_info_cards(self):
        # Les seuls CTkFrame directement contenus dans main_container
        # sont les cartes d'information. Le titre et le bouton sont des
        # CTkLabel / CTkButton et sont donc conservés.
        for widget in self.main_container.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

    # ------------------------------------------------------------------
    # Fenêtres secondaires
    # ------------------------------------------------------------------

    def center_popup(
        self,
        popup,
        width,
        height,
    ):
        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        x = (
            parent_x
            + (parent_width // 2)
            - (width // 2)
        )
        y = (
            parent_y
            + (parent_height // 2)
            - (height // 2)
        )

        popup.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ------------------------------------------------------------------
    # Langue
    # ------------------------------------------------------------------

    def refresh_language(self):
        self.lang_util = PageLang(self.app)

        self.header_label.configure(
            text=self.lang_util.t("mon_profil")
        )
        self.info_title.configure(
            text=self.lang_util.t("mes_informations")
        )
        self.btn_edit.configure(
            text=self.lang_util.t("modifier_information")
        )
