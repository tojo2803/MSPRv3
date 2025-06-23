# =============================================================================
# Script : etl_table_transmission_mere_enfant.py
# Description : 
# Ce script traite les données de transmission du HIV de la mère à l'enfant.
# 
# EXTRACTION :
# - Source : prevention_of_mother_to_child_transmission_by_country_clean.csv
# - Données : Taux de transmission mère-enfant par pays
# - Période : 2018
# 
# TRANSFORMATION :
# - Standardisation des noms de pays (minuscules, sans espaces)
# - Liaison avec la table pays pour obtenir les id_pays
# - Conversion des valeurs en nombres entiers
# - Structure : id_transmission, id_pays, besoin_arv, pourcentage_recu
# 
# CHARGEMENT :
# - Fichier : table_transmission_mere_enfant.csv
# - Format : CSV (séparateur: ',', encodage: UTF-8)
# =============================================================================

import pandas as pd
import numpy as np
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
    EXTRACTION : Lecture des fichiers sources
    Returns:
        tuple: (DataFrame pays, DataFrame prevention) ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de l'extraction...")
        
        # Vérification des fichiers sources
        files_to_check = {
            'pays': Path('../DatasetClean/pays_clean.csv'),
            'prevention': Path('../SourceData/prevention_of_mother_to_child_transmission_by_country_clean.csv')
        }
        
        # Vérifie l'existence de chaque fichier
        for name, file_path in files_to_check.items():
            if not file_path.exists():
                raise FileNotFoundError(f"Fichier {name} introuvable : {file_path}")
        
        # Lecture des données avec vérification
        pays_df = pd.read_csv(files_to_check['pays'])
        if pays_df.empty:
            raise ValueError("Le fichier pays est vide")
            
        prevention_df = pd.read_csv(files_to_check['prevention'])
        if prevention_df.empty:
            raise ValueError("Le fichier prévention est vide")
            
        logging.info("✅ Extraction réussie")
        return pays_df, prevention_df
        
    except FileNotFoundError as e:
        logging.error(f"❌ Erreur d'accès fichier : {str(e)}")
        return None, None
    except ValueError as e:
        logging.error(f"❌ Erreur de données : {str(e)}")
        return None, None
    except Exception as e:
        logging.error(f"❌ Erreur inattendue lors de l'extraction : {str(e)}")
        return None, None

# ---------------------- 🟡 TRANSFORMATION (Transform) ----------------------
def transform_data(pays_df, prevention_df):
    """
    TRANSFORMATION : Nettoyage et structuration des données
    Args:
        pays_df (DataFrame): DataFrame des pays
        prevention_df (DataFrame): DataFrame des données de prévention
    Returns:
        DataFrame: Données transformées ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de la transformation...")
        
        # 1. Nettoyage des colonnes
        try:
            prevention_df.columns = prevention_df.columns.str.strip()
            required_columns = ['Country', 'Needing antiretrovirals_min', 'Needing antiretrovirals_median', 
                              'Needing antiretrovirals_max', 'Percentage Recieved_min', 'Percentage Recieved_median', 
                              'Percentage Recieved_max']
            if not all(col in prevention_df.columns for col in required_columns):
                raise ValueError("Colonnes manquantes dans le fichier source")
        except Exception as e:
            raise ValueError(f"Erreur lors du nettoyage des colonnes : {str(e)}")
            
        # 2. Standardisation des pays
        try:
            prevention_df['Country'] = prevention_df['Country'].str.strip().str.lower()
        except Exception as e:
            raise ValueError(f"Erreur lors de la standardisation des pays : {str(e)}")
            
        # 3. Fusion avec la table pays
        try:
            merged_df = pd.merge(prevention_df, pays_df, 
                               left_on='Country', 
                               right_on='pays', 
                               how='inner')
            if merged_df.empty:
                raise ValueError("Aucune correspondance trouvée après la fusion")
        except Exception as e:
            raise ValueError(f"Erreur lors de la fusion : {str(e)}")
            
        # 4. Conversion des données numériques
        try:
            numeric_columns = ['Needing antiretrovirals_min', 'Needing antiretrovirals_median', 
                             'Needing antiretrovirals_max', 'Percentage Recieved_min', 
                             'Percentage Recieved_median', 'Percentage Recieved_max']
            for col in numeric_columns:
                merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
        except Exception as e:
            raise ValueError(f"Erreur lors de la conversion numérique : {str(e)}")
            
        # 5. Construction du DataFrame final
        transmission_data = []
        error_count = 0
        for _, row in merged_df.iterrows():
            try:
                if pd.notna(row['Needing antiretrovirals_median']) and pd.notna(row['id_pays']):
                    transmission_data.append({
                        'id_transmission': len(transmission_data) + 1,
                        'id_pays': int(row['id_pays']),
                        'besoin_arv_min': int(round(float(row['Needing antiretrovirals_min']))),
                        'besoin_arv_median': int(round(float(row['Needing antiretrovirals_median']))),
                        'besoin_arv_max': int(round(float(row['Needing antiretrovirals_max']))),
                        'pourcentage_recu_min': int(round(float(row['Percentage Recieved_min']))) if pd.notna(row['Percentage Recieved_min']) else 0,
                        'pourcentage_recu_median': int(round(float(row['Percentage Recieved_median']))) if pd.notna(row['Percentage Recieved_median']) else 0,
                        'pourcentage_recu_max': int(round(float(row['Percentage Recieved_max']))) if pd.notna(row['Percentage Recieved_max']) else 0
                    })
            except ValueError as e:
                error_count += 1
                logging.warning(f"⚠️ Ligne ignorée - Pays: {row['Country']}")
                continue
                
        if error_count > 0:
            logging.warning(f"⚠️ {error_count} lignes ignorées pendant la transformation")
            
        result_df = pd.DataFrame(transmission_data)
        if result_df.empty:
            raise ValueError("Aucune donnée valide après transformation")
            
        logging.info("✅ Transformation réussie")
        return result_df
        
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
        
        output_file = Path('../DatasetClean/table_transmission_mere_enfant.csv')
        
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
            
        logging.info(f"✅ Chargement réussi - {len(df)} lignes sauvegardées")
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
        logging.info("🚀 Début du processus ETL pour transmission_mere_enfant")
        
        # EXTRACTION
        pays_df, prevention_df = extract_data()
        if pays_df is None or prevention_df is None:
            raise Exception("Échec de l'extraction des données")
            
        # TRANSFORMATION
        transformed_df = transform_data(pays_df, prevention_df)
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