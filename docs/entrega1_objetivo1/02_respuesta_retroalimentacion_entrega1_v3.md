# Respuesta a la retroalimentación de la Entrega I (versión 3, definitiva)

*Transcripción a texto de `Respuesta_Retroalimentacion_EntregaI_v3.pdf` (9 págs.). El PDF original, con los diagramas, es el entregable oficial. Las figuras 1-3 (estrella inicial, estrella actualizada y constelación de consumo) están en `esquema_estrella_powerbi.png` y en el PDF.*

**TFM — Business Analytics e Inteligencia Artificial**
Análisis multidimensional del estrés estudiantil mediante Business Analytics e Inteligencia Artificial con datos académicos, conductuales y textuales
Andrés Francisco García Grajales · Obed Isaí Alvarado Núñez · Roberto Mario Brochero López · Raúl Cervantes Iglesias · Santiago Nicolas Viuche Pinilla

Este documento detalla las acciones correctivas aplicadas al modelo de datos y a la arquitectura analítica del proyecto en respuesta a la evaluación de la Entrega I. Cada sección reproduce la observación del tutor, describe la acción tomada y señala el entregable donde queda implementada.

La arquitectura descrita está implementada y en funcionamiento: la base de datos se creó en MySQL (XAMPP/MariaDB) con las 19 tablas del modelo v2, se añadió una capa de vistas en esquema estrella para consumo en Power BI, y se cargaron los 334.318 registros de los doce datasets. La sección 6 documenta la verificación ejecutada sobre esos datos y la sección 7 el seguimiento de los compromisos en el Objetivo 2.

## 1. Renombrado de claves primarias

**Observación:** "que las tablas tengan un campo que es la clave que se llama registro_id… es bastante mejorable. Se debe renombrar esos campos a algo más legible e identificable."

**Acción aplicada:** todas las claves primarias genéricas se sustituyeron por identificadores semánticos que describen la entidad. Las claves naturales de los CSV se conservan donde existen, también con nombre legible.

| Tabla | Clave anterior (v1) | Clave nueva (v2) |
|---|---|---|
| b1_academic_stress | registro_id | id_encuesta_estres |
| b1_anxiety | registro_id | id_encuesta_ansiedad |
| b1_mental_health_survey | registro_id | id_encuesta_salud_mental |
| b1_student_habits | student_id (natural) | id_estudiante (natural) |
| b2_social_media_sleep | user_id (natural) | id_usuario_red (natural) |
| b2_smmh | registro_id | id_respuesta_smmh |
| b2_lifestyle | registro_id | id_registro_estilo_vida |
| b3_dreaddit_post | post_frag_id | id_fragmento_post (natural) |
| b3_depression_student | registro_id | id_perfil_estudiante |
| b4_dass_respondente | respondente_id | id_respondente_dass |
| b4_dass_item | (respondente_id, item_num) | (id_respondente_dass, numero_item) |
| b4_mental_health | registro_id | id_caso_salud_mental |

Implementado en `modelo_datos_mysql_v2.sql` (todas las FKs e índices actualizados; las dimensiones adoptan el mismo patrón: id_bloque, id_dataset, id_genero, etc.).

## 2. Dimensiones conformes: eliminación de los silos

**Observación:** "Diseñar el modelo físico vinculando las tablas de hechos únicamente a dimensiones de metadatos (dim_bloque o dim_dataset) genera silos insalvables. […] sí comparten atributos analíticos comunes (como la edad, el género o el nivel educativo). […] necesitáis Dimensiones Conformes tales como dim_demografica o dim_rango_edad. De lo contrario, en Power BI será imposible aplicar un filtro global de 'Mujeres de 18 a 25 años'."

**Acción aplicada:** cuatro dimensiones conformes compartidas por las doce tablas de hechos. Se optó por dimensiones atómicas separadas (en lugar de una única dim_demografica) por ser el patrón recomendado en Power BI para segmentadores independientes.

- `dim_genero`: Masculino / Femenino / Otro / No reportado. Armoniza codificaciones heterogéneas (cadenas en inglés, códigos 1/2/3 del DASS, identidades de texto libre).
- `dim_rango_edad`: <18, 18-25, 26-35, 36-50, >50, No reportado, con edad_min y edad_max. La banda 18-25 materializa el proxy de población estudiantil.
- `dim_nivel_educativo`: Secundaria o menos / Grado universitario / Posgrado / No reportado.
- `dim_nivel_estres`: el constructo analítico unificado (sección 3).

