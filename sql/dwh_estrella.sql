-- ###########################################################################
-- #  PASO 4 de 6  |  ENTREGA 2 - DATAWAREHOUSE EN ESTRELLA
-- #  Crea las 8 tablas dwh_* (INCLUIDA dwh_kpi_catalogo) con sus llaves foraneas, vacias.
-- #  Diagrama : dwh_estrella_ERD.png
-- #  Siguiente: PASO 5: notebook 08_etl_transformaciones_kpis_v4.ipynb
-- #  OPCIONAL: si no lo ejecutas, el notebook del paso 5 crea estas mismas tablas por si solo.
-- ###########################################################################

-- DISENO: cada tabla de hechos guarda SOLO claves foraneas hacia las dimensiones
-- conformes (dim_genero, dim_rango_edad, dim_nivel_educativo, dim_nivel_estres,
-- dim_dataset, dim_bloque, dim_subreddit) mas sus medidas. Ninguna repite texto de
-- las dimensiones. Es el esquema en estrella: hecho central (dwh_hechos_estres_unificado)
-- y hechos agregados que comparten las mismas dimensiones, de modo que un filtro
-- como "Mujeres de 18-25" funciona en todas las tablas a la vez.

USE tfm_estres_estudiantil_2;

SET FOREIGN_KEY_CHECKS = 0;
DROP VIEW  IF EXISTS vw_modelo_resultados;
DROP TABLE IF EXISTS dwh_modelo_resultados, dwh_kpi_resultados, dwh_kpi_catalogo,
                     dwh_brecha_tratamiento, dwh_dass_severidad, dwh_nlp_senales,
                     dwh_agg_prevalencia, dwh_hechos_estres_unificado;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- T1  HECHO CENTRAL  (grano: 1 registro de las 9 fuentes con senal real)
-- ============================================================================
CREATE TABLE dwh_hechos_estres_unificado (
  id_hecho            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset          TINYINT UNSIGNED NOT NULL,
  id_genero           TINYINT UNSIGNED NOT NULL,
  id_rango_edad       TINYINT UNSIGNED NOT NULL,
  id_nivel_educativo  TINYINT UNSIGNED NOT NULL,
  id_nivel_estres     TINYINT UNSIGNED NOT NULL,
  demografia_completa BOOLEAN NOT NULL COMMENT '1 si genero y edad son reportados',
  PRIMARY KEY (id_hecho),
  CONSTRAINT fk_t1_dataset FOREIGN KEY (id_dataset)         REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_t1_genero  FOREIGN KEY (id_genero)          REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_t1_edad    FOREIGN KEY (id_rango_edad)      REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_t1_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_t1_estres  FOREIGN KEY (id_nivel_estres)    REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- T2  HECHO AGREGADO  (grano: bloque x genero x rango de edad)
-- ============================================================================
CREATE TABLE dwh_agg_prevalencia (
  id_agg            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_bloque         TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL,
  id_rango_edad     TINYINT UNSIGNED NOT NULL,
  n_total           INT UNSIGNED NOT NULL,
  n_estres_alto     INT UNSIGNED NOT NULL,
  n_estres_moderado INT UNSIGNED NOT NULL,
  n_estres_bajo     INT UNSIGNED NOT NULL,
  pct_estres_alto   DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (id_agg),
  CONSTRAINT fk_t2_bloque FOREIGN KEY (id_bloque)     REFERENCES dim_bloque(id_bloque),
  CONSTRAINT fk_t2_genero FOREIGN KEY (id_genero)     REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_t2_edad   FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad)
) ENGINE=InnoDB;

-- ============================================================================
-- T3  HECHO AGREGADO NLP  (grano: subreddit x nivel de estres)
-- ============================================================================
CREATE TABLE dwh_nlp_senales (
  id_senal            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_subreddit        SMALLINT UNSIGNED NOT NULL,
  id_nivel_estres     TINYINT UNSIGNED NOT NULL,
  n_posts             INT UNSIGNED NOT NULL,
  sentimiento_medio   DECIMAL(7,4) NOT NULL,
  liwc_ansiedad_medio DECIMAL(7,4) NOT NULL,
  liwc_emo_neg_medio  DECIMAL(7,4) NOT NULL,
  liwc_emo_pos_medio  DECIMAL(7,4) NOT NULL,
  longitud_media_palabras DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (id_senal),
  CONSTRAINT fk_t3_subreddit FOREIGN KEY (id_subreddit)    REFERENCES dim_subreddit(id_subreddit),
  CONSTRAINT fk_t3_estres    FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- T4  HECHO AGREGADO DASS  (grano: genero x rango de edad x nivel educativo)
-- ============================================================================
CREATE TABLE dwh_dass_severidad (
  id_dass_sev        INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_genero          TINYINT UNSIGNED NOT NULL,
  id_rango_edad      TINYINT UNSIGNED NOT NULL,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL,
  n_respondentes     INT UNSIGNED NOT NULL,
  depresion_media    DECIMAL(6,2) NOT NULL,
  ansiedad_media     DECIMAL(6,2) NOT NULL,
  estres_medio       DECIMAL(6,2) NOT NULL,
  pct_estres_severo  DECIMAL(5,2) NOT NULL COMMENT '% con estres >= 40 (baremo DASS)',
  PRIMARY KEY (id_dass_sev),
  CONSTRAINT fk_t4_genero FOREIGN KEY (id_genero)          REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_t4_edad   FOREIGN KEY (id_rango_edad)      REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_t4_edu    FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo)
) ENGINE=InnoDB;

