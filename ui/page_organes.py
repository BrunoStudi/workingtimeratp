import customtkinter as ctk
import json
import re

from tkinter import messagebox
from utils.page_lang import PageLang
from config.paths import MATERIELS_FILE


class PageOrganes(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.lang_util = PageLang(app)

        self.expand_state = {}

        # --- Header ---
        header = ctk.CTkFrame(self, border_width=1, border_color="blue",
                              fg_color="#1E5CC4", height=60)
        header.pack(fill="x", padx=5, pady=5)
        self.header_label = ctk.CTkLabel(
            header,
            text=self.lang_util.t("ajout_organe_titre"),
            font=("Roboto", 24),
            text_color="white"
        )
        self.header_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Zone ajout organe ---
        frame_add = ctk.CTkFrame(self, border_width=1,
                                 border_color=("gray75", "gray30"),
                                 corner_radius=10)
        frame_add.pack(pady=10, padx=20, fill="x")

        self.label_organe = ctk.CTkLabel(
            frame_add, text=self.lang_util.t("ajout_organe"), font=("Roboto", 16)
        )
        self.label_organe.pack(pady=5)

        self.entry_materiel = ctk.CTkEntry(
            frame_add, placeholder_text=self.lang_util.t("nom_organe")
        )
        self.entry_materiel.pack(pady=5)

        self.entry_sous = ctk.CTkEntry(
            frame_add, placeholder_text=self.lang_util.t("sous_organe")
        )
        self.entry_sous.pack(pady=5)

        self.no_sub_var = ctk.BooleanVar()
        self.label_no_sub = ctk.CTkCheckBox(
            frame_add,
            text=self.lang_util.t("pas_de_sous_organe"),
            variable=self.no_sub_var,
            command=self.toggle_sous
        )
        self.label_no_sub.pack(pady=5)

        self.label_btn_add = ctk.CTkButton(
            frame_add,
            text=self.lang_util.t("ajout_mettre_a_jour"),
            command=self.add_materiel
        )
        self.label_btn_add.pack(pady=10)

        # --- Liste des organes ---
        frame_list = ctk.CTkFrame(self, border_width=1,
                                  border_color=("gray75", "gray30"),
                                  corner_radius=10)
        frame_list.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_organ_exist = ctk.CTkLabel(
            frame_list,
            text=self.lang_util.t("organes_existants"),
            font=("Roboto", 16)
        )
        self.label_organ_exist.pack(pady=5)

        self.list_frame = ctk.CTkScrollableFrame(
            frame_list,
            border_width=1,
            border_color=("gray70", "gray25")
        )
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.load_materiels()

    # -------------------------
    def toggle_sous(self):
        self.entry_sous.configure(
            state="disabled" if self.no_sub_var.get() else "normal"
        )

    # -------------------------
    def toggle_organe(self, mat):
        self.expand_state[mat] = not self.expand_state.get(mat, False)
        self.load_materiels()

    # -------------------------
    def load_materiels(self):
        self.materiels = {}

        if MATERIELS_FILE.exists():
            try:
                with open(MATERIELS_FILE, "r", encoding="utf-8") as f:
                    self.materiels = json.load(f).get("materiels", {})
            except:
                self.materiels = {}

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for mat, info in self.materiels.items():
            self.expand_state.setdefault(mat, False)

            mat_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            mat_frame.pack(fill="x", padx=10, pady=(5, 0))

            btn_expand = ctk.CTkButton(
                mat_frame,
                text="+" if not self.expand_state[mat] else "−",
                width=28,
                height=28,
                command=lambda m=mat: self.toggle_organe(m)
            )
            btn_expand.pack(side="left", padx=(0, 6))

            ctk.CTkLabel(
                mat_frame,
                text=mat,
                font=("Roboto", 14, "bold")
            ).pack(side="left")

            ctk.CTkButton(
                mat_frame,
                text=self.lang_util.t("supprimer"),
                width=80,
                command=lambda m=mat: self.delete_materiel(m),
                fg_color="#880000",
                hover_color="#520000"
            ).pack(side="right")

            sous_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            if self.expand_state[mat]:
                sous_frame.pack(fill="x", padx=25, pady=2)

                if info.get("no_sub", False):
                    ctk.CTkLabel(
                        sous_frame,
                        text=self.lang_util.t("pas_de_sous_organe"),
                        text_color="gray"
                    ).pack(anchor="w")
                else:
                    for sm in info.get("sous", []):
                        sub_frame = ctk.CTkFrame(sous_frame, fg_color="transparent")
                        sub_frame.pack(fill="x", pady=2)

                        ctk.CTkLabel(sub_frame, text=sm).pack(side="left")

                        ctk.CTkButton(
                            sub_frame,
                            text=self.lang_util.t("supprimer"),
                            width=80,
                            command=lambda m=mat, s=sm: self.delete_sous_materiel(m, s),
                            fg_color="#880000",
                            hover_color="#520000"
                        ).pack(side="right")

    # -------------------------
    def add_materiel(self):
        mat = self.entry_materiel.get().strip().upper()
        sous = self.entry_sous.get().strip()
        no_sub = self.no_sub_var.get()

        pattern_mat = r"^(?:[A-Z]{3}[0-9]{1}\.[A-Z]{2}|[A-Z]{5,7}\.[A-Z]{2})$"
        pattern_sous = r"[A-Z]{3,7}[0-9]{0,2}\.[A-Z]{2}"

        if not mat or not re.match(pattern_mat, mat):
            messagebox.showwarning(self.lang_util.t("erreur"),
                                   self.lang_util.t("format_organe_invalide"))
            return

        if not no_sub and not re.fullmatch(pattern_sous, sous):
            messagebox.showwarning(self.lang_util.t("erreur"),
                                   self.lang_util.t("format_sous_organe_invalide"))
            return

        self.materiels.setdefault(mat, {"sous": [], "no_sub": no_sub})

        if no_sub:
            self.materiels[mat]["no_sub"] = True
            self.materiels[mat]["sous"] = []
        else:
            self.materiels[mat]["no_sub"] = False
            if sous not in self.materiels[mat]["sous"]:
                self.materiels[mat]["sous"].append(sous)

        self.save_materiels()

        depann_page = self.app.pages.get("depann")
        if depann_page:
            depann_page.refresh_materiels()

        self.entry_materiel.delete(0, "end")
        self.entry_sous.delete(0, "end")
        self.no_sub_var.set(False)
        self.toggle_sous()

        self.expand_state[mat] = True
        self.load_materiels()

        messagebox.showinfo("OK", f"{mat} mis à jour.")

    # -------------------------
    def delete_materiel(self, mat):
        if messagebox.askyesno(
            "Confirmation",
            f"Supprimer l'organe '{mat}' et tous ses sous-organes ?"
        ):
            self.materiels.pop(mat, None)
            self.expand_state.pop(mat, None)
            self.save_materiels()
            self.load_materiels()

    # -------------------------
    def delete_sous_materiel(self, mat, sous):
        if mat in self.materiels and sous in self.materiels[mat]["sous"]:
            if messagebox.askyesno(
                "Confirmation",
                f"Supprimer le sous-organe '{sous}' ?"
            ):
                self.materiels[mat]["sous"].remove(sous)
                if not self.materiels[mat]["sous"]:
                    self.materiels[mat]["no_sub"] = True
                self.save_materiels()
                self.load_materiels()

    # -------------------------
    def save_materiels(self):
        with open(MATERIELS_FILE, "w", encoding="utf-8") as f:
            json.dump({"materiels": self.materiels},
                      f, ensure_ascii=False, indent=2)

    # -------- Rafraichissement de la langue -------------
    def refresh_language(self):
        self.lang_util = PageLang(self.app)

        # Header
        self.header_label.configure(text=self.lang_util.t("ajout_organe_titre"))

        # Formulaire ajout
        self.label_organe.configure(text=self.lang_util.t("ajout_organe"))
        self.entry_materiel.configure(placeholder_text=self.lang_util.t("nom_organe"))
        self.entry_sous.configure(placeholder_text=self.lang_util.t("nom_sous_organe"))
        self.label_no_sub.configure(text=self.lang_util.t("pas_de_sous_organe"))
        self.label_btn_add.configure(text=self.lang_util.t("ajout_mettre_a_jour"))

        # Titre liste
        self.label_organ_exist.configure(text=self.lang_util.t("organes_existants"))

        # IMPORTANT : reconstruire la liste complète
        self.load_materiels()