Cada tabla de hechos incorpora las cuatro claves foráneas conformes. El miembro "No reportado" (id=0), práctica estándar en modelado dimensional, permite conformar también las fuentes anónimas (Dreaddit carece de demografía por diseño) sin excluirlas ni admitir nulos en las FKs. El porcentaje de "No reportado" de cada dimensión documenta la cobertura demográfica real de cada fuente. La verificación se detalla en la sección 6.

## 3. Marco conceptual de la capa analítica global

**Observación:** "Al tener escalas y variables objetivo tan variadas en cada bloque […] falta un planteamiento conceptual claro de qué se va a predecir o medir exactamente en la capa analítica global de la solución."

**Acción aplicada:** se define el constructo unificado del proyecto, el nivel de estrés/malestar armonizado, como variable ordinal de tres niveles (Bajo / Moderado / Alto), materializada en `dim_nivel_estres`. Cada dataset mapea su variable objetivo nativa mediante criterios explícitos, documentados en la tabla de gobernanza `dim_mapeo_estres`:

| Fuente | Variable nativa | Criterio de armonización |
|---|---|---|
| Academic Stress | Índice 1-5 | 1-2 Bajo · 3 Moderado · 4-5 Alto |
| Anxiety | GAD_T (0-21) | 0-4 · 5-9 · 10-21 (umbrales clínicos GAD-7) |
| MH Survey / SMMH | Likert 1-5 | 1-2 · 3 · 4-5 |
| Dreaddit | Etiqueta 0/1 | 0 Bajo · 1 Alto (etiquetado manual) |
| Depression Student | Yes/No | No Bajo · Yes Alto |
| DASS-42 | score_estres (14-56) | 14-28 · 29-39 · 40-56 (baremos DASS) |
| Mental Health (chanchal24) | Estrés creciente Yes/Maybe/No | No Bajo · Maybe Moderado · Yes Alto |
| Sintéticos (3 fuentes) | Niveles nativos | Mapeo directo; solo capa descriptiva (sección 4) |

En el Objetivo 2 cada modelo predice la variable nativa de su dataset (respetando el análisis independiente comprometido en la propuesta) y sus resultados se leen en la capa armonizada común; en el Objetivo 3, `dim_nivel_estres` es la métrica transversal de todos los dashboards. El proyecto deja de ser una suma de mini-proyectos: es una arquitectura hub-and-spoke donde las fuentes conservan su granularidad pero convergen en un mismo constructo medible y filtrable.

## 4. Política sobre datasets sintéticos en el modelado

**Observación:** "si pensáis usarlos en la fase de modelado predictivo (Objetivo 2) […] las redes o modelos predictivos aprenderán relaciones matemáticas artificiales generadas por un software, restándole toda validez científica al entregable final del Máster."

**Acción aplicada:** se formaliza la exclusión de los tres datasets sintéticos (student_habits_performance, social_media_sleep_stress_productivity y Mental_Health_Lifestyle) del modelado predictivo. La política queda grabada en el modelo mediante la columna `uso_modelado` de `dim_dataset` ('incluido'/'excluido'), de modo que es consultable y auditable. Su papel queda acotado a:

- Caso de estudio de calidad del dato en el Objetivo 1: su detección como sintéticos es un resultado legítimo del EDA.
- Capa descriptiva de los dashboards del Objetivo 3, siempre rotulados como fuentes sintéticas, sin alimentar conclusiones sustantivas.

El Objetivo 2 se entrenó exclusivamente sobre las nueve fuentes con señal real, leyendo la política desde la propia base de datos (sección 7).

## 5. Capa de consumo en esquema estrella (versión definitiva)

**Diagnóstico.** El modelo físico v2 es una constelación con una rama en copo de nieve (hechos → dim_dataset → dim_bloque). Es correcta en la base de datos, pero penaliza el rendimiento y complica el DAX en Power BI. Solución: arquitectura en dos capas; la base conserva su normalización y seis vistas la aplanan para consumo analítico: `vw_hechos_estres` (una única tabla de hechos) y cinco dimensiones planas (`vw_dim_dataset`, que absorbe dim_bloque, y las cuatro conformes).

### 5.1 Diseño inicial y diseño actualizado

