import json
import re
from tkinter import messagebox

import customtkinter as ctk

from config.paths import MATERIELS_FILE
from utils.page_lang import PageLang


HEADER_COLOR = "#1E5CC4"
DELETE_COLOR = "#880000"
DELETE_HOVER_COLOR = "#520000"

# Formats conservés depuis la version actuelle.
# Organe : ABC1.DE ou ABCDE.DE1 (5 à 7 lettres avant le point)
# Sous-organe : 3 à 7 lettres, 0 à 2 chiffres, puis .XX
ORGANE_PATTERN = re.compile(
    r"^(?:[A-Z]{3}[0-9]\.[A-Z]{2}|[A-Z]{5,7}\.[A-Z]{2}1|[A-Z]{5,7}\.[A-Z]{2})$"
)
SOUS_ORGANE_PATTERN = re.compile(
    r"^[A-Z]{3,7}[0-9]{0,2}\.[A-Z]{2}$"
)


class PageOrganes(ctk.CTkFrame):
    """Gestion des organes et sous-organes utilisés par l'application."""

    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.lang_util = PageLang(app)

        self.expand_state = {}
        self.materiels = {}

        self._create_header()
        self._create_add_section()
        self._create_list_section()

        self.load_materiels()

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _create_header(self):
        header = ctk.CTkFrame(
            self,
            border_width=1,
            border_color="blue",
            fg_color=HEADER_COLOR,
            height=60,
        )
        header.pack(
            fill="x",
            padx=5,
            pady=5,
        )

        self.header_label = ctk.CTkLabel(
            header,
            text=self.lang_util.t("ajout_organe_titre"),
            font=("Roboto", 24),
            text_color="white",
        )
        self.header_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

    def _create_add_section(self):
        frame_add = ctk.CTkFrame(
            self,
            border_width=1,
            border_color=("gray75", "gray30"),
            corner_radius=10,
        )
        frame_add.pack(
            pady=10,
            padx=20,
            fill="x",
        )

        self.label_organe = ctk.CTkLabel(
            frame_add,
            text=self.lang_util.t("ajout_organe"),
            font=("Roboto", 16),
        )
        self.label_organe.pack(pady=5)

        self.entry_materiel = ctk.CTkEntry(
            frame_add,
            placeholder_text=self.lang_util.t("nom_organe"),
        )
        self.entry_materiel.pack(pady=5)

        self.entry_sous = ctk.CTkEntry(
            frame_add,
            placeholder_text=self.lang_util.t("sous_organe"),
        )
        self.entry_sous.pack(pady=5)

        self.no_sub_var = ctk.BooleanVar()

        self.label_no_sub = ctk.CTkCheckBox(
            frame_add,
            text=self.lang_util.t("pas_de_sous_organe"),
            variable=self.no_sub_var,
            command=self.toggle_sous,
        )
        self.label_no_sub.pack(pady=5)

        self.label_btn_add = ctk.CTkButton(
            frame_add,
            text=self.lang_util.t("ajout_mettre_a_jour"),
            command=self.add_materiel,
        )
        self.label_btn_add.pack(pady=10)

    def _create_list_section(self):
        frame_list = ctk.CTkFrame(
            self,
            border_width=1,
            border_color=("gray75", "gray30"),
            corner_radius=10,
        )
        frame_list.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True,
        )

        self.label_organ_exist = ctk.CTkLabel(
            frame_list,
            text=self.lang_util.t("organes_existants"),
            font=("Roboto", 16),
        )
        self.label_organ_exist.pack(pady=5)

        self.list_frame = ctk.CTkScrollableFrame(
            frame_list,
            border_width=1,
            border_color=("gray70", "gray25"),
        )
        self.list_frame.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True,
        )

    # ------------------------------------------------------------------
    # État de l'interface
    # ------------------------------------------------------------------

    def toggle_sous(self):
        self.entry_sous.configure(
            state="disabled"
            if self.no_sub_var.get()
            else "normal"
        )

    def toggle_organe(self, mat):
        self.expand_state[mat] = not self.expand_state.get(
            mat,
            False,
        )
        self.load_materiels()

    # ------------------------------------------------------------------
    # Chargement / affichage des matériels
    # ------------------------------------------------------------------

    def load_materiels(self):
        self.materiels = self._read_materiels_file()
        self._clear_material_list()

        for mat, info in self.materiels.items():
            self.expand_state.setdefault(
                mat,
                False,
            )
            self._create_material_row(
                mat,
                info,
            )

    @staticmethod
    def _read_materiels_file():
        if not MATERIELS_FILE.exists():
            return {}

        try:
            with MATERIELS_FILE.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return data.get(
                "materiels",
                {},
            )

        except (json.JSONDecodeError, OSError):
            return {}

    def _clear_material_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

    def _create_material_row(self, mat, info):
        mat_frame = ctk.CTkFrame(
            self.list_frame,
            fg_color="transparent",
        )
        mat_frame.pack(
            fill="x",
            padx=10,
            pady=(5, 0),
        )

        btn_expand = ctk.CTkButton(
            mat_frame,
            text=(
                "−"
                if self.expand_state[mat]
                else "+"
            ),
            width=28,
            height=28,
            command=lambda material=mat: self.toggle_organe(material),
        )
        btn_expand.pack(
            side="left",
            padx=(0, 6),
        )

        ctk.CTkLabel(
            mat_frame,
            text=mat,
            font=("Roboto", 14, "bold"),
        ).pack(side="left")

        ctk.CTkButton(
            mat_frame,
            text=self.lang_util.t("supprimer"),
            width=80,
            command=lambda material=mat: self.delete_materiel(material),
            fg_color=DELETE_COLOR,
            hover_color=DELETE_HOVER_COLOR,
        ).pack(side="right")

        if self.expand_state[mat]:
            self._create_sub_materials(
                mat,
                info,
            )

    def _create_sub_materials(self, mat, info):
        sous_frame = ctk.CTkFrame(
            self.list_frame,
            fg_color="transparent",
        )
        sous_frame.pack(
            fill="x",
            padx=25,
            pady=2,
        )

        if info.get("no_sub", False):
            ctk.CTkLabel(
                sous_frame,
                text=self.lang_util.t("pas_de_sous_organe"),
                text_color="gray",
            ).pack(anchor="w")
            return

        for sous in info.get("sous", []):
            self._create_sub_material_row(
                sous_frame,
                mat,
                sous,
            )

    def _create_sub_material_row(
        self,
        parent,
        mat,
        sous,
    ):
        sub_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        sub_frame.pack(
            fill="x",
            pady=2,
        )

        ctk.CTkLabel(
            sub_frame,
            text=sous,
        ).pack(side="left")

        ctk.CTkButton(
            sub_frame,
            text=self.lang_util.t("supprimer"),
            width=80,
            command=lambda material=mat, sub=sous: self.delete_sous_materiel(
                material,
                sub,
            ),
            fg_color=DELETE_COLOR,
            hover_color=DELETE_HOVER_COLOR,
        ).pack(side="right")

    # ------------------------------------------------------------------
    # Ajout / mise à jour
    # ------------------------------------------------------------------

    def add_materiel(self):
        mat = self.entry_materiel.get().strip().upper()
        sous = self.entry_sous.get().strip()
        no_sub = self.no_sub_var.get()

        if not self._is_valid_material(mat):
            messagebox.showwarning(
                self.lang_util.t("erreur"),
                self.lang_util.t("format_organe_invalide"),
            )
            return

        if (
            not no_sub
            and not self._is_valid_sub_material(sous)
        ):
            messagebox.showwarning(
                self.lang_util.t("erreur"),
                self.lang_util.t("format_sous_organe_invalide"),
            )
            return

        self.materiels.setdefault(
            mat,
            {
                "sous": [],
                "no_sub": no_sub,
            },
        )

        if no_sub:
            self.materiels[mat]["no_sub"] = True
            self.materiels[mat]["sous"] = []
        else:
            self.materiels[mat]["no_sub"] = False

            if sous not in self.materiels[mat]["sous"]:
                self.materiels[mat]["sous"].append(sous)

        self.save_materiels()
        self._refresh_depannage_page()
        self._reset_form()

        self.expand_state[mat] = True
        self.load_materiels()

        messagebox.showinfo(
            "OK",
            f"{mat} mis à jour.",
        )

    @staticmethod
    def _is_valid_material(mat):
        return bool(
            mat
            and ORGANE_PATTERN.fullmatch(mat)
        )

    @staticmethod
    def _is_valid_sub_material(sous):
        return bool(
            SOUS_ORGANE_PATTERN.fullmatch(sous)
        )

    def _refresh_depannage_page(self):
        depann_page = self.app.pages.get("depann")

        if depann_page:
            depann_page.refresh_materiels()

    def _reset_form(self):
        self.entry_materiel.delete(
            0,
            "end",
        )
        self.entry_sous.delete(
            0,
            "end",
        )
        self.no_sub_var.set(False)
        self.toggle_sous()

    # ------------------------------------------------------------------
    # Suppression
    # ------------------------------------------------------------------

    def delete_materiel(self, mat):
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Supprimer l'organe '{mat}' et tous ses sous-organes ?",
        )

        if not confirmation:
            return

        self.materiels.pop(
            mat,
            None,
        )
        self.expand_state.pop(
            mat,
            None,
        )

        self.save_materiels()
        self.load_materiels()

    def delete_sous_materiel(
        self,
        mat,
        sous,
    ):
        if (
            mat not in self.materiels
            or sous not in self.materiels[mat]["sous"]
        ):
            return

        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Supprimer le sous-organe '{sous}' ?",
        )

        if not confirmation:
            return

        self.materiels[mat]["sous"].remove(sous)

        if not self.materiels[mat]["sous"]:
            self.materiels[mat]["no_sub"] = True

        self.save_materiels()
        self.load_materiels()

    # ------------------------------------------------------------------
    # Sauvegarde
    # ------------------------------------------------------------------

    def save_materiels(self):
        MATERIELS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with MATERIELS_FILE.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                {
                    "materiels": self.materiels,
                },
                file,
                ensure_ascii=False,
                indent=2,
            )

    # ------------------------------------------------------------------
    # Langue
    # ------------------------------------------------------------------

    def refresh_language(self):
        self.lang_util = PageLang(self.app)

        self.header_label.configure(
            text=self.lang_util.t("ajout_organe_titre")
        )
        self.label_organe.configure(
            text=self.lang_util.t("ajout_organe")
        )
        self.entry_materiel.configure(
            placeholder_text=self.lang_util.t("nom_organe")
        )
        self.entry_sous.configure(
            placeholder_text=self.lang_util.t("nom_sous_organe")
        )
        self.label_no_sub.configure(
            text=self.lang_util.t("pas_de_sous_organe")
        )
        self.label_btn_add.configure(
            text=self.lang_util.t("ajout_mettre_a_jour")
        )
        self.label_organ_exist.configure(
            text=self.lang_util.t("organes_existants")
        )

        # Les boutons "Supprimer" sont créés dynamiquement :
        # reconstruire la liste applique donc immédiatement la traduction.
        self.load_materiels()
