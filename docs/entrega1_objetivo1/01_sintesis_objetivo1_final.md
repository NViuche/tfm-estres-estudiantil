*Conversión a texto de `Sintesis objetivo 1 Final.docx` (versión final, 24 págs. en PDF). Las 13 figuras están en la carpeta `figurasObje1` del paquete y en el Word/PDF originales.*

*TRABAJO FINAL DE MÁSTER — Business Analytics e Inteligencia Artificial*

*Análisis multidimensional del estrés estudiantil mediante Business Analytics e Inteligencia Artificial con datos académicos, conductuales y textuales*

- *Andrés Francisco García Grajales*

- *Obed Isaí Alvarado Núñez*

- *Roberto Mario Brochero López*

- *Raúl Cervantes Iglesias*

- *Santiago Nicolas Viuche Pinilla*

# Desarrollo del Objetivo 1: Análisis Exploratorio y Descriptivo

Objetivo 1 (versión actualizada): Realizar un análisis exploratorio y descriptivo de múltiples datasets organizados en diferentes bloques analíticos (factores internos, hábitos digitales, percepción emocional y validación psicológica), con el fin de evaluar la calidad de cada fuente de datos e identificar patrones y relaciones entre variables académicas, comportamentales y niveles de estrés estudiantil.

## Metodología del análisis exploratorio de datos (EDA)

El análisis se aplicó sobre doce datasets organizados en cuatro bloques analíticos, manteniendo el enfoque de análisis en paralelo definido en la propuesta: cada dataset se estudió de forma independiente, sin integración entre fuentes, para extraer conclusiones desde perspectivas complementarias del mismo fenómeno.

A cada dataset estructurado se le aplicó una plantilla homogénea de cinco pasos, lo que garantiza la comparabilidad de resultados entre bloques:

1.  Carga e inventario: dimensiones, tipos de variables, diccionario de datos y particularidades de lectura (codificación de caracteres, separadores).

2.  Calidad de datos: detección de nulos, duplicados, valores anómalos y columnas redundantes, con decisión documentada para cada incidencia.

3.  Análisis univariante: distribución de la variable objetivo (nivel de estrés, depresión o ansiedad según el dataset) y de las variables explicativas principales.

4.  Análisis bivariante: correlaciones de Pearson para variables numéricas y ordinales, tablas de contingencia para categóricas, siempre respecto a la variable de malestar psicológico.

5.  Síntesis de hallazgos: tres a cinco conclusiones por dataset, incluida la evaluación de su calidad y valor explicativo.

Para el corpus textual del Bloque 3 (Dreaddit) los pasos 3 y 4 se adaptaron al análisis de texto: balance de clases, longitud de los posts, distribución por subreddit de origen y comparación de señales léxicas (sentimiento y categorías del diccionario psicolingüístico LIWC) entre las clases estrés y no-estrés.

Todo el análisis se implementó en Python 3 (pandas, matplotlib, seaborn) mediante cuatro scripts reproducibles —uno por bloque— que generan automáticamente las trece figuras del capítulo, complementados por un quinto script que formaliza las reglas de calidad del dato. Los cinco se entregan también como notebooks de Jupyter documentados celda a celda, con explicaciones dirigidas tanto a público técnico como no técnico. La estructura de carpetas del repositorio replica la organización por bloques del inventario de datos.

| Script/Notebook                       | Contenido                                                                                                                                      |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| 01_eda_bloque1_factores_internos      | EDA de 4 datasets: estrés académico, ansiedad GAD-7, encuesta de salud mental, hábitos vs rendimiento. Genera 4 figuras.                       |
| 02_eda_bloque2_habitos_digitales      | EDA de 3 datasets: uso de redes/sueño/productividad, SMMH, estilo de vida. Genera 3 figuras.                                                   |
| 03_eda_bloque3_percepcion_emocional   | EDA textual de Dreaddit (train+test) y perfil estructurado complementario. Genera 3 figuras.                                                   |
| 04_eda_bloque4_validacion_psicologica | Cálculo de subescalas DASS-42 según codebook oficial, desagregación demográfica y análisis de búsqueda de tratamiento. Genera 3 figuras.       |
| 05_reglas_calidad_dato                | 49 reglas de calidad formalizadas como código, con estado OK/AVISO/ERROR y acción correctiva por regla. Exporta el cuadro de resultados a CSV. |

## Bloque 1 — Factores Internos (Core del Estrés)

Este bloque agrupa cuatro datasets centrados en variables internas del estudiante: percepción del estrés académico, ansiedad medida con escalas clínicas, salud mental universitaria y relación entre hábitos personales y rendimiento.

| Dataset                                       | N                   | variable objetivo           | hallazgo principal                                                                                  |
|-----------------------------------------------|---------------------|-----------------------------|-----------------------------------------------------------------------------------------------------|
| 1.1 Academic Stress (poushal02)               | 140                 | Índice estrés 1-5           | Más del 60% reporta estrés en niveles 4-5; la etapa de grado concentra la mayor parte de la muestra |
| 1.2 Anxiety GAD-7 (petalme)                   | 13.464 (9.302 est.) | GAD_T (0-21)                | Ansiedad correlaciona -0.40 con satisfacción vital y +0.44 con ansiedad social                      |
| 1.3 Mental Health Survey (abdullahashfaqvirk) | 87                  | depression, anxiety (1-5)   | Aislamiento social: r=0.71 con depresión; carga académica: r=0.38                                   |
| 1.4 Student Habits (abhi88377)                | 1000                | mental_health_rating (1-10) | Sin correlación con hábitos (r≈0): datos sintéticos en la dimensión de salud mental                 |

