-- =============================================================================
-- Script : import_data.sql
-- Description : Import des données depuis les fichiers CSV
-- =============================================================================

-- Nettoyage des tables existantes
TRUNCATE TABLE traitement, transmission_mere_enfant, statistique, population_hiv, mortalite, pays, type_traitement, type_statistique, unite CASCADE;

-- Désactiver temporairement les contraintes pour l'import
SET session_replication_role = 'replica';

-- Import des données de référence
\COPY pays(id_pays, nom_pays, region) FROM '../DatasetClean/pays_clean.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');
\COPY type_traitement(id_type_traitement, nom_type_traitement) FROM '../DatasetClean/type_traitement_clean.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');
\COPY type_statistique(id_type_statistique, nom_type_statistique) FROM '../DatasetClean/type_statistique_clean.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');
\COPY unite(id_unite, nom_unite) FROM '../DatasetClean/unite_clean.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

-- Import des données principales
\COPY mortalite(id, id_pays, annee, valeur) FROM '../DatasetClean/table_mortalite.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

\COPY population_hiv(id, id_pays, annee, valeur) FROM '../DatasetClean/table_population_hiv.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

\COPY statistique(id, id_pays, annee, valeur, id_unite, id_type_statistique) FROM '../DatasetClean/table_statistique.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

-- Import des données transmission_mere_enfant
CREATE TEMP TABLE temp_transmission (
    id_transmission INTEGER,
    id_pays INTEGER,
    besoin_arv_min INTEGER,
    besoin_arv_median INTEGER,
    besoin_arv_max INTEGER,
    pourcentage_recu_min INTEGER,
    pourcentage_recu_median INTEGER,
    pourcentage_recu_max INTEGER
);

\COPY temp_transmission FROM '../DatasetClean/table_transmission_mere_enfant.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

INSERT INTO transmission_mere_enfant (id, id_pays, valeur, id_unite)
SELECT id_transmission, id_pays, pourcentage_recu_median, 2
FROM temp_transmission;

DROP TABLE temp_transmission;

-- Import des données de traitement (conversion de 'couverture' en 'valeur')
CREATE TEMP TABLE temp_traitement (
    id INTEGER,
    id_pays INTEGER,
    id_type_traitement INTEGER,
    couverture INTEGER
);

\COPY temp_traitement FROM '../DatasetClean/table_traitement.csv' WITH (FORMAT CSV, HEADER, DELIMITER ',', ENCODING 'UTF8');

INSERT INTO traitement (id, id_pays, id_type_traitement, valeur)
SELECT id, id_pays, id_type_traitement, couverture
FROM temp_traitement;

DROP TABLE temp_traitement;

-- Réactiver les contraintes
SET session_replication_role = 'origin';

-- Vérification des données importées
SELECT 'pays' as table_name, COUNT(*) as count FROM pays
UNION ALL
SELECT 'mortalite', COUNT(*) FROM mortalite
UNION ALL
SELECT 'population_hiv', COUNT(*) FROM population_hiv
UNION ALL
SELECT 'statistique', COUNT(*) FROM statistique
UNION ALL
SELECT 'transmission_mere_enfant', COUNT(*) FROM transmission_mere_enfant
UNION ALL
SELECT 'traitement', COUNT(*) FROM traitement
ORDER BY table_name; 