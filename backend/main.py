from fastapi import FastAPI, Depends, HTTPException
import joblib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import models, schemas
from database import engine, get_db
import sys
import os

from prediction import create_voting_regressor, prepare_data_generic, preprocess_features, train_voting_regressor
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Déclare `app`
app = FastAPI(title="MSPR API", version="1.0.0")

# ========================
# Configuration de la langue
# ========================

LANG = os.getenv("LANG", "fr")  # "fr" par défaut

# Dictionnaire de traductions
TRANSLATIONS = {
    "root_message": {
        "fr": "Bienvenue sur l'API MSPR!",
        "en": "Welcome to the MSPR API!",
        "de": "Willkommen bei der MSPR API!"
    },
    "preflight_ok": {
        "fr": "Préflight OPTIONS accepté",
        "en": "Preflight OPTIONS accepted",
        "de": "Preflight OPTIONS akzeptiert"
    },
    "country_not_found": {
        "fr": "Pays non trouvé",
        "en": "Country not found",
        "de": "Land nicht gefunden"
    },
    "country_deleted": {
        "fr": "Pays supprimé avec succès",
        "en": "Country successfully deleted",
        "de": "Land erfolgreich gelöscht"
    },
    "invalid_table": {
        "fr": "Table invalide",
        "en": "Invalid table",
        "de": "Ungültige Tabelle"
    },
    "region_or_country_required": {
        "fr": "Region ou pays doivent être renseignés",
        "en": "Region or country must be provided",
        "de": "Region oder Land müssen angegeben werden"
    },
    "unknown_table": {
        "fr": "Table inconnue",
        "en": "Unknown table",
        "de": "Unbekannte Tabelle"
    },
    "merge_key_error": {
        "fr": "Les clés de fusion ne correspondent pas entre les tables",
        "en": "Merge keys do not match between tables",
        "de": "Die Schlüsselfelder stimmen zwischen den Tabellen nicht überein"
    },
    "table_not_found": {
        "fr": "Table '{table}' introuvable",
        "en": "Table '{table}' not found",
        "de": "Tabelle '{table}' nicht gefunden"
    },
    "missing_dataframe": {
        "fr": "Le DataFrame est manquant",
        "en": "DataFrame is missing",
        "de": "DataFrame fehlt"
    },
    "target_required": {
        "fr": "La colonne cible est requise pour l'entraînement",
        "en": "Target column is required for training",
        "de": "Zielspalte für das Training erforderlich"
    },
    "avant_separation": {
    "fr": "Avant séparation, taille du DataFrame : {shape}",
    "en": "Before split, DataFrame shape: {shape}",
    "de": "Vor der Trennung, DataFrame-Größe: {shape}"
    },
    "model_trained": {
        "fr": "Modèle entraîné avec succès",
        "en": "Model trained successfully",
        "de": "Modell erfolgreich trainiert"
    }
}

def tr(key, **kwargs):
    """Fonction utilitaire pour traduire les messages."""
    msg = TRANSLATIONS.get(key, {}).get(LANG, TRANSLATIONS.get(key, {}).get("fr", key))
    return msg.format(**kwargs) if kwargs else msg

# ========================
# Configuration des CORS
# ========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines. Tu peux spécifier ici une liste d'origines autorisées.
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP (GET, POST, etc.).
    allow_headers=["Authorization", "Content-Type","*"],  # Permet tous les types d'en-têtes.
)
@app.options("/{path:path}")
async def options_handler():
    return {"message": tr("preflight_ok")}


# Initialisation de la base de données
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("startup")
async def startup():
    await init_db()


# ========================
# Endpoints PAYS
# ========================
@app.get("/payslist/")
async def get_pays(db: AsyncSession = Depends(get_db)):
    """
    Endpoint pour récupérer les informations des pays depuis la table `pays`.
    """
    result = await db.execute(select(models.Pays))
    pays_list = result.scalars().all()
    return [{"id": pays.id_pays, "nom": pays.nom_pays, "region": pays.region} for pays in pays_list]


@app.get("/pays/", response_model=List[schemas.Pays])
async def get_pays(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Pays))
    return result.scalars().all()


@app.post("/pays/", response_model=schemas.Pays)
async def create_pays(pays: schemas.PaysCreate, db: AsyncSession = Depends(get_db)):
    new_pays = models.Pays(**pays.dict())
    db.add(new_pays)
    await db.commit()
    await db.refresh(new_pays)
    return new_pays


