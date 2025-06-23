from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv(dotenv_path="C:/Users/gaels/OneDrive/Documents/ECOLE-EPSI/Mspr/API/.env")

# Récupération des variables d'environnement
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
print(f"User: {POSTGRES_USER}, Password: {POSTGRES_PASSWORD}, Host: {POSTGRES_HOST}, Port: {POSTGRES_PORT}, DB: {POSTGRES_DB}")
# Vérification des variables d'environnement
if not all(
    [POSTGRES_USER,POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB]
):
    raise ValueError(
        "❌ Erreur : Certaines variables d'environnement ne sont pas chargées. Vérifie ton fichier .env !"
    )

# Construction sécurisée de l'URL de la base de données
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
print(f"✅ Connexion à la base de données : {DATABASE_URL}")

# Création du moteur SQLAlchemy asynchrone avec optimisation des connexions
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Active les logs SQL pour le débogage
    pool_size=10,  # Nombre max de connexions en pool
    max_overflow=20,  # Nombre max de connexions excédentaires
)

# Création de la session asynchrone
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base déclarative pour les modèles
Base = declarative_base()


# Dépendance pour récupérer la session de la base de données
async def get_db():
    async with SessionLocal() as session:
        yield session
