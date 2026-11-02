# Definición de KPIs (Entrega 2)

*Transcripción a texto de `KPIs_TFM.docx`. El Word original es el entregable oficial.*

**TFM — Business Analytics e Inteligencia Artificial · Análisis multidimensional del estrés estudiantil · Entrega 2 — ETL y KPIs**

Este documento define los seis indicadores clave (KPIs) del proyecto, calculados en el notebook 08_etl_transformaciones_kpis y almacenados en la tabla `dwh_kpi_resultados` del datawarehouse. Cada ejecución del ETL registra una nueva fila por KPI con su marca de tiempo, de modo que la tabla conserva el histórico. Los KPIs se definen sobre las nueve fuentes con señal real; los tres datasets sintéticos quedan excluidos conforme a la política acordada.

## 1. Resumen
| # | KPI | Unidad | Fuente de cálculo |
|---|---|---|---|
| 1 | Tasa de estrés Alto global | % | dwh_hechos_estres_unificado |
| 2 | Brecha de género en ansiedad | puntos | b4_dass_respondente |
| 3 | Índice de riesgo crítico | % | Depression Student |
| 4 | Tasa de búsqueda de tratamiento | % | dwh_brecha_tratamiento |
| 5 | Poder discriminante LIWC | ratio | b3_dreaddit_post |
| 6 | Cobertura demográfica | % | dwh_hechos_estres_unificado |

## 2. Ficha de cada KPI

### KPI 1 — Tasa de estrés Alto global
- **Definición:** porcentaje de registros en nivel de estrés Alto sobre el total de las nueve fuentes reales conformadas.
- **Fórmula:** (registros con nivel_estres = 'Alto' / total de registros) × 100
- **Valor de referencia:** ≈ 33,7 %
- **Interpretación:** mide la carga global de malestar elevado; línea base para comparar segmentos y seguir la evolución si se incorporan datos.

### KPI 2 — Brecha de género en ansiedad (DASS)
- **Definición:** diferencia entre la ansiedad media de mujeres y hombres en la escala DASS-42, subset 18-25 años.
- **Fórmula:** ansiedad_media(Mujer) − ansiedad_media(Hombre)
- **Valor de referencia:** ≈ +2,9 puntos (Mujer 31,0 − Hombre 28,1)
- **Interpretación:** cuantifica la brecha de género en ansiedad, bien documentada en la literatura; orienta políticas de atención diferenciada.

### KPI 3 — Índice de riesgo crítico
- **Definición:** porcentaje de estudiantes con pensamientos suicidas que además presentan depresión.
- **Fórmula:** (con pensamientos suicidas Y depresión / con pensamientos suicidas) × 100
- **Valor de referencia:** ≈ 72,7 %
- **Interpretación:** indicador de alerta temprana; vincula la ideación suicida con la depresión y refuerza la necesidad de derivación prioritaria.
- **Nota de validez:** se calcula sobre Depression Student. Su comportamiento en el modelado (AUC ≈ 0,998 con diez variables gruesas) sugiere que la etiqueta podría estar generada por una fórmula; se interpreta con cautela hasta consultarlo con el tutor.

### KPI 4 — Tasa de búsqueda de tratamiento
- **Definición:** porcentaje de estudiantes que han buscado tratamiento psicológico, con desglose por antecedentes familiares y por estrés creciente.
- **Fórmula:** (estudiantes con tratamiento = 'Yes' / total estudiantes) × 100
- **Valor de referencia:** ≈ 49,4 % global; 35,1 % sin antecedentes vs 72,4 % con antecedentes
- **Interpretación:** mide el acceso real a la ayuda; la brecha es cultural y de acceso, no de necesidad.

### KPI 5 — Poder discriminante LIWC
- **Definición:** ratio entre la densidad media de palabras de ansiedad (LIWC) de la clase estrés y la de la clase no-estrés en Dreaddit.
- **Fórmula:** liwc_ansiedad_medio(Estrés) / liwc_ansiedad_medio(No estrés)
- **Valor de referencia:** ≈ 2,58 (1,31 vs 0,51)
- **Interpretación:** fuerza de la señal léxica para distinguir estrés en texto; justifica la viabilidad del modelado NLP.

### KPI 6 — Cobertura demográfica
- **Definición:** porcentaje de registros con género y edad reportados (no 'No reportado') sobre el total unificado.
- **Fórmula:** (registros con demografia_completa = TRUE / total) × 100
- **Valor de referencia:** ≈ 17 %
- **Interpretación:** KPI de calidad del dato; el valor bajo se explica por las fuentes anónimas (Dreaddit) y sin edad (chanchal24) y advierte sobre el alcance de los filtros demográficos en los dashboards.

## 3. Almacenamiento y trazabilidad
Los resultados se guardan en `dwh_kpi_resultados`, relacionada por clave foránea con `dwh_kpi_catalogo` (definición de cada KPI). Cada ejecución del ETL inserta seis filas nuevas (una por KPI) con `fecha_ejecucion`: el valor nunca se sobrescribe, se versiona. Permite en la Entrega 3 tarjetas con el último valor y gráficos de evolución temporal.
