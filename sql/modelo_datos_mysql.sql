-- ============================================================================
-- ENTREGA 1 (CORRECCION v2) - MODELO DE DATOS EN MySQL
-- TFM: Analisis multidimensional del estres estudiantil (BA & IA)
-- ============================================================================
-- CAMBIOS RESPECTO A v1 (en respuesta a la retroalimentacion del tutor):
--  1) DIMENSIONES CONFORMES: dim_genero, dim_rango_edad, dim_nivel_educativo
--     y dim_nivel_estres. Todas las tablas de hechos las comparten, lo que
--     habilita filtros globales en Power BI (p.ej. "Mujeres de 18-25")
--     sobre TODAS las fuentes a la vez, eliminando los silos.
--  2) CLAVES PRIMARIAS RENOMBRADAS con nombres legibles e identificables
--     (id_encuesta_estres, id_respondente_dass, ...) en lugar de registro_id.
--  3) dim_nivel_estres es ademas el CONSTRUCTO ANALITICO UNIFICADO del TFM:
--     cada dataset mapea su variable objetivo nativa (binaria, Likert,
--     continua o categorica) a un nivel ordinal comun Bajo/Moderado/Alto
--     mediante criterios documentados (columna criterio de dim_mapeo_estres).
--  4) dim_dataset conserva el linaje e incorpora la columna uso_modelado:
--     los datasets sinteticos quedan EXCLUIDOS del modelado predictivo.
-- Los miembros 'No reportado' (id=0) permiten conformar hechos sin demografia.
-- ============================================================================

DROP DATABASE IF EXISTS tfm_estres_estudiantil_2;
CREATE DATABASE tfm_estres_estudiantil_2
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tfm_estres_estudiantil_2;

-- ============================================================================
-- DIMENSIONES DE GOBIERNO (linaje)
-- ============================================================================

CREATE TABLE dim_bloque (
  id_bloque     TINYINT UNSIGNED NOT NULL,
  nombre        VARCHAR(60)  NOT NULL,
  descripcion   VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_bloque)
) ENGINE=InnoDB;

INSERT INTO dim_bloque VALUES
 (1,'Factores internos','Core del estres: estres academico, ansiedad, salud mental, habitos'),
 (2,'Habitos digitales','Factores externos: redes sociales, pantalla, estilo de vida'),
 (3,'Percepcion emocional','IA/NLP: corpus textual Dreaddit y perfil de depresion estudiantil'),
 (4,'Validacion psicologica','Escalas clinicas DASS-42 y encuesta masiva de salud mental');

CREATE TABLE dim_dataset (
  id_dataset    TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_bloque     TINYINT UNSIGNED NOT NULL,
  codigo        VARCHAR(30)  NOT NULL UNIQUE,
  nombre        VARCHAR(120) NOT NULL,
  fuente        VARCHAR(255) NOT NULL,
  n_filas       INT UNSIGNED NOT NULL,
  n_columnas    SMALLINT UNSIGNED NOT NULL,
  calidad       ENUM('inferencial','tecnico') NOT NULL
                COMMENT 'Evaluacion de calidad del Objetivo 1',
  uso_modelado  ENUM('incluido','excluido') NOT NULL
                COMMENT 'Politica Objetivo 2: sinteticos excluidos del modelado predictivo',
  PRIMARY KEY (id_dataset),
  CONSTRAINT fk_dataset_bloque FOREIGN KEY (id_bloque)
    REFERENCES dim_bloque(id_bloque)
) ENGINE=InnoDB;

