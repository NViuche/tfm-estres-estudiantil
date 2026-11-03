# Seguimiento del proyecto

Retroalimentación del tutor en cada entrega, cómo se resolvió, y limitaciones y pendientes.

## Entrega 1: análisis, perfilado y modelo de datos

El tutor valoró el reto de combinar fuentes tan distintas (datos clínicos, encuestas académicas y texto de redes sociales) y la fase de diagnóstico y gobernanza del dato. Señaló cinco aspectos a mejorar, que se resolvieron así:

| Observación del tutor | Cómo se resolvió |
|---|---|
| El modelo entidad-relación queda por debajo del nivel de un máster y las claves genéricas `registro_id` son poco legibles | Modelo v2 con claves semánticas (p. ej. `id_encuesta_estres`, `id_respondente_dass`): 7 dimensiones y tablas de hechos por fuente ([`sql/modelo_datos_mysql.sql`](sql/modelo_datos_mysql.sql)). La v1 criticada se conserva en el historial (rama `entrega1/modelo-datos`) |
| Sin un identificador común, el TFM corre el riesgo de fragmentarse en 4 o 5 mini-proyectos | Arquitectura hub-and-spoke: 11 tablas de hechos unificadas en la vista `vw_hechos_estres` (UNION ALL) |
| Hechos ligados solo a dimensiones de metadatos (`dim_bloque`, `dim_dataset`): silos que impiden un filtro global en Power BI | 4 dimensiones conformes: `dim_genero`, `dim_rango_edad`, `dim_nivel_educativo` y `dim_nivel_estres` (miembro «No reportado» con id 0). Verificado con el filtro «mujeres de 18–25 con estrés Alto»: 7.446 casos en 7 fuentes |
| Usar datasets sintéticos en el modelado restaría validez científica | Student Habits, Social Media/Sleep y Mental Health Lifestyle (15.000 filas) marcados con `uso_modelado = 'excluido'`; solo se usan en la capa descriptiva y como caso de calidad del dato |
| Falta definir qué se mide o predice en la capa analítica global, con targets tan distintos (binario, continuo, categórico) | Constructo unificado de nivel de estrés Bajo / Moderado / Alto, con el mapeo de cada dataset en `dim_mapeo_estres` (GAD-7 y DASS con sus baremos clínicos) |

El detalle está en la respuesta a la retroalimentación ([`docs/entrega1_objetivo1/`](docs/entrega1_objetivo1/)).

## Entrega 2: ETL, KPIs y modelado

Valoración del tutor: **calidad sobresaliente**. Destacó:

- el rigor técnico y la estructura del proceso ETL;
- el diseño del Data Warehouse orientado al análisis multidimensional;
- la justificación de las métricas de evaluación de los modelos;
- la prevención de fugas de datos;
- el feature engineering;
- la serialización del pipeline completo;
- la trazabilidad de los KPIs históricos;
- la alineación entre las tablas de hechos unificadas y el esquema en estrella/constelación.

No pidió correcciones.

## Entrega 3: Power BI e insights

Pendiente de entrega y de retroalimentación del tutor. Avance:

- **Informe de Power BI** ([`powerbi/`](powerbi/)) con 5 páginas: panorama general, demografía, lenguaje (Dreaddit), validación psicológica y modelos predictivos.
  - Tiene segmentadores por bloque, género, edad y nivel educativo, y menú de navegación entre páginas.
  - Usa como métrica transversal la dimensión `dim_nivel_estres`, y los resultados del modelado (`vw_modelo_resultados`) como segunda tabla de hechos.
- **Cifras validadas:** cada valor de control del informe coincide con el calculado en SQL sobre MySQL (ver [`tests/pruebas.md`](tests/pruebas.md)).
- **Fuente de datos:** el informe lee CSV exportados de MySQL. La conexión directa a MySQL de XAMPP no funciona: sin cifrado, Power BI pide el modo SSL `None`, que el conector actual ya no admite.
- **Pendientes:** el documento de insights y la migración de la base de datos a la nube (Supabase), para conectar el informe sin pasar por CSV.

## Limitaciones conocidas

- Tres tareas de modelado tienen menos de 600 registros, así que sus resultados varían mucho.
- Varias poblaciones no son estudiantiles (jugadores online, Reddit, población general).
- No se usó deep learning, búsqueda de hiperparámetros ni ajuste de umbrales.
- Los modelos son de investigación, no de diagnóstico clínico.
- Depression Student obtiene un AUC de 0,998, lo que indica una posible etiqueta generada por fórmula. Se reporta con cautela.
- 67 respondentes del DASS (0,17 %) sin género informado quedaron como «Otro» en lugar de «No reportado» (efecto de 0,02 puntos en la cobertura demográfica).

## Pendiente

- Decidir si Depression Student se mantiene en el modelado (excluirlo solo requiere un `UPDATE` sobre `dim_dataset`).
- Entrega 3: documento de insights; migración a Supabase; corregir las tildes de los nombres de bloque en MySQL («Percepcion emocional» → «Percepción emocional»).

---
<!-- relacionado -->
**Relacionado:** [README](README.md) · [Problema y objetivos](investigacion/problema.md) · [Respuesta a la Entrega 1](docs/entrega1_objetivo1/02_respuesta_retroalimentacion_entrega1_v3.md) · [Síntesis ETL y KPIs](docs/entrega2_objetivo2/02_sintesis_entrega2_etl_kpis.md) · [Síntesis del modelado](docs/entrega2_objetivo2/01_sintesis_objetivo2_modelado.md) · [Guía de Power BI](docs/entrega3_objetivo3/guia_power_bi.md) · [Pruebas](tests/pruebas.md)
