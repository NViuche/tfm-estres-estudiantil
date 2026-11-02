# Objetivo 2: Modelado predictivo del estrés (clasificación y NLP)

*Transcripción a texto de `Sintesis_Objetivo2_Modelado.pdf` (13 págs.). El PDF original, con las matrices de confusión, importancias de variables y la figura de AUC, es el entregable oficial (las figuras están en `figuras_modelado/` del paquete).*

**TFM — Business Analytics e Inteligencia Artificial.** Andrés Francisco García Grajales · Obed Isaí Alvarado Núñez · Roberto Mario Brochero López · Raúl Cervantes Iglesias · Santiago Nicolas Viuche Pinilla

## 1. Alcance y relación con las entregas
El Objetivo 2 de la propuesta es desarrollar modelos de inteligencia artificial para la predicción del estrés, con clasificación sobre datos estructurados y NLP sobre datos textuales, manteniendo un análisis independiente por dataset. Según el Alcance oficial del máster, el Machine Learning es la parte opcional de la Entrega 3. Este trabajo se apoya en las fuentes y su calidad (Entrega 1), el datawarehouse y los KPIs (Entrega 2) y la capa de consumo en estrella (retroalimentación de la Entrega I).

Todo el código está en `09_modelado_objetivo2.ipynb`. Las cifras proceden de su ejecución de validación sobre los mismos CSV del proyecto (semilla 42; scikit-learn 1.8.0, XGBoost 3.4.1) y pueden variar en las milésimas con otras versiones.

## 2. Integración con el esquema estrella
La lógica de modelado no cambia: cada dataset se modela de forma independiente desde sus CSV. Hay tres puntos de contacto con la estrella:

- **La política de modelado se lee de la base de datos.** El notebook consulta `uso_modelado` en `vw_dim_dataset` y modela solo las fuentes 'incluido'. Si una fuente pasa a 'excluido', se omite sin tocar el código. Sin conexión a MySQL aplica la política por defecto (verificado en ambos modos con resultados idénticos).
- **Los resultados vuelven al datawarehouse.** Se cargan en `dwh_modelo_resultados` (creada por `dwh_estrella.sql`), con `id_dataset` como FK hacia `dim_dataset` y la columna `lectura_capa_armonizada`.
- **Una segunda tabla de hechos, sin tocar la estrella.** `vw_modelo_resultados` (grano: dataset × modelo × ejecución) comparte con `vw_hechos_estres` la dimensión `vw_dim_dataset`, formando una constelación: en Power BI un mismo segmentador de bloque, calidad o uso_modelado filtra registros y resultados.

| Tarea de modelado | id_dataset | Bloque | Protocolo | n |
|---|---|---|---|---|
| B1_ACADSTRESS | 1 | Factores internos | CV 5x3 | 140 |
| B1_ANXIETY | 2 | Factores internos | Hold-out 80/20 | 9.302 |
| B1_MHSURVEY | 3 | Factores internos | CV 5x3 | 87 |
| B2_SMMH | 6 | Hábitos digitales | CV 5x3 | 481 |
| B3_DEPSTUDENT | 10 | Percepción emocional | CV 5x3 | 502 |
| B4_DASS | 11 | Validación psicológica | Hold-out 80/20 | 23.039 |
| B4_MENTALHEALTH | 12 | Validación psicológica | Hold-out 80/20 | 54.207 |
| B3_DREADDIT | 8 (y 9) | Percepción emocional | Train/Test original | 3.549 |

Dreaddit (train, id 8, y test, id 9) es una única tarea, registrada con id_dataset = 8; sus métricas se miden sobre la partición de prueba. Los tres sintéticos (ids 4, 5 y 7) no se modelan.