@app.put("/pays/{pays_id}/", response_model=schemas.Pays)
async def update_pays(
    pays_id: int, pays: schemas.PaysCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Pays).where(models.Pays.id_pays == pays_id))
    db_pays = result.scalar_one_or_none()

    if not db_pays:
        raise HTTPException(status_code=404, detail=tr("country_not_found"))

    await db.execute(
        update(models.Pays).where(models.Pays.id_pays == pays_id).values(**pays.dict())
    )
    await db.commit()
    return {**pays.dict(), "id_pays": pays_id}


@app.delete("/pays/{pays_id}/")
async def delete_pays(pays_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Pays).where(models.Pays.id_pays == pays_id))
    db_pays = result.scalar_one_or_none()

    if not db_pays:
        raise HTTPException(status_code=404, detail=tr("country_not_found"))

    await db.execute(delete(models.Pays).where(models.Pays.id_pays == pays_id))
    await db.commit()
    return {"message": tr("country_deleted")}


# ========================
# Endpoints POPULATION HIV
# ========================


@app.get("/population_hiv/", response_model=List[schemas.PopulationHIV])
async def get_population_hiv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.PopulationHIV))
    return result.scalars().all()


@app.post("/population_hiv/", response_model=schemas.PopulationHIV)
async def create_population_hiv(
    data: schemas.PopulationHIVCreate, db: AsyncSession = Depends(get_db)
):
    new_data = models.PopulationHIV(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return new_data


# ========================
# Endpoints MORTALITE
# ========================


@app.get("/mortalite/", response_model=List[schemas.Mortalite])
async def get_mortalite(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Mortalite))
    return result.scalars().all()


@app.post("/mortalite/", response_model=schemas.Mortalite)
async def create_mortalite(
    data: schemas.MortaliteCreate, db: AsyncSession = Depends(get_db)
):
    new_data = models.Mortalite(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return new_data


# ========================
# Endpoints TRANSMISSION MÈRE-ENFANT
# ========================


@app.get("/transmission/", response_model=List[schemas.TransmissionMereEnfant])
async def get_transmission(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.TransmissionMereEnfant))
    return result.scalars().all()


@app.post("/transmission/", response_model=schemas.TransmissionMereEnfant)
async def create_transmission(
    data: schemas.TransmissionMereEnfantCreate, db: AsyncSession = Depends(get_db)
):
    new_data = models.TransmissionMereEnfant(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return new_data


# ========================
# Endpoints STATISTIQUES
# ========================


@app.get("/statistiques/", response_model=List[schemas.Statistique])
async def get_statistiques(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Statistique))
    return result.scalars().all()


@app.post("/statistiques/", response_model=schemas.Statistique)
async def create_statistique(
    data: schemas.StatistiqueCreate, db: AsyncSession = Depends(get_db)
):
    new_data = models.Statistique(**data.dict())
    db.add(new_data)
    await db.commit()
    await db.refresh(new_data)
    return new_data


# ========================
# ROOT ENDPOINT
# ========================


@app.get("/")
async def read_root():
    return {"message": tr("root_message"), "langue": LANG}


# ========================
# ENDPOINT prédiction
# ========================

@app.post("/dataframe/")
async def create_dataframe(payload: dict, db: AsyncSession = Depends(get_db)):
    """
    Endpoint pour générer un DataFrame croisé basé sur les choix de l'utilisateur.
    """
    region = payload.get("region")
    pays = payload.get("pays")
    table = payload.get("table")
    target_column = payload.get("target_column")

    if table not in ["mortalite", "population_hiv", "statistique", "traitement", "transmission_mere_enfant", "type_statistique", "type_traitement", "unite"]:
        raise HTTPException(status_code=400, detail=tr("invalid_table"))
    if not region and not pays:
        raise HTTPException(status_code=400, detail=tr("region_or_country_required"))


    query_pays = select(models.Pays)
    if region:
        query_pays = query_pays.filter(models.Pays.region == region)
    if pays:
        query_pays = query_pays.filter(models.Pays.nom_pays == pays)

    result_pays = await db.execute(query_pays)
    data_pays = result_pays.scalars().all()

