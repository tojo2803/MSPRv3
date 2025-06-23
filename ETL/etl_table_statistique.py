# =============================================================================
# Script : etl_table_statistique.py
# Description : 
# Ce script traite les données statistiques générales liées au HIV.
# 
# EXTRACTION :
# - Sources : 
#   * no_of_people_living_with_hiv_by_country_clean.csv
#   * no_of_deaths_by_country_clean.csv
#   * prevention_of_mother_to_child_transmission_by_country_clean.csv
# - Données : Statistiques diverses par pays et par année
# - Période : 2000-2018
# 
# TRANSFORMATION :
# - Standardisation des noms de pays (minuscules, sans espaces)
# - Liaison avec la table pays pour obtenir les id_pays
# - Calcul des taux et pourcentages
# - Structure : id_statistique, id_pays, annee, id_type_statistique, valeur, id_unite
# 
# CHARGEMENT :
# - Fichier : table_statistique.csv
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
        tuple: (DataFrame pays, DataFrame population, DataFrame mortalite, DataFrame prevention) 
        ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de l'extraction...")
        
        # Vérification des fichiers sources
        files_to_check = {
            'pays': Path('../DatasetClean/pays_clean.csv'),
            'population': Path('../SourceData/no_of_people_living_with_hiv_by_country_clean.csv'),
            'mortalite': Path('../SourceData/no_of_deaths_by_country_clean.csv'),
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
            
        population_df = pd.read_csv(files_to_check['population'])
        if population_df.empty:
            raise ValueError("Le fichier population est vide")
            
        mortalite_df = pd.read_csv(files_to_check['mortalite'])
        if mortalite_df.empty:
            raise ValueError("Le fichier mortalité est vide")
            
        prevention_df = pd.read_csv(files_to_check['prevention'])
        if prevention_df.empty:
            raise ValueError("Le fichier prévention est vide")
            
        logging.info("✅ Extraction réussie")
        return pays_df, population_df, mortalite_df, prevention_df
        
    except FileNotFoundError as e:
        logging.error(f"❌ Erreur d'accès fichier : {str(e)}")
        return None, None, None, None
    except ValueError as e:
        logging.error(f"❌ Erreur de données : {str(e)}")
        return None, None, None, None
    except Exception as e:
        logging.error(f"❌ Erreur inattendue lors de l'extraction : {str(e)}")
        return None, None, None, None

# ---------------------- 🟡 TRANSFORMATION (Transform) ----------------------
def transform_data(pays_df, population_df, mortalite_df, prevention_df):
    """
    TRANSFORMATION : Nettoyage et structuration des données
    Args:
        pays_df (DataFrame): DataFrame des pays
        population_df (DataFrame): DataFrame des données population
        mortalite_df (DataFrame): DataFrame des données mortalité
        prevention_df (DataFrame): DataFrame des données prévention
    Returns:
        DataFrame: Données transformées ou None en cas d'erreur
    """
    try:
        logging.info("🔄 Début de la transformation...")
        
        # 1. Nettoyage des colonnes
        try:
            population_df.columns = population_df.columns.str.strip()
            mortalite_df.columns = mortalite_df.columns.str.strip()
            prevention_df.columns = prevention_df.columns.str.strip()
            
            # Vérification des colonnes requises
            required_columns_pop = ['Country', 'Year', 'Count_median']
            required_columns_mort = ['Country', 'Year', 'Count_median']
            required_columns_prev = ['Country', 'Percentage Recieved_median']
            
            if not all(col in population_df.columns for col in required_columns_pop):
                raise ValueError("Colonnes manquantes dans le fichier population")
            if not all(col in mortalite_df.columns for col in required_columns_mort):
                raise ValueError("Colonnes manquantes dans le fichier mortalité")
            if not all(col in prevention_df.columns for col in required_columns_prev):
                raise ValueError("Colonnes manquantes dans le fichier prévention")
                
        except Exception as e:
            raise ValueError(f"Erreur lors du nettoyage des colonnes : {str(e)}")
            
        # 2. Standardisation des pays
        try:
            population_df['Country'] = population_df['Country'].str.strip().str.lower()
            mortalite_df['Country'] = mortalite_df['Country'].str.strip().str.lower()
            prevention_df['Country'] = prevention_df['Country'].str.strip().str.lower()
        except Exception as e:
            raise ValueError(f"Erreur lors de la standardisation des pays : {str(e)}")
            
        # 3. Fusion avec la table pays
        try:
            population_df = pd.merge(population_df, pays_df, 
                                   left_on='Country', 
                                   right_on='pays', 
                                   how='inner')
            mortalite_df = pd.merge(mortalite_df, pays_df, 
                                   left_on='Country', 
                                   right_on='pays', 
                                   how='inner')
            prevention_df = pd.merge(prevention_df, pays_df, 
                                   left_on='Country', 
                                   right_on='pays', 
                                   how='inner')
            
            if population_df.empty and mortalite_df.empty and prevention_df.empty:
                raise ValueError("Aucune correspondance trouvée après la fusion")
        except Exception as e:
            raise ValueError(f"Erreur lors de la fusion : {str(e)}")
            
        # 4. Construction du DataFrame final
        statistique_data = []
        error_count = 0
        for _, row in population_df.iterrows():
            try:
                if pd.notna(row['Count_median']) and pd.notna(row['id_pays']):
                    statistique_data.append({
                        'id': len(statistique_data) + 1,
                        'id_pays': int(row['id_pays']),
                        'annee': int(row['Year']),
                        'valeur': int(round(float(row['Count_median']))),
                        'id_unite': 2,  # 2 = pourcentage
                        'id_type_statistique': 1  # 1 = taux de prévalence
                    })
            except ValueError:
                error_count += 1
                continue  # Silencieusement ignorer les erreurs de conversion
        
        for _, row in mortalite_df.iterrows():
            try:
                if pd.notna(row['Count_median']) and pd.notna(row['id_pays']):
                    statistique_data.append({
                        'id': len(statistique_data) + 1,
                        'id_pays': int(row['id_pays']),
                        'annee': int(row['Year']),
                        'valeur': int(round(float(row['Count_median']))),
                        'id_unite': 2,  # 2 = pourcentage
                        'id_type_statistique': 2  # 2 = taux de mortalité
                    })
            except ValueError:
                error_count += 1
                continue  # Silencieusement ignorer les erreurs de conversion
        
        for _, row in prevention_df.iterrows():
            try:
                if pd.notna(row['Percentage Recieved_median']) and pd.notna(row['id_pays']):
                    statistique_data.append({
                        'id': len(statistique_data) + 1,
                        'id_pays': int(row['id_pays']),
                        'annee': 2018,  # Année de référence
                        'valeur': int(round(float(row['Percentage Recieved_median']))),
                        'id_unite': 2,  # 2 = pourcentage
                        'id_type_statistique': 3  # 3 = taux de transmission mère-enfant
                    })
            except ValueError:
                error_count += 1
                continue  # Silencieusement ignorer les erreurs de conversion
                
        if error_count > 0:
            logging.warning(f"⚠️ {error_count} lignes ignorées pendant la transformation")
            
        result_df = pd.DataFrame(statistique_data)
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
        
        output_file = Path('../DatasetClean/table_statistique.csv')
        
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
        logging.info("\nTypes de statistiques inclus :")
        logging.info("1. Taux de prévalence du VIH")
        logging.info("2. Taux de mortalité liée au VIH")
        logging.info("3. Taux de transmission mère-enfant")
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
        logging.info("🚀 Début du processus ETL pour statistique")
        
        # EXTRACTION
        pays_df, population_df, mortalite_df, prevention_df = extract_data()
        if pays_df is None or population_df is None or mortalite_df is None or prevention_df is None:
            raise Exception("Échec de l'extraction des données")
            
        # TRANSFORMATION
        transformed_df = transform_data(pays_df, population_df, mortalite_df, prevention_df)
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