## 3. Diseño metodológico
| Decisión | Qué se hizo | Por qué |
|---|---|---|
| Fuentes | 9 fuentes 'incluido' → 8 tareas. Los 3 sintéticos quedan fuera | Exigencia del tutor: los datos sintéticos restan validez científica |
| Independencia | Un modelo por dataset, sin fusionar fuentes | Metodología de análisis en paralelo |
| Candidatos | Baseline + Regresión Logística + Random Forest + XGBoost. NLP: además TF-IDF con LR, SVM y Naive Bayes, y un híbrido con LIWC | Días 6 y 8 del máster |
| Evaluación | n < 1000: validación cruzada estratificada 5×3 (15 evaluaciones). n ≥ 1000: hold-out 80/20 estratificado. Dreaddit: partición original | Con 87 filas un único hold-out es inestable (Día 5: sobreajuste) |
| Métrica principal | AUC; F1 y Accuracy se comparan siempre contra el baseline | El Accuracy engaña con clases desbalanceadas |
| Fuga de datos | Se excluyen las variables que construyen el target (ítems GAD-7, ítems DASS, 'anxiety' en MH Survey, confidence y subreddit en Dreaddit) | Evita resultados triviales |
| Ética | Religión, orientación sexual y raza no se usan como predictores | No se modelan atributos sensibles |
| Deep learning | No se aplica (MLP, LSTM: Días 9-10) | Con datos tabulares de 87 a 54.000 filas, regresión y árboles son el punto de partida estándar; queda como línea futura |
| Industrialización | Pipeline completo (preprocesado + modelo) en .pkl y .json | Día 11 |

**Cómo leer las métricas.** Accuracy: proporción de aciertos (engaña si una clase domina). F1: equilibrio entre precisión y exhaustividad de la clase de interés (en multiclase, promedio macro). AUC: probabilidad de que el modelo puntúe más alto a un caso positivo que a uno negativo; 0,5 es el azar y 1 la separación perfecta. Brecha: Accuracy de entrenamiento menos Accuracy de prueba; valores superiores a ≈ 0,15 indican sobreajuste. El baseline predice siempre la clase mayoritaria y fija el suelo que cualquier modelo debe superar.

## 4. Modelado por dataset

### B1_ACADSTRESS — estrés académico
Factores internos · id_dataset 1 · 140 registros · target: índice de estrés académico (1-5) · clases: 1: 4,3 % · 2: 6,4 % · 3: 25,7 % · 4: 40,0 % · 5: 23,6 % · CV 5x3 · 5 numéricas + 3 categóricas.
**Feature engineering:** Label Encoding de la etapa académica (orden natural); One-Hot de entorno, afrontamiento y hábitos; derivada `presion_total` = pares + hogar + competencia.
**Más influyentes:** presion_total (0.25), competencia (0.20), presion_pares (0.15), presion_hogar (0.12).
**Lectura armonizada:** 1-2 Bajo, 3 Moderado, 4-5 Alto.

| Modelo | Accuracy | F1 | AUC | ± AUC | Brecha |
|---|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.400 | 0.114 | 0.500 | 0.000 | 0.000 |
| Regresión Logística | 0.350 | 0.338 | 0.715 | 0.056 | 0.184 |
| **Random Forest** | 0.395 | 0.383 | 0.730 | 0.035 | 0.433 |
| XGBoost | 0.388 | 0.369 | 0.672 | 0.058 | 0.548 |

El mejor modelo (Random Forest) alcanza AUC ≈ 0,73, pero su Accuracy (≈ 0,40) no supera al baseline (0,40): ordena los niveles mejor que el azar pero no acierta el nivel exacto. La brecha de ≈ 0,43 revela sobreajuste fuerte. Con 140 filas y clases de apenas 6 y 9 casos, predecir cinco niveles es demasiado ambicioso: resultado exploratorio. `presion_total` encabeza la importancia, lo que respalda el hallazgo del Objetivo 1. Mejora posible: trabajar con los tres niveles de la capa armonizada o ampliar la muestra.

