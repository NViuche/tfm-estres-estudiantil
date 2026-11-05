-- =====================================================================
-- Correcciones de datos aplicadas SOLO en Supabase (MySQL queda igual)
-- 1. Tildes y eñes en los textos que muestran el Power BI y el prototipo.
-- 2. Antecedentes familiares: «Yes» → «Sí».
-- Los valores nativos de los datasets (p. ej. «Yes/No» en objetivo_nativo
-- o variable_nativa) no se tocan: son las categorías originales.
-- =====================================================================
CREATE FUNCTION tfm.con_tildes(t text) RETURNS text LANGUAGE plpgsql IMMUTABLE AS $$
DECLARE
  par text[];
  -- Sustitución por palabra completa (\m … \M) y sensible a mayúsculas
  pares text[][] := ARRAY[
    ['estres', 'estrés'], ['academico', 'académico'], ['habitos', 'hábitos'], ['Habitos', 'Hábitos'],
    ['depresion', 'depresión'], ['Depresion', 'Depresión'], ['Percepcion', 'Percepción'],
    ['Validacion', 'Validación'], ['psicologica', 'psicológica'], ['psicologico', 'psicológico'],
    ['clinicas', 'clínicas'], ['clinicos', 'clínicos'], ['clinicamente', 'clínicamente'],
    ['minima', 'mínima'], ['minimo', 'mínimo'], ['segun', 'según'], ['sintetico', 'sintético'],
    ['genero', 'género'], ['anos', 'años'], ['Indice', 'Índice'], ['critico', 'crítico'],
    ['ademas', 'además'], ['busqueda', 'búsqueda'], ['demografica', 'demográfica'], ['senal', 'señal'],
    ['Regresion', 'Regresión'], ['Logistica', 'Logística'], ['Hibrido', 'Híbrido'],
    ['formula', 'fórmula'], ['autoreportada', 'autorreportada']];
BEGIN
  IF t IS NULL THEN RETURN NULL; END IF;
  FOREACH par SLICE 1 IN ARRAY pares LOOP
    t := regexp_replace(t, '\m' || par[1] || '\M', par[2], 'g');
  END LOOP;
  RETURN t;
END $$;

UPDATE tfm.dim_bloque            SET nombre = tfm.con_tildes(nombre), descripcion = tfm.con_tildes(descripcion);
UPDATE tfm.dim_mapeo_estres      SET criterio = tfm.con_tildes(criterio);
UPDATE tfm.dim_nivel_estres      SET descripcion = tfm.con_tildes(descripcion);
UPDATE tfm.dwh_kpi_catalogo      SET nombre = tfm.con_tildes(nombre), descripcion = tfm.con_tildes(descripcion);
UPDATE tfm.dwh_kpi_resultados    SET detalle = tfm.con_tildes(detalle);
UPDATE tfm.dwh_modelo_resultados SET modelo = tfm.con_tildes(modelo), target = tfm.con_tildes(target),
                                     lectura_capa_armonizada = tfm.con_tildes(lectura_capa_armonizada),
                                     alerta = tfm.con_tildes(alerta);

UPDATE tfm.dwh_brecha_tratamiento SET antecedentes_familiares = 'Sí' WHERE antecedentes_familiares = 'Yes';
ALTER TABLE tfm.dwh_brecha_tratamiento DROP CONSTRAINT dwh_brecha_tratamiento_antecedentes_familiares_check;
ALTER TABLE tfm.dwh_brecha_tratamiento ADD CHECK (antecedentes_familiares IN ('Sí', 'No'));

DROP FUNCTION tfm.con_tildes(text);
