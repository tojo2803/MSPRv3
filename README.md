# Projet MSPR - Données VIH Mondiales

## Description
Ce projet ETL (Extract, Transform, Load) traite les données mondiales sur le VIH pour créer une base de données structurée PostgreSQL. Il comprend des informations sur la prévalence, la mortalité, les traitements et la transmission mère-enfant du VIH par pays.

## Structure du Projet
```
.
├── ETL/                    # Scripts ETL
│   ├── run_etl.sh         # Script principal d'exécution
│   ├── etl.log            # Fichier de logs
│   └── *.py               # Scripts Python ETL
├── SQL/                    # Scripts SQL
│   ├── create_tables.sql  # Création des tables
│   ├── clean_tables.sql   # Nettoyage des tables
│   ├── import_data.sql    # Import des données
│   └── create_views.sql   # Création des vues
├── SourceData/            # Données sources
├── DatasetClean/          # Données transformées
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
```

## Structure de la Base de Données

### Tables de Référence

1. **pays**
   - `id_pays` SERIAL PRIMARY KEY
   - `nom_pays` VARCHAR(100) NOT NULL
   - `region` VARCHAR(100)
   - `sous_region` VARCHAR(100)

2. **unite**
   - `id_unite` SERIAL PRIMARY KEY
   - `nom_unite` VARCHAR(50) NOT NULL

3. **type_statistique**
   - `id_type_statistique` SERIAL PRIMARY KEY
   - `nom_type_statistique` VARCHAR(100) NOT NULL

4. **type_traitement**
   - `id_type_traitement` SERIAL PRIMARY KEY
   - `nom_type_traitement` VARCHAR(100) NOT NULL

### Tables Principales

5. **population_hiv**
   - `id` SERIAL PRIMARY KEY
   - `id_pays` INTEGER (FK → pays)
   - `annee` INTEGER
   - `valeur` DECIMAL(10,2)
   - `id_unite` INTEGER (FK → unite)
   - UNIQUE(id_pays, annee)

6. **mortalite**
   - `id` SERIAL PRIMARY KEY
   - `id_pays` INTEGER (FK → pays)
   - `annee` INTEGER
   - `valeur` DECIMAL(10,2)
   - `id_unite` INTEGER (FK → unite)
   - UNIQUE(id_pays, annee)

7. **transmission_mere_enfant**
   - `id` SERIAL PRIMARY KEY
   - `id_pays` INTEGER (FK → pays)
   - `valeur` DECIMAL(10,2)
   - `id_unite` INTEGER (FK → unite)
   - UNIQUE(id_pays)

8. **traitement**
   - `id` SERIAL PRIMARY KEY
   - `id_pays` INTEGER (FK → pays)
   - `valeur` DECIMAL(10,2)
   - `id_unite` INTEGER (FK → unite)
   - `id_type_traitement` INTEGER (FK → type_traitement)
   - UNIQUE(id_pays, id_type_traitement)

9. **statistique**
   - `id` SERIAL PRIMARY KEY
   - `id_pays` INTEGER (FK → pays)
   - `annee` INTEGER
   - `valeur` DECIMAL(10,2)
   - `id_unite` INTEGER (FK → unite)
   - `id_type_statistique` INTEGER (FK → type_statistique)
   - UNIQUE(id_pays, annee, id_type_statistique)

### Vues

1. **vue_powerbi_complete**
   - Informations pays :
     - `id_pays` (INTEGER)
     - `nom_pays` (VARCHAR)
     - `region` (VARCHAR)
   - Année de référence :
     - `annee` (INTEGER)
   - Données HIV :
     - `population_hiv` (DECIMAL)
     - `unite_population_hiv` (VARCHAR)
   - Données mortalité :
     - `mortalite` (DECIMAL)
     - `unite_mortalite` (VARCHAR)
   - Transmission mère-enfant :
     - `transmission_mere_enfant` (DECIMAL)
     - `unite_transmission` (VARCHAR)
   - Traitements :
     - `traitement_adulte` (DECIMAL)
     - `traitement_enfant` (DECIMAL)
     - `unite_traitement` (VARCHAR)
   - Statistiques :
     - `valeur_statistique` (DECIMAL)
     - `type_statistique` (VARCHAR)
     - `unite_statistique` (VARCHAR)
   - Calculs supplémentaires :
     - `evolution_population_hiv` (DECIMAL)
     - `evolution_mortalite` (DECIMAL)
   - Moyennes régionales :
     - `moyenne_population_hiv_region` (DECIMAL)
     - `moyenne_mortalite_region` (DECIMAL)
     - `moyenne_transmission_region` (DECIMAL)
     - `moyenne_traitement_adulte_region` (DECIMAL)
     - `moyenne_traitement_enfant_region` (DECIMAL)