### B1_ANXIETY — ansiedad GAD-7 (estudiantes)
Factores internos · id_dataset 2 · 9.302 registros · target: GAD-7 ≥ 10 · clases: No alto (<10) 82,7 % · Alto (≥10) 17,3 % · Hold-out 80/20 · 7 numéricas + 4 categóricas.
**Feature engineering:** fuga evitada (los ítems GAD1-7 y GADE se excluyen porque GAD_T es su suma); derivadas con cortes clínicos (swl_insatisfecho si SWL ≤ 14; spin_alto si SPIN ≥ 19); horas_juego acotada a 112 h/semana (regla de calidad R4).
**Más influyentes:** spin (0.27), swl (0.23), horas_juego (0.16), edad (0.09).
**Lectura armonizada:** GAD-7 ≥ 10 equivale a nivel Alto.

| Modelo | Accuracy | F1 | AUC | Brecha |
|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.827 | 0.000 | 0.500 | 0.000 |
| **Regresión Logística** | 0.730 | 0.453 | 0.764 | 0.004 |
| Random Forest | 0.798 | 0.400 | 0.745 | 0.145 |
| XGBoost | 0.829 | 0.299 | 0.754 | 0.039 |

Es el ejemplo de la trampa del Accuracy: el baseline "nunca hay ansiedad alta" obtiene 83 % de Accuracy con F1 = 0, de modo que supera en Accuracy a todos los modelos sin detectar un solo caso. La Regresión Logística (Accuracy ≈ 0,73) logra F1 ≈ 0,45 y AUC ≈ 0,77, el mejor equilibrio, con sobreajuste casi nulo (brecha ≈ 0,00 frente a ≈ 0,15 del Random Forest): gana el modelo más simple. SPIN y SWL dominan la importancia, coherente con el Objetivo 1. Limitación: la población original son jugadores online.

### B1_MHSURVEY — salud mental universitaria
Factores internos · id_dataset 3 · 87 registros · target: depresión autoreportada (3 niveles) · clases: Bajo 31,0 % · Moderado 24,1 % · Alto 44,8 % · CV 5x3 · 13 numéricas + 5 categóricas.
**Feature engineering:** fuga evitada ('anxiety' se excluye, r = 0,84 con el target); cgpa y average_sleep pasan de rangos de texto a orden numérico; One-Hot de residencia y año; derivadas `carga_presion` (interacción) y `bienestar` = satisfacción − aislamiento.
**Más influyentes:** aislamiento (0.16), bienestar (0.13), financiero (0.09), inseguridad (0.08).
**Lectura armonizada:** depresión 1-5 mapeada a Bajo / Moderado / Alto.

| Modelo | Accuracy | F1 | AUC | ± AUC | Brecha |
|---|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.448 | 0.206 | 0.500 | 0.000 | -0.000 |
| Regresión Logística | 0.621 | 0.572 | 0.771 | 0.069 | 0.225 |
| Random Forest | 0.614 | 0.509 | 0.764 | 0.071 | 0.378 |
| **XGBoost** | 0.621 | 0.551 | 0.789 | 0.069 | 0.379 |

AUC ≈ 0,76-0,79 y Accuracy ≈ 0,62 frente a 0,45 del baseline: hay señal real. La desviación entre repeticiones (±0,07) es del tamaño de las diferencias entre modelos, así que XGBoost, Regresión Logística y Random Forest son estadísticamente indistinguibles con n = 87; los árboles sobreajustan (brecha ≈ 0,38). La derivada `bienestar` queda segunda en importancia, tras aislamiento, lo que confirma al aislamiento social como predictor central.

