from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import os


LANG = os.getenv("LANG", "fr")

TRANSLATIONS = {
    "df_shape": {
        "fr": "Taille du DataFrame avant préparation : {shape}",
        "en": "DataFrame size before preparation: {shape}",
        "de": "DataFrame-Größe vor der Vorbereitung: {shape}"
    },
    "df_columns": {
        "fr": "Colonnes présentes : {columns}",
        "en": "Columns present: {columns}",
        "de": "Vorhandene Spalten: {columns}"
    },
    "target_found": {
        "fr": "Colonne cible : {target}",
        "en": "Target column: {target}",
        "de": "Zielspalte: {target}"
    },
    "current_index": {
        "fr": "Index actuel : {index}",
        "en": "Current index: {index}",
        "de": "Aktueller Index: {index}"
    },
    "target_missing": {
        "fr": "Colonne cible non spécifiée ou absente. Utilisation des seules caractéristiques.",
        "en": "Target column not specified or missing. Using features only.",
        "de": "Zielspalte nicht angegeben oder fehlt. Nur Merkmale werden verwendet."
    },
    "features_shape": {
        "fr": "Données préparées. Dimensions des caractéristiques : {shape}",
        "en": "Data prepared. Features shape: {shape}",
        "de": "Daten vorbereitet. Merkmalsdimensionen: {shape}"
    },
    "target_count": {
        "fr": "Colonne cible détectée. Nombre de cibles : {count}",
        "en": "Target column detected. Number of targets: {count}",
        "de": "Zielspalte erkannt. Anzahl der Ziele: {count}"
    },
    "before_preprocessing": {
        "fr": "Avant prétraitement, types des colonnes :\n{dtypes}",
        "en": "Before preprocessing, column types:\n{dtypes}",
        "de": "Vorverarbeitung, Spaltentypen:\n{dtypes}"
    },
    "categorical_detected": {
        "fr": "Colonnes catégoriques détectées : {cols}",
        "en": "Categorical columns detected: {cols}",
        "de": "Kategorische Spalten erkannt: {cols}"
    },
    "no_categorical": {
        "fr": "Aucune colonne catégorique détectée.",
        "en": "No categorical columns detected.",
        "de": "Keine kategorischen Spalten erkannt."
    },
    "non_numeric_detected": {
        "fr": "Colonnes non numériques détectées après encodage : {cols}",
        "en": "Non-numeric columns detected after encoding: {cols}",
        "de": "Nicht-numerische Spalten nach Codierung erkannt: {cols}"
    },
    "after_preprocessing": {
        "fr": "Après prétraitement, dimensions de X : {shape}",
        "en": "After preprocessing, X shape: {shape}",
        "de": "Nach der Vorverarbeitung, X-Dimension: {shape}"
    },
    "train_size": {
        "fr": "Taille de X_train : {xtrain}, Taille de y_train : {ytrain}",
        "en": "X_train size: {xtrain}, y_train size: {ytrain}",
        "de": "X_train Größe: {xtrain}, y_train Größe: {ytrain}"
    },
    "test_size": {
        "fr": "Taille de X_test : {xtest}, Taille de y_test : {ytest}",
        "en": "X_test size: {xtest}, y_test size: {ytest}",
        "de": "X_test Größe: {xtest}, y_test Größe: {ytest}"
    },
    "training": {
        "fr": "Entraînement du modèle...",
        "en": "Training the model...",
        "de": "Modell wird trainiert..."
    },
    "trained": {
        "fr": "Modèle entraîné avec succès.",
        "en": "Model trained successfully.",
        "de": "Modell erfolgreich trainiert."
    },
    "evaluating": {
        "fr": "Évaluation du modèle...",
        "en": "Evaluating the model...",
        "de": "Modellbewertung..."
    },
    "results": {
        "fr": "Résultats :",
        "en": "Results:",
        "de": "Ergebnisse:"
    },
    "rmse": {
        "fr": "Root Mean Squared Error (RMSE) : {rmse:.2f}",
        "en": "Root Mean Squared Error (RMSE): {rmse:.2f}",
        "de": "Root Mean Squared Error (RMSE): {rmse:.2f}"
    },
    "r2": {
        "fr": "R² score : {r2:.2f}",
        "en": "R² score: {r2:.2f}",
        "de": "R² Wert: {r2:.2f}"
    },
    "plot_title": {
    "fr": "Comparaison des valeurs réelles et prédictions",
    "en": "Comparison of actual values and predictions",
    "de": "Vergleich von Ist-Werten und Vorhersagen"
    }
}

def tr(key, **kwargs):
    msg = TRANSLATIONS.get(key, {}).get(LANG, TRANSLATIONS.get(key, {}).get("fr", key))
    return msg.format(**kwargs) if kwargs else msg