### Análisis de bloque:

Los tres datasets con señal real convergen en que la presión académica y el aislamiento social son los predictores internos más consistentes del malestar psicológico. En el dataset de estrés académico (1.1), más del 60 % de los estudiantes se sitúa en los dos niveles más altos de la escala, y la presión de pares se asocia a mayores índices de estrés.

El dataset de ansiedad (1.2) aporta la mayor muestra del bloque y tres escalas clínicamente validadas: GAD-7 (ansiedad generalizada), SWL (satisfacción con la vida) y SPIN (ansiedad social). En el subconjunto estudiantil (n=9.302), la ansiedad correlaciona negativamente con la satisfacción vital (r=−0.40) y positivamente con la ansiedad social (r=+0.44), un patrón robusto y coherente con la literatura clínica que valida la calidad de la fuente. Aplicando los umbrales clínicos del GAD-7, cerca de la mitad del subconjunto presenta ansiedad mínima, pero una proporción relevante alcanza niveles moderados o severos. Cabe documentar que el contexto original del dataset es población de jugadores online; el subconjunto estudiantil es válido para el análisis con esa salvedad.

La encuesta de salud mental universitaria (1.3) es la fuente más rica en correlaciones: el aislamiento social es el predictor más fuerte de la depresión de todo el proyecto (r=0.71), seguido de la inseguridad ante el futuro (r=0.47) y la carga académica (r=0.38); la satisfacción con los estudios actúa como factor protector.

### Gráficas por dataset:

#### Bloque 1:

##### academic Stress level - maintainance 1.csv

<img src="media/image1.png" style="width:6.1375in;height:2.14514in" />

Figura 1. Ejecución academic Stress level - maintainance 1

Distribución del índice de estrés académico (\$n=140\$)

- Contexto: Histograma de frecuencias que evalúa la percepción subjetiva del estrés en una muestra de 140 estudiantes mediante una escala de Likert (1=bajo, 5=alto).

- Interpretación: La distribución muestra una marcada asimetría negativa (sesgada a la derecha). La mayor concentración de la muestra se sitúa en los niveles 4 (más de 50 estudiantes) y 3, evidenciando que una amplia mayoría de la población estudiantil percibe su nivel de estrés en rangos de moderado a severo. Los niveles bajos (1 y 2) presentan una representatividad marginal.

Estrés por etapa académica

- Contexto: Diagrama de caja (boxplot) que contrasta la dispersión del índice de estrés según el nivel de instrucción (undergraduate, high school, post-graduate).

- Interpretación: Los niveles de mediana son equivalentes en las tres etapas (fijados en 4.0), denotando que la presión es transversal al nivel educativo. No obstante, el grupo de high school exhibe una mayor variabilidad en sus respuestas (ocupando todo el espectro del 1 al 5), mientras que en post-graduate el estrés se homogeniza en la parte alta de la escala, eliminando puntuaciones bajas y consolidando un sesgo de malestar crónico

##### anxiety.csv

<img src="media/image2.png" style="width:6.1375in;height:2.14792in" />

Figura 2. Ejecución anxiety.csv

Distribución GAD_T — ansiedad (estudiantes, \$n=9302\$)

- Contexto: Histograma probabilístico de la puntuación total de la escala GAD-7 (herramienta clínica para medir el Trastorno de Ansiedad Generalizada) en una submuestra depurada de 9,302 estudiantes.

- Interpretación: Se observa una curva con declinación exponencial, concentrando las frecuencias más altas en puntajes de 0 a 5 (ansiedad mínima a leve). Sin embargo, la persistencia de la cola derecha confirma un porcentaje significativo de la población estudiantil que puntúa en rangos de ansiedad moderada (6-14) y severa (15-21), requiriendo atención o seguimiento clínico.

Ansiedad vs. Satisfacción con la vida (\$r = -0.40\$)

- Contexto: Gráfico de dispersión (scatterplot) que evalúa la relación entre la puntuación GAD-7 (ansiedad) y el indicador SWL_T (Satisfacción con la Vida).

- Interpretación: El coeficiente de correlación de Pearson (\$r = -0.40\$) formaliza una relación lineal inversa moderada. Estadísticamente demuestra que a medida que los síntomas de ansiedad generalizada se agudizan, la percepción de la satisfacción vital de los estudiantes sufre un detrimento proporcional, corroborando el impacto directo de la salud mental en el bienestar global del individuo.

##### MentalHealthSurvey.csv

<img src="media/image3.png" style="width:6.1375in;height:4.90694in" />

Figura 3. Ejecución MentalHealthSurvey.csv

Matriz de Correlación de Factores de Salud Mental

- Contexto: Un mapa de calor (heatmap) que evalúa la fuerza y dirección de las relaciones lineales (Coeficiente de Pearson) entre variables psicométricas y académicas.