### B2_SMMH — redes sociales y salud mental
Hábitos digitales · id_dataset 6 · 481 registros · target: se siente deprimido/a ≥ 4 · clases: Bajo (<4) 54,1 % · Alto (≥4) 45,9 % · CV 5x3 · 23 numéricas + 3 categóricas.
**Feature engineering:** se excluye la pregunta 19 (interés en actividades) por ser síntoma del mismo constructo; One-Hot de las plataformas (multi-selección en dummies); tiempo_diario ordinal; derivadas `uso_ansioso` = (inquietud + distracción fácil + preocupación) / 3 e `impacto_social` = (comparación + validación) / 2.
**Más influyentes:** preocupacion (0.13), uso_ansioso (0.10), dificultad_concentracion (0.08), impacto_social (0.07).
**Lectura armonizada:** valor ≥ 4 equivale a nivel Alto.

| Modelo | Accuracy | F1 | AUC | ± AUC | Brecha |
|---|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.540 | 0.000 | 0.500 | 0.000 | -0.000 |
| Regresión Logística | 0.736 | 0.726 | 0.792 | 0.037 | 0.033 |
| **Random Forest** | 0.741 | 0.730 | 0.793 | 0.038 | 0.233 |
| XGBoost | 0.702 | 0.680 | 0.778 | 0.043 | 0.296 |

Fuente de hábitos digitales con señal real: AUC ≈ 0,79 y Accuracy ≈ 0,74 frente a 0,54; Regresión Logística y Random Forest empatan, así que el patrón es esencialmente lineal. Dos de las cuatro variables más importantes son derivadas, y ni el tiempo diario ni las plataformas figuran entre las primeras: importa el patrón de uso, no cuánto se usa. `uso_ansioso` (r ≈ 0,56) no supera a su mejor componente, la preocupación (r ≈ 0,59); aporta estabilidad al promediar tres señales.

### B3_DEPSTUDENT — depresión estudiantil (con alerta)
Percepción emocional · id_dataset 10 · 502 registros · target: Depression (Yes/No) · clases: sin depresión 49,8 % · con depresión 50,2 % · CV 5x3 · 10 numéricas + 1 categórica.
**Feature engineering:** Label Encoding ordinal de sueño y dieta; binarias para pensamientos suicidas y antecedentes; derivada `riesgo_alto` (presión ≥ 4 y estrés financiero ≥ 4).
**Más influyentes:** pens_suicidas (0.22), presion (0.21), edad (0.12), satisfaccion (0.10).
**Lectura armonizada:** No = Bajo, Yes = Alto.

| Modelo | Accuracy | F1 | AUC | ± AUC | Brecha |
|---|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.502 | 0.668 | 0.500 | 0.000 | 0.000 |
| **Regresión Logística** | 0.979 | 0.979 | 0.998 | 0.002 | 0.012 |
| Random Forest | 0.900 | 0.903 | 0.974 | 0.014 | 0.098 |
| XGBoost | 0.929 | 0.930 | 0.987 | 0.008 | 0.071 |

La Regresión Logística obtiene AUC ≈ 0,998 y Accuracy ≈ 0,98, un resultado demasiado perfecto para datos clínicos reales. Se trata con cautela (sección 6).

### B4_DASS — DASS-42, 18-25 años
Validación psicológica · id_dataset 11 · 23.039 registros · target: nivel de estrés DASS-42 (baremos) · clases: Bajo 28,8 % · Moderado 35,7 % · Alto 35,5 % · Hold-out 80/20 · 8 numéricas + 4 categóricas.
**Feature engineering:** ningún ítem DASS como predictor (los de estrés definen el target); las 10 respuestas TIPI se convierten en las 5 puntuaciones Big Five (invirtiendo ítems inversos con 8 − x); One-Hot de género, entorno de infancia, lengua nativa y estado civil; religión, orientación y raza excluidas por ética.
**Más influyentes:** estab_emocional (0.31), responsabilidad (0.10), extraversion (0.10), apertura (0.10).
**Lectura armonizada:** baremos DASS: ≤28 Bajo, 29-39 Moderado, ≥40 Alto.

