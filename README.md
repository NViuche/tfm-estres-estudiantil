# TFM — Análisis multidimensional del estrés estudiantil

Trabajo Final de Máster en Business Analytics e Inteligencia Artificial (UNIE / INESDI). Analiza el estrés estudiantil a partir de 12 datasets públicos organizados en 4 bloques: factores internos, hábitos digitales, percepción emocional y validación psicológica. Cada fuente se estudia por separado y todas se comparan a través de un constructo común de nivel de estrés (Bajo / Moderado / Alto), sobre un modelo en estrella en MySQL, notebooks de Python y Power BI (pendiente).

**Equipo:** Raúl Cervantes Iglesias, Santiago Nicolas Viuche Pinilla, Obed Isaí Alvarado Núñez, Roberto Mario Brochero López, Andrés Francisco García Grajales.

El problema, el enfoque, los objetivos y los hallazgos principales están en [`investigacion/problema.md`](investigacion/problema.md).

## Estructura

```
tfm-estres-estudiantil/
├── README.md
├── SEGUIMIENTO.md          retroalimentación del tutor por entrega, limitaciones y pendientes
├── investigacion/
│   └── problema.md         problema, enfoque, objetivos y hallazgos
├── data/
│   └── datasets/           fichas en Markdown de cada CSV original, por bloque (sin CSV)
├── sql/                    modelo MySQL v2, capa estrella para Power BI y DWH
├── notebooks/              EDA, calidad, armonización, ingesta, ETL/KPIs y modelado
├── modelos/                modelos entrenados (.pkl) con su metadata (.json)
├── resultados/             métricas del modelado
├── tests/
│   └── pruebas.md          reglas de calidad del dato y validación de la carga
├── figuras/                gráficos del EDA y del modelado, y diagramas ERD
└── docs/                   documentos entregados (Entrega 1 y Entrega 2)
```

| Carpeta | Contenido |
|---|---|
| `notebooks/` | `TFM_Notebook_Entrega1_y_Entrega2.ipynb` (notebook integrado de las entregas 1 y 2), EDA 01–04, reglas de calidad 05, armonización 06, ingesta 07, validación de la carga 07b, ETL/KPIs 08 y modelado 09 |
| `sql/` | `modelo_datos_mysql_v2.sql`, `esquema_estrella_powerbi_DEFINITIVO.sql`, `dwh_estrella.sql` |
| `docs/entrega1_objetivo1/` | Síntesis del Objetivo 1, diccionario de datos (Excel y Markdown), respuesta a la retroalimentación del tutor |
| `docs/entrega2_objetivo2/` | Síntesis de ETL y KPIs, definición de KPIs, síntesis del modelado |

## Fuentes de datos

Los CSV originales **no se incluyen** en el repositorio. Se descargan desde sus fuentes; la estructura, tipos, nulos y estadísticos de cada uno están en [`data/datasets/`](data/datasets/00_INDICE.md).

