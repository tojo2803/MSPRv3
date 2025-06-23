# =============================================================================
# Script : etl_table_type_statistique.py
# Description : 
# Ce script crée la table de référence des types de statistiques.
# 
# EXTRACTION :
# - Source : Données en dur (pas de source externe)
# - Données : Liste des types de statistiques utilisées
# 
# TRANSFORMATION :
# - Attribution d'identifiants uniques
# - Structure : id_type_statistique, type_statistique
# 
# CHARGEMENT :
# - Fichier : type_statistique_clean.csv
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
    EXTRACTION : Création des données des types de statistiques
    Returns:
        DataFrame: DataFrame des types de statistiques ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de l'extraction...")
        
        # Définition des types de statistiques
        types_statistiques = [
            {'id_type_statistique': 1, 'type_statistique': 'taux de prévalence'},
            {'id_type_statistique': 2, 'type_statistique': 'taux de mortalité'},
            {'id_type_statistique': 3, 'type_statistique': 'taux de transmission mère-enfant'},
            {'id_type_statistique': 4, 'type_statistique': 'taux de couverture traitement'},
            {'id_type_statistique': 5, 'type_statistique': 'taux de nouvelles infections'}
        ]
        
        # Création du DataFrame
        type_statistique_df = pd.DataFrame(types_statistiques)
        
        if type_statistique_df.empty:
            raise ValueError("Erreur lors de la création du DataFrame des types de statistiques")
            
        logging.info("✅ Extraction réussie")
        return type_statistique_df
        
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
        df (DataFrame): DataFrame des types de statistiques
    Returns:
        DataFrame: Données transformées ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de la transformation...")
        
        # Vérification des colonnes requises
        required_columns = ['id_type_statistique', 'type_statistique']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Colonnes manquantes dans le DataFrame")
            
        # Vérification des types de données
        if not df['id_type_statistique'].dtype.kind in 'ui':  # unsigned integer
            df['id_type_statistique'] = df['id_type_statistique'].astype(int)
        if not df['type_statistique'].dtype == 'object':  # string
            df['type_statistique'] = df['type_statistique'].astype(str)
            
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
        
        output_file = Path('../DatasetClean/type_statistique_clean.csv')
        
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
            
        logging.info(f"✅ Chargement réussi - {len(df)} types de statistiques enregistrés")
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
        logging.info("🚀 Début du processus ETL pour type_statistique")
        
        # EXTRACTION
        type_statistique_df = extract_data()
        if type_statistique_df is None:
            raise Exception("Échec de l'extraction des données")
            
        # TRANSFORMATION
        transformed_df = transform_data(type_statistique_df)
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