| Modelo | Accuracy | F1 | AUC | Brecha |
|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.357 | 0.175 | 0.500 | 0.000 |
| Regresión Logística | 0.569 | 0.567 | 0.762 | -0.003 |
| Random Forest | 0.564 | 0.566 | 0.754 | 0.383 |
| **XGBoost** | 0.579 | 0.584 | 0.762 | 0.032 |

Predecir el estrés solo con perfil y personalidad da AUC ≈ 0,76 y Accuracy ≈ 0,58 frente a 0,36 del baseline. La estabilidad emocional domina (≈ 0,31, el triple que cualquier otro rasgo), coherente con la relación entre neuroticismo y estrés. Regresión Logística y XGBoost empatan; XGBoost apenas sobreajusta (≈ 0,03) frente al Random Forest (≈ 0,38): la regularización importa. La personalidad explica una parte del estrés, no su totalidad.

### B4_MENTALHEALTH — búsqueda de tratamiento (estudiantes)
Validación psicológica · id_dataset 12 · 54.207 registros · target: ha buscado tratamiento (Yes/No) · clases: sin tratamiento 50,6 % · con tratamiento 49,4 % · Hold-out 80/20 · 5 numéricas + 9 categóricas.
**Feature engineering:** el target es una conducta, no un nivel de estrés; Label Encoding ordinal de días en casa, estrés creciente y cambios de humor; One-Hot del resto; derivada `vulnerabilidad` = antecedentes + historial propio.
**Más influyentes:** antecedentes (0.27), conoce_opciones_Yes (0.16), vulnerabilidad (0.11), conoce_opciones_No (0.06).
**Lectura armonizada:** conducta de búsqueda de ayuda (no es nivel de estrés): alimenta el KPI de tratamiento.

| Modelo | Accuracy | F1 | AUC | Brecha |
|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.506 | 0.000 | 0.500 | 0.000 |
| Regresión Logística | 0.703 | 0.708 | 0.765 | -0.003 |
| Random Forest | 0.698 | 0.712 | 0.729 | 0.022 |
| **XGBoost** | 0.718 | 0.728 | 0.769 | -0.004 |

XGBoost: AUC ≈ 0,77 y Accuracy ≈ 0,72 frente a 0,51, sin sobreajuste. Los antecedentes familiares encabezan la importancia y `estres_creciente` no figura entre las primeras: el modelo reproduce el hallazgo del Objetivo 1 (el estrés percibido no mueve la búsqueda de ayuda; la familiaridad con la salud mental sí). Cautela: `conoce_opciones` (≈ 0,16) puede ser consecuencia de estar en tratamiento y no su causa (causalidad inversa).

## 5. NLP: detección de estrés en texto (B3_DREADDIT)
Se comparan tres enfoques sobre la partición train/test original (2.834 textos de entrenamiento y 715 de prueba tras la regla de calidad R7, que excluye los fragmentos '#NAME?'; la regla R6 alinea las columnas por nombre; sin solapamiento de post_id entre particiones): (1) las 105 variables psicolingüísticas precalculadas (LIWC, DAL, legibilidad, sentimiento); (2) TF-IDF de unigramas y bigramas con tres clasificadores; (3) un híbrido. No se eliminan las stop-words porque los pronombres ('I', 'me') son señal de estrés. Se excluyen `confidence` (no existe al predecir), `subreddit` (casi equivale a la etiqueta) y las variables `social_*`.

| Modelo | Accuracy | F1 | AUC | Brecha |
|---|---|---|---|---|
| Baseline (clase mayoritaria) | 0.516 | 0.681 | 0.500 | 0.008 |
| LIWC + Regresión Logística | 0.744 | 0.757 | 0.835 | 0.042 |
| LIWC + Random Forest | 0.754 | 0.770 | 0.834 | 0.245 |
| LIWC + XGBoost | 0.732 | 0.752 | 0.835 | 0.240 |
| TF-IDF + Regresión Logística | 0.716 | 0.733 | 0.822 | 0.217 |
| TF-IDF + SVM lineal | 0.732 | 0.745 | 0.820 | 0.265 |
| TF-IDF + Naive Bayes | 0.719 | 0.766 | 0.831 | 0.225 |
| **Híbrido (TF-IDF + LIWC) + RegLog** | 0.748 | 0.762 | 0.838 | 0.085 |

