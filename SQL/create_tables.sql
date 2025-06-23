-- =============================================================================
-- Script : create_tables.sql
-- Description : 
-- Ce script crée toutes les tables nécessaires dans la base de données :
-- - Tables de référence (pays, unités, types)
-- - Tables de données (population_hiv, mortalité, transmission, traitements)
-- - Tables de statistiques
-- Il définit également toutes les contraintes et relations entre les tables.
-- =============================================================================

-- Création des tables de référence
CREATE TABLE IF NOT EXISTS pays (
    id_pays SERIAL PRIMARY KEY,
    nom_pays VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    sous_region VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS unite (
    id_unite SERIAL PRIMARY KEY,
    nom_unite VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS type_statistique (
    id_type_statistique SERIAL PRIMARY KEY,
    nom_type_statistique VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS type_traitement (
    id_type_traitement SERIAL PRIMARY KEY,
    nom_type_traitement VARCHAR(100) NOT NULL
);

-- Création des tables principales
CREATE TABLE IF NOT EXISTS population_hiv (
    id SERIAL PRIMARY KEY,
    id_pays INTEGER REFERENCES pays(id_pays),
    annee INTEGER,
    valeur INTEGER,
    id_unite INTEGER REFERENCES unite(id_unite),
    UNIQUE(id_pays, annee)
);

CREATE TABLE IF NOT EXISTS mortalite (
    id SERIAL PRIMARY KEY,
    id_pays INTEGER REFERENCES pays(id_pays),
    annee INTEGER,
    valeur INTEGER,
    id_unite INTEGER REFERENCES unite(id_unite),
    UNIQUE(id_pays, annee)
);

CREATE TABLE IF NOT EXISTS transmission_mere_enfant (
    id SERIAL PRIMARY KEY,
    id_pays INTEGER REFERENCES pays(id_pays),
    besoin_arv_min INTEGER,
    besoin_arv_median INTEGER,
    besoin_arv_max INTEGER,
    pourcentage_recu_min INTEGER,
    pourcentage_recu_median INTEGER,
    pourcentage_recu_max INTEGER,
    id_unite INTEGER REFERENCES unite(id_unite),
    UNIQUE(id_pays)
);

CREATE TABLE IF NOT EXISTS traitement (
    id SERIAL PRIMARY KEY,
    id_pays INTEGER REFERENCES pays(id_pays),
    valeur INTEGER,
    id_unite INTEGER REFERENCES unite(id_unite),
    id_type_traitement INTEGER REFERENCES type_traitement(id_type_traitement),
    UNIQUE(id_pays, id_type_traitement)
);

CREATE TABLE IF NOT EXISTS statistique (
    id SERIAL PRIMARY KEY,
    id_pays INTEGER REFERENCES pays(id_pays),
    annee INTEGER,
    valeur INTEGER,
    id_unite INTEGER REFERENCES unite(id_unite),
    id_type_statistique INTEGER REFERENCES type_statistique(id_type_statistique),
    UNIQUE(id_pays, annee, id_type_statistique)
); 