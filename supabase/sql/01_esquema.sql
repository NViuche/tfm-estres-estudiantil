-- =====================================================================
-- TFM Estrés estudiantil · Esquema PostgreSQL en Supabase (esquema tfm)
-- Traducción de MySQL (tfm_estres_estudiantil_2): capa estrella + DWH
-- + resultados del modelado. Las tablas originales b1_* … b4_* no se
-- migran; los hechos de vw_hechos_estres se guardan en hechos_estres.
-- Tipos: tinyint unsigned → smallint · int unsigned → integer ·
--        enum → text con CHECK · datetime → timestamp
-- =====================================================================
DROP SCHEMA IF EXISTS tfm CASCADE;
CREATE SCHEMA tfm;
COMMENT ON SCHEMA tfm IS 'TFM Análisis multidimensional del estrés estudiantil (UNIE / INESDI)';

-- ---------------------------------------------------------------- dimensiones
CREATE TABLE tfm.dim_bloque (
  id_bloque    smallint PRIMARY KEY,
  nombre       varchar(60)  NOT NULL,
  descripcion  varchar(255) NOT NULL
);

CREATE TABLE tfm.dim_dataset (
  id_dataset    smallint PRIMARY KEY,
  id_bloque     smallint NOT NULL REFERENCES tfm.dim_bloque,
  codigo        varchar(30)  NOT NULL UNIQUE,
  nombre        varchar(120) NOT NULL,
  fuente        varchar(255) NOT NULL,
  n_filas       integer  NOT NULL,
  n_columnas    smallint NOT NULL,
  calidad       text NOT NULL CHECK (calidad IN ('inferencial', 'tecnico')),
  uso_modelado  text NOT NULL CHECK (uso_modelado IN ('incluido', 'excluido'))
);

CREATE TABLE tfm.dim_genero (
  id_genero  smallint PRIMARY KEY,
  codigo     char(2)     NOT NULL UNIQUE,
  nombre     varchar(20) NOT NULL
);

CREATE TABLE tfm.dim_mapeo_estres (
  id_mapeo         smallint PRIMARY KEY,
  id_dataset       smallint NOT NULL REFERENCES tfm.dim_dataset,
  variable_nativa  varchar(60)  NOT NULL,
  criterio         varchar(255) NOT NULL
);

CREATE TABLE tfm.dim_nivel_educativo (
  id_nivel_educativo  smallint PRIMARY KEY,
  nivel               varchar(30) NOT NULL UNIQUE
);

CREATE TABLE tfm.dim_nivel_estres (
  id_nivel_estres  smallint PRIMARY KEY,
  nivel            varchar(12)  NOT NULL UNIQUE,
  descripcion      varchar(120) NOT NULL
);

CREATE TABLE tfm.dim_rango_edad (
  id_rango_edad  smallint PRIMARY KEY,
  rango          varchar(15) NOT NULL UNIQUE,
  edad_min       smallint,
  edad_max       smallint
);

CREATE TABLE tfm.dim_subreddit (
  id_subreddit  integer PRIMARY KEY,
  nombre        varchar(50) NOT NULL UNIQUE
);

-- ---------------------------------------------------------------- hechos de la capa estrella
-- Materialización de vw_hechos_estres de MySQL (unión de los 12 datasets, incluidos los sintéticos)
CREATE TABLE tfm.hechos_estres (
  id_registro         integer  NOT NULL,
  tabla_origen        varchar(40) NOT NULL,
  id_dataset          smallint NOT NULL REFERENCES tfm.dim_dataset,
  id_genero           smallint NOT NULL REFERENCES tfm.dim_genero,
  id_rango_edad       smallint NOT NULL REFERENCES tfm.dim_rango_edad,
  id_nivel_educativo  smallint NOT NULL REFERENCES tfm.dim_nivel_educativo,
  id_nivel_estres     smallint NOT NULL REFERENCES tfm.dim_nivel_estres,
  objetivo_nativo     varchar(40),
  PRIMARY KEY (tabla_origen, id_registro)
);
CREATE INDEX ON tfm.hechos_estres (id_dataset);
CREATE INDEX ON tfm.hechos_estres (id_nivel_estres);

-- ---------------------------------------------------------------- DWH
CREATE TABLE tfm.dwh_hechos_estres_unificado (
  id_hecho             integer PRIMARY KEY,
  id_dataset           smallint NOT NULL REFERENCES tfm.dim_dataset,
  id_genero            smallint NOT NULL REFERENCES tfm.dim_genero,
  id_rango_edad        smallint NOT NULL REFERENCES tfm.dim_rango_edad,
  id_nivel_educativo   smallint NOT NULL REFERENCES tfm.dim_nivel_educativo,
  id_nivel_estres      smallint NOT NULL REFERENCES tfm.dim_nivel_estres,
  demografia_completa  smallint NOT NULL CHECK (demografia_completa IN (0, 1))
);
COMMENT ON COLUMN tfm.dwh_hechos_estres_unificado.demografia_completa IS '1 si género y edad son reportados';

