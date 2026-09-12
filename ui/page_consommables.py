import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox as msg
import json

from openpyxl import load_workbook
from tkinter import messagebox
from utils.page_lang import PageLang
from config.paths import CONSOMMABLES_FILE, EXCEL_RESEAU

# ================= JSONL STORE =================
CONSOMMABLES_FILE.parent.mkdir(parents=True, exist_ok=True)  # assure que le dossier existe

# --------- Charger la liste des consommables -----------
def load_consommables():
    if not CONSOMMABLES_FILE.exists():
        return []
    consommables = []
    with open(CONSOMMABLES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                consommables.append(json.loads(line))
    return consommables

# -------------- Sauvegarder les données ----------------
def save_consommable(consommable):
    with open(CONSOMMABLES_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(consommable, ensure_ascii=False) + "\n")

# -------------- Supprimer une entrée -------------------
def delete_from_jsonl(cid):
    consommables = load_consommables()
    # comparer en nettoyant les IDs
    consommables = [c for c in consommables if str(c["id"]).strip() != str(cid).strip()]
    with open(CONSOMMABLES_FILE, "w", encoding="utf-8") as f:
        for c in consommables:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

# ================= PAGE =================
class PageConsommables(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.lang_util = PageLang(app)

        # ================= HEADER =================
        header = ctk.CTkFrame(self, border_width=1, border_color="blue", fg_color="#1E5CC4", height=60)
        header.pack(fill="x", padx=5, pady=5)
        header.pack_propagate(False)
        self.header_label = ctk.CTkLabel(header, text=self.lang_util.t("consommables_titre"), font=("Roboto", 24), text_color="white")
        self.header_label.pack(expand=True)

        # ================= FORM =================
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        # ================= SEARCH BAR =================
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=(5, 0))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text=self.lang_util.t("rechercher"),
            width=480
        )
        self.search_entry.pack(side="left", padx=5)

        self.search_btn = ctk.CTkButton(
            search_frame,
            text=self.lang_util.t("rechercher"),
            width=120,
            command=self.search_consommables
        )
        self.search_btn.pack(side="left", padx=5, pady=5)

        self.entry_id = ctk.CTkEntry(form_frame, width=150, placeholder_text=self.lang_util.t("consommable_id"))
        self.entry_id.pack(side="left", padx=5, pady=5)

        self.entry_nom = ctk.CTkEntry(form_frame, width=300, placeholder_text=self.lang_util.t("consommable_nom"))
        self.entry_nom.pack(side="left", padx=5, pady=5)

        self.btn_add = ctk.CTkButton(form_frame, text=self.lang_util.t("ajouter"), command=self.add_consommable)
        self.btn_add.pack(side="left", padx=5)

        self.btn_refresh_network = ctk.CTkButton(
            form_frame,
            text="Rafraîchir depuis le réseau",
            command=self.refresh_from_network
        )

        self.btn_refresh_network.pack(pady=10)

        # Reinitialiser la liste lorsque le champs est vide
        self.search_entry.bind(
            "<KeyRelease>",
            lambda e: self.load_data(self.search_entry.get())
        )

        # ================= TREEVIEW =================
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = (
            "id",
            "nom",
            "quantite_stoe",
            "quantite_vg"
        )
        style = ttk.Style()
        style.theme_use("default")

        # style isolé pour ce treeview
        style.configure(
            "Consommables.Treeview.Heading",
            background="#DADADA",
            foreground="#000000",
            font=("Roboto", 10)
        )
        style.map(
            "Consommables.Treeview.Heading",
            background=[("active", "#C8C8C8")]
        )

        # Scrollbar verticale
        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )
        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Consommables.Treeview",
            height=20,
            yscrollcommand=scrollbar_y.set
        )
        
        self.tree.tag_configure(
            "rupture",
            background="#FF3030",
            foreground="black"
        )

        self.tree.tag_configure(
            "stoe_vide",
            background="#FFA500",
            foreground="black"
        )

        self.tree.heading("id", text=self.lang_util.t("consommable_id"))
        self.tree.heading("nom", text=self.lang_util.t("consommable_nom"))
        self.tree.heading("quantite_stoe", text="Quantité STOE")
        self.tree.heading("quantite_vg", text="Quantité VG")

        self.tree.column("id", width=20, anchor="center")
        self.tree.column("nom", width=500, anchor="w")
        self.tree.column("quantite_stoe", width=20, anchor="center")
        self.tree.column("quantite_vg", width=20, anchor="center")

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Liaison scrollbar -> Treeview
        scrollbar_y.configure(
            command=self.tree.yview
        )

        # ================= CONTEXT MENU =================
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label=self.lang_util.t("supprimer"), command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)

        # ============= CHARGER LES DONNEES ==============
        self.load_data()

    # ================= METHODES =================
    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        self.tree.selection_set(row_id)
        self.menu.tk_popup(event.x_root, event.y_root)

    def delete_selected(self):
        if not msg.askyesno("Confirmation", "Supprimer ce consommable ?"):
            return
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.tree.item(item)["values"]
        cid = str(values[0]).strip()
        self.tree.delete(item)
        delete_from_jsonl(cid)

    def load_data(self, search_text=""):
        self.tree.delete(*self.tree.get_children())

        search_text = search_text.lower().strip()

        for item in load_consommables():
            cid = str(item["id"])
            nom = str(item["nom"])

            quantite_stoe = item.get("quantite_stoe", 0)
            quantite_vg = item.get("quantite_vg", 0)

            if search_text:
                if search_text not in cid.lower() and search_text not in nom.lower():
                    continue

            # Déterminer la couleur de la ligne
            if quantite_stoe == 0 and quantite_vg == 0:
                tags = ("id_bold", "rupture")

            elif quantite_stoe == 0 and quantite_vg >= 1:
                tags = ("id_bold", "stoe_vide")

            else:
                tags = ("id_bold",)

            self.tree.insert(
                "",
                "end",
                values=(
                    cid,
                    nom.upper(),
                    quantite_stoe,
                    quantite_vg
                ),
                tags=tags
            )

    def consommable_exists(self, cid):
        cid = str(cid).strip()
        for row in self.tree.get_children():
            if str(self.tree.item(row)["values"][0]).strip() == cid:
                return True
        return False

    def add_consommable(self):
        cid = self.entry_id.get().strip()
        nom = self.entry_nom.get().strip().upper()
        if not cid or not nom:
            return
        if self.consommable_exists(cid):
            return
        consommable = {"id": cid, "nom": nom}
        save_consommable(consommable)
        self.tree.insert("", "end", values=(cid, nom), tags=("id_bold",))
        self.entry_id.delete(0, "end")
        self.entry_nom.delete(0, "end")
    
    def search_consommables(self):
        search_text = self.search_entry.get()
        self.load_data(search_text)

    def refresh_from_network(self):
        try:
            workbook = load_workbook(
                EXCEL_RESEAU,
                read_only=True,
                data_only=True
            )

            sheet = workbook["referentiel-articles"]

            # ================= RÉCUPÉRATION EXCEL =================
            articles_reseau = []

            for row in sheet.iter_rows(min_row=2, values_only=True):

                code_article = row[0]
                description = row[2]

                # Code article obligatoire
                if code_article is None:
                    continue

                # Description obligatoire
                if description is None:
                    continue

                description = str(description).strip()

                # Ignorer les descriptions vides / null
                if not description:
                    continue

                if description.lower() in ("~~null~~", "~null~", "null", "none"):
                    continue

                # Uniformiser le code article
                code_article = str(code_article).strip()

                quantite_stoe = row[6]
                quantite_vg = row[7]

                # Si la cellule Excel est vide
                if quantite_stoe is None:
                    quantite_stoe = 0

                if quantite_vg is None:
                    quantite_vg = 0

                articles_reseau.append({
                    "id": str(code_article).strip(),
                    "nom": description,
                    "quantite_stoe": quantite_stoe,
                    "quantite_vg": quantite_vg
                })

            workbook.close()

            # ================= LECTURE JSON LOCAL =================
            consommables_locaux = {}

            if CONSOMMABLES_FILE.exists():
                with open(CONSOMMABLES_FILE, "r", encoding="utf-8") as f:
                    for ligne in f:

                        ligne = ligne.strip()

                        if not ligne:
                            continue

                        try:
                            consommable = json.loads(ligne)

                            code = str(consommable["id"]).strip()

                            consommables_locaux[code] = consommable

                        except (json.JSONDecodeError, KeyError):
                            continue

            # ================= SYNCHRONISATION =================
            nouveaux = 0
            modifies = 0

            for article in articles_reseau:

                code = article["id"]

                if code not in consommables_locaux:

                    consommables_locaux[code] = article
                    nouveaux += 1

                else:
                    # Vérifier si le nom a changé
                    ancien = consommables_locaux[code]

                    modification = False

                    if ancien.get("nom", "") != article["nom"]:
                        ancien["nom"] = article["nom"]
                        modification = True

                    if ancien.get("quantite_stoe", 0) != article["quantite_stoe"]:
                        ancien["quantite_stoe"] = article["quantite_stoe"]
                        modification = True

                    if ancien.get("quantite_vg", 0) != article["quantite_vg"]:
                        ancien["quantite_vg"] = article["quantite_vg"]
                        modification = True

                    if modification:
                        modifies += 1

            # ================= SAUVEGARDE JSONL =================
            with open(CONSOMMABLES_FILE, "w", encoding="utf-8") as f:

                for consommable in consommables_locaux.values():

                    f.write(
                        json.dumps(
                            consommable,
                            ensure_ascii=False
                        ) + "\n"
                    )

            # ================= RAFRAÎCHIR TREEVIEW =================

            for item in self.tree.get_children():
                self.tree.delete(item)

            for consommable in consommables_locaux.values():

                quantite_stoe = consommable.get("quantite_stoe", 0)
                quantite_vg = consommable.get("quantite_vg", 0)

                tag = ""

                if quantite_stoe == 0 and quantite_vg == 0:
                    tag = "rupture"

                elif quantite_stoe == 0 and quantite_vg >= 1:
                    tag = "stoe_vide"
                
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        consommable.get("id", ""),
                        consommable.get("nom", ""),
                        quantite_stoe,
                        quantite_vg
                    ),
                    tags=(tag,)
                )

            messagebox.showinfo(
                "Rafraîchissement terminé",
                f"{len(articles_reseau)} articles trouvés dans le référentiel.\n\n"
                f"{nouveaux} nouveaux articles ajoutés.\n"
                f"{modifies} articles mis à jour.\n\n"
                f"{len(consommables_locaux)} consommables enregistrés localement."
            )

        except FileNotFoundError:
            messagebox.showerror(
                "Erreur",
                "Le fichier eBOARD_AIC EK1.xlsx est introuvable."
            )

        except KeyError:
            messagebox.showerror(
                "Erreur",
                "L'onglet 'referentiel-articles' est introuvable."
            )

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de rafraîchir le référentiel :\n\n{e}"
            )

    # Traduction du language
    def refresh_language(self):
        self.lang_util = PageLang(self.app)
        self.header_label.configure(text=self.lang_util.t("consommables_titre"))
        self.entry_id.configure(placeholder_text=self.lang_util.t("consommable_id"))
        self.entry_nom.configure(placeholder_text=self.lang_util.t("consommable_nom"))
        self.btn_add.configure(text=self.lang_util.t("ajouter"))
        self.tree.heading("id", text=self.lang_util.t("consommable_id"))
        self.tree.heading("nom", text=self.lang_util.t("consommable_nom"))
        self.search_entry.configure(placeholder_text=self.lang_util.t("rechercher"))
        self.search_btn.configure(text=self.lang_util.t("rechercher"))