| Bloque | Dataset | Fuente |
|---|---|---|
| 1. Factores internos | Student Academic Stress Real World Dataset | [Kaggle](https://www.kaggle.com/datasets/poushal02/student-academic-stress-real-world-dataset) |
| 1. Factores internos | Student Mental Health Survey | [Kaggle](https://www.kaggle.com/datasets/abdullahashfaqvirk/student-mental-health-survey) |
| 1. Factores internos | Student Anxiety Dataset (GAD-7) | [Kaggle](https://www.kaggle.com/datasets/petalme/student-anxiety-dataset/data) |
| 1. Factores internos | Student Habits vs Academic Performance* | [GitHub](https://github.com/abhi88377/Student-Habits-vs-Academic-Performance/blob/main/student_habits_performance.csv) |
| 2. Hábitos digitales | Social Media Usage vs Sleep, Stress & Productivity* | [Kaggle](https://www.kaggle.com/datasets/jayjoshi37/social-media-usage-vs-sleep-stress-and-productivity) |
| 2. Hábitos digitales | Social Media and Mental Health | [Kaggle](https://www.kaggle.com/datasets/souvikahmed071/social-media-and-mental-health) |
| 2. Hábitos digitales | Mental Health Lifestyle* | [GitHub](https://github.com/datafit17/Mental_Health_Lifestyle) |
| 3. Percepción emocional | Stress Analysis in Social Media (Dreaddit, train y test) | [Kaggle](https://www.kaggle.com/datasets/payaldhokane/stress-analysis-in-social-media-dataset) |
| 3. Percepción emocional | Student Mental Health Analysis (Depression Student) | [GitHub](https://github.com/prajwalg26/Student_Mental_Health_Analysis) |
| 4. Validación psicológica | Depression Anxiety Stress Scales Responses (DASS-42) | [Kaggle](https://www.kaggle.com/datasets/lucasgreenwell/depression-anxiety-stress-scales-responses) |
| 4. Validación psicológica | Mental Health Dataset | [Kaggle](https://www.kaggle.com/code/chanchal24/mental-health-dataset/input) |

\* Datasets sintéticos: se usan en la capa descriptiva y se excluyen del modelado.

## Cómo ejecutarlo

Requisitos: Python 3 con Jupyter, y MySQL (probado con XAMPP; base de datos `tfm_estres_estudiantil_2`).

1. Descarga los CSV desde las fuentes de arriba y colócalos en `data/raw/`, un subdirectorio por bloque con la carpeta de cada dataset (p. ej. `data/raw/Bloque 1/1 Student anxiety dataset/anxiety.csv`; la ruta exacta de cada archivo está en su ficha de `data/datasets/`). Si tu MySQL tiene contraseña, ajusta `DB_PASS`.

   Los notebooks usan rutas relativas a `notebooks/`: leen los datos de `../data/raw` (`BASE`) y escriben lo que generan en `../salidas/objetivo1` o `../salidas/objetivo2` (`ALMC`). Ninguna de las dos carpetas se versiona. Ejecútalos con la carpeta `notebooks/` como directorio de trabajo (es lo habitual en Jupyter y VS Code).
2. `sql/modelo_datos_mysql_v2.sql`
3. `sql/esquema_estrella_powerbi_DEFINITIVO.sql`
4. Ingesta: `notebooks/07_carga_datos_mysql.ipynb` (o la sección B.1 del notebook integrado). Se ejecuta una sola vez; después, `07b_validacion_carga_datos.ipynb` comprueba la carga.
5. `sql/dwh_estrella.sql` (opcional; el notebook 08 crea las tablas si faltan)
6. ETL y KPIs: `notebooks/08_etl_transformaciones_kpis.ipynb` (o la sección B.2 del notebook integrado)
7. Modelado: `notebooks/09_modelado_objetivo2.ipynb`

El notebook 06 genera la capa armonizada (CSV) que no se versiona; se regenera al ejecutarlo.

## Versiones de los notebooks

Los notebooks que pasaron por varias versiones se guardan con un único nombre. Su evolución está en el historial de git: cada versión es un commit en una rama de trabajo, que después se fusionó en `main`.

| Rama | Notebook | Versiones (un commit cada una) |
|---|---|---|
| `entrega1/eda-calidad` | `01`–`04` EDA y `05_reglas_calidad_dato.ipynb` | inicial → final |
| `entrega2/etl-kpis` | `08_etl_transformaciones_kpis.ipynb` | v1 (reconstruida) → v2 → v3 → v4 |
| `notebook-integrado` | `TFM_Notebook_Entrega1_y_Entrega2.ipynb` | EDA de la Entrega 1 → Entregas 1 y 2 → versión final |

Para ver una versión anterior: `git log --oneline -- notebooks/<archivo>` y `git show <commit>:notebooks/<archivo>`, o desde la pestaña *History* del archivo en GitHub.

## Estado

- **Entrega 1 (EDA, calidad, modelo de datos) y Entrega 2 (ingesta, ETL, KPIs, modelado):** completadas. Se cargaron 334.318 filas; 319.318 pertenecen a las 9 fuentes incluidas en el modelado.
- **Entrega 3 (Power BI e insights):** pendiente.