| Aspecto | Diagrama inicial (Fig. 1) | Diagrama actualizado (Fig. 2) |
|---|---|---|
| Fuentes de datos | No se muestran: solo la tabla de hechos | Los 12 datasets, agrupados por bloque, con sus filas y una flecha a la tabla de hechos |
| Total de registros | Indicaba 320.318 (cifra errónea) | 334.318 = 140 + 13.464 + 87 + 1.000 + 11.000 + 481 + 3.000 + 2.834 + 715 + 502 + 39.767 + 261.328 |
| Datasets sintéticos | Sin distinguir | Marcados (borde discontinuo y asterisco): cargados para la capa descriptiva, excluidos del modelado |
| Linaje | No explicado | `id_dataset` identifica la fuente (1 a 12); `b4_dass_item` queda fuera por tener grano de ítem |
| Estructura de vistas | 6 vistas (1 hecho + 5 dimensiones) | Las mismas 6 vistas: sin cambio estructural |

### 5.2 Qué relaciona la estrella

`vw_hechos_estres` une con UNION ALL las 11 tablas de hechos, que contienen los 12 datasets (Dreaddit train y test comparten tabla y se distinguen por id_dataset 8 y 9). Cada fila conserva su fuente en `id_dataset` y comparte las cuatro claves conformes (género, rango de edad, nivel educativo y nivel de estrés).

| id | Dataset | Bloque | Tabla de origen | Filas | Calidad | Modelado |
|---|---|---|---|---|---|---|
| 1 | Academic Stress | Factores internos | b1_academic_stress | 140 | inferencial | incluido |
| 2 | Anxiety GAD-7 | Factores internos | b1_anxiety | 13.464 | inferencial | incluido |
| 3 | MH Survey | Factores internos | b1_mental_health_survey | 87 | inferencial | incluido |
| 4 | Student Habits | Factores internos | b1_student_habits | 1.000 | técnico | excluido |
| 5 | Social Media/Sleep | Hábitos digitales | b2_social_media_sleep | 11.000 | técnico | excluido |
| 6 | SMMH | Hábitos digitales | b2_smmh | 481 | inferencial | incluido |
| 7 | Lifestyle | Hábitos digitales | b2_lifestyle | 3.000 | técnico | excluido |
| 8 | Dreaddit train | Percepción emocional | b3_dreaddit_post | 2.834 | inferencial | incluido |
| 9 | Dreaddit test | Percepción emocional | b3_dreaddit_post | 715 | inferencial | incluido |
| 10 | Depression Student | Percepción emocional | b3_depression_student | 502 | inferencial | incluido (en revisión) |
| 11 | DASS-42 | Validación psicológica | b4_dass_respondente | 39.767 | inferencial | incluido |
| 12 | Mental Health | Validación psicológica | b4_mental_health | 261.328 | inferencial | incluido |
| | **TOTAL** | | 11 tablas | **334.318** | | 9 incluidos |

**Cuadre de totales.** 334.318 menos los 15.000 registros de los tres sintéticos (1.000 + 11.000 + 3.000) dan 319.318, la misma cifra que produce la tabla T1 del datawarehouse (Entrega 2) al unificar las nueve fuentes con señal real. La excepción deliberada es `b4_dass_item` (42 ítems por respondente): su grano es el ítem, no la persona.

### 5.3 Endurecimiento del SQL y versión definitiva

Al consultar la vista, MariaDB devolvió el error #1271 (mezcla ilegal de collations en el UNION). Se corrigió forzando `COLLATE utf8mb4_unicode_ci` en las 22 expresiones de texto del UNION. Archivo definitivo: `esquema_estrella_powerbi.sql` (sustituye a cualquier copia anterior). Respecto a la primera versión: incorpora el COLLATE, apunta a la base real `tfm_estres_estudiantil_2`, añade dos consultas de verificación (V1: 12 filas, una por dataset; V2: total 334.318 y 319.318 en fuentes incluidas) y no cambia la estructura (las mismas 6 vistas).

## 6. Verificación sobre la base de datos en producción

Orden de ejecución: `modelo_datos_mysql_v2.sql` (crea base y 19 tablas con dimensiones conformes y de gobierno pobladas) → `esquema_estrella_powerbi.sql` (6 vistas) → `07_carga_datos_mysql.ipynb` (lee los 12 CSV, calcula las claves conformes fila a fila, aplica las reglas de calidad —exclusión de los 4 fragmentos corruptos '#NAME?' de Dreaddit y filtrado de edades inválidas en DASS-42— y carga 334.318 registros).

Sobre esa base se ejecutó el filtro exacto que la retroalimentación señalaba como imposible, **mujeres, de 18 a 25 años, con nivel de estrés Alto**, como una única consulta contra la vista de hechos:

