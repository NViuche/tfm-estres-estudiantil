# Entrega 2: ETL, transformaciones y KPIs sobre un datawarehouse en estrella

*Transcripción a texto de `Sintesis_Entrega2_ETL_KPIs.pdf` (3 págs.). El PDF original, con el diagrama, es el entregable oficial. El diagrama está en `dwh_estrella_ERD.png`.*

**TFM — Business Analytics e Inteligencia Artificial.** Andrés Francisco García Grajales · Obed Isaí Alvarado Núñez · Roberto Mario Brochero López · Raúl Cervantes Iglesias · Santiago Nicolas Viuche Pinilla

Esta entrega construye el datawarehouse del proyecto como un esquema en estrella y lo alimenta con un proceso ETL en Python que lee de MySQL y escribe en MySQL. El resultado son cinco tablas de hechos con sus transformaciones, seis KPIs con histórico de ejecuciones y la prueba de que todas las claves apuntan a las dimensiones conformes que pidió el tutor en la retroalimentación de la Entrega I.

## 1. Arquitectura: de las tablas ingestadas al datawarehouse
| Capa | Objetos | Papel en el ETL |
|---|---|---|
| Ingesta (Entrega 1) | 19 tablas normalizadas cargadas por el notebook 07 con los 334.318 registros de los 12 datasets | Origen. Cada dataset conserva sus columnas propias en su tabla |
| Capa de consumo | Vistas `vw_hechos_estres` y `vw_dim_dataset` (esquema_estrella_powerbi.sql) | Origen de T1. Une los 12 datasets por sus cinco claves conformes y marca cuáles se modelan |
| Datawarehouse (esta entrega) | 8 tablas `dwh_*` creadas por `dwh_estrella.sql`: 5 hechos de transformación, catálogo e histórico de KPIs, y resultados del Objetivo 2 | Destino. Hechos que solo guardan claves hacia las dimensiones conformes y sus medidas |

Las dimensiones conformes (género, rango de edad, nivel educativo, nivel de estrés, dataset, bloque y subreddit) son las mismas tablas que usan la ingesta y la estrella: por eso un filtro como «Mujeres de 18-25 años» actúa a la vez sobre todos los hechos. Cada tabla de hechos del DWH declara sus claves foráneas con restricciones reales de MySQL, de modo que no pueden existir registros huérfanos.

## 2. Transformaciones
El notebook `08_etl_transformaciones_kpis_v4.ipynb` aplica cinco transformaciones de tipos distintos. Todas extraen de MySQL, transforman con pandas y cargan en una tabla nueva. Al empezar vacía las cinco tablas, de modo que puede relanzarse sin duplicar datos.

| # | Transformación | Tipo | Destino | Filas | Resultado destacado |
|---|---|---|---|---|---|
| T1 | Registros de las 9 fuentes con señal real, desde la estrella | Integración | dwh_hechos_estres_unificado | 319.318 | La validación psicológica aporta el 94 % del volumen |
| T2 | Prevalencia de estrés por bloque × género × edad | Agregación | dwh_agg_prevalencia | 49 | En los grupos grandes el estrés Alto va del 14,7 % al 52,3 %; 18 grupos tienen menos de 30 registros |
| T3 | Señales lingüísticas de Dreaddit por subreddit y nivel | Resumen estadístico | dwh_nlp_senales | 20 | En los 10 subreddits, más ansiedad LIWC y menos sentimiento con estrés |
| T4 | DASS 18-25 por género × nivel educativo, con % de estrés severo | Pivote + umbral clínico | dwh_dass_severidad | 12 | «Otro» con secundaria o menos: estrés medio 38,4 y 50 % en rango severo |
| T5 | Tratamiento según estrés creciente × antecedentes familiares | Contingencia | dwh_brecha_tratamiento | 6 | ≈ 35 % sin antecedentes frente a ≈ 72 % con ellos, en los tres niveles de estrés |

## 3. KPIs
Los seis indicadores se calculan en Python y se guardan en `dwh_kpi_resultados`, una fila por KPI y ejecución con su fecha. Definición en `dwh_kpi_catalogo` y en `KPIs_TFM.docx` (ver `03_kpis.md`).

| KPI | Valor | Unidad | Interpretación |
|---|---|---|---|
| Tasa de estrés Alto global | 33,68 | % | Uno de cada tres registros está en estrés Alto |
| Brecha de género en ansiedad | 2,89 | puntos | Mujeres 31,0 frente a 28,1 de los hombres (DASS, 18-25) |
| Índice de riesgo crítico | 72,69 | % | El 73 % de quienes reportan pensamientos suicidas presenta depresión (ver nota de validez en KPIs) |
| Tasa de búsqueda de tratamiento | 49,41 | % | La mitad de los estudiantes ha buscado tratamiento |
| Poder discriminante LIWC | 2,58 | ratio | El vocabulario de ansiedad es 2,6 veces mayor en los textos con estrés |
| Cobertura demográfica | 17,01 | % | Solo el 17 % de los registros tiene género y edad reportados |

## 4. Calidad y verificación
- **Integridad de la estrella:** el notebook comprueba 14 relaciones entre hechos y dimensiones y exige 0 claves huérfanas.
- **Cuadre con la estrella:** los registros de las fuentes «incluido» de `vw_hechos_estres` deben sumar lo mismo que T1: 334.318 − 15.000 sintéticos = 319.318.
- **Requisitos comprobados al inicio:** si falta una tabla, una vista o los datos, el notebook se detiene e indica qué script ejecutar.
- **Limitación conocida de la ingesta:** 67 de los 39.767 respondentes del DASS (0,17 %) no contestaron el género y la ingesta los clasificó como «Otro» en lugar de «No reportado». Efecto mínimo (0,02 puntos en la cobertura demográfica); se corregiría en una recarga futura.

El tipo de problema de aprendizaje de cada dataset y el feature engineering se documentan en el notebook del Objetivo 2 (09).

## 5. Entregables
| Archivo | Contenido |
|---|---|
| dwh_estrella.sql | Crea las 8 tablas del DWH con sus claves foráneas (ejecutar una vez) |
| 08_etl_transformaciones_kpis_v4.ipynb | Notebook documentado: transformaciones T1-T5, KPIs y verificaciones |
| dwh_estrella_ERD.png | Diagrama del DWH en estrella |
| KPIs_TFM.docx | Definición de cada KPI |
| Sintesis_Entrega2_ETL_KPIs.pdf | Este documento |

---
<!-- relacionado -->
**Relacionado:** [README](../../README.md) · [Definición de KPIs](03_kpis_definicion.md) · [Síntesis del modelado](01_sintesis_objetivo2_modelado.md) · [Pruebas](../../tests/pruebas.md)
