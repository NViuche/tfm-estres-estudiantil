-- Vista vw_fuentes: metadatos de cada dataset para la página «9 Fuentes» del informe.
-- Une dim_dataset (fuente y número de columnas) con dim_mapeo_estres (variable nativa de estrés y
-- criterio con el que se lleva al nivel común Bajo / Moderado / Alto). Una fila por dataset.
-- La misma vista existe en MySQL (local_xampp/sql/vw_fuentes_mysql.sql).
-- Se ejecuta después de 02_vistas.sql.

CREATE OR REPLACE VIEW tfm.vw_fuentes AS
SELECT d.id_dataset,
       d.fuente,
       d.n_columnas,
       m.variable_nativa,
       m.criterio
FROM tfm.dim_dataset d
LEFT JOIN tfm.dim_mapeo_estres m ON m.id_dataset = d.id_dataset;

COMMENT ON VIEW tfm.vw_fuentes IS 'Fuente, columnas y criterio de mapeo del estrés de cada dataset (página 9 Fuentes)';
