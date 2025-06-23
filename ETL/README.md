# Scripts ETL

Scripts Python pour nettoyer et transformer les données de l'OMS.

## Fichiers
- `run_etl.sh` : Script principal qui lance tous les traitements
- `etl_table_pays.py` : Traitement des pays
- `etl_table_unite.py` : Traitement des unités
- `etl_table_type_statistique.py` : Types de statistiques
- `etl_table_type_traitement.py` : Types de traitements
- `etl_table_population_hiv.py` : Données VIH
- `etl_table_mortalite.py` : Données mortalité
- `etl_table_transmission_mere_enfant.py` : Transmission mère-enfant
- `etl_table_traitement.py` : Données traitements
- `etl_table_statistique.py` : Statistiques générales

## Dépendances
- Python 3.8+
- pandas : Traitement des données
- numpy : Calculs numériques
- python-dateutil : Gestion des dates
- pytz : Gestion des fuseaux horaires

## Fonctionnement
1. Lecture des CSV depuis `../SourceData`
2. Nettoyage :
   - Suppression des lignes vides
   - Standardisation des noms de pays
   - Conversion des valeurs
3. Génération des fichiers dans `../DatasetClean`

## Installation
```bash
# Créer l'environnement virtuel
python3 -m venv etl_env
source etl_env/bin/activate  # Unix
# ou
.\etl_env\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation
```bash
# Lancer le traitement
bash run_etl.sh
``` 