- Interpretación: Existe una correlación positiva fuerte y crítica (\$r \approx 0.6\$ a \$0.8\$) en el bloque de indicadores de malestar: depression, anxiety, isolation (aislamiento) y future_insecurity. Esto confirma que estas condiciones coexisten y se retroalimentan sintomáticamente. Por otro lado, la variable academic_pressure muestra correlaciones positivas moderadas con este bloque, mientras que la satisfacción con el estudio (study_satisfaction) presenta una relación inversa (negativa), validando que a mayor bienestar psicológico y menor presión, la percepción del desempeño académico mejora.

##### student_habits_performance.csv

<img src="media/image4.png" style="width:6.1375in;height:2.14792in" />

Figura 4. Ejecución student_habits_performance.csv

mental_health_rating: distribución uniforme

- Contexto: Histograma que analiza la variable del estado autopercibido de la salud mental en una escala del 1 al 10 (\$n=1000\$).

- Interpretación: La gráfica muestra una distribución uniforme perfecta. En términos metodológicos y de auditoría de datos, este comportamiento no es natural en muestras biológicas o psicológicas reales (donde se esperaría una distribución normal o asimétrica). Como bien lo indica el título del gráfico original, esto constituye un indicio estadístico inequívoco de que esta variable en particular proviene de un conjunto de datos sintéticos o generados algorítmicamente.

Impacto de las Horas de Estudio en el Rendimiento Académico

- Contexto: Un gráfico de dispersión (scatterplot) con una línea de tendencia que correlaciona las horas de estudio diarias con la calificación final del examen (exam_score).

- Interpretación: La visualización exhibe una relación lineal positiva y robusta. A medida que incrementan las horas de estudio dedicadas por día, el exam_score se eleva de forma sostenida, convergiendo cerca del puntaje máximo (100) al superar las 6 o 7 horas. La baja dispersión de los puntos alrededor de la recta de regresión denota que el tiempo de estudio efectivo es un predictor altamente confiable y de gran peso específico para el éxito cuantitativo del estudiante.

## Bloque 2 — Factores Externos (Hábitos Digitales)

> Este bloque analiza la relación entre el uso de redes sociales, el estilo de vida digital y el bienestar psicológico desde tres fuentes complementarias.

| Dataset                                    | N      | variable objetivo          | hallazgo principal                                                                    |
|--------------------------------------------|--------|----------------------------|---------------------------------------------------------------------------------------|
| 2.1 Social Media/Sleep/Stress (jayjoshi37) | 11.000 | stress_level (3 niveles)   | Correlaciones ≤0.02 y clases exactamente balanceadas: datos sintéticos                |
| 2.2 SMMH (souvikahmed071)                  | 481    | Sentirse deprimido/a (1-5) | Preocupación: r=0.59; dificultad de concentración: r=0.51; comparación social: r=0.42 |
| 2.3 Mental Health Lifestyle (datafit17)    | 3.000  | Stress Level (3 niveles)   | Correlaciones ≈0 con todas las variables de estilo de vida: datos sintéticos          |

### Análisis de bloque:

La fuente con valor inferencial real de este bloque es la encuesta SMMH (2.2). Su hallazgo central es que no es el tiempo total de uso de redes sociales lo que predice el malestar, sino la calidad del patrón de uso: las correlaciones más altas con sentirse deprimido/a corresponden a la preocupación excesiva (r=0.59), la dificultad de concentración (r=0.51) y la fluctuación del interés en actividades cotidianas (r=0.49), todas indicadoras de un uso ansioso o compulsivo. La comparación social a través de redes muestra asociación moderada (r=0.42), y los problemas de sueño vinculados al uso (r=0.37) trazan un puente con la fatiga académica documentada en el Bloque 1: uso problemático → peor sueño → mayor malestar percibido.

### Gráficas por Dataset:

#### Bloque 2:

##### social_media_sleep_stress_productivity_11000.csv

<img src="media/image5.png" style="width:6.1375in;height:2.14792in" />

Figura 5. Ejecución social_media_sleep_stress_productivity_11000.csv

stress_level perfectamente balanceado (n=11.000)

- Contexto: Gráfico de barras que contabiliza los registros en cada nivel de estrés (Low, Medium, High) sobre el total de 11.000 usuarios del dataset.

- Interpretación: Las tres categorías presentan frecuencias prácticamente idénticas (~33% cada una), un reparto que no ocurre en poblaciones reales, donde los niveles de estrés se distribuyen de forma asimétrica. Esta uniformidad perfecta constituye, en términos de auditoría de datos, el primer indicio de generación sintética de la variable objetivo.

Correlaciones ≈ 0 en todas las variables

- Contexto: Mapa de calor (heatmap) con el coeficiente de Pearson entre las variables numéricas del dataset (edad, horas de pantalla, redes, sueño, ejercicio, estudio/trabajo, productividad) y el nivel de estrés codificado ordinalmente (stress_ord).

- Interpretación: Fuera de la diagonal, todos los coeficientes se sitúan entre −0.02 y +0.02: ninguna variable guarda relación lineal con ninguna otra. Las horas de redes sociales, el sueño o el ejercicio no aportan información alguna sobre el estrés reportado. Junto con el balance artificial del panel izquierdo, confirma que la fuente carece de valor inferencial y se restringe a uso técnico (validación de pipelines y dashboards de volumen), documentando la ausencia de asociación como hallazgo legítimo del EDA.

