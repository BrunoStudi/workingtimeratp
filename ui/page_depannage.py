import customtkinter as ctk
import tkinter.messagebox as msg
import shutil
import json

from PIL import Image
from pathlib import Path
from tkinter import filedialog
from pathlib import Path
from utils.page_lang import PageLang
from config.paths import DEPANNAGE_FILE, MATERIELS_FILE


# Enregistrement des images depannage dans pictures dossier utilisateur
IMAGES_DIR = Path.home() / "Pictures" / "WorkingTimeRatp"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Chargement de la BDD json dépannages
def load_depannages():
    if not DEPANNAGE_FILE.exists():
        return []

    try:
        if DEPANNAGE_FILE.stat().st_size == 0:
            return []

        with open(DEPANNAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("depannages", [])

    except json.JSONDecodeError:
        return []

# Vérifie si un dépannage est present
def depannage_exists(organe, sous_organe):
    return any(
        d.get("organe") == organe and d.get("sous_organe") == sous_organe
        for d in load_depannages()
    )

# Classe principale
class PageDepannage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.lang_util = PageLang(app)

        # ================= HEADER =================
        header = ctk.CTkFrame(self, border_width=1, border_color="blue", fg_color="#1E5CC4", height=60)
        header.pack(fill="x", padx=5, pady=5)
        header.pack_propagate(False)
        self.header_label = ctk.CTkLabel(header, text=self.lang_util.t("depannage_titre"), font=("Roboto", 24), text_color="white")
        self.header_label.pack(expand=True)

        # ================= FORM DROPDOWNS =================
        form_frame = ctk.CTkFrame(self, border_width=1)
        form_frame.pack(fill="x", padx=10, pady=10)

        form_frame_ia = ctk.CTkFrame(self, border_width=1)
        form_frame_ia.pack(fill="x", padx=10, pady=10)

        # Label et dropdown organe
        self.organe_label = ctk.CTkLabel(form_frame, text=self.lang_util.t("Sélectionnez_organe"))
        self.organe_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.organe_var = ctk.StringVar(value="")  # valeur initiale vide
        self.organe_menu = ctk.CTkOptionMenu(form_frame, values=[], variable=self.organe_var, command=self.organe_selected)
        self.organe_menu.grid(row=0, column=1, sticky="w", padx=5, pady=(10,10))

        # Label et dropdown sous-organe
        self.sous_label = ctk.CTkLabel(form_frame, text=self.lang_util.t("Selectionnez-sous-organe"))
        self.sous_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.sous_var = ctk.StringVar(value="")
        self.sous_menu = ctk.CTkOptionMenu(form_frame, values=[], variable=self.sous_var, command=self.sous_selected)
        self.sous_menu.grid(row=1, column=1, sticky="w", padx=5, pady=(5,10))

        # Bouton "Afficher dépannage" (initialement caché)
        self.btn_afficher = ctk.CTkButton(form_frame, text=self.lang_util.t("depannage_aff"), command=self.afficher_depannage)
        self.btn_afficher.grid(row=2, column=2, columnspan=2, padx=(35,0), pady=15)
        self.btn_afficher.grid_remove()  # bouton caché par défaut

        # Permet de créer des colonnes de largeur 1 pour le btn IA sur une ligne
        for i in range(3):
            form_frame_ia.grid_columnconfigure(i, weight=1)

        # Bouton intelligence artificielle
        self.btn_ia = ctk.CTkButton(form_frame_ia, text=self.lang_util.t("prediction_ia"))
        self.btn_ia.grid(row=1, column=0, columnspan=3, padx=10, pady=15, sticky="")

        # ================= CHARGEMENT DES DONNÉES =================
        self.materiels_data = self.load_materiels()
        self.organe_menu.configure(values=list(self.materiels_data.keys()))

    # ================= MÉTHODES =================
    def load_materiels(self):
        if not MATERIELS_FILE.exists():
            return {}
        with open(MATERIELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("materiels", {})

    def organe_selected(self, value):
        if value not in self.materiels_data:
            self.sous_menu.configure(values=[])
            self.sous_var.set("")
            self.btn_afficher.grid_remove()
            return

        sous_list = self.materiels_data[value].get("sous", [])
        if not sous_list:
            sous_list = ["Aucun"]

        self.sous_var.set(sous_list[0])
        self.sous_menu.configure(values=sous_list)
        self.update_bouton_afficher()

    def sous_selected(self, value):
        """Appelé quand le sous-organe est sélectionné"""
        self.update_bouton_afficher()

    def update_bouton_afficher(self):
        """Afficher le bouton uniquement si un sous-organe valide est sélectionné"""
        if self.sous_var.get() and self.sous_var.get() != "Aucun":
            self.btn_afficher.grid()  # bouton visible
        else:
            self.btn_afficher.grid_remove()  # bouton caché

    def afficher_depannage(self):
        organe = self.organe_var.get()
        sous = self.sous_var.get()

        # Sécurité
        if not organe or not sous or sous == "Aucun":
            return

        # Vérification existence dépannage
        if not depannage_exists(organe, sous):
            reponse = msg.askyesno(
                "Aucune donnée",
                "Il n'existe pas de données de dépannage pour cet organe.\n\n"
                "Voulez-vous ajouter une procédure de dépannage ?"
            )

            if reponse:
                self.ajouter_depannage(organe, sous)
            return

        # Si on arrive ici, les données existent
        self.afficher_popup_depannage_existante(organe, sous)

    # Centrer le popup
    def center_popup(self, popup, width, height):
        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        popup.geometry(f"{width}x{height}+{x}+{y}")

    def afficher_popup_depannage_existante(self, organe, sous):
        depannages = [
            d for d in load_depannages()
            if d["organe"] == organe and d["sous_organe"] == sous
        ]

        if not depannages:
            msg.showerror("Erreur", "Aucune donnée trouvée.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title(f"Dépannage • {organe} → {sous}")
        popup.transient(self)      # lié à la fenêtre parente
        popup.grab_set()           # bloque la fenêtre principale
        popup.lift()               # passe au premier plan
        popup.focus_force()        # donne le focus clavier
        popup.resizable(False, False)
        self.center_popup(popup, 540, 780)

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ============== TITRE SCÉNARIO ===============
        ctk.CTkLabel(
            frame,
            text="Scénario",
            font=("Roboto", 16, "bold")
        ).pack(anchor="w",padx=(10,0), pady=(0, 5))

        scenario_frame = ctk.CTkFrame(frame)
        scenario_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.scenario_selected = None
        self.etape_selected = None

        def select_scenario(scenario):
            self.scenario_selected = scenario
            afficher_etapes()

        scenarios_uniques = []
        seen = set()

        for d in depannages:
            scenario = d.get("scenario")
            if scenario and scenario not in seen:
                seen.add(scenario)
                scenarios_uniques.append(d)

        for d in scenarios_uniques:
            ctk.CTkButton(
                scenario_frame,
                text=d["scenario"],
                width=60,
                command=lambda s=d: select_scenario(s)
            ).pack(side="left", padx=(0,5))

        # ============== TITRE ÉTAPE ===============
        ctk.CTkLabel(
            frame,
            text="Étape",
            font=("Roboto", 16, "bold")
        ).pack(anchor="w", padx=(10,0), pady=(10, 5))

        etape_frame = ctk.CTkFrame(frame)
        etape_frame.pack(fill="x", padx=10, pady=(0, 10))

        desc_box = ctk.CTkTextbox(frame, height=150)
        desc_box.pack(fill="x", padx=10, pady=10)

        photo_label = ctk.CTkLabel(frame, text="")
        photo_label.pack(pady=10)

        # Frame navigation photos (juste sous la photo)
        carousel_nav = ctk.CTkFrame(frame)
        carousel_nav.pack(pady=(0, 10))

        self.btn_prev = ctk.CTkButton(
            carousel_nav,
            text="◀",
            width=40
        )
        self.btn_prev.pack(side="left", padx=(0, 40))

        self.btn_next = ctk.CTkButton(
            carousel_nav,
            text="▶",
            width=40
        )
        self.btn_next.pack(side="right", padx=(40, 0))

        def afficher_etapes():
            for w in etape_frame.winfo_children():
                w.destroy()

            for d in depannages:
                if d["scenario"] == self.scenario_selected["scenario"]:
                    ctk.CTkButton(
                        etape_frame,
                        text=d["etape"],  # uniquement le chiffre
                        width=60,
                        command=lambda e=d: afficher_contenu(e)
                    ).pack(side="left", padx=(0,5))

        def afficher_contenu(data):
            self.etape_selected = data

            # Description avec marge
            desc_box.delete("1.0", "end")
            desc_box.insert("1.0", data.get("description", ""))
            desc_box.configure(padx=10, pady=10)

            # Reset photo
            photo_label.configure(image=None, text="")
            photo_label.unbind("<Button-1>")

            # --- Gestion photos ---
            # Récupération de la liste de photos (multi-photos)
            self.current_photos = data.get("photos", [])
            
            # Rétrocompatibilité pour l'ancienne clé 'photo'
            if not self.current_photos and data.get("photo"):
                self.current_photos = [data["photo"]]

            self.photo_index = 0

            def afficher_photo_carrousel():
                photo_label.configure(image=None, text="")
                photo_label.unbind("<Button-1>")  # IMPORTANT

                if not self.current_photos:
                    photo_label.configure(text="Aucune photo")
                    return

                photo_file = self.current_photos[self.photo_index]
                path = IMAGES_DIR / photo_file
                if path.exists():
                    img = Image.open(path)
                    img.thumbnail((320, 240))
                    ctk_img = ctk.CTkImage(img, size=img.size)
                    photo_label.configure(image=ctk_img, cursor="hand2", text="")
                    photo_label.image = ctk_img

                    # Click → image en grand
                    photo_label.bind(
                        "<Button-1>",
                        lambda e, p=path: afficher_image_grande(p)
                    )
                else:
                    photo_label.configure(text="Photo introuvable")

            # --- Boutons flèches ---
            def photo_suivante():
                if self.current_photos:
                    self.photo_index = (self.photo_index + 1) % len(self.current_photos)
                    afficher_photo_carrousel()

            def photo_precedente():
                if self.current_photos:
                    self.photo_index = (self.photo_index - 1) % len(self.current_photos)
                    afficher_photo_carrousel()

            self.btn_prev.configure(command=photo_precedente)
            self.btn_next.configure(command=photo_suivante)

            afficher_photo_carrousel()

        def afficher_image_grande(path):
            popup_img = ctk.CTkToplevel(self)
            popup_img.title("Aperçu de l'image")
            popup_img.transient(self)
            popup_img.grab_set()
            popup_img.resizable(False, False)

            # Taille raisonnable par défaut
            self.center_popup(popup_img, 900, 735)

            frame = ctk.CTkFrame(popup_img)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Chargement image
            img = Image.open(path)

            # Adapter à la fenêtre (sans déformer)
            max_size = (860, 620)
            img.thumbnail(max_size)

            ctk_img = ctk.CTkImage(img, size=img.size)

            img_label = ctk.CTkLabel(frame, image=ctk_img, text="")
            img_label.pack(expand=True)
            img_label.image = ctk_img  # IMPORTANT

            ctk.CTkButton(
                frame,
                text="Fermer",
                width=120,
                command=popup_img.destroy
            ).pack(pady=10)

        # ================= BOUTONS =================
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(padx=10, pady=15)

        ctk.CTkButton(
            btn_frame,
            text="Modifier",
            command=lambda: (
                popup.destroy(),
                self.ajouter_depannage(
                    organe,
                    sous,
                    self.etape_selected
                )
            )
        ).pack(side="left", padx=(0,10))

        ctk.CTkButton(
            btn_frame,
            text="Ajouter",
            command=lambda: (
                popup.destroy(),
                self.ajouter_depannage(organe, sous)
            )
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Fermer",
            command=popup.destroy
        ).pack(side="left", padx=(10,0))

    def ajouter_depannage(self, organe, sous, data_existante=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Ajouter/Modifier une procédure de dépannage")
        popup.resizable(False, False)

        # Centrage
        self.center_popup(popup, 600, 750)
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== Validation pour 3 chiffres =====
        def only_three_digits(P):
            return P.isdigit() and len(P) <= 3 or P == ""
        validate_cmd = popup.register(only_three_digits)

        # --- Scénario ---
        ctk.CTkLabel(frame, text="Scénario (3 chiffres)").pack(anchor="w", padx=10)
        scenario_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(validate_cmd, "%P"))
        scenario_entry.pack(fill="x", padx=10, pady=(0,10))

        # --- Étape ---
        ctk.CTkLabel(frame, text="Étape (3 chiffres)").pack(anchor="w", padx=10)
        etape_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(validate_cmd, "%P"))
        etape_entry.pack(fill="x", padx=10, pady=(0,10))

        # --- Description ---
        ctk.CTkLabel(frame, text="Description").pack(anchor="w", padx=10)
        description_text = ctk.CTkTextbox(frame, height=120)
        description_text.pack(fill="x", padx=10, pady=(0,10))

        # --- Upload multi-photos ---
        self.photos_paths = []  # liste des chemins Path

        ctk.CTkLabel(frame, text="Photos").pack(anchor="w", padx=10)
        photo_frame = ctk.CTkFrame(frame)
        photo_frame.pack(fill="x", padx=10, pady=(0,10))

        # Label qui indique combien de photos sont sélectionnées
        photo_label_upload = ctk.CTkLabel(photo_frame, text="Aucune photo sélectionnée")
        photo_label_upload.pack(side="left", fill="x", expand=True, padx=(0,5))

        def upload_photos():
            files = filedialog.askopenfilenames(
                title="Sélectionner des images",
                filetypes=[("Images", "*.png *.jpg *.jpeg")]
            )
            for f in files:
                path = Path(f)
                if path not in self.photos_paths:
                    self.photos_paths.append(path)
            photo_label_upload.configure(text=f"{len(self.photos_paths)} photo(s) sélectionnée(s)")

        ctk.CTkButton(photo_frame, text="Parcourir", command=upload_photos).pack(side="right")

        # --- Pré-remplissage si modification ---
        if data_existante:
            scenario_entry.insert(0, data_existante.get("scenario", ""))
            etape_entry.insert(0, data_existante.get("etape", ""))
            description_text.insert("1.0", data_existante.get("description", ""))

            # Photos multiples
            if "photos" in data_existante:
                self.photos_paths.extend([IMAGES_DIR / p for p in data_existante["photos"]])
            elif "photo" in data_existante:
                self.photos_paths.append(IMAGES_DIR / data_existante["photo"])

            if self.photos_paths:
                photo_label_upload.configure(text=f"{len(self.photos_paths)} photo(s) sélectionnée(s)")

        # --- Carrousel photo ---
        carrousel_frame = ctk.CTkFrame(frame)
        carrousel_frame.pack(fill="x", padx=10, pady=(10,5))

        photo_index = 0
        photo_display = ctk.CTkLabel(carrousel_frame, text="Aucune photo")
        photo_display.pack()

        def update_carrousel():
            nonlocal photo_index
            if not self.photos_paths:
                photo_display.configure(text="Aucune photo", image=None)
                return

            path = self.photos_paths[photo_index]
            if path.exists():
                img = Image.open(path)
                img.thumbnail((320, 240))
                ctk_img = ctk.CTkImage(img, size=img.size)
                photo_display.configure(image=ctk_img, text="")
                photo_display.image = ctk_img

        def prev_photo():
            nonlocal photo_index
            if not self.photos_paths:
                return
            photo_index = (photo_index - 1) % len(self.photos_paths)
            update_carrousel()

        def next_photo():
            nonlocal photo_index
            if not self.photos_paths:
                return
            photo_index = (photo_index + 1) % len(self.photos_paths)
            update_carrousel()

        nav_frame = ctk.CTkFrame(carrousel_frame)
        nav_frame.pack(pady=5)

        ctk.CTkButton(nav_frame, text="◀", width=50, command=prev_photo).pack(side="left", padx=5)
        ctk.CTkButton(nav_frame, text="▶", width=50, command=next_photo).pack(side="left", padx=5)

        update_carrousel()

        # --- Boutons Valider / Annuler ---
        def valider():
            scenario_val = scenario_entry.get()
            etape_val = etape_entry.get()
            description_val = description_text.get("1.0", "end").strip()

            if not scenario_val or not etape_val or not description_val:
                msg.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
                return

            # Copie des photos dans IMAGES_DIR et renommage
            saved_photos = []
            for idx, path in enumerate(self.photos_paths, start=1):
                if not path.exists():
                    continue

                # Cas 1 : photo déjà existante dans IMAGES_DIR, on la garde telle quelle
                if path.parent == IMAGES_DIR:
                    saved_photos.append(path.name)
                    continue

                # Cas 2 : nouvelle photo choisie par l'utilisateur, on la copie
                ext = path.suffix
                filename = f"{organe}_{sous}_{scenario_val}_{etape_val}_{idx}{ext}"
                dest = IMAGES_DIR / filename
                try:
                    shutil.copy(path, dest)
                except Exception as e:
                    msg.showerror("Erreur", f"Impossible de copier l'image {path} :\n{e}")
                    return
                saved_photos.append(filename)

            # Données finales
            new_data = {
                "organe": organe,
                "sous_organe": sous,
                "scenario": scenario_val,
                "etape": etape_val,
                "description": description_val,
                "photos": saved_photos
            }

            # Lecture fichier existant
            if DEPANNAGE_FILE.exists() and DEPANNAGE_FILE.stat().st_size > 0:
                try:
                    with open(DEPANNAGE_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}

            if "depannages" not in data:
                data["depannages"] = []

            # Suppression ancienne entrée si modification
            if data_existante:
                data["depannages"] = [
                    d for d in data["depannages"]
                    if not (
                        d["organe"] == organe and
                        d["sous_organe"] == sous and
                        d["scenario"] == data_existante["scenario"] and
                        d["etape"] == data_existante["etape"]
                    )
                ]

            data["depannages"].append(new_data)

            # Sauvegarde
            with open(DEPANNAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            msg.showinfo("Succès", "Procédure ajoutée avec succès.")
            popup.destroy()

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Annuler", width=120, command=popup.destroy).pack(side="left", padx=(0,10))
        ctk.CTkButton(btn_frame, text="Valider", width=120, command=valider).pack(side="left", padx=(10,0))

    def refresh_materiels(self):
        """Recharge les organes et sous-organes depuis le JSON"""
        self.materiels_data = self.load_materiels()

        organes = list(self.materiels_data.keys())
        self.organe_menu.configure(values=organes)

        # Reset sélection
        if organes:
            self.organe_var.set(organes[0])
            self.organe_selected(organes[0])
        else:
            self.organe_var.set("")
            self.sous_menu.configure(values=[])
            self.sous_var.set("")
            self.btn_afficher.grid_remove()

    # Traduction du language
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("depannage_titre"))
        self.organe_label.configure(text=self.lang_util.t("selectionnez_organe"))
        self.sous_label.configure(text=self.lang_util.t("selectionnez-sous-organe"))
        self.btn_afficher.configure(text=self.lang_util.t("depannage_aff"))
        self.btn_ia.configure(text=self.lang_util.t("prediction_ia"))