# Mapping précis entre nom de table (frontend) et classe modèle Python
    MODEL_MAPPING = {
        "mortalite": models.Mortalite,
        "population_hiv": models.PopulationHIV,
        "statistique": models.Statistique,
        "traitement": models.Traitement,
        "transmission_mere_enfant": models.TransmissionMereEnfant,
        "type_statistique": models.TypeStatistique,
        "type_traitement": models.TypeTraitement,
        "unite": models.Unite,
        "pays": models.Pays,
    }
    model = MODEL_MAPPING.get(table)
    if not model:
        raise HTTPException(status_code=400, detail=tr("unknown_table"))
    query_table = select(model)
    result_table = await db.execute(query_table)
    data_table = result_table.scalars().all()

    # Conversion des données en DataFrames
    df_pays = pd.DataFrame([item.__dict__ for item in data_pays])
    df_table = pd.DataFrame([item.__dict__ for item in data_table])

    # Nettoyage des colonnes inutiles
    df_pays = df_pays.drop("_sa_instance_state", axis=1, errors="ignore")
    df_table = df_table.drop("_sa_instance_state", axis=1, errors="ignore")
    print(f"✅ df_pays : { df_pays }")
    print(f"✅ df_table { df_table }")  
    # Fusion des deux DataFrames pour créer un DataFrame croisé
    try:
        dataframe_croise = pd.merge(df_pays, df_table, on="id_pays", how="inner")
        return {"dataframe": dataframe_croise.to_dict()}
    except KeyError:
        raise HTTPException(status_code=400, detail=tr("merge_key_error"))



@app.get("/tables/")
async def get_available_tables():
    """
    Endpoint pour fournir les noms des tables disponibles et leurs relations.
    """
    tables = {
        "pays": ["region"],
        "mortalite": [],
        "population_hiv": [],
        "statistique": [],
        "traitement": [],
        "transmission_mere_enfant": [],
    }
    return {"tables": tables}

@app.get("/columns/{table_name}")
async def get_columns(table_name: str):
    """
    Endpoint pour récupérer la liste des colonnes disponibles dans une table donnée.
    """
    TABLE_MAPPING = {
        "mortalite": models.Mortalite,
        "population_hiv": models.PopulationHIV,
        "statistique": models.Statistique,
        "traitement": models.Traitement,
        "transmission_mere_enfant": models.TransmissionMereEnfant
        # Ajoute ici d'autres tables et leurs modèles
    }

    # Vérifie si la table existe
    model = TABLE_MAPPING.get(table_name)
    if not model:
        raise HTTPException(status_code=404, detail=tr("table_not_found", table=table_name))

    # Récupère les colonnes du modèle
    columns = [column.key for column in model.__table__.columns]
    return {"columns": columns}

@app.post("/train_model/")
async def train_model_endpoint(payload: dict):
    """
    Endpoint pour entraîner le modèle avec les données fournies.
    """
    dataframe_dict = payload.get("dataframe")
    target_column = payload.get("target_column")
    if not dataframe_dict:
        raise HTTPException(status_code=400, detail=tr("missing_dataframe"))

    # Convertir le dictionnaire en DataFrame
    df = pd.DataFrame.from_dict(dataframe_dict)
    print(tr("avant_separation", shape=df.shape))

    # Préparer X et y
    X = df.drop(columns=[target_column, "region", "nom_pays", "sous_region", "id_unite"], errors="ignore")
    y = df[target_column]

    X = preprocess_features(X)
    X, y = prepare_data_generic(df, target_column=target_column)

    if y is None:
        raise HTTPException(status_code=400, detail=tr("target_required"))

    model = create_voting_regressor()
    trained_model = train_voting_regressor(model, X, y)
    joblib.dump(trained_model, "voting_regressor.pkl")

    # Prédictions sur tout X
    predictions = trained_model.predict(X)
    # Labels pour l'axe X (exemple : années si dispo, sinon index)
    labels = list(df["annee"]) if "annee" in df.columns else list(range(len(predictions)))

    return {
        "prediction": list(predictions),
        "labels": labels,
        "message": tr("model_trained")
    }

# ========================
# RUN SERVER
# ========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8084, reload=True)


#========================= 
# END POINTS US - GESTION SCALABILITE
#=========================

from fastapi import Query
from sqlalchemy.orm import selectinload

@app.get("/us/mortalite/")
async def get_us_mortalite(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    year: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Mortalite).options(selectinload(models.Mortalite.pays))
    if year:
        query = query.where(models.Mortalite.annee == year)
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    data = result.scalars().all()
    return [
        {
            "id": m.id,
            "id_pays": m.id_pays,
            "nom_pays": m.pays.nom_pays if m.pays else None,  # <-- Ajout ici
            "annee": m.annee,
            "valeur": m.valeur,
            "id_unite": m.id_unite
        }
        for m in data
    ]

from sqlalchemy import func

@app.get("/us/mortalite/count/")
async def count_us_mortalite(
    year: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(func.count(models.Mortalite.id))
    if year:
        query = query.where(models.Mortalite.annee == year)
    result = await db.execute(query)
    count = result.scalar()
    return {"count": count}