INSERT INTO dim_dataset (id_bloque,codigo,nombre,fuente,n_filas,n_columnas,calidad,uso_modelado) VALUES
 (1,'B1_ACADSTRESS','Academic Stress','kaggle.com/datasets/poushal02/student-academic-stress-real-world-dataset',140,9,'inferencial','incluido'),
 (1,'B1_ANXIETY','Student Anxiety GAD-7','kaggle.com/datasets/petalme/student-anxiety-dataset',13464,55,'inferencial','incluido'),
 (1,'B1_MHSURVEY','Student Mental Health Survey','kaggle.com/datasets/abdullahashfaqvirk/student-mental-health-survey',87,21,'inferencial','incluido'),
 (1,'B1_HABITS','Student Habits vs Performance','github.com/abhi88377/Student-Habits-vs-Academic-Performance',1000,16,'tecnico','excluido'),
 (2,'B2_SOCIALMEDIA','Social Media vs Sleep/Stress/Productivity','kaggle.com/datasets/jayjoshi37/social-media-usage-vs-sleep-stress-and-productivity',11000,10,'tecnico','excluido'),
 (2,'B2_SMMH','Social Media and Mental Health','kaggle.com/datasets/souvikahmed071/social-media-and-mental-health',481,21,'inferencial','incluido'),
 (2,'B2_LIFESTYLE','Mental Health Lifestyle','github.com/datafit17/Mental_Health_Lifestyle',3000,12,'tecnico','excluido'),
 (3,'B3_DREADDIT_TR','Dreaddit train','kaggle.com/datasets/payaldhokane/stress-analysis-in-social-media-dataset',2838,116,'inferencial','incluido'),
 (3,'B3_DREADDIT_TE','Dreaddit test','kaggle.com/datasets/payaldhokane/stress-analysis-in-social-media-dataset',715,116,'inferencial','incluido'),
 (3,'B3_DEPSTUDENT','Depression Student Dataset','github.com/prajwalg26/Student_Mental_Health_Analysis',502,11,'inferencial','incluido'),
 (4,'B4_DASS','DASS-42','kaggle.com/datasets/lucasgreenwell/depression-anxiety-stress-scales-responses',39775,172,'inferencial','incluido'),
 (4,'B4_MENTALHEALTH','Mental Health Dataset','kaggle.com/code/chanchal24/mental-health-dataset',261328,17,'inferencial','incluido');

CREATE TABLE dim_subreddit (
  id_subreddit  SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre        VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (id_subreddit)
) ENGINE=InnoDB;

INSERT INTO dim_subreddit (nombre) VALUES
 ('ptsd'),('relationships'),('anxiety'),('domesticviolence'),('assistance'),
 ('survivorsofabuse'),('homeless'),('almosthomeless'),('stress'),('food_pantry');

-- ============================================================================
-- DIMENSIONES CONFORMES (compartidas por TODAS las tablas de hechos)
-- ============================================================================

CREATE TABLE dim_genero (
  id_genero   TINYINT UNSIGNED NOT NULL,
  codigo      CHAR(2)     NOT NULL UNIQUE,
  nombre      VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_genero)
) ENGINE=InnoDB;

INSERT INTO dim_genero VALUES
 (0,'NR','No reportado'),
 (1,'M','Masculino'),
 (2,'F','Femenino'),
 (3,'O','Otro');

CREATE TABLE dim_rango_edad (
  id_rango_edad TINYINT UNSIGNED NOT NULL,
  rango         VARCHAR(15) NOT NULL UNIQUE,
  edad_min      TINYINT UNSIGNED NULL,
  edad_max      TINYINT UNSIGNED NULL,
  PRIMARY KEY (id_rango_edad)
) ENGINE=InnoDB;

INSERT INTO dim_rango_edad VALUES
 (0,'No reportado',NULL,NULL),
 (1,'<18',13,17),
 (2,'18-25',18,25),      -- proxy de poblacion estudiantil del TFM
 (3,'26-35',26,35),
 (4,'36-50',36,50),
 (5,'>50',51,90);

CREATE TABLE dim_nivel_educativo (
  id_nivel_educativo TINYINT UNSIGNED NOT NULL,
  nivel              VARCHAR(30) NOT NULL UNIQUE,
  PRIMARY KEY (id_nivel_educativo)
) ENGINE=InnoDB;

INSERT INTO dim_nivel_educativo VALUES
 (0,'No reportado'),
 (1,'Secundaria o menos'),
 (2,'Grado universitario'),
 (3,'Posgrado');

-- Constructo analitico unificado del proyecto: nivel de estres armonizado
CREATE TABLE dim_nivel_estres (
  id_nivel_estres TINYINT UNSIGNED NOT NULL,
  nivel           VARCHAR(12) NOT NULL UNIQUE,
  descripcion     VARCHAR(120) NOT NULL,
  PRIMARY KEY (id_nivel_estres)
) ENGINE=InnoDB;

