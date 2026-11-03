-- ============================================================================
-- ENTREGA 1 - MODELO DE DATOS EN MySQL
-- TFM: Analisis multidimensional del estres estudiantil (BA & IA)
-- ============================================================================
-- Enfoque del modelo:
--   El TFM adopta un ANALISIS EN PARALELO: los datasets NO se integran entre
--   si, por lo que el modelo se organiza como tablas de hechos independientes
--   (una por dataset) agrupadas por bloque analitico, mas tres tablas maestras
--   (dimensiones) que normalizan catalogos repetidos entre tablas:
--     - dim_bloque      : catalogo de los 4 bloques analiticos
--     - dim_dataset     : inventario de los 12 datasets (FK a dim_bloque)
--     - dim_subreddit   : catalogo de subreddits del corpus Dreaddit
--   Las tablas de hechos llevan FK a dim_dataset (linaje del dato) y, en el
--   caso de Dreaddit, FK a dim_subreddit. dreaddit_test ademas define la
--   relacion train/test mediante el campo particion.
--   Los CSV que no traen identificador natural reciben una PK AUTO_INCREMENT.
-- ============================================================================

DROP DATABASE IF EXISTS tfm_estres_estudiantil;
CREATE DATABASE tfm_estres_estudiantil
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tfm_estres_estudiantil;

-- ============================================================================
-- TABLAS MAESTRAS (DIMENSIONES)
-- ============================================================================

CREATE TABLE dim_bloque (
  bloque_id     TINYINT UNSIGNED NOT NULL,
  nombre        VARCHAR(60)  NOT NULL,
  descripcion   VARCHAR(255) NOT NULL,
  PRIMARY KEY (bloque_id)
) ENGINE=InnoDB;

INSERT INTO dim_bloque VALUES
 (1,'Factores internos','Core del estres: estres academico, ansiedad, salud mental, habitos'),
 (2,'Habitos digitales','Factores externos: redes sociales, pantalla, estilo de vida'),
 (3,'Percepcion emocional','IA/NLP: corpus textual Dreaddit y perfil de depresion estudiantil'),
 (4,'Validacion psicologica','Escalas clinicas DASS-42 y encuesta masiva de salud mental');

CREATE TABLE dim_dataset (
  dataset_id    TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  bloque_id     TINYINT UNSIGNED NOT NULL,
  codigo        VARCHAR(30)  NOT NULL UNIQUE,      -- p.ej. 'B1_ANXIETY'
  nombre        VARCHAR(120) NOT NULL,
  fuente        VARCHAR(255) NOT NULL,             -- URL Kaggle/GitHub
  n_filas       INT UNSIGNED NOT NULL,
  n_columnas    SMALLINT UNSIGNED NOT NULL,
  calidad       ENUM('inferencial','tecnico') NOT NULL
                COMMENT 'Resultado de la evaluacion de calidad del Objetivo 1',
  PRIMARY KEY (dataset_id),
  CONSTRAINT fk_dataset_bloque FOREIGN KEY (bloque_id)
    REFERENCES dim_bloque(bloque_id)
) ENGINE=InnoDB;

