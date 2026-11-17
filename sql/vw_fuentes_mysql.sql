-- Vista vw_fuentes (MySQL): metadatos de cada dataset para la página «9 Fuentes» del informe.
-- Une dim_dataset (fuente y número de columnas) con dim_mapeo_estres (variable nativa de estrés y
-- criterio con el que se lleva al nivel común Bajo / Moderado / Alto). Una fila por dataset.
-- Equivale a supabase/sql/06_vista_fuentes.sql. Se exporta a CSV con scripts/exportar_mysql_cli.py.

CREATE OR REPLACE VIEW vw_fuentes AS
SELECT d.id_dataset,
       d.fuente,
       d.n_columnas,
       m.variable_nativa,
       m.criterio
FROM dim_dataset d
LEFT JOIN dim_mapeo_estres m ON m.id_dataset = d.id_dataset;
