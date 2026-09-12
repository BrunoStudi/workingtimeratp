# 📋 Changelog

Toutes les modifications notables apportées à **Journées de travail RATP – Application agent** sont documentées dans ce fichier.

---

## 🚀 Version 1.41.43

**Date de publication : 10 septembre 2026**
**Statut : Stable**

---

## ✨ Nouvelles fonctionnalités

### 🕒 Temps de travail & heures variables

- Blocage de la saisie les week-ends avec message d’avertissement.
- Gestion et affichage du temps travaillé quotidien.
- Gestion du cumul des heures variables (HV).
- Affichage des HV cumulées avec plafond selon le rôle de l’utilisateur.
- Ajout d’un bouton permettant de réinitialiser les HV.
- Ajout du temps de travail mensuel sur la page d’accueil.
- Ajout du temps restant à saisir dans Magellan sur la page d’accueil.
- Ajout d’un système de tri par mois et par année dans l’historique.
- Ajout de popups interactifs pour sélectionner les heures et les minutes.

### 🏠 Page d’accueil

- Nouvelle interface pour la page d’accueil.
- Ajout d’un message de bienvenue personnalisé.
- Ajout d’un badge représentant le rôle de l’utilisateur.
- Ajout de la date et de l’heure.
- Ajout de raccourcis vers les outils métier.
- Ajout de la possibilité de créer des raccourcis personnalisés.
- Ajout d’une icône personnalisée pour chaque raccourci.

### 📝 Interventions

- Ajout des champs **N°** pour les organes et sous-organes lors d’une saisie.
- Ajout d’un champ de recherche dans l’historique des interventions.
- Ajout d’un menu contextuel permettant d’afficher la description d’une intervention.
- Ajout d’une case **Activité support** sur la page de saisie.
- Ajout d’un système déroulant pour la liste des organes dans la page d’ajout d’organes.
- Ajout de la gestion des matériels et sous-matériels via fichiers JSON avec mise à jour dynamique.

### 📦 Consommables

- Ajout d’une page dédiée à la gestion des consommables.
- Ajout d’un système de recherche des consommables.
- Ajout d’une synchronisation depuis un classeur Excel disponible sur le réseau.
- Récupération automatique des informations depuis la feuille `referentiel-articles`.
- Ajout des quantités disponibles en magasin **STOE**.
- Ajout des quantités disponibles en magasin **VG**.
- Ajout d’un code couleur pour identifier rapidement l’état des stocks :

  - 🔴 STOE = 0 et VG = 0.
  - 🟠 STOE = 0 et VG supérieur ou égal à 1.
  - Aucun marquage si du stock est disponible en STOE.

### 🔧 Dépannage

- Ajout d’une page dédiée aux procédures de dépannage des cartes électroniques.
- Ajout de procédures organisées par organes, sous-organes et scénarios.
- Ajout de la possibilité d’associer plusieurs photos à une procédure.
- Ajout d’un carrousel permettant de parcourir les photos.
- Ajout de l’affichage agrandi des photos.

### 👤 Profil utilisateur

- Ajout d’une page Profil.
- Ajout de la possibilité de modifier les informations du profil.
- Ajout de couleurs différentes selon le grade ou le rôle de l’utilisateur.

### 🌍 Interface & langues

- Traduction des pages et composants via `PageLang`.
- Rafraîchissement dynamique de la langue.
- Traduction des messages d’erreur et d’avertissement.
- Centrage des différentes fenêtres modales par rapport à la fenêtre principale.

---

## 🛠️ Correctifs

### 🕒 Temps de travail & HV

- Correction de l’affichage du temps total à `0h00` au début d’une nouvelle journée.
- Correction de différents calculs liés aux HV.
- Correction du cumul journalier des HV.
- Correction d’un problème empêchant le recalcul des HV après une réinitialisation.
- Correction d’un problème où les HV historiques pouvaient être effacées ou réaffichées incorrectement après un reset.
- Correction de l’affichage des HV dans les exports Excel et PDF.
- Correction d’un problème où les HV restaient systématiquement à `0h00` dans certains exports.

