# API2 - État actuel et problèmes

## Structure actuelle
L'API est structurée avec les fichiers suivants :
- `database.py` : Configuration de la connexion PostgreSQL
- `models.py` : Modèles SQLAlchemy (User, Product, Order, OrderItem, Todo)
- `schemas.py` : Schémas Pydantic pour la validation des données
- `main.py` : Routes FastAPI
- `.env` : Configuration de la base de données

## Configuration de la base de données
- Base de données : PostgreSQL
- Nom de la BDD : `bdd_mspr`
- Utilisateur : `florentbaccard` ou ton user car tu doit créé la bdd sur ton post.

## Problèmes actuels

### 1. Problème de compatibilité Python 3.13
Il y a des conflits de compatibilité entre Python 3.13 et certaines dépendances :
- FastAPI
- Pydantic
- SQLAlchemy

### 2. Erreurs d'installation des dépendances
Nous avons essayé plusieurs versions des packages :
```
fastapi==0.68.0
uvicorn==0.15.0
sqlalchemy==1.4.23
psycopg[binary]>=3.0.18
python-dotenv==0.19.0
pydantic==1.8.2
```

### 3. Erreur au lancement
Lors du lancement de l'API avec `uvicorn main:app --reload --port 8084`, nous obtenons une erreur liée à Pydantic et FastAPI.

## Solutions possibles

1. Rétrograder Python à une version plus stable (3.11 ou 3.12)
2. Attendre des mises à jour des packages pour supporter Python 3.13
3. Utiliser des versions plus anciennes mais stables des packages

## État de la base de données
La base de données PostgreSQL est accessible et contient déjà des tables :
```sql
mortalite
pays
population_hiv
statistique
traitement
transmission_mere_enfant
type_statistique
type_traitement
unite
```

## Prochaines étapes suggérées
1. Résoudre les problèmes de compatibilité des dépendances
2. Tester la création des nouvelles tables
3. Implémenter et tester les routes API 