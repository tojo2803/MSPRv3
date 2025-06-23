# Données nettoyées

Fichiers CSV générés par les scripts ETL, prêts à être importés dans la base PostgreSQL.

## Fichiers générés
- `pays_clean.csv` : Liste des pays avec leurs IDs
- `unite_clean.csv` : Types d'unités (%, nombre, taux)
- `type_statistique_clean.csv` : Types de statistiques
- `type_traitement_clean.csv` : Types de traitements
- `table_population_hiv.csv` : Données population VIH
- `table_mortalite.csv` : Données mortalité
- `table_transmission_mere_enfant.csv` : Données transmission
- `table_traitement.csv` : Données traitements
- `table_statistique.csv` : Statistiques générales

## Structure
Tous les fichiers utilisent le point-virgule (;) comme séparateur et UTF-8 comme encodage.

## Important
Ne pas modifier ces fichiers manuellement. Si des changements sont nécessaires, modifier les données sources et relancer l'ETL. 