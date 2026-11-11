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

Entregables listos; pendiente de la retroalimentación del tutor. Avance:

- **Informe de Power BI** ([`powerbi/`](powerbi/)) con 8 páginas en el menú: inicio (menú principal), panorama, demografía, lenguaje (Dreaddit), validación psicológica, modelos predictivos, KPIs y Explorar. El fichero entregado es el `.pbix` de la versión Supabase (se entrega aparte: lleva los datos dentro).
  - Tiene segmentadores por bloque, género, edad y nivel educativo, sincronizados entre Panorama, Demografía y Explorar, y menú de navegación entre páginas.
  - Para cubrir los puntos de la rúbrica sobre imágenes y explotación: fondo, iconos y logos de UNIE e INESDI en Inicio; jerarquía bloque → dataset; *Obtener detalles* hacia una ficha por dataset; tooltip de página; árbol de descomposición e influenciadores clave en Explorar (con la columna calculada `nivel_estres`, que los influenciadores necesitan para analizar por registro).
  - Las páginas Inicio y KPIs responden a la rúbrica de la Entrega 3: menú principal, los 6 KPIs del DWH visibles con su histórico y su definición, y la distribución completa del nivel de estrés por dataset.
  - Usa como métrica transversal la dimensión `dim_nivel_estres`, y los resultados del modelado (`vw_modelo_resultados`) como segunda tabla de hechos.
- **Cifras validadas:** cada valor de control del informe coincide con el calculado en SQL sobre MySQL (ver [`tests/pruebas.md`](tests/pruebas.md)).
- **Fuente de datos:** el informe local lee CSV exportados de MySQL. La conexión directa a MySQL de XAMPP no funciona: sin cifrado, Power BI pide el modo SSL `None`, que el conector actual ya no admite.
- **Base de datos en la nube** ([`supabase/`](supabase/README.md)): esquema PostgreSQL `tfm` con las dimensiones, el DWH y los hechos de la capa estrella. La migración se valida sola contra MySQL (17 de 17 tablas y 7 de 7 cifras de control). En Supabase se corrigieron las tildes de bloques, KPIs y modelos, y «Yes» pasó a «Sí». Una copia del informe se conecta a Supabase con un usuario de solo lectura.
- **Prototipo web** ([`prototipo/`](prototipo/README.md)): las páginas del informe en un HTML con los datos incrustados desde Supabase, una carpeta por versión. La v2 añade una pestaña de arquitectura con los tres diagramas del modelo; de la v3 a la v8 replican las mejoras del Power BI (Explorar con árbol de descomposición e influenciadores, ficha del dataset, tooltip, logos). La v9 enlaza desde la pestaña de arquitectura la documentación de Supabase y tres consultas de datos en vivo (catálogo de datasets, KPIs y mejor modelo por dataset), de solo lectura con la clave pública. La v10, la final, enlaza además este repositorio y el documento de insights (Inicio y pie), la fuente original y la ficha técnica de cada dataset, y el notebook o script de cada paso del recorrido de los datos. Está publicada como servicio web: https://claude.ai/artifact/7DuVNnNh38qLgELbcKAG8b.
- **Documento de insights** ([`docs/entrega3_objetivo3/insights/`](docs/entrega3_objetivo3/insights/README.md)): Word de 12 páginas con 7 insights. Cada uno documenta qué muestra, cómo se encontró en el informe (página, gráfico y filtro), su comprobación dentro de cada dataset para descartar efectos de composición, su implicación y sus cautelas. Los influenciadores clave del propio Power BI confirman varios (por ejemplo, «Rango de edad es <18» multiplica por 1,51 la probabilidad de estrés Alto).
- **Diagramas corregidos** ([`figuras/diagramas/`](figuras/diagramas/README.md)): el modelo v2 tiene 20 tablas (no 19) y `vw_hechos_estres` devuelve 334.318 filas (no 320.318). Los diagramas entregados se conservan aparte.

## Limitaciones conocidas

- Tres tareas de modelado tienen menos de 600 registros, así que sus resultados varían mucho.
- Varias poblaciones no son estudiantiles (jugadores online, Reddit, población general).
- No se usó deep learning, búsqueda de hiperparámetros ni ajuste de umbrales.
- Los modelos son de investigación, no de diagnóstico clínico.
- Depression Student obtiene un AUC de 0,998, lo que indica una posible etiqueta generada por fórmula. Se reporta con cautela.
- 67 respondentes del DASS (0,17 %) sin género informado quedaron como «Otro» en lugar de «No reportado» (efecto de 0,02 puntos en la cobertura demográfica).

## Pendiente

- Decidir si Depression Student se mantiene en el modelado (excluirlo solo requiere un `UPDATE` sobre `dim_dataset`).
- Entrega 3: incorporar la retroalimentación del tutor cuando llegue. Las tildes y el «Sí» están corregidos en Supabase; el informe local con MySQL los mantiene como en origen.
- Siguiente fase: memoria final (~50 páginas) y presentación de la defensa.
- `b4_dass_item` existe en el modelo, pero está vacía: no se cargaron las respuestas por ítem del DASS-42.

---
<!-- relacionado -->
**Relacionado:** [README](README.md) · [Problema y objetivos](investigacion/problema.md) · [Respuesta a la Entrega 1](docs/entrega1_objetivo1/02_respuesta_retroalimentacion_entrega1_v3.md) · [Síntesis ETL y KPIs](docs/entrega2_objetivo2/02_sintesis_entrega2_etl_kpis.md) · [Síntesis del modelado](docs/entrega2_objetivo2/01_sintesis_objetivo2_modelado.md) · [Guía de Power BI](docs/entrega3_objetivo3/guia_power_bi.md) · [Pruebas](tests/pruebas.md)