##### smmh.csv

<img src="media/image6.png" style="width:6.1375in;height:3.83611in" />

Figura 6. Ejecución smmh.csv

Correlación con «sentirse deprimido/a» (n=481)

- Contexto: Gráfico de barras horizontales donde cada barra representa el coeficiente de Pearson entre un comportamiento digital (escala Likert 1-5) y la frecuencia con la que el encuestado declara sentirse deprimido o decaido.

- Interpretación: Emerge un gradiente claro y clínicamente coherente: la preocupación excesiva encabeza la relación (r=0.59), seguida de la dificultad de concentración (r=0.51) y la fluctuación del interés en actividades cotidianas (r=0.49); en el tramo intermedio se sitúan la comparación social (r=0.42) y la distracción fácil (r=0.41), y cierran los problemas de sueño (r≈0.37) y el uso sin propósito (r≈0.33). El hallazgo central del bloque se formaliza aquí: no es el tiempo total de exposición a las redes lo que se asocia al malestar, sino el patrón de uso ansioso, compulsivo y comparativo. Es la única fuente del bloque con señal real y sustenta las conclusiones sustantivas del mismo.

##### Mental_Health_Lifestyle_Dataset.csv

<img src="media/image7.png" style="width:6.1375in;height:2.14792in" />

Figura 7. Ejecución Mental_Health_Lifestyle_Dataset.csv

Condición de salud mental (n=3.000)

- Contexto: Gráfico de barras que contabiliza los registros por condición de salud mental declarada (Ansiedad, TEPT, Depresión, Bipolar y la categoría 'Ninguna', producto de la recodificación de los NaN semánticos).

- Interpretación: Las cinco categorías presentan frecuencias casi idénticas (~570-630 registros), un equilibrio incompatible con la prevalencia real de estos diagnósticos en cualquier población, donde unos trastornos son sensiblemente más frecuentes que otros. Se repite el patrón de asignación aleatoria uniforme observado en el dataset 2.1.

Horas de sueño por nivel de estrés

- Contexto: Diagrama de caja (boxplot) que contrasta la distribución de horas de sueño entre los tres niveles de estrés (Low, Moderate, High).

- Interpretación: Las tres cajas son prácticamente idénticas en mediana y dispersión: dormir más o menos no discrimina el nivel de estrés en estos datos, en contradicción con la evidencia clínica consolidada sobre la relación sueño-estrés. Refuerza la clasificación de la fuente como sintética: se documenta como limitación y su uso queda restringido al plano técnico (segmentaciones multi-país en los dashboards del Objetivo 3), sin extraer de ella conclusiones sobre el estrés real.

## Bloque 3 — Percepción Emocional (IA / NLP)

Este bloque aborda el estrés desde el lenguaje: analiza texto real escrito por usuarios en Reddit (corpus Dreaddit) y lo complementa con un perfil estructurado del malestar estudiantil.

| Dataset                                | N           | variable objetivo   | hallazgo principal                                                                                                  |
|----------------------------------------|-------------|---------------------|---------------------------------------------------------------------------------------------------------------------|
| 3.1 Dreaddit train+test (payaldhokane) | 2.838 + 715 | label estrés (0/1)  | Palabras de ansiedad LIWC ×2.5 en clase estrés; sentimiento +0.10 vs −0.02                                          |
| 3.2 Depression Student (prajwalg26)    | 502         | Depression (Yes/No) | 73% de quienes reportan pensamientos suicidas presentan depresión; presión académica +57% en el grupo con depresión |

### Análisis de bloque:

El corpus Dreaddit (3.1) es la fuente textual del proyecto: 2.838 fragmentos de posts de Reddit etiquetados manualmente como estresantes (n=1.488) o no estresantes (n=1.350), un balance prácticamente óptimo para clasificación. El EDA textual revela señales discriminantes claras antes de entrenar ningún modelo: el sentimiento medio es positivo en los posts sin estrés (+0.103) y ligeramente negativo en los posts con estrés (−0.016), y la densidad de palabras asociadas a ansiedad según el diccionario LIWC es 2.5 veces mayor en la clase estrés (1.28 vs 0.51). La emoción negativa también discrimina entre clases, y la positiva es mayor en los posts sin estrés.

El corpus incluye 116 variables derivadas (107 categorías LIWC, índices del Diccionario de Afecto y métricas de legibilidad), lo que permitirá en el Objetivo 2 comparar un modelo basado en estas features psicolingüísticas con otro que genere sus propias representaciones del texto (TF-IDF, embeddings). Los subreddits dominantes (ptsd, relationships, anxiety) indican que el estrés capturado es de naturaleza mayormente relacional y clínica; esta salvedad se considerará al generalizar los resultados al contexto estrictamente académico.

El dataset complementario (3.2) aporta el vínculo más crítico del proyecto entre malestar y riesgo: el 73 % de los estudiantes que reportan pensamientos suicidas presenta depresión, frente al 26 % de quienes no los reportan. La presión académica media es un 57 % mayor en el grupo con depresión (3.66 vs 2.34) y el estrés financiero muestra el mismo patrón. Con un target balanceado (252/250), es un candidato idóneo para los modelos de clasificación del Objetivo 2.

### Gráficas por Dataset:

#### Bloque 3:

