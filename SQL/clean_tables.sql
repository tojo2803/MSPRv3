-- =============================================================================
-- Script : clean_tables.sql
-- Description : 
-- Ce script nettoie la base de données en :
-- - Supprimant toutes les tables existantes
-- - Réinitialisant les séquences
-- - Préparant la base pour une nouvelle importation
-- À utiliser avec précaution car il supprime toutes les données !
-- =============================================================================

-- Désactiver temporairement les contraintes de clé étrangère
SET session_replication_role = 'replica';

-- Nettoyage des tables principales
TRUNCATE TABLE statistique CASCADE;
TRUNCATE TABLE traitement CASCADE;
TRUNCATE TABLE transmission_mere_enfant CASCADE;
TRUNCATE TABLE mortalite CASCADE;
TRUNCATE TABLE population_hiv CASCADE;

-- Nettoyage des tables de référence
TRUNCATE TABLE pays CASCADE;
TRUNCATE TABLE unite CASCADE;
TRUNCATE TABLE type_statistique CASCADE;
TRUNCATE TABLE type_traitement CASCADE;

-- Réactiver les contraintes de clé étrangère
SET session_replication_role = 'origin'; 