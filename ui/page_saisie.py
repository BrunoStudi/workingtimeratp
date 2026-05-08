import customtkinter as ctk
import json
import re

from datetime import date, datetime
from utils.page_lang import PageLang
from tkinter import messagebox
from config.paths import MATERIELS_FILE, DATA_FILE

class PageSaisie(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Création de l'utilitaire de traduction
        self.lang_util = PageLang(app)

        # Variable des boutons popup a NONE 
        # pour eviter le crash de l'application lors de la traduction
        self.btn_h_close = None
        self.btn_m_close = None

        # --- Header ---
        header = ctk.CTkFrame(
            self, 
            border_width=1, 
            border_color="blue", 
            fg_color="#1E5CC4", 
            height=60)
        header.pack(
            fill="x", 
            pady=5, 
            padx=5)
        self.header_label=ctk.CTkLabel(
            header, 
            text=self.lang_util.t("saisie_intervention"), 
            font=("Roboto", 24), 
            text_color="white")
        self.header_label.place(
            relx=0.5, 
            rely=0.5, 
            anchor="center")

        # --- Bloc Temps ---
        frame_time = ctk.CTkFrame(
            self, 
            fg_color="transparent")
        frame_time.pack(
            pady=40,
            anchor="w",
            padx=(245, 5))

        # Heure de début
        self.label_h_debut=ctk.CTkLabel(
            frame_time, 
            text=self.lang_util.t("heure_debut"), 
            font=("Roboto", 16))
        
        self.label_h_debut.grid(
            row=0, 
            column=0, 
            padx=10, 
            pady=10, 
            sticky="w")
        
        ctk.CTkButton(
            frame_time, 
            text="H", 
            width=40, 
            height=35, 
            command=lambda: self.open_hour_selector("debut")).grid(
                row=0, 
                column=1, 
                padx=5)
        
        self.entry_h_debut = ctk.CTkEntry(
            frame_time, 
            width=60, 
            justify="center")
        
        self.entry_h_debut.grid(
            row=0, 
            column=2, 
            padx=5)

        # label ":"
        ctk.CTkLabel(
            frame_time, 
            text=":", 
            font=("Roboto", 18)).grid(
                row=0, 
                column=3, 
                padx=2)

        self.entry_m_debut = ctk.CTkEntry(
            frame_time, 
            width=60, 
            justify="center")
        
        self.entry_m_debut.grid(
            row=0, 
            column=4, 
            padx=5)

        ctk.CTkButton(
            frame_time, 
            text="M", 
            width=40, 
            height=35, 
            command=lambda: self.open_minute_selector("debut")).grid(
                row=0, 
                column=5, 
                padx=5)

       # Heure de fin
        self.label_h_fin=ctk.CTkLabel(
            frame_time, 
            text=self.lang_util.t("heure_fin"), 
            font=("Roboto", 16))
        
        self.label_h_fin.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=10, 
            sticky="w")
        
        ctk.CTkButton(
            frame_time, 
            text="H", 
            width=40, 
            height=35, 
            command=lambda: self.open_hour_selector("fin")).grid(
                row=1, 
                column=1, 
                padx=5)
        
        self.entry_h_fin = ctk.CTkEntry(
            frame_time, 
            width=60, 
            justify="center")
        
        self.entry_h_fin.grid(
            row=1, 
            column=2, 
            padx=5)

        # label ":"
        ctk.CTkLabel(
            frame_time, 
            text=":", 
            font=("Roboto", 18)).grid(
                row=1, 
                column=3, 
                padx=2)

        self.entry_m_fin = ctk.CTkEntry(
            frame_time, 
            width=60, 
            justify="center")
        
        self.entry_m_fin.grid(
            row=1, 
            column=4, 
            padx=5)

        ctk.CTkButton(
            frame_time, 
            text="M", 
            width=40, 
            height=35, 
            command=lambda: self.open_minute_selector("fin")).grid(
                row=1, 
                column=5, 
                padx=5)

        # --- Checkbox Activité support ---
        self.support_var = ctk.BooleanVar()
        self.check_support = ctk.CTkCheckBox(
            self,
            text=self.lang_util.t("activite_support"),
            variable=self.support_var,
            command=self.toggle_support
        )
        self.check_support.pack(pady=(10, 0))

        # --- Dropdown Matériel / Sous-matériel ---
        frame_mat = ctk.CTkFrame(
            self, 
            fg_color="transparent")
        frame_mat.pack(
            pady=20,
            anchor="w",
            padx=(245, 5))

        self.label_materiel=ctk.CTkLabel(
            frame_mat, 
            text=self.lang_util.t("organe"), 
            font=("Roboto", 16))
        
        self.label_materiel.grid(
            row=0, 
            column=0, 
            padx=10, 
            pady=5, 
            sticky="w")
        
        self.dropdown_materiel = ctk.CTkComboBox(
            frame_mat, 
            values=[], 
            command=self.update_sous)
        
        self.dropdown_materiel.grid(
            row=0, 
            column=1, 
            padx=5)

        self.entry_num_materiel = ctk.CTkEntry(
            frame_mat,
            width=80,
            placeholder_text="N°"
        )

        self.entry_num_materiel.grid(
            row=0, 
            column=2, 
            padx=(5, 0))

        self.label_sous=ctk.CTkLabel(
            frame_mat, 
            text=self.lang_util.t("sous_organe"), 
            font=("Roboto", 16))
        
        self.label_sous.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=10, 
            sticky="w")
        
        self.dropdown_sous = ctk.CTkComboBox(
            frame_mat, 
            values=[])
        
        self.dropdown_sous.grid(
            row=1, 
            column=1, 
            padx=5)

        self.entry_num_sous = ctk.CTkEntry(
            frame_mat,
            width=80,
            placeholder_text="N°"
        )

        self.entry_num_sous.grid(
            row=1, 
            column=2, 
            padx=(5, 0))

        # CheckBox
        self.no_sous_var = ctk.BooleanVar()
        self.check_no_sub = ctk.CTkCheckBox(
            frame_mat, 
            text=self.lang_util.t("pas_de_sous_organe"), 
            variable=self.no_sous_var, 
            command=self.toggle_sous)
        
        self.no_organe_var = ctk.BooleanVar()
        self.check_no_organe = ctk.CTkCheckBox(
            frame_mat,
            text=self.lang_util.t("pas_d_organe"),
            variable=self.no_organe_var,
            command=self.toggle_organe
        )

        self.check_no_sub.grid(
            row=2,
            column=2,
            pady=10,
            sticky="w"
        )

        self.check_no_organe.grid(
            row=2,
            column=1,
            pady=10,
            padx=(10, 0),
            sticky="w"
        )

        # --- Description de l'intervention ---
        frame_desc = ctk.CTkFrame(
            self, 
            fg_color="transparent")
        
        frame_desc.pack(
            pady=(10, 0), 
            padx=20)

        self.label_desc=ctk.CTkLabel(
            frame_desc,
            text=self.lang_util.t("description_intervention"),
            font=("Roboto", 16)
        )

        self.label_desc.pack(
            anchor="w", 
            pady=(0, 5))

        self.entry_description = ctk.CTkTextbox(
            frame_desc,
            height=80,
            wrap="word",
            width=600,
            border_width=1,
            border_color="black"
        )

        self.entry_description.pack(fill="x")

        # Checkbox Magellan
        self.ext_done = ctk.BooleanVar()
        self.check_magellan=ctk.CTkCheckBox(
            self, 
            text=self.lang_util.t("saisie_magellan"), 
            variable=self.ext_done)
        
        self.check_magellan.pack(pady=(20,0))

        # Valider
        self.btn_save=ctk.CTkButton(
            self, 
            text=self.lang_util.t("enregistrer"), 
            command=self.save)
        
        self.btn_save.pack(pady=(20,20))

        self.load_materiels_dropdown()

    # Méthode pour detecter si on est Samedi ou Dimanche (jour de non travail)
    def is_weekend(self, date_str: str) -> bool:
        """
        date_str au format YYYY-MM-DD
        """
        try:
            d = datetime.fromisoformat(date_str)
            return d.weekday() >= 5  # 5 = samedi, 6 = dimanche
        except:
            return False

    def reset_form(self):
        # Heures / minutes
        self.entry_h_debut.delete(0, "end")
        self.entry_m_debut.delete(0, "end")
        self.entry_h_fin.delete(0, "end")
        self.entry_m_fin.delete(0, "end")

        # Numéros
        self.entry_num_materiel.delete(0, "end")
        self.entry_num_sous.delete(0, "end")

        self.support_var.set(False)
        self.toggle_support()

        # Description
        self.entry_description.delete("1.0", "end")

        # Checkboxes
        self.no_sous_var.set(False)
        self.ext_done.set(False)

        # Dropdowns
        if self.dropdown_materiel.cget("values"):
            first = self.dropdown_materiel.cget("values")[0]
            self.dropdown_materiel.set(first)
            self.update_sous(first)
        else:
            self.dropdown_materiel.set("")
            self.dropdown_sous.set("")

        # Message "enregistré" (évite empilement)
        if hasattr(self, "label_enregistre") and self.label_enregistre.winfo_exists():
            self.label_enregistre.destroy()

    def show_success_message(self):
        # Supprimer l'ancien message s'il existe
        if hasattr(self, "label_enregistre") and self.label_enregistre.winfo_exists():
            self.label_enregistre.destroy()

        self.label_enregistre = ctk.CTkLabel(
            self,
            text=self.lang_util.t("enregistre"),
            text_color="green"
        )
        self.label_enregistre.pack()

        # Disparition automatique après 2 secondes (2000 ms)
        self.after(2000, self.hide_success_message)

    def hide_success_message(self):
        if hasattr(self, "label_enregistre") and self.label_enregistre.winfo_exists():
            self.label_enregistre.destroy()

    # ---------------------------------------------------------------
    # Charger matériels depuis JSON
    # ---------------------------------------------------------------
    def load_materiels_dropdown(self):
        self.materiels_dict = {}
        if MATERIELS_FILE.exists():
            try:
                with open(MATERIELS_FILE, "r", encoding="utf-8") as f:
                    self.materiels_dict = json.load(f).get("materiels", {})
            except:
                self.materiels_dict = {}

        materiels_keys = list(self.materiels_dict.keys())
        self.dropdown_materiel.configure(values=materiels_keys)

        if materiels_keys:
            first = materiels_keys[0]
            self.dropdown_materiel.set(first)
            self.update_sous(first)

    # ---------------------------------------------------------------
    def sync_organe_ui(self):
        """
        Met à jour l'état des champs organe / sous-organe
        en fonction des checkboxes no_organe_var et no_sous_var
        """

        no_organe = self.no_organe_var.get()
        no_sous = self.no_sous_var.get()

        # --- Cas interdit (sécurité)
        if no_organe and no_sous:
            self.no_sous_var.set(False)
            no_sous = False

        # =============================
        # Gestion ORGANE
        # =============================
        if no_organe:
            self.dropdown_materiel.configure(state="disabled")
            self.entry_num_materiel.configure(state="disabled")
            self.dropdown_materiel.set("")
            self.entry_num_materiel.delete(0, "end")
        else:
            self.dropdown_materiel.configure(state="normal")
            self.entry_num_materiel.configure(state="normal")

        # =============================
        # Gestion SOUS-ORGANE
        # =============================
        if no_sous:
            self.dropdown_sous.configure(state="disabled")
            self.entry_num_sous.configure(state="disabled")
            self.dropdown_sous.set("")
            self.entry_num_sous.delete(0, "end")
        else:
            self.dropdown_sous.configure(state="normal")
            self.entry_num_sous.configure(state="normal")

            # Recharge normale si organe actif
            if not no_organe:
                selected = self.dropdown_materiel.get()
                if selected:
                    self.update_sous(selected)

    def update_sous(self, selected):
        data = self.materiels_dict.get(selected, {})
        if not data or data.get("no_sub", False) or self.no_sous_var.get():
            self.dropdown_sous.configure(values=[])
            self.dropdown_sous.set("")
            self.no_sous_var.set(True)
        else:
            sous_list = data.get("sous", [])
            self.dropdown_sous.configure(values=sous_list)
            if sous_list:
                self.dropdown_sous.set(sous_list[0])
            self.no_sous_var.set(False)

    def toggle_sous(self):
        if self.no_sous_var.get():
            self.no_organe_var.set(False)
        self.sync_organe_ui()

    def toggle_organe(self):
        if self.no_organe_var.get():
            self.no_sous_var.set(False)
        self.sync_organe_ui()

    def refresh_materiels(self):
        previous = self.dropdown_materiel.get()
        self.load_materiels_dropdown()
        if previous in self.dropdown_materiel.cget("values"):
            self.dropdown_materiel.set(previous)
            self.update_sous(previous)

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
        x -= 100
        y -= 250

        popup.geometry(f"+{x}+{y}")

    def toggle_support(self):
        is_support = self.support_var.get()
        self.no_organe_var.set(False)
        self.no_sous_var.set(False)

        widgets = [
            self.dropdown_materiel,
            self.entry_num_materiel,
            self.dropdown_sous,
            self.entry_num_sous,
            self.check_no_sub,
            self.check_no_organe,
        ]

        if is_support:
            # Désactiver
            for w in widgets:
                w.configure(state="disabled")

            # Nettoyer les valeurs
            self.dropdown_materiel.set("")
            self.dropdown_sous.set("")
            self.entry_num_materiel.delete(0, "end")
            self.entry_num_sous.delete(0, "end")
            self.no_sous_var.set(False)
            self.no_organe_var.set(False)
        else:
            # Réactiver
            for w in widgets:
                w.configure(state="normal")

            # Restaurer la logique normale
            values = self.dropdown_materiel.cget("values")
            if values:
                self.dropdown_materiel.set(values[0])
                self.update_sous(values[0])

    # ---------------------------------------------------------------
    # Sélecteurs heures / minutes
    # ---------------------------------------------------------------
    def open_hour_selector(self, mode):
        popup = ctk.CTkToplevel(self)
        self.popup_hour = popup
        popup.title(self.lang_util.t("choisir_heure"))
        popup.iconbitmap("ui/assets/train.ico")
        popup.geometry("280x300")
        popup.grab_set()

        popup.update_idletasks()
        self.center_popup(popup)

        # --- Frame pour boutons heures (GRID) ---
        frame_grid = ctk.CTkFrame(popup)
        frame_grid.pack(pady=10)

        for h in range(24):
            ctk.CTkButton(
                frame_grid,
                text=str(h).zfill(2),
                width=60,
                command=lambda val=h: self.set_hour(mode, val, popup)
            ).grid(
                row=h//4, 
                column=h%4, 
                padx=5, 
                pady=5)

        # --- Bouton fermer (PACK) ---
        def close_popup():
            popup.destroy()

        self.btn_h_close=ctk.CTkButton(
            popup,
            text=self.lang_util.t("fermer"),
            fg_color="#404040",
            hover_color="#202020",
            corner_radius=12,
            width=120,
            command=close_popup
        )
        self.btn_h_close.pack(pady=10)

    def set_hour(self, mode, value, popup):
        entry = self.entry_h_debut if mode=="debut" else self.entry_h_fin
        entry.delete(0,"end")
        entry.insert(0,str(value).zfill(2))
        popup.destroy()

    def open_minute_selector(self, mode):
        popup = ctk.CTkToplevel(self)
        self.popup_minute = popup
        popup.title(self.lang_util.t("choisir_minutes"))
        popup.iconbitmap("ui/assets/train.ico")
        popup.geometry("350x430")
        popup.grab_set()

        popup.update_idletasks()
        self.center_popup(popup)

        # --- Frame pour les boutons minutes (GRID) ---
        frame_grid = ctk.CTkFrame(popup)
        frame_grid.pack(pady=10)

        for m in range(60):
            ctk.CTkButton(
                frame_grid,
                text=str(m).zfill(2),
                width=50,
                command=lambda val=m: self.set_minute(mode, val, popup)
            ).grid(
                row=m//6, 
                column=m%6, 
                padx=4, 
                pady=4)

        # --- Bouton fermer (PACK) ---
        def close_popup():
            popup.destroy()

        self.btn_m_close=ctk.CTkButton(
            popup,
            text=self.lang_util.t("fermer"),
            fg_color="#404040",
            hover_color="#202020",
            corner_radius=12,
            width=120,
            command=close_popup
        )
        self.btn_m_close.pack(pady=10)

    def set_minute(self, mode, value, popup):
        entry = self.entry_m_debut if mode=="debut" else self.entry_m_fin
        entry.delete(0,"end")
        entry.insert(0,str(value).zfill(2))
        popup.destroy()

    # ---------------------------------------------------------------
    # Enregistrer saisie
    # ---------------------------------------------------------------
    def save(self):
        if self.no_organe_var.get() and self.no_sous_var.get():
            messagebox.showwarning(
                self.lang_util.t("erreur"),
                self.lang_util.t("combinaison_interdite_organe_sous")
            )
            return

        jour = str(date.today())

        # --- Blocage week-end ---
        if self.is_weekend(jour):
            messagebox.showwarning(
                self.lang_util.t("jour_non_travaille"),
                self.lang_util.t("saisie_interdite_weekend")
            )
            return

        # --- Lire le fichier data.jsonl correctement (JSONL : une entrée par ligne) ---
        all_entries = []
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        all_entries.append(json.loads(line))
                    except Exception:
                        # ignorer les lignes corrompues
                        continue

        # Entrées du jour
        entries_today = [e for e in all_entries if e.get("jour") == jour]

        # Récupérer les valeurs saisies
        try:
            h_debut = int(self.entry_h_debut.get())
            m_debut = int(self.entry_m_debut.get())
            h_fin = int(self.entry_h_fin.get())
            m_fin = int(self.entry_m_fin.get())
        except Exception:
            ctk.CTkLabel(self, text=self.lang_util.t("remplir_horaires_correctement"), text_color="red").pack()
            return

        total_debut = h_debut * 60 + m_debut
        total_fin = h_fin * 60 + m_fin

        if total_fin <= total_debut:
            ctk.CTkLabel(
                self, 
                text=self.lang_util.t("heure_fin_apres_debut"), 
                text_color="red").pack()
            return

        new_duration = total_fin - total_debut
        if new_duration == 0:
            ctk.CTkLabel(
                self, 
                text=self.lang_util.t("temps_non_zero"), 
                text_color="red").pack()
            return

        # ----------------------
        # Vérification chevauchement
        # ----------------------
        for e in entries_today:
            hd = e.get("heure_debut")
            hf = e.get("heure_fin")
            if not hd or not hf:
                continue
            try:
                eh1, em1 = map(int, hd.split(":"))
                eh2, em2 = map(int, hf.split(":"))
            except Exception:
                continue
            exist_start = eh1 * 60 + em1
            exist_end = eh2 * 60 + em2

            # Formule universelle de chevauchement
            if (total_debut < exist_end) and (total_fin > exist_start):
                texte = self.lang_util.t("chevauchement_detecte")  # récupère "⚠️ Chevauchement détecté avec {heure_debut} → {heure_fin}"
                ctk.CTkLabel(
                    self,
                    text=texte.format(heure_debut=e.get('heure_debut'), 
                                      heure_fin=e.get('heure_fin')),
                    text_color="red"
                ).pack()
                return

        # ----------------------
        # Vérification limite journalière 8h24 (504 minutes)
        # ----------------------
        # Calculer total_today en utilisant temps_total si présent sinon en dérivant depuis heures
        total_today = 0
        for e in entries_today:
            t = e.get("temps_total")
            if isinstance(t, int):
                total_today += t
            else:
                # tentative de calcul à partir des heures
                hd = e.get("heure_debut")
                hf = e.get("heure_fin")
                try:
                    eh1, em1 = map(int, hd.split(":"))
                    eh2, em2 = map(int, hf.split(":"))
                    total_today += (eh2 * 60 + em2) - (eh1 * 60 + em1)
                except Exception:
                    continue

        DAILY_LIMIT = 8 * 60 + 24  # 504 minutes
        if total_today + new_duration > DAILY_LIMIT:
            remaining = max(0, DAILY_LIMIT - total_today)
            rh = remaining // 60
            rm = remaining % 60
            texte = self.lang_util.t("limite_journaliere_depassee")
            ctk.CTkLabel(
                self,
                text=texte.format(rh=rh, rm=rm),
                text_color="red"
            ).pack()
            return

        # --- Préparer l'entrée et sauvegarder ---
        # ----------------------
        # Validation des champs N°
        # ----------------------
        if not self.support_var.get() and not self.no_organe_var.get():
            num_materiel = self.entry_num_materiel.get().strip()

            if not num_materiel:
                messagebox.showwarning(
                    self.lang_util.t("champ_obligatoire"),
                    self.lang_util.t("numero_organe_obligatoire")
                )
                return

            if not re.fullmatch(r"^([A-Za-z]\d{2,4}|\d{2,5})$", num_materiel):
                messagebox.showwarning(
                    self.lang_util.t("format_invalide"),
                    self.lang_util.t("numero_organe_format")
                )
                return

            if not self.no_sous_var.get():
                num_sous = self.entry_num_sous.get().strip()

                if not num_sous:
                    messagebox.showwarning(
                        self.lang_util.t("champ_obligatoire"),
                        self.lang_util.t("numero_sous_organe_obligatoire")
                    )
                    return

                if not re.fullmatch(r"^([A-Za-z]\d{2,4}|\d{2,5})$", num_sous):
                    messagebox.showwarning(
                        self.lang_util.t("format_invalide"),
                        self.lang_util.t("numero_sous_organe_format")
                    )
                    return

        if self.support_var.get():
            materiel = "ACTIVITE-SUPPORT"
            sous = ""

        elif self.no_organe_var.get():
            materiel = ""
            sous_base = self.dropdown_sous.get()
            num_sous = self.entry_num_sous.get().strip()
            sous = f"{sous_base}-{num_sous}" if num_sous else sous_base

        else:
            materiel_base = self.dropdown_materiel.get()
            num_materiel = self.entry_num_materiel.get().strip()
            materiel = f"{materiel_base}-{num_materiel}" if num_materiel else materiel_base

            if self.no_sous_var.get():
                sous = ""
            else:
                sous_base = self.dropdown_sous.get()
                num_sous = self.entry_num_sous.get().strip()
                sous = f"{sous_base}-{num_sous}" if num_sous else sous_base

        description = self.entry_description.get("1.0", "end").strip()

        entry = {
            "jour": jour,
            "heure_debut": f"{h_debut:02d}:{m_debut:02d}",
            "heure_fin": f"{h_fin:02d}:{m_fin:02d}",
            "temps_total": new_duration,
            "materiel": materiel,
            "sous_materiel": sous,
            "description": description,
            "saisie_magellan": self.ext_done.get()
        }
        
        from main import save_data
        save_data(entry)

        # Nettoyage complet du formulaire
        self.reset_form()

        self.show_success_message()

    # --- Méthode pour rafraîchir la langue ---
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("saisie_intervention"))
        self.label_h_debut.configure(text=self.lang_util.t("heure_debut"))
        self.label_h_fin.configure(text=self.lang_util.t("heure_fin"))
        self.label_materiel.configure(text=self.lang_util.t("organe"))
        self.label_sous.configure(text=self.lang_util.t("sous_organe"))
        self.check_no_sub.configure(text=self.lang_util.t("pas_de_sous_organe"))
        self.label_desc.configure(text=self.lang_util.t("description_intervention"))
        self.check_magellan.configure(text=self.lang_util.t("saisie_magellan"))
        self.btn_save.configure(text=self.lang_util.t("enregistrer"))
        self.check_support.configure(text=self.lang_util.t("activite_support"))
        self.check_no_organe.configure(text=self.lang_util.t("pas_d_organe"))
        
        if hasattr(self, "label_enregistre") and self.label_enregistre.winfo_exists():
            self.label_enregistre.configure(text=self.lang_util.t("enregistre"))

        # Boutons popups : existe encore pour la traduction ?
        if (
            hasattr(self, "btn_h_close")
            and self.btn_h_close is not None
            and self.btn_h_close.winfo_exists()
        ):
            self.btn_h_close.configure(text=self.lang_util.t("fermer"))
            if hasattr(self, "popup_hour") and self.popup_hour.winfo_exists():
                self.popup_hour.title(self.lang_util.t("choisir_heure"))
        
        if (
            hasattr(self, "btn_m_close")
            and self.btn_m_close is not None
            and self.btn_m_close.winfo_exists()
        ):
            self.btn_m_close.configure(text=self.lang_util.t("fermer"))
            if hasattr(self, "popup_minute") and self.popup_minute.winfo_exists():
                self.popup_minute.title(self.lang_util.t("choisir_minutes"))

  