##### dreaddit-train.csv + dreaddit-test.csv

<img src="media/image8.png" style="width:6.1375in;height:1.71875in" />

Figura 8. Ejecución dreaddit-train.csv + dreaddit-test.csv

Balance de clases (train, n=2.838)

- Contexto: Gráfico de barras que contabiliza los fragmentos del conjunto de entrenamiento en cada clase: No estrés (0) y Estrés (1).

- Interpretación: El corpus está prácticamente balanceado (1.350 sin estrés frente a 1.488 con estrés). La ausencia de desbalance reduce el riesgo de que el clasificador del Objetivo 2 favorezca una clase sobre otra y permite emplear métricas como la exactitud (Accuracy) sin sesgo relevante.

Sentimiento por clase

- Contexto: Diagrama de caja que compara la distribución del puntaje de sentimiento (polaridad del texto, de -1 a +1) entre ambas clases.

- Interpretación: La clase sin estrés presenta una mediana ligeramente positiva y la clase con estrés una mediana cercana a cero o ligeramente negativa, con amplia dispersión y valores atípicos en ambos grupos. Pese al solapamiento considerable, los textos de estrés tienden a expresar emociones más negativas: el sentimiento aporta información útil para clasificar, aunque por sí solo no basta para distinguir las clases.

Densidad de palabras de ansiedad (LIWC)

- Contexto: Gráfico de barras que compara, entre clases, el porcentaje medio de palabras del post pertenecientes a la categoría 'ansiedad' del diccionario psicolingüístico LIWC.

- Interpretación: Es la señal más discriminante del EDA textual: los posts con estrés alcanzan una densidad de 1.28 frente a 0.51 en los posts sin estrés, aproximadamente 2.5 veces más vocabulario de ansiedad, preocupación, miedo y tensión emocional. Anticipa que las categorías léxicas serán predictores fuertes en el modelado.

<img src="media/image9.png" style="width:6.1375in;height:2.14792in" />

Figura 9. Ejecución dreaddit-train.csv + dreaddit-test.csv

Longitud de los posts por clase

- Contexto: Histograma que compara el número de palabras por publicación entre las dos clases.

- Interpretación: Ambas distribuciones son similares, con una ligera tendencia de la clase estrés a publicaciones más largas (media 88.8 vs 82.2 palabras) y una cola derecha más pronunciada: quienes manifiestan estrés tienden a explicar su situación con más detalle. La diferencia, no obstante, es insuficiente para considerar la longitud un predictor principal.

Posts por subreddit de origen

- Contexto: Gráfico de barras horizontales con el número de fragmentos aportados por cada una de las diez comunidades (subreddits) de origen.

- Interpretación: Dominan ptsd (584), relationships (552) y anxiety (503), seguidas de comunidades sobre violencia doméstica, abuso y precariedad. El corpus procede de espacios donde es frecuente la manifestación de malestar psicológico, lo que aporta variabilidad temática; a la vez, indica que el estrés capturado es de naturaleza mayormente relacional y clínica, salvedad que debe considerarse al generalizar los modelos al contexto estrictamente académico.

##### Depression+Student+Dataset.csv

<img src="media/image10.png" style="width:6.1375in;height:2.14792in" />

Figura 10. Ejecución Depression+Student+Dataset.csv

% con depresión según pensamientos suicidas

- Contexto: Gráfico de barras que compara el porcentaje de estudiantes con depresión entre quienes reportan y no reportan pensamientos suicidas (n=502).

- Interpretación: La diferencia es muy marcada: cerca del 73% de quienes reportan pensamientos suicidas presentan depresión, frente al 26% de quienes no los reportan —casi el triple de probabilidad—. La asociación es consistente con la literatura clínica y constituye el indicador de riesgo más relevante del dataset.

Presión académica según depresión

- Contexto: Diagrama de caja que contrasta el nivel de presión académica (escala 1-5) entre estudiantes con y sin depresión.

- Interpretación: Las medianas difieren con claridad (≈2 sin depresión frente a ≈4 con depresión) y los valores del grupo con depresión son sistemáticamente superiores, con cierto solapamiento. La gráfica no establece causalidad, pero evidencia que mayores niveles de presión académica se asocian con mayor frecuencia de depresión, en línea con el patrón transversal del proyecto.

## Bloque 4 — Validación Psicológica

Este bloque ancla los hallazgos de los bloques anteriores en instrumentos clínicamente validados. La escala DASS-42 se calculó siguiendo el codebook oficial incluido con el dataset, que define la asignación de los 42 ítems a las tres subescalas y los códigos de las variables demográficas.

| Dataset                                | N                       | variable objetivo              | hallazgo principal                                                                                            |
|----------------------------------------|-------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------------|
| 4.1 DASS-42 (lucasgreenwell)           | 39.775 → 23.031 (18-25) | Subescalas Dep/Anx/Str (14-56) | Mujeres: ansiedad 31.0 vs hombres 28.1; a menor nivel educativo, mayor malestar                               |
| 4.2 Mental Health dataset (chanchal24) | 261.328 → 54.207 est.   | Treatment, IncreasingStress    | El estrés creciente no eleva la búsqueda de tratamiento (48-51%); los antecedentes familiares sí (72% vs 35%) |

### Análisis de bloque:

El DASS-42 (4.1) aporta la referencia normativa más robusta del proyecto: 39.775 respuestas válidas (2017-2019), de las que 23.031 corresponden al rango 18-25 años, adoptado como proxy de población estudiantil. Las medias de las subescalas en este subconjunto (Depresión 35.0, Ansiedad 30.4, Estrés 35.2, en escala 14-56) sitúan a la población joven en el rango de malestar moderado-alto, coherente con los niveles de estrés autoreportados en los Bloques 1 y 2.

La desagregación demográfica —posible gracias a los códigos del codebook oficial— confirma dos patrones bien documentados en la literatura: las mujeres reportan mayor ansiedad media que los hombres (31.0 vs 28.1) y las personas del grupo de género “Otro” presentan el mayor malestar en las tres subescalas, lo que señala colectivos prioritarios para la intervención. Asimismo, a menor nivel educativo completado, mayores puntuaciones en las tres dimensiones.

El dataset masivo de chanchal24 (4.2), filtrado a estudiantes (n=54.207), aporta el hallazgo con mayor implicación práctica del bloque: la probabilidad de buscar tratamiento apenas varía con el nivel de estrés creciente (48-51 % en todas las categorías), lo que sugiere una brecha de acceso o estigma —el malestar no se traduce en búsqueda de ayuda—. En contraste, los antecedentes familiares de enfermedad mental sí duplican la búsqueda de tratamiento (72.4 % vs 35.1 %), probablemente por mayor familiaridad y normalización del cuidado de la salud mental en esos hogares.

### Gráficas por Dataset:

#### Bloque 4:

##### data.csv (DASS-42)

<img src="media/image11.png" style="width:6.1375in;height:2.15972in" />

Figura 11. Ejecución data.csv (DASS-42)

Subescalas DASS-42, subset 18-25 años (n=23.039)

- Contexto: Tres histogramas con la distribución de las puntuaciones (rango 14-56) de las subescalas Depresión, Ansiedad y Estrés en el subconjunto de 18-25 años, proxy de población estudiantil; la línea discontinua marca la media de cada una (35.0, 30.4 y 35.2).

- Interpretación: Cada dimensión presenta una forma característica. Ansiedad muestra una asimetría positiva clara: la mayoría se concentra en puntuaciones bajas-moderadas (pico en ≈22-28) con una cola derecha de casos elevados. Estrés exhibe una distribución aproximadamente simétrica centrada en valores medios-altos (pico en ≈33-38), confirmando que es la dimensión de malestar más extendida en la población joven. Depresión se reparte de forma casi plana en todo el rango con un pico llamativo en el valor máximo (efecto techo): un subgrupo no despreciable alcanza la puntuación más alta posible, perfil que requeriría atención clínica prioritaria. En conjunto, la mayoría se sitúa en rangos leves-moderados, pero las colas superiores de las tres subescalas identifican proporciones relevantes con malestar severo.

<img src="media/image12.png" style="width:6.1375in;height:1.92431in" />

Figura 12. Ejecución data.csv (DASS-42)

DASS medio por género

- Contexto: Gráfico de barras agrupadas con la puntuación media de cada subescala (Depresión, Ansiedad, Estrés) por género, usando las etiquetas del codebook oficial (Hombre, Mujer, Otro).

- Interpretación: Las mujeres puntúan por encima de los hombres en las tres dimensiones (ansiedad 31.0 vs 28.1), brecha de género bien documentada en la literatura de salud mental universitaria. El grupo 'Otro' presenta el mayor malestar en las tres subescalas —especialmente en Depresión (40.2)—, emergiendo como perfil de especial vulnerabilidad y colectivo prioritario para la intervención.

DASS medio por nivel educativo

- Contexto: Gráfico de barras agrupadas con la media de cada subescala según el nivel educativo completado (Menos que secundaria, Secundaria, Grado universitario, Posgrado).

- Interpretación: Se observa un gradiente educativo descendente en las tres dimensiones: a menor nivel educativo completado, mayor malestar (la Depresión cae de ≈39 en 'Menos que secundaria' a ≈34 en los niveles universitarios). El grupo 'Menos que secundaria' concentra las puntuaciones más altas de las tres subescalas, lo que sugiere que el nivel educativo actúa como factor protector indirecto —probablemente mediado por edad, recursos y estabilidad—.

##### Mental Health dataset1.csv

<img src="media/image13.png" style="width:6.1375in;height:2.15972in" />

Figura 13. Ejecución Mental Health dataset1.csv

Tratamiento según estrés creciente (estudiantes, n=54.207)

- Contexto: Gráfico de barras apiladas al 100% que muestra, para cada categoría de estrés creciente (Yes / No / Maybe), qué porcentaje de estudiantes ha buscado tratamiento psicológico.

- Interpretación: El resultado es un no-hallazgo muy informativo: la proporción que busca tratamiento permanece prácticamente constante (48-51%) en las tres categorías —percibir más estrés no se traduce en mayor búsqueda de ayuda—. Esta desconexión entre malestar percibido y conducta de búsqueda sugiere una brecha de acceso o estigma, y fundamenta el patrón transversal 6.4 de la síntesis: el valor de detectar el estrés por vías indirectas (lenguaje, comportamiento digital) cuando la autodeclaración no desemboca en ayuda profesional.