INSERT INTO dim_dataset (bloque_id,codigo,nombre,fuente,n_filas,n_columnas,calidad) VALUES
 (1,'B1_ACADSTRESS','Academic Stress','kaggle.com/datasets/poushal02/student-academic-stress-real-world-dataset',140,9,'inferencial'),
 (1,'B1_ANXIETY','Student Anxiety GAD-7','kaggle.com/datasets/petalme/student-anxiety-dataset',13464,55,'inferencial'),
 (1,'B1_MHSURVEY','Student Mental Health Survey','kaggle.com/datasets/abdullahashfaqvirk/student-mental-health-survey',87,21,'inferencial'),
 (1,'B1_HABITS','Student Habits vs Performance','github.com/abhi88377/Student-Habits-vs-Academic-Performance',1000,16,'tecnico'),
 (2,'B2_SOCIALMEDIA','Social Media vs Sleep/Stress/Productivity','kaggle.com/datasets/jayjoshi37/social-media-usage-vs-sleep-stress-and-productivity',11000,10,'tecnico'),
 (2,'B2_SMMH','Social Media and Mental Health','kaggle.com/datasets/souvikahmed071/social-media-and-mental-health',481,21,'inferencial'),
 (2,'B2_LIFESTYLE','Mental Health Lifestyle','github.com/datafit17/Mental_Health_Lifestyle',3000,12,'tecnico'),
 (3,'B3_DREADDIT_TR','Dreaddit train','kaggle.com/datasets/payaldhokane/stress-analysis-in-social-media-dataset',2838,116,'inferencial'),
 (3,'B3_DREADDIT_TE','Dreaddit test','kaggle.com/datasets/payaldhokane/stress-analysis-in-social-media-dataset',715,116,'inferencial'),
 (3,'B3_DEPSTUDENT','Depression Student Dataset','github.com/prajwalg26/Student_Mental_Health_Analysis',502,11,'inferencial'),
 (4,'B4_DASS','DASS-42','kaggle.com/datasets/lucasgreenwell/depression-anxiety-stress-scales-responses',39775,172,'inferencial'),
 (4,'B4_MENTALHEALTH','Mental Health Dataset','kaggle.com/code/chanchal24/mental-health-dataset',261328,17,'inferencial');

CREATE TABLE dim_subreddit (
  subreddit_id  SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre        VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (subreddit_id)
) ENGINE=InnoDB;

INSERT INTO dim_subreddit (nombre) VALUES
 ('ptsd'),('relationships'),('anxiety'),('domesticviolence'),('assistance'),
 ('survivorsofabuse'),('homeless'),('almosthomeless'),('stress'),('food_pantry');

-- ============================================================================
-- BLOQUE 1 - FACTORES INTERNOS
-- ============================================================================

CREATE TABLE b1_academic_stress (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  ts_respuesta      VARCHAR(30),
  etapa_academica   VARCHAR(30),
  presion_pares     TINYINT CHECK (presion_pares BETWEEN 1 AND 5),
  presion_hogar     TINYINT CHECK (presion_hogar BETWEEN 1 AND 5),
  entorno_estudio   VARCHAR(60),
  estrategia_afrontamiento VARCHAR(120),
  habitos_nocivos   VARCHAR(30),
  competencia_academica TINYINT CHECK (competencia_academica BETWEEN 1 AND 5),
  indice_estres     TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO'
                    CHECK (indice_estres BETWEEN 1 AND 5),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b1as_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

CREATE TABLE b1_anxiety (
  registro_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id      TINYINT UNSIGNED NOT NULL,
  s_no            INT UNSIGNED COMMENT 'Identificador secuencial del CSV',
  gad1 TINYINT, gad2 TINYINT, gad3 TINYINT, gad4 TINYINT,
  gad5 TINYINT, gad6 TINYINT, gad7 TINYINT,
  gade            VARCHAR(60),
  swl_total       TINYINT,
  spin_total      SMALLINT,
  gad_total       TINYINT COMMENT 'VARIABLE OBJETIVO: GAD-7 (0-21)',
  horas_juego     DECIMAL(6,1),
  genero          VARCHAR(20),
  edad            TINYINT UNSIGNED,
  ocupacion       VARCHAR(60) COMMENT 'Work: filtrar estudiantes',
  nivel_educativo VARCHAR(60),
  pais_residencia CHAR(3),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b1anx_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id),
  INDEX idx_b1anx_ocupacion (ocupacion)
) ENGINE=InnoDB;

