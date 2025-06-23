# Documentation - Base de données HIV/SIDA

Ce projet contient les scripts pour générer et alimenter la base de données PostgreSQL avec les données HIV/SIDA de l'OMS.

## Installation

1. **PostgreSQL**
   ```bash
   # Mac
   brew install postgresql@14
   brew services start postgresql@14

   # Linux/Windows
   # Installer depuis postgresql.org
   ```

2. **Mise en place**
   ```bash
   git clone <URL_DU_PROJET>
   cd <NOM_DU_PROJET>
   createdb bdd_mspr
   ```

## Fichiers importants
```
projet/
├── SQL/                  # Scripts de création de la base
├── ETL/                  # Scripts de nettoyage des données
├── DatasetClean/        # Données prêtes à l'import
└── SourceData/          # Données brutes de l'OMS
```

## Étapes à suivre

1. **Préparation des données**
   ```bash
   cd ETL
   python3 -m venv etl_env
   source etl_env/bin/activate  # ou .\etl_env\Scripts\activate sur Windows
   pip install -r requirements.txt
   bash run_etl.sh             # Nettoie les données de l'OMS
   ```

2. **Import dans PostgreSQL**
   ```bash
   cd ../SQL
   psql -d bdd_mspr -f create_tables.sql
   psql -d bdd_mspr -f import_data.sql
   psql -d bdd_mspr -f create_views.sql
   ```

## Connexion PowerBI
- Base de données : bdd_mspr
- Vue à utiliser : vue_powerbi_complete
- Données disponibles : HIV, mortalité, transmission mère-enfant

## En cas de problème
- Base inaccessible : Vérifier que PostgreSQL tourne
- Données manquantes : Relancer l'ETL
- Erreur d'import : Vérifier les droits sur DatasetClean/

Contact : [email de l'équipe]