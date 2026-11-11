-- Calidad y gobierno del dato: resultados de las reglas de calidad y registro de controles.
--
-- dwh_calidad_reglas    las 49 reglas del notebook 05 (antes de la carga), con su dimensión de calidad
-- dwh_calidad_controles los controles de validación de la carga (07b), del ETL (08), de la migración,
--                       de la seguridad y del informe, con su resultado y su origen
--
-- Las carga scripts/cargar_calidad_dato.py (la misma estructura existe en MySQL).
-- Se ejecuta después de 01_esquema.sql, que borra y rehace el esquema tfm.

DROP TABLE IF EXISTS tfm.dwh_calidad_reglas;
DROP TABLE IF EXISTS tfm.dwh_calidad_controles;

CREATE TABLE tfm.dwh_calidad_reglas (
  id_regla        smallint PRIMARY KEY,
  id_dataset      smallint NOT NULL REFERENCES tfm.dim_dataset,
  regla           varchar(160) NOT NULL,
  dimension       text NOT NULL CHECK (dimension IN ('Completitud', 'Validez', 'Unicidad', 'Consistencia', 'Conformidad')),
  evaluados       integer NOT NULL,
  incumplen       integer NOT NULL,
  pct_incumplen   numeric(7,2) NOT NULL,
  estado          text NOT NULL CHECK (estado IN ('OK', 'AVISO', 'ERROR')),
  accion          varchar(200) NOT NULL,
  fase            varchar(30) NOT NULL
);

CREATE TABLE tfm.dwh_calidad_controles (
  id_control      smallint PRIMARY KEY,
  fase            varchar(30) NOT NULL,
  control         varchar(80) NOT NULL,
  resultado       varchar(240) NOT NULL,
  estado          text NOT NULL CHECK (estado IN ('OK', 'AVISO', 'ERROR')),
  origen          varchar(80) NOT NULL
);

COMMENT ON TABLE tfm.dwh_calidad_reglas IS 'Reglas de calidad del dato (notebook 05) por dataset y dimensión de calidad';
COMMENT ON TABLE tfm.dwh_calidad_controles IS 'Registro de controles de validación: carga, ETL, migración, seguridad e informe';