2. **vue_indicateurs_pays**
   - `id_pays` (INTEGER)
   - `nom_pays` (VARCHAR)
   - `region` (VARCHAR)
   - `taux_transmission_mere_enfant` (DECIMAL)
   - `taux_traitement_adulte` (DECIMAL)
   - `taux_traitement_enfant` (DECIMAL)

3. **vue_evolution_temporelle**
   - `id_pays` (INTEGER)
   - `nom_pays` (VARCHAR)
   - `region` (VARCHAR)
   - `annee` (INTEGER)
   - `population_hiv` (DECIMAL)
   - `mortalite` (DECIMAL)
   - `valeur_statistique` (DECIMAL)
   - `nom_type_statistique` (VARCHAR)

### Vue Globale

La base de données contient une vue unique et complète nommée **vue_globale** qui regroupe toutes les informations nécessaires pour PowerBI :

1. **Informations de base**
   - Pays :
     - `id_pays` (INTEGER)
     - `nom_pays` (VARCHAR)
     - `region` (VARCHAR)
     - `sous_region` (VARCHAR)
   - Temps :
     - `annee` (INTEGER)

2. **Indicateurs principaux**
   - Population HIV :
     - `population_hiv` (DECIMAL)
     - `unite_population_hiv` (VARCHAR)
   - Mortalité :
     - `mortalite` (DECIMAL)
     - `unite_mortalite` (VARCHAR)
   - Transmission mère-enfant :
     - `transmission_mere_enfant` (DECIMAL)
     - `unite_transmission` (VARCHAR)
   - Traitements :
     - `traitement_adulte` (DECIMAL)
     - `traitement_enfant` (DECIMAL)
     - `unite_traitement` (VARCHAR)
   - Statistiques :
     - `valeur_statistique` (DECIMAL)
     - `type_statistique` (VARCHAR)
     - `unite_statistique` (VARCHAR)

3. **Indicateurs calculés**
   - Évolutions :
     - `evolution_population_hiv` (DECIMAL)
     - `evolution_mortalite` (DECIMAL)
   - Moyennes régionales :
     - `moyenne_population_hiv_region` (DECIMAL)
     - `moyenne_mortalite_region` (DECIMAL)
     - `moyenne_transmission_region` (DECIMAL)
     - `moyenne_traitement_adulte_region` (DECIMAL)
     - `moyenne_traitement_enfant_region` (DECIMAL)
   - Classements :
     - `rang_population_hiv` (INTEGER)
     - `rang_mortalite` (INTEGER)
     - `percentile_population_hiv` (DECIMAL)
     - `percentile_mortalite` (DECIMAL)

Cette vue unique permet de :
- Créer tous types de visualisations dans PowerBI
- Analyser les tendances temporelles
- Comparer les pays et les régions
- Calculer des statistiques avancées
- Optimiser les performances des requêtes

## Dépendances

### Base de Données
- PostgreSQL 12 ou supérieur
- Encodage UTF-8

### Python et Bibliothèques
- Python 3.8 ou supérieur
- pandas >= 2.0.0
- numpy >= 1.24.0
- python-dateutil >= 2.8.2
- pytz >= 2023.3
- six >= 1.16.0

### Modules Python Standard
- logging (journalisation)
- sys (fonctions système)
- pathlib (gestion des chemins)

## Installation

1. Créer la base de données :
```bash
createdb mspr_dev
```

2. Installer les dépendances Python :
```bash
pip install -r ETL/requirements.txt
```

3. Initialiser la base de données :
```bash
psql mspr_dev -f SQL/create_tables.sql
psql mspr_dev -f SQL/import_data.sql
psql mspr_dev -f SQL/create_views.sql
```

## Validation des Données

Le script d'import effectue les vérifications suivantes :
- Pas de valeurs négatives (converties en 0)
- Pourcentages limités entre 0 et 100
- Vérification des clés étrangères
- Unicité des combinaisons de clés
- Cohérence des types de données

## Logs
Les logs sont enregistrés dans `ETL/etl.log` avec :
- Horodatage de chaque opération
- Niveau de gravité (INFO, WARNING, ERROR)
- Description détaillée des événements
- Statut de réussite/échec des opérations

## Choix Techniques

### Approche Procédurale vs POO
Le projet utilise une approche procédurale plutôt que la Programmation Orientée Objet (POO) pour plusieurs raisons :

1. **Nature du projet ETL**
   - Scripts ETL simples et directs
   - Opérations principalement linéaires (Extraction → Transformation → Chargement)
   - Pas de comportements complexes qui justifieraient des classes

2. **Type de données**
   - Données tabulaires simples
   - Transformations directes
   - Pas de hiérarchies complexes d'objets

3. **Maintenance**
   - Scripts procéduraux plus faciles à déboguer
   - Processus ETL clair et séquentiel
   - Logs simples à suivre

L'approche procédurale avec des fonctions bien définies est plus adaptée et plus efficace pour ce type de traitement de données. La POO aurait ajouté une complexité inutile dans ce contexte.