Los tres enfoques rinden de forma muy parecida (AUC 0,82-0,84, Accuracy 0,72-0,75, frente a 0,52 del baseline). El híbrido es el mejor, pero con 715 textos de prueba las diferencias de ≈ 0,01 no son concluyentes: una Regresión Logística sobre LIWC (AUC 0,835) iguala a XGBoost. Los modelos sobre TF-IDF sobreajustan más (brecha 0,22-0,27) que el híbrido (0,08) y que la regresión sobre LIWC (0,04). El F1 del baseline (0,68) es alto porque predice siempre la clase mayoritaria 'estrés'.

**Qué dice el lenguaje.** El modelo detecta el 78 % de los textos con estrés (recall) y descarta correctamente el 71 % de los que no lo tienen. Los términos que más empujan hacia estrés son *me, my, feel, even, because, just, am* (lenguaje centrado en uno mismo); hacia no estrés: *you, we, her, your, url, met, she*. Coincide con el Objetivo 1 (primera persona 10,8 % en posts de estrés frente a 7,1 %), marcador clásico de rumiación.

**Despliegue.** El mejor modelo necesita variables LIWC (diccionario con licencia) que no se pueden calcular sobre texto nuevo. Por eso se guarda también `modelo_B3_DREADDIT_solo_texto.pkl` (TF-IDF + Regresión Logística, AUC 0,82), que solo requiere el texto; el notebook incluye un ejemplo de uso. Limitación: el corpus procede de subreddits de PTSD, relaciones y violencia doméstica; el estrés capturado es relacional y clínico, no estrictamente académico.

## 6. Alerta: un resultado demasiado perfecto (B3_DEPSTUDENT)
La Regresión Logística obtiene AUC ≈ 0,998 y Accuracy ≈ 0,98 con diez variables gruesas. Para distinguir entre fuga de datos y otra causa, el notebook mide el AUC de cada variable por separado y el de árboles de decisión muy simples:

| Variable (por separado) | AUC |
|---|---|
| presion | 0.769 |
| pens_suicidas | 0.733 |
| financiero | 0.668 |
| satisfaccion | 0.666 |
| edad | 0.625 |
| horas_estudio | 0.613 |
| Árbol de profundidad 2 | 0.826 |
| Árbol de profundidad 4 | 0.900 |
| Regresión Logística (todas las variables) | 0.998 |

Ninguna columna filtra la etiqueta (la mejor, presión académica, llega a 0,77), pero la combinación lineal de varias la reproduce casi sin error: patrón típico de etiquetas generadas por una fórmula. No puede afirmarse que el dataset sea sintético, pero es un indicio serio. Dado que la política es no modelar datos sintéticos, el resultado se reporta con cautela y no se usa como evidencia sustantiva. Este dataset sustenta además el KPI de riesgo crítico (72,7 %). **Recomendación: consultarlo con el tutor.** Si se decide excluirlo: `UPDATE dim_dataset SET uso_modelado='excluido', calidad='tecnico' WHERE codigo='B3_DEPSTUDENT'`; la exclusión se propaga a la estrella, a Power BI y al notebook.

