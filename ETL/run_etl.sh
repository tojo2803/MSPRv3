#!/bin/bash

# =============================================================================
# Script : run_etl.sh
# Description : 
# Ce script exécute tous les scripts ETL dans l'ordre logique :
# 1. Tables de référence
# 2. Tables principales
# =============================================================================

echo "🚀 Début du processus ETL global"
echo "==============================="

# Fonction pour exécuter un script Python et vérifier son statut
run_etl_script() {
    echo "⏳ Exécution de $1..."
    python "$1"
    if [ $? -eq 0 ]; then
        echo "✅ $1 terminé avec succès"
        echo "-----------------------------"
    else
        echo "❌ Erreur lors de l'exécution de $1"
        exit 1
    fi
}

echo "📚 1. Tables de référence"
echo "-----------------------------"
run_etl_script "etl_table_unite.py"
run_etl_script "etl_table_type_statistique.py"
run_etl_script "etl_table_type_traitement.py"

echo "📊 2. Tables principales"
echo "-----------------------------"
run_etl_script "etl_table_pays.py"
run_etl_script "etl_table_population_hiv.py"
run_etl_script "etl_table_mortalite.py"
run_etl_script "etl_table_transmission_mere_enfant.py"
run_etl_script "etl_table_traitement.py"
run_etl_script "etl_table_statistique.py"

echo "✨ Processus ETL global terminé avec succès"
echo "===============================" 