CREATE TABLE b1_mental_health_survey (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  genero            VARCHAR(20),
  edad              TINYINT UNSIGNED,
  universidad       VARCHAR(60),
  nivel_estudios    VARCHAR(30),
  carrera           VARCHAR(60),
  anio_academico    VARCHAR(20),
  cgpa_rango        VARCHAR(20) COMMENT 'Texto-rango: recodificar a ordinal',
  satisfaccion_estudios TINYINT CHECK (satisfaccion_estudios BETWEEN 1 AND 5),
  carga_academica   TINYINT CHECK (carga_academica BETWEEN 1 AND 5),
  presion_academica TINYINT CHECK (presion_academica BETWEEN 1 AND 5),
  aislamiento       TINYINT CHECK (aislamiento BETWEEN 1 AND 5),
  inseguridad_futuro TINYINT CHECK (inseguridad_futuro BETWEEN 1 AND 5),
  depresion         TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO'
                    CHECK (depresion BETWEEN 1 AND 5),
  ansiedad          TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO'
                    CHECK (ansiedad BETWEEN 1 AND 5),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b1mhs_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

CREATE TABLE b1_student_habits (
  student_id        VARCHAR(12) NOT NULL COMMENT 'PK natural del CSV (S1000...)',
  dataset_id        TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED,
  genero            VARCHAR(20),
  horas_estudio_dia DECIMAL(4,1),
  horas_redes       DECIMAL(4,1),
  horas_streaming   DECIMAL(4,1),
  trabajo_parcial   ENUM('Yes','No'),
  asistencia_pct    DECIMAL(5,2),
  horas_sueno       DECIMAL(4,1),
  calidad_dieta     VARCHAR(20),
  frecuencia_ejercicio TINYINT,
  educacion_padres  VARCHAR(30) NULL COMMENT '9.1% nulos: imputar por moda',
  calidad_internet  VARCHAR(20),
  salud_mental      TINYINT COMMENT 'Senal sintetica documentada'
                    CHECK (salud_mental BETWEEN 1 AND 10),
  nota_examen       DECIMAL(5,2) CHECK (nota_examen BETWEEN 0 AND 100),
  PRIMARY KEY (student_id),
  CONSTRAINT fk_b1hab_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 2 - HABITOS DIGITALES
-- ============================================================================

CREATE TABLE b2_social_media_sleep (
  user_id           INT UNSIGNED NOT NULL COMMENT 'PK natural del CSV',
  dataset_id        TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED,
  genero            VARCHAR(20),
  plataforma        VARCHAR(30),
  horas_redes       DECIMAL(4,1),
  horas_pantalla    DECIMAL(4,1) CHECK (horas_pantalla BETWEEN 0 AND 24),
  horas_sueno       DECIMAL(4,1) CHECK (horas_sueno BETWEEN 0 AND 24),
  horas_estudio_trabajo DECIMAL(4,1),
  minutos_ejercicio SMALLINT UNSIGNED,
  productividad     DECIMAL(5,2),
  nivel_estres      ENUM('Low','Medium','High') NOT NULL
                    COMMENT 'VARIABLE OBJETIVO',
  PRIMARY KEY (user_id),
  CONSTRAINT fk_b2sm_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

CREATE TABLE b2_smmh (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  ts_respuesta      VARCHAR(30),
  edad              TINYINT UNSIGNED,
  genero            VARCHAR(30),
  estado_relacion   VARCHAR(30),
  ocupacion         VARCHAR(30),
  usa_redes         ENUM('Yes','No'),
  plataformas       VARCHAR(255) COMMENT 'Multi-seleccion: separar en dummies (Obj.2)',
  tiempo_diario     VARCHAR(40),
  uso_sin_proposito TINYINT CHECK (uso_sin_proposito BETWEEN 1 AND 5),
  distraccion_redes TINYINT CHECK (distraccion_redes BETWEEN 1 AND 5),
  inquietud_sin_redes TINYINT CHECK (inquietud_sin_redes BETWEEN 1 AND 5),
  distraccion_facil TINYINT CHECK (distraccion_facil BETWEEN 1 AND 5),
  preocupacion      TINYINT CHECK (preocupacion BETWEEN 1 AND 5),
  dificultad_concentracion TINYINT CHECK (dificultad_concentracion BETWEEN 1 AND 5),
  comparacion_social TINYINT CHECK (comparacion_social BETWEEN 1 AND 5),
  sentimiento_comparacion TINYINT CHECK (sentimiento_comparacion BETWEEN 1 AND 5),
  busqueda_validacion TINYINT CHECK (busqueda_validacion BETWEEN 1 AND 5),
  se_siente_deprimido TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO'
                    CHECK (se_siente_deprimido BETWEEN 1 AND 5),
  fluctuacion_interes TINYINT CHECK (fluctuacion_interes BETWEEN 1 AND 5),
  problemas_sueno   TINYINT CHECK (problemas_sueno BETWEEN 1 AND 5),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b2smmh_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

CREATE TABLE b2_lifestyle (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  pais              VARCHAR(30),
  edad              TINYINT UNSIGNED,
  genero            VARCHAR(20),
  nivel_ejercicio   VARCHAR(20),
  tipo_dieta        VARCHAR(30),
  horas_sueno       DECIMAL(4,1) CHECK (horas_sueno BETWEEN 0 AND 24),
  nivel_estres      ENUM('Low','Moderate','High') NOT NULL
                    COMMENT 'VARIABLE OBJETIVO',
  condicion_salud_mental VARCHAR(30) NOT NULL DEFAULT 'Ninguna'
                    COMMENT 'NaN del CSV recodificados como Ninguna',
  horas_trabajo_semana DECIMAL(4,1),
  horas_pantalla    DECIMAL(4,1),
  interaccion_social DECIMAL(4,1),
  felicidad         DECIMAL(4,1),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b2life_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 3 - PERCEPCION EMOCIONAL (NLP)
-- ============================================================================
-- dreaddit_post unifica train y test en una tabla con campo 'particion';
-- conserva el id original del corpus como PK natural y normaliza el
-- subreddit via FK. Las 107 columnas LIWC se conservan en el CSV para el
-- pipeline Python; en la BD se materializan las senales usadas en el EDA
-- (el resto puede anadirse con ALTER TABLE si el modelado lo requiere).

CREATE TABLE b3_dreaddit_post (
  post_frag_id      INT UNSIGNED NOT NULL COMMENT 'PK natural: columna id del corpus',
  dataset_id        TINYINT UNSIGNED NOT NULL COMMENT 'FK: train o test',
  particion         ENUM('train','test') NOT NULL,
  subreddit_id      SMALLINT UNSIGNED NOT NULL,
  post_id           VARCHAR(20),
  rango_frases      VARCHAR(20),
  texto             TEXT NOT NULL,
  etiqueta_estres   TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO'
                    CHECK (etiqueta_estres IN (0,1)),
  confianza_etiqueta DECIMAL(4,2),
  ts_publicacion    BIGINT UNSIGNED,
  karma             INT,
  num_comentarios   INT,
  sentimiento       DECIMAL(6,3),
  liwc_ansiedad     DECIMAL(6,2),
  liwc_emo_negativa DECIMAL(6,2),
  liwc_emo_positiva DECIMAL(6,2),
  liwc_primera_persona DECIMAL(6,2),
  legibilidad_fk    DECIMAL(6,2),
  PRIMARY KEY (post_frag_id),
  CONSTRAINT fk_b3dr_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id),
  CONSTRAINT fk_b3dr_subreddit FOREIGN KEY (subreddit_id)
    REFERENCES dim_subreddit(subreddit_id),
  INDEX idx_b3dr_particion (particion),
  INDEX idx_b3dr_label (etiqueta_estres)
) ENGINE=InnoDB;

CREATE TABLE b3_depression_student (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  genero            VARCHAR(20),
  edad              TINYINT UNSIGNED CHECK (edad BETWEEN 15 AND 60),
  presion_academica TINYINT CHECK (presion_academica BETWEEN 1 AND 5),
  satisfaccion_estudios TINYINT CHECK (satisfaccion_estudios BETWEEN 1 AND 5),
  duracion_sueno    VARCHAR(30),
  habitos_alimentarios VARCHAR(30),
  pensamientos_suicidas ENUM('Yes','No'),
  horas_estudio     DECIMAL(4,1),
  estres_financiero TINYINT CHECK (estres_financiero BETWEEN 1 AND 5),
  antecedentes_familiares ENUM('Yes','No'),
  depresion         ENUM('Yes','No') NOT NULL COMMENT 'VARIABLE OBJETIVO',
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b3dep_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 4 - VALIDACION PSICOLOGICA
-- ============================================================================
-- DASS-42 se modela en dos tablas normalizadas (1:N):
--   b4_dass_respondente : una fila por participante (demograficos + subescalas)
--   b4_dass_item        : 42 filas por participante (respuesta por item)
-- Esto evita una tabla de 172 columnas y demuestra la relacion PK-FK evaluada.

CREATE TABLE b4_dass_respondente (
  respondente_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  pais              CHAR(2),
  edad              TINYINT UNSIGNED COMMENT 'Regla de calidad: rango plausible'
                    CHECK (edad BETWEEN 13 AND 90),
  genero            TINYINT COMMENT '1=Hombre,2=Mujer,3=Otro (codebook)',
  educacion         TINYINT COMMENT '1=<sec,2=sec,3=grado,4=posgrado',
  ingles_nativo     TINYINT,
  religion          TINYINT,
  orientacion       TINYINT,
  estado_civil      TINYINT,
  carrera           VARCHAR(120),
  seg_intro         INT UNSIGNED,
  seg_test          INT UNSIGNED,
  seg_encuesta      INT UNSIGNED,
  validez_vcl_ok    BOOLEAN COMMENT 'FALSE si marco palabras inexistentes VCL6/9/12',
  score_depresion   TINYINT UNSIGNED COMMENT 'Subescala 14-56 (clave codebook)',
  score_ansiedad    TINYINT UNSIGNED COMMENT 'Subescala 14-56',
  score_estres      TINYINT UNSIGNED COMMENT 'Subescala 14-56',
  PRIMARY KEY (respondente_id),
  CONSTRAINT fk_b4dr_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id),
  INDEX idx_b4dr_edad (edad)
) ENGINE=InnoDB;

CREATE TABLE b4_dass_item (
  respondente_id    INT UNSIGNED NOT NULL,
  item_num          TINYINT UNSIGNED NOT NULL CHECK (item_num BETWEEN 1 AND 42),
  subescala         ENUM('depresion','ansiedad','estres') NOT NULL
                    COMMENT 'Asignacion oficial del codebook DASS-42',
  respuesta         TINYINT NOT NULL CHECK (respuesta BETWEEN 1 AND 4),
  posicion_en_test  TINYINT UNSIGNED,
  ms_respuesta      INT UNSIGNED,
  PRIMARY KEY (respondente_id, item_num),
  CONSTRAINT fk_b4di_respondente FOREIGN KEY (respondente_id)
    REFERENCES b4_dass_respondente(respondente_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE b4_mental_health (
  registro_id       INT UNSIGNED NOT NULL AUTO_INCREMENT,
  dataset_id        TINYINT UNSIGNED NOT NULL,
  genero            VARCHAR(20),
  pais              VARCHAR(40),
  ocupacion         VARCHAR(30) COMMENT 'Filtrar Student para el TFM',
  autonomo          ENUM('Yes','No') NULL COMMENT '1.67% nulos: imputar/Desconocido',
  antecedentes_familiares ENUM('Yes','No'),
  tratamiento       ENUM('Yes','No') NOT NULL COMMENT 'VARIABLE OBJETIVO',
  dias_en_casa      VARCHAR(30),
  cambio_habitos    VARCHAR(10),
  historial_salud_mental VARCHAR(10),
  estres_creciente  VARCHAR(10),
  cambios_humor     VARCHAR(10),
  debilidad_social  VARCHAR(10) COMMENT 'Columna duplicada .1 eliminada en carga',
  dificultad_afrontamiento VARCHAR(10),
  interes_trabajo   VARCHAR(10),
  entrevista_salud_mental VARCHAR(10),
  conoce_opciones   VARCHAR(15),
  PRIMARY KEY (registro_id),
  CONSTRAINT fk_b4mh_dataset FOREIGN KEY (dataset_id)
    REFERENCES dim_dataset(dataset_id),
  INDEX idx_b4mh_ocupacion (ocupacion)
) ENGINE=InnoDB;

-- ============================================================================
-- FIN DEL MODELO - 15 tablas: 3 dimensiones + 12 de hechos (DASS en 2 tablas,
-- Dreaddit train+test unificado en 1 tabla con particion)
-- ============================================================================