CREATE TABLE tfm.dwh_agg_prevalencia (
  id_agg             integer PRIMARY KEY,
  id_bloque          smallint NOT NULL REFERENCES tfm.dim_bloque,
  id_genero          smallint NOT NULL REFERENCES tfm.dim_genero,
  id_rango_edad      smallint NOT NULL REFERENCES tfm.dim_rango_edad,
  n_total            integer NOT NULL,
  n_estres_alto      integer NOT NULL,
  n_estres_moderado  integer NOT NULL,
  n_estres_bajo      integer NOT NULL,
  pct_estres_alto    numeric(5,2) NOT NULL
);

CREATE TABLE tfm.dwh_brecha_tratamiento (
  id_brecha                integer PRIMARY KEY,
  id_nivel_estres          smallint NOT NULL REFERENCES tfm.dim_nivel_estres,
  -- En MySQL era enum('Yes','No'); en Supabase se traduce a «Sí» / «No» (03_correcciones_datos.sql)
  antecedentes_familiares  text NOT NULL CHECK (antecedentes_familiares IN ('Yes', 'Sí', 'No')),
  n_total                  integer NOT NULL,
  n_con_tratamiento        integer NOT NULL,
  pct_tratamiento          numeric(5,2) NOT NULL
);

CREATE TABLE tfm.dwh_dass_severidad (
  id_dass_sev         integer PRIMARY KEY,
  id_genero           smallint NOT NULL REFERENCES tfm.dim_genero,
  id_rango_edad       smallint NOT NULL REFERENCES tfm.dim_rango_edad,
  id_nivel_educativo  smallint NOT NULL REFERENCES tfm.dim_nivel_educativo,
  n_respondentes      integer NOT NULL,
  depresion_media     numeric(6,2) NOT NULL,
  ansiedad_media      numeric(6,2) NOT NULL,
  estres_medio        numeric(6,2) NOT NULL,
  pct_estres_severo   numeric(5,2) NOT NULL
);

CREATE TABLE tfm.dwh_kpi_catalogo (
  id_kpi          smallint PRIMARY KEY,
  codigo          varchar(30)  NOT NULL UNIQUE,
  nombre          varchar(120) NOT NULL,
  descripcion     varchar(400) NOT NULL,
  unidad          varchar(20)  NOT NULL,
  fuente_calculo  varchar(60)  NOT NULL
);

CREATE TABLE tfm.dwh_kpi_resultados (
  id_resultado     integer PRIMARY KEY,
  id_kpi           smallint NOT NULL REFERENCES tfm.dwh_kpi_catalogo,
  codigo           varchar(30) NOT NULL,
  valor            numeric(12,4) NOT NULL,
  detalle          varchar(255),
  fecha_ejecucion  timestamp NOT NULL
);
CREATE INDEX ON tfm.dwh_kpi_resultados (fecha_ejecucion);

CREATE TABLE tfm.dwh_modelo_resultados (
  id_resultado_modelo      integer PRIMARY KEY,
  id_dataset               smallint NOT NULL REFERENCES tfm.dim_dataset,
  tarea_modelado           varchar(30) NOT NULL,
  modelo                   varchar(60) NOT NULL,
  protocolo                varchar(25) NOT NULL,
  n_registros              integer NOT NULL,
  accuracy                 numeric(6,4) NOT NULL,
  f1                       numeric(6,4) NOT NULL,
  auc                      numeric(6,4) NOT NULL,
  auc_desv                 numeric(6,4),
  brecha_acc               numeric(7,4) NOT NULL,
  es_mejor_modelo          smallint NOT NULL CHECK (es_mejor_modelo IN (0, 1)),
  target                   varchar(80)  NOT NULL,
  lectura_capa_armonizada  varchar(160) NOT NULL,
  alerta                   varchar(160),
  fecha_ejecucion          timestamp NOT NULL
);

CREATE TABLE tfm.dwh_nlp_senales (
  id_senal                 integer PRIMARY KEY,
  id_subreddit             integer  NOT NULL REFERENCES tfm.dim_subreddit,
  id_nivel_estres          smallint NOT NULL REFERENCES tfm.dim_nivel_estres,
  n_posts                  integer NOT NULL,
  sentimiento_medio        numeric(7,4) NOT NULL,
  liwc_ansiedad_medio      numeric(7,4) NOT NULL,
  liwc_emo_neg_medio       numeric(7,4) NOT NULL,
  liwc_emo_pos_medio       numeric(7,4) NOT NULL,
  longitud_media_palabras  numeric(7,2) NOT NULL
);
