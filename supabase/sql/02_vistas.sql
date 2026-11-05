-- =====================================================================
-- Vistas que consume el Power BI (mismos nombres y columnas que en MySQL)
-- =====================================================================
CREATE VIEW tfm.vw_dim_dataset AS
SELECT d.id_dataset, d.codigo, d.nombre AS dataset, b.id_bloque, b.nombre AS bloque,
       d.calidad, d.uso_modelado, d.n_filas
FROM tfm.dim_dataset d JOIN tfm.dim_bloque b ON b.id_bloque = d.id_bloque;

CREATE VIEW tfm.vw_dim_genero AS
SELECT id_genero, codigo, nombre FROM tfm.dim_genero;

CREATE VIEW tfm.vw_dim_nivel_educativo AS
SELECT id_nivel_educativo, nivel FROM tfm.dim_nivel_educativo;

CREATE VIEW tfm.vw_dim_nivel_estres AS
SELECT id_nivel_estres, nivel, descripcion FROM tfm.dim_nivel_estres;

CREATE VIEW tfm.vw_dim_rango_edad AS
SELECT id_rango_edad, rango, edad_min, edad_max FROM tfm.dim_rango_edad;

CREATE VIEW tfm.vw_hechos_estres AS
SELECT id_registro, tabla_origen, id_dataset, id_genero, id_rango_edad,
       id_nivel_educativo, id_nivel_estres, objetivo_nativo
FROM tfm.hechos_estres;

-- Resultados de la última ejecución del modelado (notebook 09)
CREATE VIEW tfm.vw_modelo_resultados AS
SELECT r.id_resultado_modelo, r.id_dataset, ds.bloque, ds.dataset, ds.calidad, ds.uso_modelado,
       r.modelo, r.protocolo, r.n_registros, r.accuracy, r.f1, r.auc, r.auc_desv, r.brecha_acc,
       r.es_mejor_modelo, r.target, r.lectura_capa_armonizada, r.alerta, r.fecha_ejecucion
FROM tfm.dwh_modelo_resultados r
JOIN tfm.vw_dim_dataset ds ON ds.id_dataset = r.id_dataset
WHERE r.fecha_ejecucion = (SELECT max(fecha_ejecucion) FROM tfm.dwh_modelo_resultados);