Tratamiento según antecedentes familiares

- Contexto: Gráfico de barras apiladas al 100% que compara el porcentaje que busca tratamiento entre estudiantes con y sin antecedentes familiares de enfermedad mental.

- Interpretación: En contraste con el panel anterior, aquí la asociación es fuerte: los antecedentes familiares duplican con creces la búsqueda de tratamiento (72.4% frente a 35.1%). La familiaridad con la salud mental en el entorno cercano —mayor reconocimiento de síntomas y normalización del cuidado— parece pesar más en la decisión de buscar ayuda que la propia intensidad del malestar, reforzando la interpretación de la brecha como fenómeno cultural y de acceso, no de necesidad clínica.

## Síntesis transversal entre bloques

El análisis en paralelo permite identificar cuatro patrones que emergen de forma consistente en las fuentes con señal real, sin necesidad de fusionar datos:

### La presión académica es el eje central del estrés estudiantil

El Bloque 1 la identifica como predictor interno estable (r=0.38 con depresión y ansiedad; más del 60 % de estudiantes en niveles altos de estrés). El Bloque 3 cuantifica su magnitud (+57 % de presión académica en el grupo con depresión) y el Bloque 4 confirma que los niveles de malestar de la población joven se sitúan en el rango moderado-alto de una escala clínica normativa.

### El aislamiento social y el uso ansioso de redes median el malestar

El aislamiento social es el predictor más fuerte de todo el proyecto (r=0.71, Bloque 1). El Bloque 2 lo complementa: no es el tiempo en redes sino el patrón de uso —preocupación (r=0.59), comparación social (r=0.42)— lo que se asocia al malestar, sugiriendo que las redes amplifican el aislamiento percibido cuando el uso es pasivo y comparativo.

### El lenguaje refleja el estrés de forma detectable

El Bloque 3 demuestra que los posts de usuarios bajo estrés contienen 2.5 veces más vocabulario de ansiedad y un tono emocional significativamente más negativo. Esto habilita la detección temprana del estrés a partir de texto cotidiano —objetivo del modelado NLP del Objetivo 2— y conecta con el hallazgo 6.4.

### Existe una brecha entre el malestar y la búsqueda de ayuda

El Bloque 4 muestra que el estrés creciente no aumenta la búsqueda de tratamiento en estudiantes, mientras que la familiaridad con la salud mental (antecedentes familiares) sí la duplica. Combinado con 6.3, este hallazgo justifica el valor práctico del proyecto: detectar el estrés por vías indirectas (lenguaje, comportamiento digital) puede llegar donde la autodeclaración y la búsqueda espontánea de ayuda no llegan.

En conjunto, los cuatro patrones describen un ciclo: la presión académica genera malestar que se expresa en el lenguaje digital, se agrava con el aislamiento y el uso problemático de redes, y rara vez desemboca en búsqueda de ayuda profesional. Este marco, derivado del EDA y no de hipótesis previas, orienta los modelos del Objetivo 2 y los indicadores de los dashboards del Objetivo 3.

## Evaluación de calidad y decisiones de preprocesamiento

Conforme a la versión actualizada del Objetivo 1, la evaluación de la calidad de cada fuente es un resultado explícito de esta fase. Las incidencias detectadas en el EDA se formalizaron posteriormente como 49 reglas de calidad ejecutables (sección 8.2), cuya ejecución añadió dos hallazgos que el análisis exploratorio no había capturado: el distinto orden de columnas entre las particiones de Dreaddit y la presencia de textos corruptos en el corpus. La siguiente tabla consolida las decisiones adoptadas:

| Dataset                     | Incidencia detectada                                                                                                                     | Decisión aplicada                                                                                                                                                |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1.1 Academic Stress         | Espacios en nombres de columnas; 1 nulo                                                                                                  | Normalización de nombres (strip); nulo sin impacto                                                                                                               |
| 1.2 Anxiety                 | Codificación latin1; contexto no académico                                                                                               | Lectura con encoding latin1; filtro por Work==Student documentado                                                                                                |
| 1.3 Mental Health Survey    | cgpa y average_sleep como rangos de texto                                                                                                | Pendiente Objetivo 2: recodificar a ordinal                                                                                                                      |
| 1.4 Student Habits          | 91 nulos (9.1%) en parental_education_level; señal sintética en salud mental                                                             | Imputación por moda o exclusión en Objetivo 2; uso restringido a validación técnica                                                                              |
| 2.1 Social Media/Sleep      | Sin señal real (r≤0.02); clases balanceadas artificialmente                                                                              | Codificación ordinal Low/Medium/High → 0/1/2; uso técnico                                                                                                        |
| 2.2 SMMH                    | 30 nulos en columna de organización; plataformas como multi-selección                                                                    | Sin impacto; pendiente Objetivo 2: dummies por plataforma                                                                                                        |
| 2.3 Mental Health Lifestyle | 595 NaN (19.8%) en Mental Health Condition; sin señal real                                                                               | NaN recodificados como 'Ninguna' (ausencia de diagnóstico); uso técnico                                                                                          |
| 3.1 Dreaddit                | 4 posts con texto '#NAME?' (celdas corruptas de Excel en la fuente); train y test con mismo conjunto de 116 columnas pero distinto orden | Excluir los 4 fragmentos corruptos del corpus NLP (regla R7); alinear columnas por nombre antes del modelado (regla R6); partición train/test original respetada |
| 3.2 Depression Student      | Sin nulos ni duplicados                                                                                                                  | Sin limpieza necesaria                                                                                                                                           |
| 4.1 DASS-42                 | Edades inválidas (valores tipo año); separador TAB; respuestas que marcan palabras inexistentes (VCL6/9/12)                              | Filtro a rango 13-90 (8 registros eliminados); lectura con sep tab; subescalas según codebook oficial; control de validez VCL documentado como regla             |
| 4.2 Mental Health dataset   | Columna SocialWeakness.1 duplicada; 4.356 nulos en SelfEmployed                                                                          | Columna duplicada eliminada; filtro Occupation==Student para todos los análisis                                                                                  |