INSERT INTO dim_nivel_estres VALUES
 (0,'No aplica','Registro sin variable de malestar mapeable'),
 (1,'Bajo','Malestar minimo o ausente segun el criterio nativo del dataset'),
 (2,'Moderado','Malestar intermedio segun el criterio nativo del dataset'),
 (3,'Alto','Malestar elevado o clinicamente relevante segun el criterio nativo');

-- Tabla de gobernanza: documenta el criterio de mapeo de cada dataset
CREATE TABLE dim_mapeo_estres (
  id_mapeo     TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset   TINYINT UNSIGNED NOT NULL,
  variable_nativa VARCHAR(60) NOT NULL,
  criterio     VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_mapeo),
  CONSTRAINT fk_mapeo_dataset FOREIGN KEY (id_dataset)
    REFERENCES dim_dataset(id_dataset)
) ENGINE=InnoDB;

INSERT INTO dim_mapeo_estres (id_dataset, variable_nativa, criterio) VALUES
 (1,'indice_estres (1-5)','1-2=Bajo; 3=Moderado; 4-5=Alto'),
 (2,'GAD_T (0-21)','0-4=Bajo (minima); 5-9=Moderado (leve); 10-21=Alto (moderada/severa, umbrales clinicos GAD-7)'),
 (3,'depresion (1-5)','1-2=Bajo; 3=Moderado; 4-5=Alto'),
 (4,'salud_mental (1-10, invertida)','8-10=Bajo; 5-7=Moderado; 1-4=Alto. Dataset sintetico: solo capa descriptiva'),
 (5,'nivel_estres (Low/Medium/High)','Mapeo directo. Dataset sintetico: solo capa descriptiva'),
 (6,'se_siente_deprimido (1-5)','1-2=Bajo; 3=Moderado; 4-5=Alto'),
 (7,'nivel_estres (Low/Moderate/High)','Mapeo directo. Dataset sintetico: solo capa descriptiva'),
 (8,'etiqueta_estres (0/1)','0=Bajo; 1=Alto (etiquetado manual del corpus)'),
 (9,'etiqueta_estres (0/1)','0=Bajo; 1=Alto (etiquetado manual del corpus)'),
 (10,'depresion (Yes/No)','No=Bajo; Yes=Alto'),
 (11,'score_estres DASS (14-56)','14-28=Bajo (normal); 29-39=Moderado (leve/moderado); 40-56=Alto (severo+, baremos DASS-42)'),
 (12,'estres_creciente (Yes/Maybe/No)','No=Bajo; Maybe=Moderado; Yes=Alto');

-- ============================================================================
-- BLOQUE 1 - FACTORES INTERNOS
-- ============================================================================

CREATE TABLE b1_academic_stress (
  id_encuesta_estres INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  ts_respuesta      VARCHAR(30),
  etapa_academica   VARCHAR(30),
  presion_pares     TINYINT CHECK (presion_pares BETWEEN 1 AND 5),
  presion_hogar     TINYINT CHECK (presion_hogar BETWEEN 1 AND 5),
  entorno_estudio   VARCHAR(60),
  estrategia_afrontamiento VARCHAR(120),
  habitos_nocivos   VARCHAR(30),
  competencia_academica TINYINT CHECK (competencia_academica BETWEEN 1 AND 5),
  indice_estres     TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO nativa (1-5)'
                    CHECK (indice_estres BETWEEN 1 AND 5),
  PRIMARY KEY (id_encuesta_estres),
  CONSTRAINT fk_b1ae_dataset  FOREIGN KEY (id_dataset)  REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b1ae_genero   FOREIGN KEY (id_genero)   REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b1ae_edad     FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b1ae_edu      FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b1ae_estres   FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

CREATE TABLE b1_anxiety (
  id_encuesta_ansiedad INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  num_secuencial_csv INT UNSIGNED COMMENT 'S. No. original del CSV',
  gad1 TINYINT, gad2 TINYINT, gad3 TINYINT, gad4 TINYINT,
  gad5 TINYINT, gad6 TINYINT, gad7 TINYINT,
  gade              VARCHAR(60),
  swl_total         TINYINT,
  spin_total        SMALLINT,
  gad_total         TINYINT COMMENT 'VARIABLE OBJETIVO nativa: GAD-7 (0-21)',
  horas_juego       DECIMAL(6,1),
  edad              TINYINT UNSIGNED,
  ocupacion         VARCHAR(60) COMMENT 'Work: filtrar estudiantes',
  pais_residencia   CHAR(3),
  PRIMARY KEY (id_encuesta_ansiedad),
  CONSTRAINT fk_b1an_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b1an_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b1an_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b1an_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b1an_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres),
  INDEX idx_b1an_ocupacion (ocupacion)
) ENGINE=InnoDB;