### 📝 Saisie & historique

- Correction des erreurs liées aux chevauchements d’interventions.
- Harmonisation des formats d’heure et de minutes.
- Correction des validations des champs **N°** afin de limiter les caractères autorisés.
- Correction de l’affichage des popups de description dans l’historique.
- Correction du fond non transparent de certaines fenêtres de description.
- Suppression de l’ancien système de tooltips pour la description des interventions.
- Correction de la coloration de la cellule Magellan lorsqu’elle contient `Non`.
- Correction également appliquée aux exports PDF.

### 📦 Consommables

- Ajout d’une barre de défilement sur la page Consommables.
- Correction du chargement des quantités de stock STOE et VG.
- Correction de la persistance des quantités lors du redémarrage de l’application.
- Correction du réaffichage automatique des couleurs de disponibilité lors du chargement des données.

### 🔧 Dépannage

- Correction d’un problème supprimant les images après modification d’une procédure.
- Correction du rafraîchissement après ajout ou suppression d’un organe ou sous-organe.
- Correction de l’empilement des boutons de navigation du carrousel.
- Correction de l’affichage agrandi qui pouvait ouvrir plusieurs photos simultanément.
- Correction d’un message d’erreur lors de la modification d’une procédure possédant déjà une photo.

### 📊 Exports

- Correction du nom d’enregistrement des fichiers PDF et Excel.
- Correction d’un problème où seuls les éléments du mois courant apparaissaient dans les exports.
- Correction de l’affichage des HV dans les exports Excel et PDF.

### 🗂️ Données & configuration

- Amélioration de la robustesse de la lecture et de l’écriture des fichiers JSONL.
- Déplacement des fichiers JSON dans un répertoire dédié.
- Correction des chemins associés aux fichiers de données.
- Ajout de l’extension `.BAx` pour certains organes, par exemple `.BA1`.

### 🔗 Raccourcis

- Chiffrement des liens internes utilisés sur la page d’accueil.
- Correction de la position de la fenêtre de création d’un raccourci personnalisé.
- La fenêtre est désormais centrée sur la fenêtre principale.
- Correction du placement des icônes personnalisées.
- Le conteneur des raccourcis personnalisés se rétracte automatiquement lorsqu’aucun raccourci n’est présent.

### 🌍 Interface & traduction

- Correction des boutons popup `btn_h_close` et `btn_m_close` afin d’éviter certains crashs lors du changement de langue.
- Correction de plusieurs messages traduits liés aux erreurs de saisie :

  - horaires incorrects ;
  - heure de fin antérieure à l’heure de début ;
  - durée nulle (`00:00`) ;
  - chevauchement d’interventions ;
  - dépassement de la limite journalière de `8h24`.

---

## 🔐 Données & confidentialité

Les données de l’application sont stockées localement sur le poste de l’utilisateur.

Aucune information personnelle n’est collectée ou transmise automatiquement à distance.

Les liens internes utilisés par l’application ne sont pas stockés directement en clair dans le code source.

---

## 📌 Remarques

Cette version est considérée comme **stable pour un usage quotidien**.

La numérotation des versions suit le principe :

`MAJOR.MINOR.PATCH`

| Élément   | Valeur | Signification                               |
| --------- | -----: | ------------------------------------------- |
| **MAJOR** |    `1` | Première génération stable de l’application |
| **MINOR** |   `41` | Évolution fonctionnelle de l’application    |
| **PATCH** |   `43` | Correctifs et améliorations de stabilité    |

---

## 👨‍💻 Développement

**Bruno Carrière**
Équipe **EK1 • AME**

Application développée en **Python**.

Projet personnel – **2026**

Tous droits réservés.
