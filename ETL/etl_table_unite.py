# =============================================================================
# Script : etl_table_unite.py
# Description : 
# Ce script crée la table de référence des unités de mesure.
# 
# EXTRACTION :
# - Source : Données en dur (pas de source externe)
# - Données : Liste des unités de mesure utilisées
# 
# TRANSFORMATION :
# - Attribution d'identifiants uniques
# - Structure : id_unite, unite
# 
# CHARGEMENT :
# - Fichier : unite_clean.csv
# - Format : CSV (séparateur: ',', encodage: UTF-8)
# =============================================================================

import pandas as pd
import sys
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../ETL/etl.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# ---------------------- 🟢 EXTRACTION (Extract) ----------------------
def extract_data():
    """
    EXTRACTION : Création des données des unités
    Returns:
        DataFrame: DataFrame des unités ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de l'extraction...")
        
        # Définition des unités de mesure
        unites = [
            {'id_unite': 1, 'unite': 'nombre de personnes'},
            {'id_unite': 2, 'unite': 'pourcentage'},
            {'id_unite': 3, 'unite': 'ratio'},
            {'id_unite': 4, 'unite': 'année'}
        ]
        
        # Création du DataFrame
        unite_df = pd.DataFrame(unites)
        
        if unite_df.empty:
            raise ValueError("Erreur lors de la création du DataFrame des unités")
            
        logging.info("✅ Extraction réussie")
        return unite_df
        
    except ValueError as e:
        logging.error(f"❌ Erreur de données : {str(e)}")
        return None
    except Exception as e:
        logging.error(f"❌ Erreur inattendue lors de l'extraction : {str(e)}")
        return None

# ---------------------- 🟡 TRANSFORMATION (Transform) ----------------------
def transform_data(df):
    """
    TRANSFORMATION : Vérification et nettoyage des données
    Args:
        df (DataFrame): DataFrame des unités
    Returns:
        DataFrame: Données transformées ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de la transformation...")
        
        # Vérification des colonnes requises
        required_columns = ['id_unite', 'unite']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Colonnes manquantes dans le DataFrame")
            
        # Vérification des types de données
        if not df['id_unite'].dtype.kind in 'ui':  # unsigned integer
            df['id_unite'] = df['id_unite'].astype(int)
        if not df['unite'].dtype == 'object':  # string
            df['unite'] = df['unite'].astype(str)
            
        # Vérification des doublons
        if df.duplicated().any():
            raise ValueError("Des doublons ont été détectés")
            
        logging.info("✅ Transformation réussie")
        return df
        
    except ValueError as e:
        logging.error(f"❌ Erreur de transformation : {str(e)}")
        return None
    except Exception as e:
        logging.error(f"❌ Erreur inattendue lors de la transformation : {str(e)}")
        return None

# ---------------------- 🔵 CHARGEMENT (Load) ----------------------
def load_data(df):
    """
    CHARGEMENT : Sauvegarde des données transformées
    Args:
        df (DataFrame): Données à sauvegarder
    Returns:
        bool: True si succès, False sinon
    """
    try:
        logging.info("🔄 Début du chargement...")
        
        output_file = Path('../DatasetClean/unite_clean.csv')
        
        # 1. Préparation du dossier de sortie
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise IOError(f"Impossible de créer le dossier de sortie : {str(e)}")
            
        # 2. Sauvegarde des données
        try:
            df.to_csv(output_file, index=False)
        except Exception as e:
            raise IOError(f"Erreur lors de la sauvegarde : {str(e)}")
            
        # 3. Vérification
        if not output_file.exists():
            raise FileNotFoundError("Le fichier n'a pas été créé")
            
        # 4. Validation des données sauvegardées
        try:
            verification_df = pd.read_csv(output_file)
            if verification_df.empty or len(verification_df) != len(df):
                raise ValueError("Les données sauvegardées sont incomplètes")
        except Exception as e:
            raise ValueError(f"Erreur lors de la vérification : {str(e)}")
            
        logging.info(f"✅ Chargement réussi - {len(df)} unités enregistrées")
        return True
        
    except (IOError, FileNotFoundError, ValueError) as e:
        logging.error(f"❌ Erreur de chargement : {str(e)}")
        return False
    except Exception as e:
        logging.error(f"❌ Erreur inattendue lors du chargement : {str(e)}")
        return False

# ---------------------- 🚀 EXECUTION ----------------------
def main():
    """
    Fonction principale : Orchestration du processus ETL
    """
    try:
        logging.info("🚀 Début du processus ETL pour unite")
        
        # EXTRACTION
        unite_df = extract_data()
        if unite_df is None:
            raise Exception("Échec de l'extraction des données")
            
        # TRANSFORMATION
        transformed_df = transform_data(unite_df)
        if transformed_df is None:
            raise Exception("Échec de la transformation des données")
            
        # CHARGEMENT
        if not load_data(transformed_df):
            raise Exception("Échec du chargement des données")
            
        logging.info("✅ Processus ETL terminé avec succès")
        
    except Exception as e:
        logging.error(f"❌ Erreur dans le processus ETL : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()