| Bloque analítico | Dataset | Casos |
|---|---|---|
| Validación psicológica | DASS-42 | 6.799 |
| Factores internos | Student Anxiety GAD-7 | 224 |
| Factores internos | Student Habits vs Performance | 183 |
| Hábitos digitales | Social Media and Mental Health | 110 |
| Percepción emocional | Depression Student Dataset | 65 |
| Hábitos digitales | Mental Health Lifestyle | 51 |
| Factores internos | Student Mental Health Survey | 14 |
| **TOTAL** | 7 fuentes de los 4 bloques | **7.446** |

El filtro demográfico global opera de forma transversal sobre fuentes sin identificador común de persona. Las fuentes ausentes lo están por una razón documentada: Dreaddit es anónimo por diseño y el dataset de chanchal24 no registra edad, por lo que sus miembros conformes son "No reportado" y quedan fuera del filtro sin generar nulos ni errores.

## 7. Seguimiento: cómo se cumplieron los compromisos en el Objetivo 2

El notebook 09 materializa los puntos 3 y 4 sobre la propia estrella:

- **La política se aplica desde la base de datos.** Lee `uso_modelado` de `vw_dim_dataset` y modela solo las fuentes 'incluido': 8 tareas sobre 9 fuentes (Dreaddit train y test forman una tarea).
- **Cada modelo predice su variable nativa y se lee en la capa armonizada.** Los resultados se cargan en `dwh_modelo_resultados`, enlazada a dim_dataset por id_dataset, con la columna `lectura_capa_armonizada` (p. ej. GAD-7 ≥ 10 equivale a nivel Alto). Es la segunda tabla de hechos de la constelación de consumo.
- **Resultado.** En las fuentes con señal real el AUC del mejor modelo se sitúa entre 0,73 y 0,84: se puede anticipar el estrés mejor que el azar, no predecirlo con precisión individual.
- **Hallazgo de validez.** Depression Student alcanza AUC ≈ 0,998. Ninguna variable aislada supera 0,77, pero una combinación lineal reproduce la etiqueta casi sin error, patrón típico de etiquetas generadas por una fórmula. No se afirma que sea sintético, pero es un indicio serio: se reporta con cautela y se propone consultarlo con el tutor. Si se confirma, basta un UPDATE sobre `dim_dataset` (uso_modelado = 'excluido') para propagar la exclusión a la estrella, a Power BI y al notebook.

El detalle metodológico y los resultados están en el documento de síntesis del Objetivo 2.

## 8. Entregables y orden de ejecución definitivo

| Paso | Archivo | Herramienta | Qué hace |
|---|---|---|---|
| 1 | modelo_datos_mysql_v2.sql | phpMyAdmin | Crea la base `tfm_estres_estudiantil_2` y las 19 tablas (7 dimensiones + 12 hechos) |
| 2 | esquema_estrella_powerbi.sql (definitivo) | phpMyAdmin | Crea las 6 vistas de la estrella |
| 3 | 07_carga_datos_mysql.ipynb | Jupyter | Carga los 334.318 registros de los 12 datasets |
| 4 | modelo_dwh_mysql.sql | phpMyAdmin | Crea las 7 tablas del datawarehouse (Entrega 2) |
| 5 | 08_etl_transformaciones_kpis_v2.ipynb | Jupyter | Transformaciones T1-T5 y 6 KPIs con histórico |
| 6 | modelo_dwh_modelos.sql | phpMyAdmin | Crea dwh_modelo_resultados y la vista vw_modelo_resultados |
| 7 | 09_modelado_objetivo2.ipynb | Jupyter | Modelado (8 tareas), serialización y carga de resultados al DWH |

Entregables: `modelo_datos_mysql_v2.sql`; `modelo_datos_ERD_v2.png`; `esquema_estrella_powerbi.sql` y diagrama definitivo; `esquema_constelacion_powerbi.png` y `modelo_dwh_modelos.sql` (resultados del Objetivo 2 como segunda tabla de hechos); `06_armonizacion_dimensiones_conformes.ipynb` y `07_carga_datos_mysql.ipynb`; este documento (trazabilidad observación → acción → entregable → verificación).

---
<!-- relacionado -->
**Relacionado:** [Síntesis del Objetivo 1](01_sintesis_objetivo1_final.md) · [Seguimiento](../../SEGUIMIENTO.md)