def prepare_data_generic(df, target_column=None):
    """
    Prépare les données pour l'entraînement d'un modèle de machine learning.
    - Sépare les caractéristiques (`features`) et la cible (`target`).
    - Si `target_column` n'est pas fourni, essaye de l'inférer ou retourne uniquement les features.
    Args:
        df (pd.DataFrame): Le DataFrame à traiter.
        target_column (str): La colonne cible (si elle est connue).

    Returns:
        X (pd.DataFrame): Les caractéristiques.
        y (pd.Series ou None): La cible (ou None si non spécifiée).
    """
    print(tr("df_shape", shape=df.shape))
    print(tr("df_columns", columns=df.columns.tolist()))

    
    if target_column and target_column in df.columns:
        # Séparer la cible et les caractéristiques
        X = df.drop(columns=[target_column, "region", "nom_pays", "sous_region","id_unite"])
        y = df[target_column]
        print(tr("target_found", target=target_column))
        print(tr("current_index", index=df.index))
        df.set_index('annee', inplace=True)
        print(tr("current_index", index=df.index))

    else:
        # Si la colonne cible n'est pas spécifiée ou introuvable, on ne retourne que les features
        print(tr("target_missing"))
        X = df
        y = None

    print(tr("features_shape", shape=X.shape))
    if y is not None:
        print(tr("target_count", count=len(y)))
    return X, y

def create_voting_regressor():
    """
    Crée un modèle combiné VotingRegressor.
    """
    model = VotingRegressor([
        ('rf', RandomForestRegressor()),
        ('knn', KNeighborsRegressor(1)),
        ('svr', SVR())
    ])
    return model

def save_training_data(new_data, file_path="training_data.csv"):
    try:
        existing_data = pd.read_csv(file_path)
        combined_data = pd.concat([existing_data, pd.DataFrame(new_data)]).drop_duplicates()
    except FileNotFoundError:
        combined_data = pd.DataFrame(new_data)

    combined_data.to_csv(file_path, index=False)

def load_training_data(file_path="training_data.csv"):
    return pd.read_csv(file_path)


def preprocess_features(X):
    """
    Prépare les caractéristiques (features) pour l'entraînement du modèle.
    - Supprime ou encode les colonnes non numériques.
    """
    print(tr("before_preprocessing", dtypes=X.dtypes))

    # Identifier les colonnes catégoriques
    categorical_cols = X.select_dtypes(include=['object', 'string']).columns

    if len(categorical_cols) > 0:
        print(tr("categorical_detected", cols=categorical_cols.tolist()))

        # Encoder les colonnes catégoriques avec OneHotEncoder
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  
        encoded = pd.DataFrame(
            encoder.fit_transform(X[categorical_cols]),
            columns=encoder.get_feature_names_out(categorical_cols)
        )

        # Supprimer les colonnes catégoriques et ajouter les colonnes encodées
        X = X.drop(columns=categorical_cols).reset_index(drop=True)
        X = pd.concat([X, encoded], axis=1)
    else:
        print(tr("no_categorical"))

    # Vérifier les colonnes non numériques restantes et les supprimer
    non_numeric_cols = X.select_dtypes(exclude=['number']).columns
    if len(non_numeric_cols) > 0:
        print(tr("non_numeric_detected", cols=non_numeric_cols.tolist()))
        X = X.drop(columns=non_numeric_cols)

    print(tr("after_preprocessing", shape=X.shape))
    return X

def train_voting_regressor(model, X, y):
    """
    Entraîne un modèle VotingRegressor avec les caractéristiques (X) et la cible (y).
    Évalue le modèle après l'entraînement.
    """

    # Séparer les données en ensemble d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(tr("train_size", xtrain=X_train.shape, ytrain=y_train.shape))
    print(tr("test_size", xtest=X_test.shape, ytest=y_test.shape))

    # Entraîner le modèle
    print(tr("training"))
    model.fit(X_train, y_train)
    print(tr("trained"))

    # Faire des prédictions
    print(tr("evaluating"))
    y_pred = model.predict(X_test)

    # Calculer les métriques
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(tr("results"))
    print(tr("rmse", rmse=rmse))
    print(tr("r2", r2=r2))

    


    plt.figure(figsize=(10, 6))
    plt.plot(y_test.values, label="Valeurs réelles", color="blue", marker="o")
    plt.plot(y_pred, label="Prédictions", color="orange", linestyle="--", marker="x")
    plt.xlabel("Index")
    plt.ylabel("Valeurs")
    plt.title(tr("plot_title"))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return model

def save_training_data(new_data, file_path="training_data.csv"):
    try:
        existing_data = pd.read_csv(file_path)
        combined_data = pd.concat([existing_data, pd.DataFrame(new_data)]).drop_duplicates()
    except FileNotFoundError:
        combined_data = pd.DataFrame(new_data)

    combined_data.to_csv(file_path, index=False)

def load_training_data(file_path="training_data.csv"):
    return pd.read_csv(file_path)

