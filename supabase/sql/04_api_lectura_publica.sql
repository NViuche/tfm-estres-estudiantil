-- Lectura pública de una muestra de los datos por la API REST de Supabase.
--
-- El esquema tfm NO se expone en la API. Solo se publican estas tres vistas en
-- el esquema public, con datos agregados (sin registros individuales), para
-- enlazarlas desde el prototipo web:
--   https://<ref>.supabase.co/rest/v1/tfm_datasets?select=*&apikey=<clave anon>
--
-- Supabase da por defecto todos los permisos del esquema public a los roles
-- anon y authenticated. Por eso se revocan y se concede solo SELECT: cualquier
-- intento de escritura por la API devuelve un error de permisos.

CREATE OR REPLACE VIEW public.tfm_datasets AS
SELECT d.codigo,
       d.dataset,
       d.bloque,
       d.calidad,
       d.uso_modelado,
       d.n_filas
FROM tfm.vw_dim_dataset d
ORDER BY d.id_bloque, d.id_dataset;

CREATE OR REPLACE VIEW public.tfm_kpis AS
SELECT c.codigo,
       c.nombre,
       c.descripcion,
       c.unidad,
       r.valor,
       r.fecha_ejecucion
FROM tfm.dwh_kpi_catalogo c
JOIN tfm.dwh_kpi_resultados r ON r.id_kpi = c.id_kpi
WHERE r.fecha_ejecucion = (SELECT max(fecha_ejecucion) FROM tfm.dwh_kpi_resultados)
ORDER BY c.id_kpi;

CREATE OR REPLACE VIEW public.tfm_modelos AS
SELECT m.bloque,
       m.dataset,
       m.modelo,
       m.n_registros,
       m.accuracy,
       m.f1,
       m.auc
FROM tfm.vw_modelo_resultados m
WHERE m.es_mejor_modelo = 1
ORDER BY m.bloque, m.dataset;

REVOKE ALL ON public.tfm_datasets, public.tfm_kpis, public.tfm_modelos FROM PUBLIC, anon, authenticated;
GRANT SELECT ON public.tfm_datasets, public.tfm_kpis, public.tfm_modelos TO anon, authenticated;

COMMENT ON VIEW public.tfm_datasets IS 'TFM estrés estudiantil: catálogo de los 12 datasets (solo lectura)';
COMMENT ON VIEW public.tfm_kpis IS 'TFM estrés estudiantil: los 6 KPIs del DWH, última ejecución (solo lectura)';
COMMENT ON VIEW public.tfm_modelos IS 'TFM estrés estudiantil: mejor modelo por dataset (solo lectura)';

NOTIFY pgrst, 'reload schema';
