-- ============================================================================
-- CAPA DE CONSUMO PARA POWER BI - ESQUEMA EN ESTRELLA PURO
-- TFM: Analisis multidimensional del estres estudiantil
-- ============================================================================
-- El modelo fisico v2 (modelo_datos_mysql_v2.sql) es una CONSTELACION con una
-- rama copo de nieve (hechos -> dim_dataset -> dim_bloque). Esta capa de
-- VISTAS lo aplana a ESTRELLA PURA, que es el patron recomendado por
-- Microsoft para Power BI:
--   * 1 tabla de hechos unificada (vw_hechos_estres) con las claves conformes
--   * 5 dimensiones planas directamente conectadas a los hechos
--   * cero cadenas dimension->dimension (dim_bloque queda desnormalizada
--     DENTRO de vw_dim_dataset)
-- En Power BI: conectar SOLO estas vistas (no las tablas fisicas) y marcar
-- las relaciones 1:* desde cada dimension hacia vw_hechos_estres.
-- Ejecutar DESPUES de modelo_datos_mysql_v2.sql sobre la misma base.
-- VERSION DEFINITIVA: base tfm_estres_estudiantil_2 y COLLATE utf8mb4_unicode_ci
-- en las 22 expresiones de texto del UNION (evita el error #1271 de MariaDB).
-- ============================================================================

USE tfm_estres_estudiantil_2;

-- ============================================================================
-- DIMENSIONES DE LA ESTRELLA (planas)
-- ============================================================================

-- Dimension dataset DESNORMALIZADA: absorbe dim_bloque (elimina el copo)
CREATE OR REPLACE VIEW vw_dim_dataset AS
SELECT d.id_dataset,
       d.codigo,
       d.nombre           AS dataset,
       b.id_bloque,
       b.nombre           AS bloque,          -- <- desnormalizado
       d.calidad,
       d.uso_modelado,
       d.n_filas
FROM dim_dataset d
JOIN dim_bloque  b ON b.id_bloque = d.id_bloque;

-- Las conformes ya son planas: se exponen tal cual con nombre de consumo
CREATE OR REPLACE VIEW vw_dim_genero          AS SELECT * FROM dim_genero;
CREATE OR REPLACE VIEW vw_dim_rango_edad      AS SELECT * FROM dim_rango_edad;
CREATE OR REPLACE VIEW vw_dim_nivel_educativo AS SELECT * FROM dim_nivel_educativo;
CREATE OR REPLACE VIEW vw_dim_nivel_estres    AS SELECT * FROM dim_nivel_estres;

-- ============================================================================
-- TABLA DE HECHOS UNIFICADA (grano: 1 fila = 1 registro de cualquier fuente)
-- ============================================================================
-- Une los 12 hechos por sus claves conformes. La variable objetivo nativa se
-- expone como texto (objetivo_nativo) para tooltip/detalle; la metrica
-- comparable entre fuentes es id_nivel_estres (constructo unificado).

CREATE OR REPLACE VIEW vw_hechos_estres AS
SELECT id_encuesta_estres        AS id_registro, 'b1_academic_stress' COLLATE utf8mb4_unicode_ci AS tabla_origen,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(indice_estres AS CHAR) COLLATE utf8mb4_unicode_ci AS objetivo_nativo
FROM b1_academic_stress
UNION ALL
SELECT id_encuesta_ansiedad, 'b1_anxiety' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(gad_total AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b1_anxiety
UNION ALL
SELECT id_encuesta_salud_mental, 'b1_mental_health_survey' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(depresion AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b1_mental_health_survey
UNION ALL
SELECT CAST(SUBSTRING(id_estudiante, 2) AS UNSIGNED), 'b1_student_habits' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(salud_mental AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b1_student_habits
UNION ALL
SELECT id_usuario_red, 'b2_social_media_sleep' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       nivel_estres_nativo COLLATE utf8mb4_unicode_ci
FROM b2_social_media_sleep
UNION ALL
SELECT id_respuesta_smmh, 'b2_smmh' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(se_siente_deprimido AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b2_smmh
UNION ALL
SELECT id_registro_estilo_vida, 'b2_lifestyle' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       nivel_estres_nativo COLLATE utf8mb4_unicode_ci
FROM b2_lifestyle
UNION ALL
SELECT id_fragmento_post, 'b3_dreaddit_post' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(etiqueta_estres AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b3_dreaddit_post
UNION ALL
SELECT id_perfil_estudiante, 'b3_depression_student' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       depresion COLLATE utf8mb4_unicode_ci
FROM b3_depression_student
UNION ALL
SELECT id_respondente_dass, 'b4_dass_respondente' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       CAST(score_estres AS CHAR) COLLATE utf8mb4_unicode_ci
FROM b4_dass_respondente
UNION ALL
SELECT id_caso_salud_mental, 'b4_mental_health' COLLATE utf8mb4_unicode_ci,
       id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres,
       estres_creciente COLLATE utf8mb4_unicode_ci
FROM b4_mental_health;

-- NOTA: b4_dass_item (detalle 42 filas/respondente) NO entra en la estrella:
-- es grano de item, no de persona. Si un dashboard lo necesita, cargarlo como
-- hecho separado con su propia relacion a vw_hechos... o mejor, dejarlo en
-- MySQL para analisis puntual via consulta.

-- ============================================================================
-- VERIFICACION: el filtro global del tutor sobre la estrella (1 sola consulta)
-- ============================================================================
-- SELECT ds.bloque, ds.dataset, COUNT(*) AS casos
-- FROM vw_hechos_estres h
-- JOIN vw_dim_dataset      ds ON ds.id_dataset      = h.id_dataset
-- JOIN vw_dim_genero       g  ON g.id_genero        = h.id_genero
-- JOIN vw_dim_rango_edad   r  ON r.id_rango_edad    = h.id_rango_edad
-- JOIN vw_dim_nivel_estres e  ON e.id_nivel_estres  = h.id_nivel_estres
-- WHERE g.codigo='F' AND r.rango='18-25' AND e.nivel='Alto'
-- GROUP BY ds.bloque, ds.dataset ORDER BY casos DESC;

-- ============================================================================
-- GUIA DE CONEXION EN POWER BI (resumen)
-- ============================================================================
-- 1. Obtener datos > MySQL > seleccionar SOLO las 6 vistas vw_*
-- 2. Vista de modelo: relaciones 1:* (una a varias), filtro en una direccion:
--      vw_dim_dataset[id_dataset]                 1 -> * vw_hechos_estres[id_dataset]
--      vw_dim_genero[id_genero]                   1 -> * vw_hechos_estres[id_genero]
--      vw_dim_rango_edad[id_rango_edad]           1 -> * vw_hechos_estres[id_rango_edad]
--      vw_dim_nivel_educativo[id_nivel_educativo] 1 -> * vw_hechos_estres[id_nivel_educativo]
--      vw_dim_nivel_estres[id_nivel_estres]       1 -> * vw_hechos_estres[id_nivel_estres]
-- 3. Ocultar en vista de informe las columnas id_* de los hechos (usar las
--    columnas descriptivas de las dimensiones en los segmentadores).
-- 4. Medida base sugerida:  Registros = COUNTROWS(vw_hechos_estres)
--    y % Estres Alto = DIVIDE(CALCULATE([Registros],
--        vw_dim_nivel_estres[nivel]="Alto"), [Registros])


-- ============================================================================
-- CONSULTAS DE VERIFICACION
-- ============================================================================
-- V1: 12 filas, una por dataset (id_dataset 1..12)
-- SELECT ds.id_dataset, ds.dataset, ds.bloque, ds.uso_modelado, COUNT(*) AS filas
-- FROM vw_hechos_estres h JOIN vw_dim_dataset ds ON ds.id_dataset = h.id_dataset
-- GROUP BY ds.id_dataset, ds.dataset, ds.bloque, ds.uso_modelado ORDER BY ds.id_dataset;
-- V2: total 334.318 y 319.318 en fuentes incluidas
-- SELECT COUNT(*) AS total,
--        SUM(ds.uso_modelado = 'incluido') AS en_fuentes_incluidas
-- FROM vw_hechos_estres h JOIN vw_dim_dataset ds ON ds.id_dataset = h.id_dataset;