Con esta evaluación, el proyecto distingue explícitamente entre fuentes con valor inferencial (1.1, 1.2, 1.3, 2.2, 3.1, 3.2, 4.1, 4.2) y fuentes con valor exclusivamente técnico (1.4, 2.1, 2.3), decisión que condiciona el peso de cada dataset en los Objetivos 2 y 3.

## Entregables Objetivo 1

Además del análisis documentado en las secciones anteriores, la Entrega 1 exige cuatro productos concretos: diccionario de datos, perfilado en notebook, reglas de calidad implementadas en Python y modelo de datos en MySQL. Todos fueron generados y verificados:

### Diccionario de datos (Excel)

El fichero Diccionario_de_Datos_TFM.xlsx contiene 13 hojas: una hoja índice con el inventario completo (bloque, fuente, filas, columnas, nulos totales, duplicados y descripción de cada dataset) y una hoja de perfilado por dataset con todas sus columnas: tipo de dato, valores no nulos y nulos (con porcentaje resaltado cuando existe algún nulo), valores únicos, mínimo, máximo y media para variables numéricas, los tres valores más frecuentes para categóricas, y la descripción del significado de cada atributo junto con la regla de calidad a vigilar. Las 172 columnas del DASS-42 y las 116 de Dreaddit se documentaron mediante descripciones generadas por patrón (ítems Q1A-Q42A, inventario TIPI, control de vocabulario VCL, categorías psicolingüísticas LIWC), garantizando que ninguna columna quede sin definir.

### Reglas de calidad del dato (Python)

El script 05_reglas_calidad_dato formaliza 49 reglas de validación siguiendo el patrón exigido (recuento de registros con campo nulo, fuera de rango, fuera de dominio o duplicado). Cada regla informa registros evaluados, incumplimientos, porcentaje, estado y acción correctiva. Resultado de la ejecución: 39 reglas OK, 10 avisos documentados y 0 errores. La formalización aportó dos hallazgos nuevos sobre el corpus Dreaddit: cuatro fragmentos cuyo texto es literalmente '#NAME?' —celdas corruptas heredadas de la fuente original, que se excluyen del corpus NLP— y la detección de que train y test comparten las 116 columnas, pero en distinto orden, lo que obliga a alinear por nombre antes del modelado. El cuadro completo de resultados se exporta automáticamente a CSV.

### Modelo de datos en MySQL y diagrama ERD

La base de datos tfm_estres_estudiantil se implementó en MySQL (vía XAMPP/MariaDB y phpMyAdmin) mediante el script modelo_datos_mysql.sql, con 15 tablas: tres dimensiones (dim_bloque, dim_dataset —que registra el linaje, la fuente y la clasificación de calidad inferencial/técnica de cada dataset— y dim_subreddit) y las tablas de hechos, una por dataset. Coherente con la metodología de análisis en paralelo, las tablas de hechos no se relacionan entre sí: sus claves foráneas apuntan a las dimensiones. Dos decisiones de diseño destacan: las particiones train y test de Dreaddit se unifican en una sola tabla con el campo particion, y el DASS-42 se normaliza en dos tablas con relación 1:N (b4_dass_respondente → b4_dass_item, 42 filas de ítems por participante), evitando una tabla de 172 columnas y demostrando la relación clave primaria–clave foránea. Las reglas de calidad se trasladaron al modelo como restricciones CHECK (rangos 1-5, edad 13-90) y dominios ENUM. El diagrama entidad-relación (modelo_datos_ERD.png) documenta gráficamente las claves primarias, foráneas y cardinalidades de las 15 tablas.

### Notebooks documentados

Los cinco procesos (cuatro EDA y reglas de calidad) se entregan como notebooks de Jupyter (.ipynb) con celdas de explicación intercaladas: una guía de lectura inicial que describe la plantilla de análisis, y una explicación breve antes de cada celda de código que aclara su función y los comandos empleados, redactada para público técnico y no técnico. Los notebooks utilizan rutas parametrizadas (BASE/ALMC) que apuntan a la estructura local de carpetas del equipo y crean automáticamente los directorios de salida.

---
<!-- relacionado -->
**Relacionado:** [README](../../README.md) · [Diccionario de datos](03_diccionario_de_datos.md) · [Respuesta a la retroalimentación](02_respuesta_retroalimentacion_entrega1_v3.md) · [Datasets](../../data/datasets/00_INDICE.md) · [Problema y objetivos](../../investigacion/problema.md)