CREATE TABLE b1_mental_health_survey (
  id_encuesta_salud_mental INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED,
  universidad       VARCHAR(60),
  carrera           VARCHAR(60),
  anio_academico    VARCHAR(20),
  cgpa_rango        VARCHAR(20),
  satisfaccion_estudios TINYINT CHECK (satisfaccion_estudios BETWEEN 1 AND 5),
  carga_academica   TINYINT CHECK (carga_academica BETWEEN 1 AND 5),
  presion_academica TINYINT CHECK (presion_academica BETWEEN 1 AND 5),
  aislamiento       TINYINT CHECK (aislamiento BETWEEN 1 AND 5),
  inseguridad_futuro TINYINT CHECK (inseguridad_futuro BETWEEN 1 AND 5),
  depresion         TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO nativa (1-5)'
                    CHECK (depresion BETWEEN 1 AND 5),
  ansiedad          TINYINT NOT NULL CHECK (ansiedad BETWEEN 1 AND 5),
  PRIMARY KEY (id_encuesta_salud_mental),
  CONSTRAINT fk_b1ms_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b1ms_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b1ms_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b1ms_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b1ms_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

CREATE TABLE b1_student_habits (
  id_estudiante     VARCHAR(12) NOT NULL COMMENT 'PK natural del CSV (student_id)',
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED,
  horas_estudio_dia DECIMAL(4,1),
  horas_redes       DECIMAL(4,1),
  horas_streaming   DECIMAL(4,1),
  trabajo_parcial   ENUM('Yes','No'),
  asistencia_pct    DECIMAL(5,2),
  horas_sueno       DECIMAL(4,1),
  calidad_dieta     VARCHAR(20),
  frecuencia_ejercicio TINYINT,
  educacion_padres  VARCHAR(30) NULL,
  calidad_internet  VARCHAR(20),
  salud_mental      TINYINT COMMENT 'Senal sintetica documentada'
                    CHECK (salud_mental BETWEEN 1 AND 10),
  nota_examen       DECIMAL(5,2) CHECK (nota_examen BETWEEN 0 AND 100),
  PRIMARY KEY (id_estudiante),
  CONSTRAINT fk_b1sh_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b1sh_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b1sh_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b1sh_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b1sh_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 2 - HABITOS DIGITALES
-- ============================================================================

CREATE TABLE b2_social_media_sleep (
  id_usuario_red    INT UNSIGNED NOT NULL COMMENT 'PK natural del CSV (user_id)',
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED,
  plataforma        VARCHAR(30),
  horas_redes       DECIMAL(4,1),
  horas_pantalla    DECIMAL(4,1) CHECK (horas_pantalla BETWEEN 0 AND 24),
  horas_sueno       DECIMAL(4,1) CHECK (horas_sueno BETWEEN 0 AND 24),
  horas_estudio_trabajo DECIMAL(4,1),
  minutos_ejercicio SMALLINT UNSIGNED,
  productividad     DECIMAL(5,2),
  nivel_estres_nativo ENUM('Low','Medium','High') NOT NULL
                    COMMENT 'VARIABLE OBJETIVO nativa',
  PRIMARY KEY (id_usuario_red),
  CONSTRAINT fk_b2sm_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b2sm_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b2sm_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b2sm_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b2sm_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

CREATE TABLE b2_smmh (
  id_respuesta_smmh INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  ts_respuesta      VARCHAR(30),
  edad              TINYINT UNSIGNED,
  estado_relacion   VARCHAR(30),
  ocupacion         VARCHAR(30),
  usa_redes         ENUM('Yes','No'),
  plataformas       VARCHAR(255),
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
  se_siente_deprimido TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO nativa (1-5)'
                    CHECK (se_siente_deprimido BETWEEN 1 AND 5),
  fluctuacion_interes TINYINT CHECK (fluctuacion_interes BETWEEN 1 AND 5),
  problemas_sueno   TINYINT CHECK (problemas_sueno BETWEEN 1 AND 5),
  PRIMARY KEY (id_respuesta_smmh),
  CONSTRAINT fk_b2sh_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b2sh_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b2sh_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b2sh_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b2sh_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

CREATE TABLE b2_lifestyle (
  id_registro_estilo_vida INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  pais              VARCHAR(30),
  edad              TINYINT UNSIGNED,
  nivel_ejercicio   VARCHAR(20),
  tipo_dieta        VARCHAR(30),
  horas_sueno       DECIMAL(4,1) CHECK (horas_sueno BETWEEN 0 AND 24),
  nivel_estres_nativo ENUM('Low','Moderate','High') NOT NULL
                    COMMENT 'VARIABLE OBJETIVO nativa',
  condicion_salud_mental VARCHAR(30) NOT NULL DEFAULT 'Ninguna',
  horas_trabajo_semana DECIMAL(4,1),
  horas_pantalla    DECIMAL(4,1),
  interaccion_social DECIMAL(4,1),
  felicidad         DECIMAL(4,1),
  PRIMARY KEY (id_registro_estilo_vida),
  CONSTRAINT fk_b2lf_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b2lf_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b2lf_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b2lf_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b2lf_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 3 - PERCEPCION EMOCIONAL (NLP)
-- ============================================================================

CREATE TABLE b3_dreaddit_post (
  id_fragmento_post INT UNSIGNED NOT NULL COMMENT 'PK natural: columna id del corpus',
  id_dataset        TINYINT UNSIGNED NOT NULL COMMENT 'train o test',
  id_subreddit      SMALLINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Corpus anonimo: 0=NR',
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Corpus anonimo: 0=NR',
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  particion         ENUM('train','test') NOT NULL,
  post_id_origen    VARCHAR(20),
  rango_frases      VARCHAR(20),
  texto             TEXT NOT NULL,
  etiqueta_estres   TINYINT NOT NULL COMMENT 'VARIABLE OBJETIVO nativa (0/1)'
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
  PRIMARY KEY (id_fragmento_post),
  CONSTRAINT fk_b3dp_dataset   FOREIGN KEY (id_dataset)   REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b3dp_subreddit FOREIGN KEY (id_subreddit) REFERENCES dim_subreddit(id_subreddit),
  CONSTRAINT fk_b3dp_genero    FOREIGN KEY (id_genero)    REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b3dp_edad      FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b3dp_edu       FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b3dp_estres    FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres),
  INDEX idx_b3dp_particion (particion),
  INDEX idx_b3dp_label (etiqueta_estres)
) ENGINE=InnoDB;

CREATE TABLE b3_depression_student (
  id_perfil_estudiante INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  edad              TINYINT UNSIGNED CHECK (edad BETWEEN 15 AND 60),
  presion_academica TINYINT CHECK (presion_academica BETWEEN 1 AND 5),
  satisfaccion_estudios TINYINT CHECK (satisfaccion_estudios BETWEEN 1 AND 5),
  duracion_sueno    VARCHAR(30),
  habitos_alimentarios VARCHAR(30),
  pensamientos_suicidas ENUM('Yes','No'),
  horas_estudio     DECIMAL(4,1),
  estres_financiero TINYINT CHECK (estres_financiero BETWEEN 1 AND 5),
  antecedentes_familiares ENUM('Yes','No'),
  depresion         ENUM('Yes','No') NOT NULL COMMENT 'VARIABLE OBJETIVO nativa',
  PRIMARY KEY (id_perfil_estudiante),
  CONSTRAINT fk_b3ds_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b3ds_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b3ds_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b3ds_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b3ds_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres)
) ENGINE=InnoDB;

-- ============================================================================
-- BLOQUE 4 - VALIDACION PSICOLOGICA
-- ============================================================================

CREATE TABLE b4_dass_respondente (
  id_respondente_dass INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  pais              CHAR(2),
  edad              TINYINT UNSIGNED COMMENT 'Regla de calidad: rango plausible'
                    CHECK (edad BETWEEN 13 AND 90),
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
  score_ansiedad    TINYINT UNSIGNED,
  score_estres      TINYINT UNSIGNED COMMENT 'VARIABLE OBJETIVO nativa (14-56)',
  PRIMARY KEY (id_respondente_dass),
  CONSTRAINT fk_b4dr_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b4dr_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b4dr_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b4dr_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b4dr_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres),
  INDEX idx_b4dr_edad (edad)
) ENGINE=InnoDB;

CREATE TABLE b4_dass_item (
  id_respondente_dass INT UNSIGNED NOT NULL,
  numero_item       TINYINT UNSIGNED NOT NULL CHECK (numero_item BETWEEN 1 AND 42),
  subescala         ENUM('depresion','ansiedad','estres') NOT NULL
                    COMMENT 'Asignacion oficial del codebook DASS-42',
  respuesta         TINYINT NOT NULL CHECK (respuesta BETWEEN 1 AND 4),
  posicion_en_test  TINYINT UNSIGNED,
  ms_respuesta      INT UNSIGNED,
  PRIMARY KEY (id_respondente_dass, numero_item),
  CONSTRAINT fk_b4di_respondente FOREIGN KEY (id_respondente_dass)
    REFERENCES b4_dass_respondente(id_respondente_dass) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE b4_mental_health (
  id_caso_salud_mental INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_dataset        TINYINT UNSIGNED NOT NULL,
  id_genero         TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_rango_edad     TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Fuente sin edad: 0=NR',
  id_nivel_educativo TINYINT UNSIGNED NOT NULL DEFAULT 0,
  id_nivel_estres   TINYINT UNSIGNED NOT NULL,
  pais              VARCHAR(40),
  ocupacion         VARCHAR(30) COMMENT 'Filtrar Student para el TFM',
  autonomo          ENUM('Yes','No') NULL,
  antecedentes_familiares ENUM('Yes','No'),
  tratamiento       ENUM('Yes','No') NOT NULL COMMENT 'VARIABLE OBJETIVO nativa',
  dias_en_casa      VARCHAR(30),
  cambio_habitos    VARCHAR(10),
  historial_salud_mental VARCHAR(10),
  estres_creciente  VARCHAR(10),
  cambios_humor     VARCHAR(10),
  debilidad_social  VARCHAR(10),
  dificultad_afrontamiento VARCHAR(10),
  interes_trabajo   VARCHAR(10),
  entrevista_salud_mental VARCHAR(10),
  conoce_opciones   VARCHAR(15),
  PRIMARY KEY (id_caso_salud_mental),
  CONSTRAINT fk_b4mh_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset(id_dataset),
  CONSTRAINT fk_b4mh_genero  FOREIGN KEY (id_genero)  REFERENCES dim_genero(id_genero),
  CONSTRAINT fk_b4mh_edad    FOREIGN KEY (id_rango_edad) REFERENCES dim_rango_edad(id_rango_edad),
  CONSTRAINT fk_b4mh_edu     FOREIGN KEY (id_nivel_educativo) REFERENCES dim_nivel_educativo(id_nivel_educativo),
  CONSTRAINT fk_b4mh_estres  FOREIGN KEY (id_nivel_estres) REFERENCES dim_nivel_estres(id_nivel_estres),
  INDEX idx_b4mh_ocupacion (ocupacion)
) ENGINE=InnoDB;

-- ============================================================================
-- EJEMPLO DE CONSULTA GLOBAL habilitada por las dimensiones conformes
-- (imposible en v1): "Mujeres de 18-25 con estres Alto" en TODAS las fuentes
-- ============================================================================
-- SELECT d.codigo, COUNT(*) AS casos
-- FROM (
--   SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b1_academic_stress
--   UNION ALL SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b1_anxiety
--   UNION ALL SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b1_mental_health_survey
--   UNION ALL SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b2_smmh
--   UNION ALL SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b3_depression_student
--   UNION ALL SELECT id_dataset, id_genero, id_rango_edad, id_nivel_estres FROM b4_dass_respondente
-- ) h
-- JOIN dim_dataset d      ON d.id_dataset = h.id_dataset
-- JOIN dim_genero g       ON g.id_genero = h.id_genero
-- JOIN dim_rango_edad r   ON r.id_rango_edad = h.id_rango_edad
-- JOIN dim_nivel_estres e ON e.id_nivel_estres = h.id_nivel_estres
-- WHERE g.codigo = 'F' AND r.rango = '18-25' AND e.nivel = 'Alto'
-- GROUP BY d.codigo;

-- FIN DEL MODELO v2: 19 tablas (7 dimensiones + 12 hechos)