## 7. Resumen comparativo
| Dataset | Mejor modelo | Protocolo | Accuracy | Baseline | F1 | AUC | Brecha |
|---|---|---|---|---|---|---|---|
| B3_DEPSTUDENT | Regresión Logística | CV 5x3 | 0.979 | 0.502 | 0.979 | 0.998 | 0.012 |
| B3_DREADDIT | Híbrido (TF-IDF + LIWC) + RegLog | Train/Test original | 0.748 | 0.516 | 0.762 | 0.838 | 0.085 |
| B2_SMMH | Random Forest | CV 5x3 | 0.741 | 0.540 | 0.730 | 0.793 | 0.233 |
| B1_MHSURVEY | XGBoost | CV 5x3 | 0.621 | 0.448 | 0.551 | 0.789 | 0.379 |
| B4_MENTALHEALTH | XGBoost | Hold-out 80/20 | 0.718 | 0.506 | 0.728 | 0.769 | -0.004 |
| B1_ANXIETY | Regresión Logística | Hold-out 80/20 | 0.730 | 0.827 | 0.453 | 0.764 | 0.004 |
| B4_DASS | XGBoost | Hold-out 80/20 | 0.579 | 0.357 | 0.584 | 0.762 | 0.032 |
| B1_ACADSTRESS | Random Forest | CV 5x3 | 0.395 | 0.400 | 0.383 | 0.730 | 0.433 |

## 8. Conclusiones y limitaciones
- Hay señal predictiva real pero moderada: AUC entre ≈ 0,73 y ≈ 0,84 en las fuentes con señal real. El estrés se puede anticipar mejor que el azar, no predecir con precisión individual.
- Ningún algoritmo domina: XGBoost gana 3 tareas, la Regresión Logística 3 (incluido el híbrido de NLP) y Random Forest 2; en varios casos la diferencia está dentro del ruido.
- Los modelos confirman el Objetivo 1: presión académica y aislamiento (Bloque 1), patrón de uso frente a tiempo de uso (Bloque 2), lenguaje autorreferencial (NLP), antecedentes familiares frente a estrés percibido en la búsqueda de ayuda, y estabilidad emocional (DASS).
- El Accuracy por sí solo engaña: en Anxiety el baseline lo supera sin detectar ningún caso.
- Un resultado demasiado bueno es una alerta, no un éxito: B3_DEPSTUDENT se reporta con cautela.
- Limitaciones: tres tareas con n < 600 (alta varianza); poblaciones distintas de la estudiantil (jugadores online, Reddit, población general); sin deep learning, búsqueda de hiperparámetros ni ajuste de umbrales; modelos de investigación, no de diagnóstico clínico.

**Siguiente paso (Entrega 3).** Los resultados se consumen en Power BI desde `vw_modelo_resultados` como página de analítica avanzada, junto con los KPIs del DWH y la estrella de registros.

## 9. Reproducibilidad y entregables
Orden de ejecución (XAMPP con MySQL en verde). Ya ejecutados: `modelo_datos_mysql_v2.sql`, `esquema_estrella_powerbi.sql` y el notebook 07. A continuación: `dwh_estrella.sql` → `08_etl_transformaciones_kpis_v4.ipynb` → `09_modelado_objetivo2.ipynb` (Kernel → Restart Kernel and Run All Cells). El notebook 09 también funciona sin base de datos (modela desde los CSV y guarda resultados en CSV). Cada modelo se guarda como pipeline completo, cargable con joblib para puntuar datos nuevos sin reentrenar.

| Archivo | Contenido |
|---|---|
| 09_modelado_objetivo2.ipynb | Notebook documentado: diseño, 8 tareas, NLP, diagnóstico, serialización, ejemplo de uso y carga al DWH |
| dwh_estrella.sql | DWH en estrella: crea todas las tablas dwh_* (incluidas dwh_modelo_resultados y su vista) |
| dwh_estrella_ERD.png | Diagrama del DWH en estrella |
| modelos/*.pkl y *.json | 9 modelos serializados (8 mejores + versión NLP solo texto) con metadata y manifest_modelos.json |
| resultados_modelado_resumen.csv / _completo.csv | Métricas de todos los modelos, con id_dataset como clave de relación con la estrella |
| figuras_modelado/*.png | Matriz de confusión e importancia por dataset y resumen de AUC |
| Sintesis_Objetivo2_Modelado.pdf | Este documento |
