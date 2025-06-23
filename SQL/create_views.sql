-- =============================================================================
-- Script : create_views.sql
-- Description : 
-- Ce script crée une vue unique et complète pour PowerBI qui regroupe 
-- toutes les données nécessaires à l'analyse.
-- =============================================================================

-- Suppression des anciennes vues
DROP VIEW IF EXISTS vue_powerbi_complete CASCADE;
DROP VIEW IF EXISTS vue_indicateurs_pays CASCADE;
DROP VIEW IF EXISTS vue_evolution_temporelle CASCADE;

-- Création de la vue globale unique
CREATE OR REPLACE VIEW vue_globale AS
WITH donnees_base AS (
    SELECT DISTINCT ON (p.id_pays, COALESCE(ph.annee, m.annee, s.annee))
        -- Informations pays
        p.id_pays,
        p.nom_pays,
        p.region,
        p.sous_region,
        
        -- Année de référence
        COALESCE(ph.annee, m.annee, s.annee) as annee,
        
        -- Données HIV
        ph.valeur as population_hiv,
        u_ph.nom_unite as unite_population_hiv,
        
        -- Données mortalité
        m.valeur as mortalite,
        u_m.nom_unite as unite_mortalite,
        
        -- Transmission mère-enfant
        tme.valeur as transmission_mere_enfant,
        u_tme.nom_unite as unite_transmission,
        
        -- Traitements
        tr_adulte.valeur as traitement_adulte,
        tr_enfant.valeur as traitement_enfant,
        u_tr.nom_unite as unite_traitement,
        
        -- Statistiques
        s.valeur as valeur_statistique,
        ts.nom_type_statistique as type_statistique,
        u_s.nom_unite as unite_statistique
    FROM pays p
    LEFT JOIN population_hiv ph ON p.id_pays = ph.id_pays
    LEFT JOIN unite u_ph ON ph.id_unite = u_ph.id_unite
    LEFT JOIN mortalite m ON p.id_pays = m.id_pays AND m.annee = ph.annee
    LEFT JOIN unite u_m ON m.id_unite = u_m.id_unite
    LEFT JOIN transmission_mere_enfant tme ON p.id_pays = tme.id_pays
    LEFT JOIN unite u_tme ON tme.id_unite = u_tme.id_unite
    LEFT JOIN traitement tr_adulte ON p.id_pays = tr_adulte.id_pays AND tr_adulte.id_type_traitement = 1
    LEFT JOIN traitement tr_enfant ON p.id_pays = tr_enfant.id_pays AND tr_enfant.id_type_traitement = 2
    LEFT JOIN unite u_tr ON tr_adulte.id_unite = u_tr.id_unite
    LEFT JOIN statistique s ON p.id_pays = s.id_pays AND s.annee = COALESCE(ph.annee, m.annee)
    LEFT JOIN type_statistique ts ON s.id_type_statistique = ts.id_type_statistique
    LEFT JOIN unite u_s ON s.id_unite = u_s.id_unite
    WHERE COALESCE(ph.annee, m.annee, s.annee) IS NOT NULL
)
SELECT 
    d.*,
    -- Calculs d'évolution
    population_hiv - LAG(population_hiv) OVER (PARTITION BY id_pays ORDER BY annee) as evolution_population_hiv,
    mortalite - LAG(mortalite) OVER (PARTITION BY id_pays ORDER BY annee) as evolution_mortalite,
    
    -- Moyennes régionales
    AVG(population_hiv) OVER (PARTITION BY region, annee) as moyenne_population_hiv_region,
    AVG(mortalite) OVER (PARTITION BY region, annee) as moyenne_mortalite_region,
    AVG(transmission_mere_enfant) OVER (PARTITION BY region) as moyenne_transmission_region,
    AVG(traitement_adulte) OVER (PARTITION BY region) as moyenne_traitement_adulte_region,
    AVG(traitement_enfant) OVER (PARTITION BY region) as moyenne_traitement_enfant_region,
    
    -- Rangs et percentiles
    RANK() OVER (PARTITION BY annee ORDER BY population_hiv DESC) as rang_population_hiv,
    RANK() OVER (PARTITION BY annee ORDER BY mortalite DESC) as rang_mortalite,
    PERCENT_RANK() OVER (PARTITION BY annee ORDER BY population_hiv) as percentile_population_hiv,
    PERCENT_RANK() OVER (PARTITION BY annee ORDER BY mortalite) as percentile_mortalite
FROM donnees_base d
ORDER BY id_pays, annee;

-- Vue des indicateurs par pays (sans dimension temporelle)
CREATE OR REPLACE VIEW vue_indicateurs_pays AS
SELECT 
    p.id_pays,
    p.nom_pays,
    p.region,
    tme.valeur as taux_transmission_mere_enfant,
    tr_adulte.valeur as taux_traitement_adulte,
    tr_enfant.valeur as taux_traitement_enfant
FROM pays p
LEFT JOIN transmission_mere_enfant tme ON p.id_pays = tme.id_pays
LEFT JOIN traitement tr_adulte ON p.id_pays = tr_adulte.id_pays AND tr_adulte.id_type_traitement = 1
LEFT JOIN traitement tr_enfant ON p.id_pays = tr_enfant.id_pays AND tr_enfant.id_type_traitement = 2;

-- Vue globale par pays et année
CREATE OR REPLACE VIEW vue_pays_annee AS
SELECT 
    p.id_pays,
    p.nom_pays,
    p.region,
    m.annee,
    m.valeur as mortalite,
    ph.population_hiv,
    tme.taux_transmission as transmission_mere_enfant
FROM pays p
LEFT JOIN mortalite m ON p.id_pays = m.id_pays
LEFT JOIN population_hiv ph ON p.id_pays = ph.id_pays AND ph.annee = m.annee
LEFT JOIN transmission_mere_enfant tme ON p.id_pays = tme.id_pays;

-- Vue statistiques détaillées
CREATE OR REPLACE VIEW vue_statistiques_detaillees AS
SELECT 
    p.id_pays,
    p.nom_pays,
    p.region,
    s.annee,
    ts.libelle as type_statistique,
    s.valeur,
    u.libelle as unite
FROM pays p
JOIN statistique s ON p.id_pays = s.id_pays
JOIN type_statistique ts ON s.id_type_statistique = ts.id_type_statistique
JOIN unite u ON s.id_unite = u.id_unite;

-- Vue évolution temporelle
CREATE OR REPLACE VIEW vue_evolution_temporelle AS
SELECT 
    p.region,
    m.annee,
    COUNT(DISTINCT p.id_pays) as nombre_pays,
    SUM(m.valeur) as total_mortalite,
    SUM(ph.population_hiv) as total_population_hiv,
    AVG(tme.taux_transmission) as moyenne_transmission
FROM pays p
LEFT JOIN mortalite m ON p.id_pays = m.id_pays
LEFT JOIN population_hiv ph ON p.id_pays = ph.id_pays AND ph.annee = m.annee
LEFT JOIN transmission_mere_enfant tme ON p.id_pays = tme.id_pays
GROUP BY p.region, m.annee
ORDER BY p.region, m.annee; 