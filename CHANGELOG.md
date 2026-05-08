# Changelog

Toutes les modifications notables de cette application sont documentées ici.

## [1.27.23] – 08-05-2026
### Ajout de fonctionnalités
- Blocage de la saisie les week-ends avec message d’avertissement.
- Gestion et affichage du temps travaillé quotidien et cumul HV.
- Popups interactifs pour sélectionner heures et minutes.
- Affichage des HV cumulées avec plafond selon rôle (Tech ou autre).
- Nouvelle interface pour la page d’accueil avec greeting + badge rôle.
- Traduction complète des pages et composants via `PageLang`.
- Gestion des erreurs de saisie avec messages traduits :
  - Saisie incorrecte des horaires.
  - Heure de fin inférieure à l’heure de début.
  - Durée nulle (00:00).
  - Chevauchement d’interventions.
  - Limite journalière de 8h24 dépassée.
- Rafraîchissement dynamique de la langue pour toutes les pages et popups.
- Ligne séparatrice dans le tableau historique pour les nouvelles journées.
- Gestion des matériels et sous-matériels via JSON avec mise à jour dynamique.
- Popups centrés sur la fenêtre principale.
- Ajouts des champs numero pour les organes et sous-organes lors d'une saisie.
- Ajout d'un champs de recherche dans la page des historiques d'interventions.
- Ajout menu contextuel "description"
- Ajout d'une checkbox activité support dans la page saisie.
- Ajout d'un bouton pour réinitialiser les HV.
- Ajout d'une page pour la gestion des Consommables (liste et recherche).
- Ajout d'une page de procédure de dépannage des cartes electroniques.
- Ajout du temps au mois sur la page accueil.
- Ajout d'un systeme de tri par mois et années pour la page historique.
- Ajout d'un systeme deroulant pour la liste des organes dans la page "ajout organes".
- Ajout du temps restant à saisir dans Magellan, affiché en page d'accueil.
- Ajout de la possibilité d'inserer plusieurs photos pour un depannage.
- Ajout d'icones raccourcis en page d'accueil pour les liens utiles.
- Ajout d'une page profil.
- Ajout de la possibilité d'éditer les informations de profil.
- Ajout d'une couleur pour les different grade de poste.

### Correctifs
- Correction de l’affichage du temps total à 0h00 au début d’une nouvelle journée.
- Correction des erreurs de chevauchement de variables dans les messages.
- Gestion des boutons popup (`btn_h_close`, `btn_m_close`) pour éviter les crashs lors de la traduction.
- Harmonisation des formats d’heure et minutes dans toutes les saisies.
- Correction des calculs HV et cumul journaliers.
- Amélioration de la robustesse lors de lecture/écriture de fichiers JSONL.
- Correction d'un bug d'affichage des popups de description dans la page historique.
- Correction du fond non transparent des popup de la page historique rendant des coins ronds sur fond carré.
- Suppression du systeme de tooltips pour la description d'un intervention.
- Correction du bug qui n'effacait pas les HV dans l'historique et les reaffichait même si resetés.
- Correction du nom d'enregistrement des fichiers PDF ou Excel.
- Correction des champs de saisies "N°" dans saisie intervention où l'on pouvais entrez autres que des chiffres et une lettre (idem dans ajout organes).
- Correction cellule magellan "non" qui est maintenant colorée, (Pareil en PDF (ligne)).
- Correction des images dans la page de procedure de depannage qui etaient effacées suite à une modification.
- Correction lors de la generation de l'excel / pdf qui affichait que le mois en cours et non tout les autres mois.
- Correction du rafraichissement de la page depannage lors de l'ajout ou suppression d'un organe ou sous organe.
- Correction de l'affichage des HV dans l'excel et PDF (qui etaient toujours egale a 0)
- Correction de l'affichage des HV sur la page d'accueil qui ne ce calculait plus apres un reset.
- Correction de l'affichage des boutons de navigation du caroussel photos, qui s'emplilaient à chaque appel d'étapes.
- Correction de l'affichage en grand de la photo dans les dépannage qui ouvrait toutes les photos d'un coup.
- Correction des HV qui restaient à 0h00 dans l'export Excel et PDF.
- Correction d'un bug qui mettait un message d'erreur lors de la modification d'un depannage si une photo etait deja presente.
- Deplacement des fichiers JSON dans un repertoire dedié avec correction des chemins dans le code.

### Remarques
- Version stable pour usage quotidien.
- La numérotation suit le schéma **MAJOR.MINOR.PATCH** :
  - MAJOR = 1 : première version stable
  - MINOR = 27 : nouvelles fonctionnalités majeures ajoutées
  - PATCH = 23 : corrections mineures récentes