-- ============================================================================
-- T5  TABLA DE CONTINGENCIA  (grano: estres creciente x antecedentes familiares)
-- ============================================================================
CREATE TABLE dwh_brecha_tratamiento (
  id_brecha               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_nivel_estres         TINYINT UNSIGNED NOT NULL COMMENT 'Estres creciente: No=Bajo, Maybe=Moderado, Yes=Alto',
  antecedentes_familiares ENUM('Yes','No') NOT NULL COMMENT 'Dimension degenerada',
  n_total                 INT UNSIGNED NOT NULL,
  n_con_tratamiento       INT UNSIGNED NOT NULL,
  pct_tratamiento         DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (id_brecha),
  CONSTRAINT fk_t5_estres FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- KPIs: catalogo (definicion) + historico de resultados (1 fila por KPI y ejecucion)
-- ============================================================================
CREATE TABLE dwh_kpi_catalogo (
  id_kpi         TINYINT UNSIGNED NOT NULL,
  codigo         VARCHAR(30)  NOT NULL UNIQUE,
  nombre         VARCHAR(120) NOT NULL,
  descripcion    VARCHAR(400) NOT NULL,
  unidad         VARCHAR(20)  NOT NULL,
  fuente_calculo VARCHAR(60)  NOT NULL,
  PRIMARY KEY (id_kpi)
) ENGINE=InnoDB;

INSERT INTO dwh_kpi_catalogo VALUES
 (1,'KPI_ESTRES_ALTO','Tasa de estres Alto global',
    'Porcentaje de registros en nivel de estres Alto sobre el total de las 9 fuentes con senal real.','%','dwh_hechos_estres_unificado'),
 (2,'KPI_BRECHA_GENERO','Brecha de genero en ansiedad (DASS)',
    'Diferencia entre la ansiedad media de mujeres y hombres en la escala DASS-42 (18-25 anos).','puntos','b4_dass_respondente'),
 (3,'KPI_RIESGO_CRITICO','Indice de riesgo critico',
    'Porcentaje de estudiantes con pensamientos suicidas que ademas presentan depresion.','%','b3_depression_student'),
 (4,'KPI_TASA_TRATAMIENTO','Tasa de busqueda de tratamiento',
    'Porcentaje de estudiantes que han buscado tratamiento psicologico.','%','dwh_brecha_tratamiento'),
 (5,'KPI_DISCRIMINANTE_LIWC','Poder discriminante LIWC',
    'Ratio entre la densidad media de palabras de ansiedad (LIWC) de la clase estres y la de no-estres en Dreaddit.','ratio','b3_dreaddit_post'),
 (6,'KPI_COBERTURA_DEMO','Cobertura demografica',
    'Porcentaje de registros con genero y edad reportados sobre el total unificado.','%','dwh_hechos_estres_unificado');

CREATE TABLE dwh_kpi_resultados (
  id_resultado    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_kpi          TINYINT UNSIGNED NOT NULL,
  codigo          VARCHAR(30)   NOT NULL,
  valor           DECIMAL(12,4) NOT NULL,
  detalle         VARCHAR(255)  NULL,
  fecha_ejecucion DATETIME      NOT NULL,
  PRIMARY KEY (id_resultado),
  CONSTRAINT fk_kpires_catalogo FOREIGN KEY (id_kpi) REFERENCES dwh_kpi_catalogo(id_kpi),
  INDEX idx_kpires_fecha (fecha_ejecucion)
) ENGINE=InnoDB;

-- ============================================================================
-- OBJETIVO 2: resultados de modelado (grano: dataset x modelo x ejecucion)
-- Comparte con la estrella la dimension dim_dataset (via id_dataset).
-- ============================================================================
CREATE TABLE dwh_modelo_resultados (
  id_resultado_modelo INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset          TINYINT UNSIGNED NOT NULL COMMENT 'Dreaddit (train+test) se registra con id 8',
  tarea_modelado      VARCHAR(30)  NOT NULL,
  modelo              VARCHAR(60)  NOT NULL,
  protocolo           VARCHAR(25)  NOT NULL,
  n_registros         INT UNSIGNED NOT NULL,
  accuracy            DECIMAL(6,4) NOT NULL,
  f1                  DECIMAL(6,4) NOT NULL,
  auc                 DECIMAL(6,4) NOT NULL,
  auc_desv            DECIMAL(6,4) NULL COMMENT 'Solo en validacion cruzada',
  brecha_acc          DECIMAL(7,4) NOT NULL COMMENT 'Accuracy train - test (sobreajuste)',
  es_mejor_modelo     BOOLEAN NOT NULL,
  target              VARCHAR(80)  NOT NULL,
  lectura_capa_armonizada VARCHAR(160) NOT NULL,
  alerta              VARCHAR(160) NULL,
  fecha_ejecucion     DATETIME NOT NULL,
  PRIMARY KEY (id_resultado_modelo),
  CONSTRAINT fk_modres_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  INDEX idx_modres_ejecucion (fecha_ejecucion)
) ENGINE=InnoDB;

-- Vista de consumo: resultados de la ULTIMA ejecucion con la dimension dataset incorporada
CREATE OR REPLACE VIEW vw_modelo_resultados AS
SELECT r.id_resultado_modelo, r.id_dataset, ds.bloque, ds.dataset, ds.calidad, ds.uso_modelado,
       r.modelo, r.protocolo, r.n_registros, r.accuracy, r.f1, r.auc, r.auc_desv, r.brecha_acc,
       r.es_mejor_modelo, r.target, r.lectura_capa_armonizada, r.alerta, r.fecha_ejecucion
FROM dwh_modelo_resultados r
JOIN vw_dim_dataset ds ON ds.id_dataset = r.id_dataset
WHERE r.fecha_ejecucion = (SELECT MAX(fecha_ejecucion) FROM dwh_modelo_resultados);

-- Comprobacion: debe listar 8 tablas dwh_* y la vista
-- SHOW FULL TABLES LIKE 'dwh_%';
