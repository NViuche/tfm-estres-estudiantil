# Diccionario de datos (Entrega I)

Conversión a texto del archivo Excel `Diccionario de datos.xlsx` (una sección por hoja). El Excel original es el entregable oficial.


## 00_Indice

| DICCIONARIO DE DATOS — TFM: Análisis multidimensional del estrés estudiantil |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Entrega 1 · Un dataset por hoja · Perfilado automático generado con Python (pandas) |  |  |  |  |  |  |  |
| Hoja | Bloque | Dataset (fuente) | Filas | Columnas | Nulos totales | Duplicados | Descripción |
| B1_AcademicStress | Bloque 1 | Academic Stress (poushal02, Kaggle) | 140 | 9 | 1 | 0 | Encuesta sobre estrés académico percibido en estudiantes. Variable objetivo: índice de estrés (1-5). |
| B1_Anxiety | Bloque 1 | Student Anxiety GAD-7 (petalme, Kaggle) | 13464 | 55 | 21709 | 0 | Escalas clínicas GAD-7 (ansiedad), SWL (satisfacción vital) y SPIN (ansiedad social) en población de jugadores online; incluye subconjunto estudiantil (Work). |
| B1_MentalHealthSurvey | Bloque 1 | Student Mental Health Survey (abdullahashfaqvirk, Kaggle) | 87 | 21 | 0 | 0 | Encuesta universitaria: depresión, ansiedad, aislamiento, carga académica y factores de entorno (escalas 1-5). |
| B1_StudentHabits | Bloque 1 | Student Habits vs Performance (abhi88377, GitHub) | 1000 | 16 | 91 | 0 | Hábitos de estudio, sueño, redes y rendimiento académico. Señal sintética en mental_health_rating (documentado). |
| B2_SocialMediaSleep | Bloque 2 | Social Media vs Sleep/Stress/Productivity (jayjoshi37, Kaggle) | 11000 | 10 | 0 | 0 | Uso de redes, sueño, productividad y estrés. Dataset sintético (correlaciones ~0, documentado). |
| B2_SMMH | Bloque 2 | Social Media and Mental Health (souvikahmed071, Kaggle) | 481 | 21 | 30 | 0 | Encuesta Likert sobre patrones de uso de redes sociales y bienestar psicológico. Fuente principal del bloque. |
| B2_Lifestyle | Bloque 2 | Mental Health Lifestyle (datafit17, GitHub) | 3000 | 12 | 595 | 0 | Estilo de vida (ejercicio, dieta, sueño, pantalla) y salud mental en 7 países. Dataset sintético (documentado). |
| B3_DreadditTrain | Bloque 3 | Dreaddit train (payaldhokane, Kaggle) | 2838 | 116 | 0 | 0 | Corpus de posts de Reddit etiquetados por estrés (0/1) con 107 categorías LIWC, índices DAL y legibilidad. Partición de entrenamiento. |
| B3_DreadditTest | Bloque 3 | Dreaddit test (payaldhokane, Kaggle) | 715 | 116 | 0 | 0 | Partición de evaluación del corpus Dreaddit. Misma estructura que train. |
| B3_DepressionStudent | Bloque 3 | Depression Student Dataset (prajwalg26, GitHub) | 502 | 11 | 0 | 0 | Perfil estructurado de depresión estudiantil: presión académica, sueño, pensamientos suicidas. Tabular (no NLP). |
| B4_DASS42 | Bloque 4 | DASS-42 (lucasgreenwell, Kaggle) | 39775 | 172 | 11427 | 0 | Escala clínica DASS-42 (2017-2019, n≈40k): 42 ítems + TIPI + control de vocabulario + demográficos. Separador TAB. Codebook oficial incluido. |
| B4_MentalHealth | Bloque 4 | Mental Health Dataset (chanchal24, Kaggle) | 261328 | 17 | 4356 | 175284 | Encuesta masiva (261k) sobre salud mental, estrés y búsqueda de tratamiento. Filtrar Occupation=Student para análisis del TFM. |

## B1_AcademicStress

| Academic Stress (poushal02, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 140 filas × 9 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Timestamp | str | 140 | 0 | 0 | 140 |  |  |  | 24/07/2025 22:05:39 (1); 24/07/2025 22:05:52 (1); 24/07/2025 22:06:39 (1) | Fecha y hora de la respuesta |
| Your Academic Stage | str | 140 | 0 | 0 | 3 |  |  |  | undergraduate (100); high school (29); post-graduate (11) | Etapa académica (high school / undergraduate / post-graduate) |
| Peer pressure | int64 | 140 | 0 | 0 | 5 | 1 | 5 | 3.07 |  | Presión de pares percibida (1-5) |
| Academic pressure from your home | int64 | 140 | 0 | 0 | 5 | 1 | 5 | 3.18 |  | Presión académica desde el hogar (1-5) |
| Study Environment | str | 139 | 1 | 0.7 | 3 |  |  |  | Peaceful (69); disrupted (38); Noisy (32) | Entorno de estudio (categórico) |
| What coping strategy you use as a student? | str | 140 | 0 | 0 | 3 |  |  |  | Analyze the situation and ha (87); Emotional breakdown (crying  (32); Social support (friends, fam (21) | Estrategia de afrontamiento |
| Do you have any bad habits like smoking, drinking on a daily basis? | str | 140 | 0 | 0 | 3 |  |  |  | No (123); Yes (10); prefer not to say (7) | Hábitos nocivos diarios (Yes/No/prefer not to say) |
| What would you rate the academic  competition in your student life | int64 | 140 | 0 | 0 | 5 | 1 | 5 | 3.49 |  | Competencia académica percibida (1-5) |
| Rate your academic stress index | int64 | 140 | 0 | 0 | 5 | 1 | 5 | 3.72 |  |  |

## B1_Anxiety

| Student Anxiety GAD-7 (petalme, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 13464 filas × 55 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| S. No. | int64 | 13464 | 0 | 0 | 13464 | 1 | 14250 | 7096.84 |  | Identificador secuencial |
| Timestamp | float64 | 13464 | 0 | 0 | 11734 | 42052 | 42058.36 | 42054.84 |  | Fecha y hora de la respuesta |
| GAD1 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.86 |  | Ítem 1 de la escala GAD-7 (0-3) |
| GAD2 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.67 |  | Ítem 2 de la escala GAD-7 (0-3) |
| GAD3 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.97 |  | Ítem 3 de la escala GAD-7 (0-3) |
| GAD4 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.72 |  | Ítem 4 de la escala GAD-7 (0-3) |
| GAD5 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.49 |  | Ítem 5 de la escala GAD-7 (0-3) |
| GAD6 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.91 |  | Ítem 6 de la escala GAD-7 (0-3) |
| GAD7 | int64 | 13464 | 0 | 0 | 4 | 0 | 3 | 0.59 |  | Ítem 7 de la escala GAD-7 (0-3) |
| GADE | str | 12815 | 649 | 4.8 | 4 |  |  |  | Not difficult at all (6236); Somewhat difficult (5148); Very difficult (1012) | Dificultad funcional derivada de la ansiedad (autoreporte) |
| SWL1 | int64 | 13464 | 0 | 0 | 7 | 1 | 7 | 3.72 |  | Ítem 1 escala SWL |
| SWL2 | int64 | 13464 | 0 | 0 | 7 | 1 | 7 | 4.6 |  | Ítem 2 escala SWL |
| SWL3 | int64 | 13464 | 0 | 0 | 7 | 1 | 7 | 4.35 |  | Ítem 3 escala SWL |
| SWL4 | int64 | 13464 | 0 | 0 | 7 | 1 | 7 | 3.76 |  | Ítem 4 escala SWL |
| SWL5 | int64 | 13464 | 0 | 0 | 7 | 1 | 7 | 3.36 |  | Ítem 5 escala SWL |
| Game | str | 13464 | 0 | 0 | 11 |  |  |  | League of Legends (11314); Other (1021); Starcraft 2 (345) | Videojuego principal |
| Platform | str | 13464 | 0 | 0 | 3 |  |  |  | PC (13219); Console (PS, Xbox, ...) (222); Smartphone / Tablet (23) | Plataforma de juego |
| Hours | float64 | 13434 | 30 | 0.2 | 84 | 0 | 8000 | 22.25 |  | Horas de juego semanales |
| earnings | str | 13464 | 0 | 0 | 314 |  |  |  | I play for fun (12112); I play mostly for fun but ea (990); I earn a living by playing t (48) | Ingresos por juego |
| whyplay | str | 13464 | 0 | 0 | 407 |  |  |  | having fun (5289); improving (4927); winning (2091) | Motivación principal para jugar |
| League | str | 11612 | 1852 | 13.8 | 1454 |  |  |  | Gold (970); Silver (650); Platinum (635) | Liga/rango competitivo |
| highestleague | float64 | 0 | 13464 | 100 | 0 |  |  |  |  | Liga más alta alcanzada |
| streams | float64 | 13364 | 100 | 0.7 | 65 | 0 | 9001 | 11.23 |  | Horas viendo streams |
| SPIN1 | float64 | 13340 | 124 | 0.9 | 5 | 0 | 4 | 0.86 |  | Ítem 1 de la escala SPIN de ansiedad social |
| SPIN2 | float64 | 13310 | 154 | 1.1 | 5 | 0 | 4 | 1.21 |  | Ítem 2 de la escala SPIN de ansiedad social |
| SPIN3 | float64 | 13324 | 140 | 1 | 5 | 0 | 4 | 1.1 |  | Ítem 3 de la escala SPIN de ansiedad social |
| SPIN4 | float64 | 13305 | 159 | 1.2 | 5 | 0 | 4 | 1.68 |  | Ítem 4 de la escala SPIN de ansiedad social |
| SPIN5 | float64 | 13298 | 166 | 1.2 | 5 | 0 | 4 | 1.25 |  | Ítem 5 de la escala SPIN de ansiedad social |
| SPIN6 | float64 | 13308 | 156 | 1.2 | 5 | 0 | 4 | 1.35 |  | Ítem 6 de la escala SPIN de ansiedad social |
| SPIN7 | float64 | 13326 | 138 | 1 | 5 | 0 | 4 | 1.05 |  | Ítem 7 de la escala SPIN de ansiedad social |
| SPIN8 | float64 | 13320 | 144 | 1.1 | 5 | 0 | 4 | 1.41 |  | Ítem 8 de la escala SPIN de ansiedad social |
| SPIN9 | float64 | 13306 | 158 | 1.2 | 5 | 0 | 4 | 1.57 |  | Ítem 9 de la escala SPIN de ansiedad social |
| SPIN10 | float64 | 13304 | 160 | 1.2 | 5 | 0 | 4 | 0.92 |  | Ítem 10 de la escala SPIN de ansiedad social |
| SPIN11 | float64 | 13277 | 187 | 1.4 | 5 | 0 | 4 | 1.83 |  | Ítem 11 de la escala SPIN de ansiedad social |
| SPIN12 | float64 | 13296 | 168 | 1.2 | 5 | 0 | 4 | 0.89 |  | Ítem 12 de la escala SPIN de ansiedad social |
| SPIN13 | float64 | 13277 | 187 | 1.4 | 5 | 0 | 4 | 0.54 |  | Ítem 13 de la escala SPIN de ansiedad social |
| SPIN14 | float64 | 13308 | 156 | 1.2 | 5 | 0 | 4 | 1.25 |  | Ítem 14 de la escala SPIN de ansiedad social |
| SPIN15 | float64 | 13317 | 147 | 1.1 | 5 | 0 | 4 | 1.41 |  | Ítem 15 de la escala SPIN de ansiedad social |
| SPIN16 | float64 | 13317 | 147 | 1.1 | 5 | 0 | 4 | 0.62 |  | Ítem 16 de la escala SPIN de ansiedad social |
| SPIN17 | float64 | 13289 | 175 | 1.3 | 5 | 0 | 4 | 0.94 |  | Ítem 17 de la escala SPIN de ansiedad social |
| Narcissism | float64 | 13441 | 23 | 0.2 | 5 | 1 | 5 | 2.03 |  | Ítem de narcisismo (1-5) |
| Gender | str | 13464 | 0 | 0 | 3 |  |  |  | Male (12699); Female (713); Other (52) | Género |
| Age | int64 | 13464 | 0 | 0 | 30 | 18 | 63 | 20.93 |  | Edad |
| Work | str | 13426 | 38 | 0.3 | 4 |  |  |  | Student at college / univers (7073); Employed (2734); Student at school (2229) | Ocupación (permite filtrar estudiantes) |
| Degree | str | 11887 | 1577 | 11.7 | 4 |  |  |  | High school diploma (or equi (8560); Bachelor (or equivalent) (2687); Master (or equivalent) (546) | Nivel educativo |
| Birthplace | str | 13464 | 0 | 0 | 126 |  |  |  | USA (4261); Germany (1376); UK (940) | País de nacimiento |
| Residence | str | 13464 | 0 | 0 | 109 |  |  |  | USA (4569); Germany (1413); UK (1032) | País de residencia |
| Reference | str | 13449 | 15 | 0.1 | 4 |  |  |  | Reddit (13324); Other (67); TeamLiquid.net (55) | Cómo conoció la encuesta |
| Playstyle | str | 13464 | 0 | 0 | 298 |  |  |  | Multiplayer - online - with  (5564); Multiplayer - online - with  (4134); Multiplayer - online - with  (2652) | Estilo de juego |
| accept | str | 13050 | 414 | 3.1 | 1 |  |  |  | Accept (13050) | Aceptación de términos |
| GAD_T | int64 | 13464 | 0 | 0 | 22 | 0 | 21 | 5.21 |  | PUNTUACIÓN TOTAL GAD-7 (0-21): ansiedad generalizada |
| SWL_T | int64 | 13464 | 0 | 0 | 31 | 5 | 35 | 19.79 |  | Puntuación total SWL: satisfacción con la vida |
| SPIN_T | float64 | 12814 | 650 | 4.8 | 69 | 0 | 68 | 19.85 |  | Puntuación total SPIN: ansiedad social |
| Residence_ISO3 | str | 13354 | 110 | 0.8 | 107 |  |  |  | USA (4569); DEU (1413); GBR (1032) | Código ISO3 de residencia |
| Birthplace_ISO3 | str | 13343 | 121 | 0.9 | 124 |  |  |  | USA (4261); DEU (1376); GBR (940) | Código ISO3 de nacimiento |

## B1_MentalHealthSurvey

| Student Mental Health Survey (abdullahashfaqvirk, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 87 filas × 21 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| gender | str | 87 | 0 | 0 | 2 |  |  |  | Male (63); Female (24) | Género |
| age | int64 | 87 | 0 | 0 | 8 | 17 | 26 | 19.94 |  | Edad |
| university | str | 87 | 0 | 0 | 9 |  |  |  | PU (56); UET (10); COMSATS (9) | Universidad |
| degree_level | str | 87 | 0 | 0 | 2 |  |  |  | Undergraduate (85); Postgraduate (2) | Nivel de estudios |
| degree_major | str | 87 | 0 | 0 | 4 |  |  |  | Data Science (41); Computer Science (34); Information Technology (9) | Carrera |
| academic_year | str | 87 | 0 | 0 | 4 |  |  |  | 1st year (34); 3rd year (28); 2nd year (15) | Año académico |
| cgpa | str | 87 | 0 | 0 | 6 |  |  |  | 3.0-3.5 (27); 3.5-4.0 (27); 2.5-3.0 (22) | Promedio académico (rango en texto) |
| residential_status | str | 87 | 0 | 0 | 2 |  |  |  | Off-Campus (65); On-Campus (22) | Tipo de residencia |
| campus_discrimination | str | 87 | 0 | 0 | 2 |  |  |  | No (65); Yes (22) | Discriminación en campus |
| sports_engagement | str | 87 | 0 | 0 | 4 |  |  |  | No Sports (42); 1-3 times (24); 4-6 times (11) | Frecuencia de deporte |
| average_sleep | str | 87 | 0 | 0 | 3 |  |  |  | 4-6 hrs (50); 7-8 hrs (32); 2-4 hrs (5) | Horas de sueño (rango en texto) |
| study_satisfaction | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.93 |  | Satisfacción con los estudios (1-5) |
| academic_workload | int64 | 87 | 0 | 0 | 4 | 2 | 5 | 3.89 |  |  |
| academic_pressure | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.78 |  | Presión académica percibida (1-5) |
| financial_concerns | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.39 |  | Preocupación financiera (1-5) |
| social_relationships | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 2.78 |  | Calidad de relaciones sociales (1-5) |
| depression | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.22 |  | VARIABLE OBJETIVO: depresión autoreportada (1-5) |
| anxiety | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.22 |  | VARIABLE OBJETIVO: ansiedad autoreportada (1-5) |
| isolation | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.24 |  | Aislamiento social percibido (1-5) |
| future_insecurity | int64 | 87 | 0 | 0 | 5 | 1 | 5 | 3.01 |  | Inseguridad ante el futuro (1-5) |
| stress_relief_activities | str | 87 | 0 | 0 | 38 |  |  |  | Religious Activities (10); Online Entertainment (9); Religious Activities, Social (6) | Actividades de alivio del estrés |

## B1_StudentHabits

| Student Habits vs Performance (abhi88377, GitHub) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 1000 filas × 16 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| student_id | str | 1000 | 0 | 0 | 1000 |  |  |  | S1000 (1); S1001 (1); S1002 (1) | Identificador del estudiante |
| age | int64 | 1000 | 0 | 0 | 8 | 17 | 24 | 20.5 |  | Edad |
| gender | str | 1000 | 0 | 0 | 3 |  |  |  | Female (481); Male (477); Other (42) | Género |
| study_hours_per_day | float64 | 1000 | 0 | 0 | 78 | 0 | 8.3 | 3.55 |  | Horas de estudio diarias |
| social_media_hours | float64 | 1000 | 0 | 0 | 60 | 0 | 7.2 | 2.51 |  | Horas diarias en redes sociales |
| netflix_hours | float64 | 1000 | 0 | 0 | 51 | 0 | 5.4 | 1.82 |  | Horas diarias de streaming |
| part_time_job | str | 1000 | 0 | 0 | 2 |  |  |  | No (785); Yes (215) | Trabajo a tiempo parcial (Yes/No) |
| attendance_percentage | float64 | 1000 | 0 | 0 | 320 | 56 | 100 | 84.13 |  | Porcentaje de asistencia |
| sleep_hours | float64 | 1000 | 0 | 0 | 68 | 3.2 | 10 | 6.47 |  | Horas de sueño |
| diet_quality | str | 1000 | 0 | 0 | 3 |  |  |  | Fair (437); Good (378); Poor (185) | Calidad de la dieta |
| exercise_frequency | int64 | 1000 | 0 | 0 | 7 | 0 | 6 | 3.04 |  | Frecuencia de ejercicio semanal |
| parental_education_level | str | 909 | 91 | 9.1 | 3 |  |  |  | High School (392); Bachelor (350); Master (167) | Nivel educativo de los padres (9.1% nulos) |
| internet_quality | str | 1000 | 0 | 0 | 3 |  |  |  | Good (447); Average (391); Poor (162) | Calidad de internet |
| mental_health_rating | int64 | 1000 | 0 | 0 | 10 | 1 | 10 | 5.44 |  | Salud mental autoreportada 1-10 (SEÑAL SINTÉTICA documentada) |
| extracurricular_participation | str | 1000 | 0 | 0 | 2 |  |  |  | No (682); Yes (318) | Participación extracurricular (Yes/No) |
| exam_score | float64 | 1000 | 0 | 0 | 480 | 18.4 | 100 | 69.6 |  | Nota de examen (0-100) |

## B2_SocialMediaSleep

| Social Media vs Sleep/Stress/Productivity (jayjoshi37, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 11000 filas × 10 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| user_id | int64 | 11000 | 0 | 0 | 11000 | 1 | 11000 | 5500.5 |  | Identificador de usuario |
| age | int64 | 11000 | 0 | 0 | 34 | 16 | 49 | 32.56 |  | Edad |
| daily_screen_time_hours | float64 | 11000 | 0 | 0 | 1101 | 1 | 12 | 6.56 |  | Horas de pantalla diarias |
| social_media_hours | float64 | 11000 | 0 | 0 | 751 | 0.5 | 8 | 4.25 |  | Horas diarias en redes sociales |
| sleep_hours | float64 | 11000 | 0 | 0 | 601 | 3 | 9 | 5.99 |  | Horas de sueño |
| exercise_minutes | int64 | 11000 | 0 | 0 | 120 | 0 | 119 | 59.47 |  | Minutos de ejercicio diarios |
| study_work_hours | float64 | 11000 | 0 | 0 | 901 | 1 | 10 | 5.54 |  | Horas de estudio/trabajo |
| productivity_score | float64 | 11000 | 0 | 0 | 6633 | 1 | 99.99 | 50.62 |  | Puntuación de productividad |
| stress_level | str | 11000 | 0 | 0 | 3 |  |  |  | Low (3715); Medium (3681); High (3604) | VARIABLE OBJETIVO: nivel de estrés (Low/Medium/High) |
| platform | str | 11000 | 0 | 0 | 5 |  |  |  | LinkedIn (2239); Snapchat (2235); YouTube (2200) | Plataforma principal de red social |

## B2_SMMH

| Social Media and Mental Health (souvikahmed071, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 481 filas × 21 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Timestamp | str | 481 | 0 | 0 | 480 |  |  |  | 5/11/2022 22:54:32 (2); 4/18/2022 19:18:47 (1); 4/18/2022 19:19:28 (1) | Fecha y hora de la respuesta |
| 1. What is your age? | float64 | 481 | 0 | 0 | 46 | 13 | 91 | 26.14 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 2. Gender | str | 481 | 0 | 0 | 9 |  |  |  | Female (263); Male (211); Nonbinary  (1) |  |
| 3. Relationship Status | str | 481 | 0 | 0 | 4 |  |  |  | Single (285); Married (101); In a relationship (88) |  |
| 4. Occupation Status | str | 481 | 0 | 0 | 4 |  |  |  | University Student (292); Salaried Worker (132); School Student (49) |  |
| 5. What type of organizations are you affiliated with? | str | 451 | 30 | 6.2 | 18 |  |  |  | University (239); Private (60); School (44) | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 6. Do you use social media? | str | 481 | 0 | 0 | 2 |  |  |  | Yes (478); No (3) | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 7. What social media platforms do you commonly use? | str | 481 | 0 | 0 | 125 |  |  |  | Facebook, Instagram, YouTube (35); Facebook, YouTube (30); Facebook, Instagram, YouTube (28) | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 8. What is the average time you spend on social media every day? | str | 481 | 0 | 0 | 6 |  |  |  | More than 5 hours (116); Between 2 and 3 hours (101); Between 3 and 4 hours (93) | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 9. How often do you find yourself using Social media without a specific purpose? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.55 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 10. How often do you get distracted by Social media when you are busy doing something? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.32 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 11. Do you feel restless if you haven't used Social media in a while? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 2.59 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 12. On a scale of 1 to 5, how easily distracted are you? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.35 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 13. On a scale of 1 to 5, how much are you bothered by worries? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.56 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 14. Do you find it difficult to concentrate on things? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.25 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 2.83 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 16. Following the previous question, how do you feel about these comparisons, generally speaking? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 2.78 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 17. How often do you look to seek validation from features of social media? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 2.46 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 18. How often do you feel depressed or down? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.26 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.17 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |
| 20. On a scale of 1 to 5, how often do you face issues regarding sleep? | int64 | 481 | 0 | 0 | 5 | 1 | 5 | 3.2 |  | Ítem de encuesta (ver enunciado completo en el nombre de la columna) |

## B2_Lifestyle

| Mental Health Lifestyle (datafit17, GitHub) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 3000 filas × 12 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Country | str | 3000 | 0 | 0 | 7 |  |  |  | USA (446); Japan (439); Australia (434) | País |
| Age | int64 | 3000 | 0 | 0 | 47 | 18 | 64 | 41.23 |  | Edad |
| Gender | str | 3000 | 0 | 0 | 3 |  |  |  | Female (1024); Other (996); Male (980) | Género |
| Exercise Level | str | 3000 | 0 | 0 | 3 |  |  |  | Low (1033); Moderate (998); High (969) | Nivel de ejercicio |
| Diet Type | str | 3000 | 0 | 0 | 5 |  |  |  | Junk Food (637); Balanced (625); Vegetarian (592) | Tipo de dieta |
| Sleep Hours | float64 | 3000 | 0 | 0 | 93 | 1.4 | 11.3 | 6.48 |  | Horas de sueño |
| Stress Level | str | 3000 | 0 | 0 | 3 |  |  |  | Low (1008); High (1002); Moderate (990) | VARIABLE OBJETIVO: estrés (Low/Moderate/High) |
| Mental Health Condition | str | 2405 | 595 | 19.8 | 4 |  |  |  | Anxiety (628); PTSD (624); Depression (580) | Diagnóstico (19.8% NaN = sin condición, recodificar 'Ninguna') |
| Work Hours per Week | int64 | 3000 | 0 | 0 | 40 | 20 | 59 | 39.47 |  | Horas de trabajo semanales |
| Screen Time per Day (Hours) | float64 | 3000 | 0 | 0 | 61 | 2 | 8 | 5.09 |  | Horas de pantalla diarias |
| Social Interaction Score | float64 | 3000 | 0 | 0 | 91 | 1 | 10 | 5.47 |  | Puntuación de interacción social |
| Happiness Score | float64 | 3000 | 0 | 0 | 91 | 1 | 10 | 5.4 |  | Puntuación de felicidad |

## B3_DreadditTrain

| Dreaddit train (payaldhokane, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 2838 filas × 116 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| subreddit | str | 2838 | 0 | 0 | 10 |  |  |  | ptsd (584); relationships (552); anxiety (503) | Subreddit de origen del post |
| post_id | str | 2838 | 0 | 0 | 2343 |  |  |  | 9md6qz (6); 7o5n2d (6); 7pg3a7 (5) | Identificador del post |
| sentence_range | str | 2838 | 0 | 0 | 173 |  |  |  | (0, 5) (337); [0, 5] (334); [5, 10] (260) | Rango de frases del fragmento |
| text | str | 2838 | 0 | 0 | 2820 |  |  |  | [NAME?] (4); Hello, You are invited to co (4); 7. This study will include o (3) | TEXTO del fragmento del post (input NLP) |
| id | int64 | 2838 | 0 | 0 | 2838 | 4 | 55757 | 13752 |  | Identificador del fragmento |
| label | int64 | 2838 | 0 | 0 | 2 | 0 | 1 | 0.52 |  | VARIABLE OBJETIVO: estrés (1) / no estrés (0), etiquetado manual |
| confidence | float64 | 2838 | 0 | 0 | 10 | 0.43 | 1 | 0.81 |  | Confianza del etiquetado (acuerdo entre anotadores) |
| social_timestamp | int64 | 2838 | 0 | 0 | 2343 | 1483274218 | 1542592460 | 1518107030.29 |  | Timestamp de publicación (epoch) |
| social_karma | int64 | 2838 | 0 | 0 | 135 | 0 | 1435 | 18.26 |  | Karma del post |
| syntax_ari | float64 | 2838 | 0 | 0 | 2659 | -6.62 | 24.07 | 4.68 |  | Índice de legibilidad ARI |
| lex_liwc_WC | int64 | 2838 | 0 | 0 | 198 | 5 | 310 | 86 |  | Categoría LIWC 'WC': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Analytic | float64 | 2838 | 0 | 0 | 1435 | 1 | 99 | 35.24 |  | Categoría LIWC 'Analytic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Clout | float64 | 2838 | 0 | 0 | 1323 | 1 | 99 | 40.95 |  | Categoría LIWC 'Clout': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Authentic | float64 | 2838 | 0 | 0 | 978 | 1 | 99 | 67.04 |  | Categoría LIWC 'Authentic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Tone | float64 | 2838 | 0 | 0 | 489 | 1 | 99 | 33.43 |  | Categoría LIWC 'Tone': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_WPS | float64 | 2838 | 0 | 0 | 360 | 2.4 | 233 | 18.19 |  | Categoría LIWC 'WPS': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Sixltr | float64 | 2838 | 0 | 0 | 938 | 0 | 65.12 | 14.86 |  | Categoría LIWC 'Sixltr': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Dic | float64 | 2838 | 0 | 0 | 833 | 27.91 | 100 | 92.35 |  | Categoría LIWC 'Dic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_function | float64 | 2838 | 0 | 0 | 1048 | 4.17 | 77.78 | 58.6 |  | Categoría LIWC 'function': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_pronoun | float64 | 2838 | 0 | 0 | 964 | 0 | 44.44 | 19.77 |  | Categoría LIWC 'pronoun': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ppron | float64 | 2838 | 0 | 0 | 889 | 0 | 30.77 | 13.99 |  | Categoría LIWC 'ppron': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_i | float64 | 2838 | 0 | 0 | 810 | 0 | 30 | 9.07 |  | Categoría LIWC 'i': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_we | float64 | 2838 | 0 | 0 | 293 | 0 | 12.96 | 0.76 |  | Categoría LIWC 'we': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_you | float64 | 2838 | 0 | 0 | 324 | 0 | 25 | 0.87 |  | Categoría LIWC 'you': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_shehe | float64 | 2838 | 0 | 0 | 548 | 0 | 23.47 | 2.71 |  | Categoría LIWC 'shehe': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_they | float64 | 2838 | 0 | 0 | 263 | 0 | 12.86 | 0.58 |  | Categoría LIWC 'they': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ipron | float64 | 2838 | 0 | 0 | 644 | 0 | 21.43 | 5.77 |  | Categoría LIWC 'ipron': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_article | float64 | 2838 | 0 | 0 | 572 | 0 | 15.53 | 4.94 |  | Categoría LIWC 'article': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_prep | float64 | 2838 | 0 | 0 | 737 | 0 | 29.63 | 13.36 |  | Categoría LIWC 'prep': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_auxverb | float64 | 2838 | 0 | 0 | 743 | 0 | 25 | 10.31 |  | Categoría LIWC 'auxverb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_adverb | float64 | 2838 | 0 | 0 | 655 | 0 | 21.43 | 6.05 |  | Categoría LIWC 'adverb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_conj | float64 | 2838 | 0 | 0 | 612 | 0 | 20.69 | 7.6 |  | Categoría LIWC 'conj': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_negate | float64 | 2838 | 0 | 0 | 398 | 0 | 12.9 | 2.26 |  | Categoría LIWC 'negate': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_verb | float64 | 2838 | 0 | 0 | 890 | 0 | 40 | 19.43 |  | Categoría LIWC 'verb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_adj | float64 | 2838 | 0 | 0 | 562 | 0 | 18.18 | 4.36 |  | Categoría LIWC 'adj': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_compare | float64 | 2838 | 0 | 0 | 424 | 0 | 15.15 | 2.29 |  | Categoría LIWC 'compare': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_interrog | float64 | 2838 | 0 | 0 | 346 | 0 | 17.86 | 1.61 |  | Categoría LIWC 'interrog': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_number | float64 | 2838 | 0 | 0 | 355 | 0 | 25 | 1.44 |  | Categoría LIWC 'number': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_quant | float64 | 2838 | 0 | 0 | 394 | 0 | 11.63 | 2.25 |  | Categoría LIWC 'quant': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_affect | float64 | 2838 | 0 | 0 | 692 | 0 | 37.5 | 6.1 |  | Categoría LIWC 'affect': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_posemo | float64 | 2838 | 0 | 0 | 497 | 0 | 20 | 2.7 |  | Categoría LIWC 'posemo': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_negemo | float64 | 2838 | 0 | 0 | 555 | 0 | 37.5 | 3.3 |  | Categoría LIWC 'negemo': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_anx | float64 | 2838 | 0 | 0 | 298 | 0 | 25 | 0.91 |  | Categoría LIWC 'anx': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_anger | float64 | 2838 | 0 | 0 | 293 | 0 | 15.79 | 0.93 |  | Categoría LIWC 'anger': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_sad | float64 | 2838 | 0 | 0 | 236 | 0 | 12.5 | 0.6 |  | Categoría LIWC 'sad': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_social | float64 | 2838 | 0 | 0 | 984 | 0 | 37.76 | 10.83 |  | Categoría LIWC 'social': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_family | float64 | 2838 | 0 | 0 | 291 | 0 | 17.95 | 0.75 |  | Categoría LIWC 'family': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_friend | float64 | 2838 | 0 | 0 | 236 | 0 | 10.28 | 0.56 |  | Categoría LIWC 'friend': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_female | float64 | 2838 | 0 | 0 | 448 | 0 | 18.06 | 1.58 |  | Categoría LIWC 'female': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_male | float64 | 2838 | 0 | 0 | 494 | 0 | 19.4 | 1.98 |  | Categoría LIWC 'male': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_cogproc | float64 | 2838 | 0 | 0 | 929 | 0 | 37.5 | 13.59 |  | Categoría LIWC 'cogproc': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_insight | float64 | 2838 | 0 | 0 | 461 | 0 | 13.24 | 2.86 |  | Categoría LIWC 'insight': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_cause | float64 | 2838 | 0 | 0 | 369 | 0 | 12.5 | 1.73 |  | Categoría LIWC 'cause': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_discrep | float64 | 2838 | 0 | 0 | 400 | 0 | 12.5 | 1.95 |  | Categoría LIWC 'discrep': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_tentat | float64 | 2838 | 0 | 0 | 521 | 0 | 16.67 | 3.32 |  | Categoría LIWC 'tentat': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_certain | float64 | 2838 | 0 | 0 | 342 | 0 | 11.86 | 1.54 |  | Categoría LIWC 'certain': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_differ | float64 | 2838 | 0 | 0 | 531 | 0 | 18.42 | 3.97 |  | Categoría LIWC 'differ': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_percept | float64 | 2838 | 0 | 0 | 433 | 0 | 22.22 | 2.25 |  | Categoría LIWC 'percept': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_see | float64 | 2838 | 0 | 0 | 232 | 0 | 10.87 | 0.57 |  | Categoría LIWC 'see': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_hear | float64 | 2838 | 0 | 0 | 244 | 0 | 9.43 | 0.61 |  | Categoría LIWC 'hear': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_feel | float64 | 2838 | 0 | 0 | 282 | 0 | 22.22 | 0.91 |  | Categoría LIWC 'feel': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_bio | float64 | 2838 | 0 | 0 | 494 | 0 | 44.44 | 2.61 |  | Categoría LIWC 'bio': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_body | float64 | 2838 | 0 | 0 | 275 | 0 | 21.11 | 0.71 |  | Categoría LIWC 'body': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_health | float64 | 2838 | 0 | 0 | 343 | 0 | 13.11 | 1.25 |  | Categoría LIWC 'health': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_sexual | float64 | 2838 | 0 | 0 | 161 | 0 | 7.34 | 0.21 |  | Categoría LIWC 'sexual': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ingest | float64 | 2838 | 0 | 0 | 202 | 0 | 33.33 | 0.41 |  | Categoría LIWC 'ingest': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_drives | float64 | 2838 | 0 | 0 | 741 | 0 | 37.5 | 7.89 |  | Categoría LIWC 'drives': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_affiliation | float64 | 2838 | 0 | 0 | 512 | 0 | 23.08 | 2.74 |  | Categoría LIWC 'affiliation': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_achieve | float64 | 2838 | 0 | 0 | 331 | 0 | 16.67 | 1.37 |  | Categoría LIWC 'achieve': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_power | float64 | 2838 | 0 | 0 | 431 | 0 | 13.33 | 2.41 |  | Categoría LIWC 'power': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_reward | float64 | 2838 | 0 | 0 | 313 | 0 | 7.55 | 1.37 |  | Categoría LIWC 'reward': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_risk | float64 | 2838 | 0 | 0 | 243 | 0 | 25 | 0.72 |  | Categoría LIWC 'risk': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focuspast | float64 | 2838 | 0 | 0 | 699 | 0 | 26.32 | 5.06 |  | Categoría LIWC 'focuspast': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focuspresent | float64 | 2838 | 0 | 0 | 945 | 0 | 35.71 | 12.32 |  | Categoría LIWC 'focuspresent': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focusfuture | float64 | 2838 | 0 | 0 | 305 | 0 | 11.86 | 1.18 |  | Categoría LIWC 'focusfuture': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_relativ | float64 | 2838 | 0 | 0 | 965 | 0 | 39.29 | 14.25 |  | Categoría LIWC 'relativ': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_motion | float64 | 2838 | 0 | 0 | 377 | 0 | 14.55 | 2 |  | Categoría LIWC 'motion': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_space | float64 | 2838 | 0 | 0 | 670 | 0 | 21.43 | 6.3 |  | Categoría LIWC 'space': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_time | float64 | 2838 | 0 | 0 | 721 | 0 | 27.27 | 6.2 |  | Categoría LIWC 'time': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_work | float64 | 2838 | 0 | 0 | 438 | 0 | 20 | 1.88 |  | Categoría LIWC 'work': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_leisure | float64 | 2838 | 0 | 0 | 278 | 0 | 13.33 | 0.79 |  | Categoría LIWC 'leisure': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_home | float64 | 2838 | 0 | 0 | 256 | 0 | 13.79 | 0.64 |  | Categoría LIWC 'home': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_money | float64 | 2838 | 0 | 0 | 309 | 0 | 14.93 | 0.79 |  | Categoría LIWC 'money': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_relig | float64 | 2838 | 0 | 0 | 117 | 0 | 8.24 | 0.12 |  | Categoría LIWC 'relig': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_death | float64 | 2838 | 0 | 0 | 123 | 0 | 11.11 | 0.14 |  | Categoría LIWC 'death': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_informal | float64 | 2838 | 0 | 0 | 260 | 0 | 13.04 | 0.83 |  | Categoría LIWC 'informal': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_swear | float64 | 2838 | 0 | 0 | 166 | 0 | 8.33 | 0.25 |  | Categoría LIWC 'swear': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_netspeak | float64 | 2838 | 0 | 0 | 159 | 0 | 11.11 | 0.26 |  | Categoría LIWC 'netspeak': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_assent | float64 | 2838 | 0 | 0 | 118 | 0 | 8.7 | 0.12 |  | Categoría LIWC 'assent': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_nonflu | float64 | 2838 | 0 | 0 | 110 | 0 | 3.85 | 0.12 |  | Categoría LIWC 'nonflu': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_filler | float64 | 2838 | 0 | 0 | 67 | 0 | 11.11 | 0.05 |  | Categoría LIWC 'filler': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_AllPunc | float64 | 2838 | 0 | 0 | 990 | 3.12 | 420.41 | 17.05 |  | Categoría LIWC 'AllPunc': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Period | float64 | 2838 | 0 | 0 | 512 | 0 | 47.06 | 6.07 |  | Categoría LIWC 'Period': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Comma | float64 | 2838 | 0 | 0 | 546 | 0 | 41.86 | 3.57 |  | Categoría LIWC 'Comma': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Colon | float64 | 2838 | 0 | 0 | 132 | 0 | 20 | 0.22 |  | Categoría LIWC 'Colon': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_SemiC | float64 | 2838 | 0 | 0 | 106 | 0 | 10.53 | 0.12 |  | Categoría LIWC 'SemiC': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_QMark | float64 | 2838 | 0 | 0 | 205 | 0 | 105.41 | 0.52 |  | Categoría LIWC 'QMark': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Exclam | float64 | 2838 | 0 | 0 | 127 | 0 | 40 | 0.19 |  | Categoría LIWC 'Exclam': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Dash | float64 | 2838 | 0 | 0 | 221 | 0 | 55.56 | 0.49 |  | Categoría LIWC 'Dash': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Quote | float64 | 2838 | 0 | 0 | 193 | 0 | 12.5 | 0.47 |  | Categoría LIWC 'Quote': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Apostro | float64 | 2838 | 0 | 0 | 510 | 0 | 25 | 3.18 |  | Categoría LIWC 'Apostro': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Parenth | float64 | 2838 | 0 | 0 | 216 | 0 | 41.94 | 0.78 |  | Categoría LIWC 'Parenth': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_OtherP | float64 | 2838 | 0 | 0 | 348 | 0 | 391.84 | 1.44 |  | Categoría LIWC 'OtherP': % de palabras del texto en esa categoría psicolingüística |
| lex_dal_max_pleasantness | float64 | 2838 | 0 | 0 | 41 | 2 | 3 | 2.8 |  | Índice DAL 'max_pleasantness' (Dictionary of Affect in Language) |
| lex_dal_max_activation | float64 | 2838 | 0 | 0 | 54 | 1.86 | 3 | 2.7 |  | Índice DAL 'max_activation' (Dictionary of Affect in Language) |
| lex_dal_max_imagery | float64 | 2838 | 0 | 0 | 6 | 2 | 3 | 2.95 |  | Índice DAL 'max_imagery' (Dictionary of Affect in Language) |
| lex_dal_min_pleasantness | float64 | 2838 | 0 | 0 | 33 | 1 | 1.9 | 1.09 |  | Índice DAL 'min_pleasantness' (Dictionary of Affect in Language) |
| lex_dal_min_activation | float64 | 2838 | 0 | 0 | 22 | 1 | 1.5 | 1.12 |  | Índice DAL 'min_activation' (Dictionary of Affect in Language) |
| lex_dal_min_imagery | float64 | 2838 | 0 | 0 | 2 | 1 | 1.2 | 1 |  | Índice DAL 'min_imagery' (Dictionary of Affect in Language) |
| lex_dal_avg_activation | float64 | 2838 | 0 | 0 | 2606 | 1.49 | 2.01 | 1.72 |  | Índice DAL 'avg_activation' (Dictionary of Affect in Language) |
| lex_dal_avg_imagery | float64 | 2838 | 0 | 0 | 2111 | 1.2 | 2.07 | 1.54 |  | Índice DAL 'avg_imagery' (Dictionary of Affect in Language) |
| lex_dal_avg_pleasantness | float64 | 2838 | 0 | 0 | 2615 | 1.56 | 2.16 | 1.88 |  | Índice DAL 'avg_pleasantness' (Dictionary of Affect in Language) |
| social_upvote_ratio | float64 | 2838 | 0 | 0 | 73 | 0.14 | 1 | 0.84 |  | Metadato social del post: upvote_ratio |
| social_num_comments | int64 | 2838 | 0 | 0 | 94 | 0 | 416 | 9.95 |  | Número de comentarios |
| syntax_fk_grade | float64 | 2838 | 0 | 0 | 2417 | -1.92 | 21.2 | 5.45 |  | Índice de legibilidad Flesch-Kincaid |
| sentiment | float64 | 2838 | 0 | 0 | 1809 | -1 | 1 | 0.04 |  | Sentimiento del texto (polaridad, -1 a 1) |

## B3_DreadditTest

| Dreaddit test (payaldhokane, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 715 filas × 116 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| id | int64 | 715 | 0 | 0 | 715 | 2 | 55783 | 13861.37 |  | Identificador del fragmento |
| subreddit | str | 715 | 0 | 0 | 10 |  |  |  | anxiety (147); relationships (142); ptsd (127) | Subreddit de origen del post |
| post_id | str | 715 | 0 | 0 | 586 |  |  |  | 8c6fwz (6); 5y4i6r (5); 884mzo (5) | Identificador del post |
| sentence_range | str | 715 | 0 | 0 | 111 |  |  |  | [0, 5] (97); (0, 5) (91); [5, 10] (64) | Rango de frases del fragmento |
| text | str | 715 | 0 | 0 | 715 |  |  |  | Its like that, if you want o (1); I man the front desk and my  (1); We'd be saving so much money (1) | TEXTO del fragmento del post (input NLP) |
| label | int64 | 715 | 0 | 0 | 2 | 0 | 1 | 0.52 |  | VARIABLE OBJETIVO: estrés (1) / no estrés (0), etiquetado manual |
| confidence | float64 | 715 | 0 | 0 | 10 | 0 | 1 | 0.72 |  | Confianza del etiquetado (acuerdo entre anotadores) |
| social_timestamp | float64 | 715 | 0 | 0 | 586 | 1483329777 | 1542583224 | 1517569805.77 |  | Timestamp de publicación (epoch) |
| social_karma | int64 | 715 | 0 | 0 | 74 | 0 | 1687 | 24.63 |  | Karma del post |
| syntax_ari | float64 | 715 | 0 | 0 | 698 | -4.8 | 22.54 | 4.71 |  | Índice de legibilidad ARI |
| lex_liwc_WC | int64 | 715 | 0 | 0 | 142 | 12 | 264 | 85.67 |  | Categoría LIWC 'WC': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Analytic | float64 | 715 | 0 | 0 | 550 | 1 | 98.22 | 34.74 |  | Categoría LIWC 'Analytic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Clout | float64 | 715 | 0 | 0 | 500 | 1 | 99 | 38.41 |  | Categoría LIWC 'Clout': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Authentic | float64 | 715 | 0 | 0 | 396 | 1 | 99 | 69.92 |  | Categoría LIWC 'Authentic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Tone | float64 | 715 | 0 | 0 | 277 | 1 | 99 | 32.38 |  | Categoría LIWC 'Tone': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_WPS | float64 | 715 | 0 | 0 | 211 | 2.4 | 60 | 17.86 |  | Categoría LIWC 'WPS': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Sixltr | float64 | 715 | 0 | 0 | 441 | 0 | 35.44 | 14.89 |  | Categoría LIWC 'Sixltr': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Dic | float64 | 715 | 0 | 0 | 421 | 66.67 | 100 | 92.51 |  | Categoría LIWC 'Dic': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_function | float64 | 715 | 0 | 0 | 475 | 16.67 | 73.47 | 58.89 |  | Categoría LIWC 'function': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_pronoun | float64 | 715 | 0 | 0 | 455 | 0 | 38.89 | 20.05 |  | Categoría LIWC 'pronoun': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ppron | float64 | 715 | 0 | 0 | 428 | 0 | 30.19 | 14.11 |  | Categoría LIWC 'ppron': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_i | float64 | 715 | 0 | 0 | 401 | 0 | 23.08 | 9.36 |  | Categoría LIWC 'i': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_we | float64 | 715 | 0 | 0 | 141 | 0 | 12.5 | 0.78 |  | Categoría LIWC 'we': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_you | float64 | 715 | 0 | 0 | 126 | 0 | 15.52 | 0.78 |  | Categoría LIWC 'you': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_shehe | float64 | 715 | 0 | 0 | 250 | 0 | 20 | 2.62 |  | Categoría LIWC 'shehe': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_they | float64 | 715 | 0 | 0 | 126 | 0 | 12.63 | 0.57 |  | Categoría LIWC 'they': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ipron | float64 | 715 | 0 | 0 | 354 | 0 | 18.18 | 5.93 |  | Categoría LIWC 'ipron': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_article | float64 | 715 | 0 | 0 | 333 | 0 | 17.65 | 4.83 |  | Categoría LIWC 'article': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_prep | float64 | 715 | 0 | 0 | 378 | 0 | 23.73 | 13.5 |  | Categoría LIWC 'prep': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_auxverb | float64 | 715 | 0 | 0 | 394 | 0 | 27.78 | 10.23 |  | Categoría LIWC 'auxverb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_adverb | float64 | 715 | 0 | 0 | 364 | 0 | 17.14 | 6.17 |  | Categoría LIWC 'adverb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_conj | float64 | 715 | 0 | 0 | 337 | 0 | 16.67 | 7.74 |  | Categoría LIWC 'conj': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_negate | float64 | 715 | 0 | 0 | 234 | 0 | 11.54 | 2.28 |  | Categoría LIWC 'negate': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_verb | float64 | 715 | 0 | 0 | 426 | 5.36 | 35.48 | 19.27 |  | Categoría LIWC 'verb': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_adj | float64 | 715 | 0 | 0 | 329 | 0 | 15.96 | 4.53 |  | Categoría LIWC 'adj': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_compare | float64 | 715 | 0 | 0 | 259 | 0 | 9.8 | 2.34 |  | Categoría LIWC 'compare': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_interrog | float64 | 715 | 0 | 0 | 207 | 0 | 10 | 1.52 |  | Categoría LIWC 'interrog': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_number | float64 | 715 | 0 | 0 | 206 | 0 | 25 | 1.38 |  | Categoría LIWC 'number': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_quant | float64 | 715 | 0 | 0 | 249 | 0 | 10.61 | 2.32 |  | Categoría LIWC 'quant': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_affect | float64 | 715 | 0 | 0 | 363 | 0 | 17.33 | 6.05 |  | Categoría LIWC 'affect': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_posemo | float64 | 715 | 0 | 0 | 258 | 0 | 14.29 | 2.61 |  | Categoría LIWC 'posemo': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_negemo | float64 | 715 | 0 | 0 | 294 | 0 | 16.67 | 3.36 |  | Categoría LIWC 'negemo': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_anx | float64 | 715 | 0 | 0 | 180 | 0 | 16.67 | 0.98 |  | Categoría LIWC 'anx': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_anger | float64 | 715 | 0 | 0 | 166 | 0 | 11.9 | 0.88 |  | Categoría LIWC 'anger': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_sad | float64 | 715 | 0 | 0 | 128 | 0 | 6.45 | 0.6 |  | Categoría LIWC 'sad': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_social | float64 | 715 | 0 | 0 | 471 | 0 | 33.33 | 10.39 |  | Categoría LIWC 'social': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_family | float64 | 715 | 0 | 0 | 129 | 0 | 10 | 0.65 |  | Categoría LIWC 'family': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_friend | float64 | 715 | 0 | 0 | 131 | 0 | 7.35 | 0.56 |  | Categoría LIWC 'friend': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_female | float64 | 715 | 0 | 0 | 198 | 0 | 18.33 | 1.6 |  | Categoría LIWC 'female': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_male | float64 | 715 | 0 | 0 | 210 | 0 | 15.09 | 1.81 |  | Categoría LIWC 'male': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_cogproc | float64 | 715 | 0 | 0 | 436 | 0 | 35.71 | 13.9 |  | Categoría LIWC 'cogproc': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_insight | float64 | 715 | 0 | 0 | 272 | 0 | 12.66 | 2.84 |  | Categoría LIWC 'insight': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_cause | float64 | 715 | 0 | 0 | 217 | 0 | 12 | 1.72 |  | Categoría LIWC 'cause': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_discrep | float64 | 715 | 0 | 0 | 241 | 0 | 11.76 | 1.9 |  | Categoría LIWC 'discrep': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_tentat | float64 | 715 | 0 | 0 | 310 | 0 | 16.13 | 3.46 |  | Categoría LIWC 'tentat': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_certain | float64 | 715 | 0 | 0 | 212 | 0 | 8.57 | 1.61 |  | Categoría LIWC 'certain': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_differ | float64 | 715 | 0 | 0 | 322 | 0 | 16.13 | 4.14 |  | Categoría LIWC 'differ': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_percept | float64 | 715 | 0 | 0 | 252 | 0 | 14.29 | 2.38 |  | Categoría LIWC 'percept': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_see | float64 | 715 | 0 | 0 | 129 | 0 | 14.29 | 0.64 |  | Categoría LIWC 'see': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_hear | float64 | 715 | 0 | 0 | 131 | 0 | 8.33 | 0.6 |  | Categoría LIWC 'hear': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_feel | float64 | 715 | 0 | 0 | 164 | 0 | 7.79 | 0.96 |  | Categoría LIWC 'feel': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_bio | float64 | 715 | 0 | 0 | 276 | 0 | 16.36 | 2.62 |  | Categoría LIWC 'bio': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_body | float64 | 715 | 0 | 0 | 147 | 0 | 9.09 | 0.72 |  | Categoría LIWC 'body': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_health | float64 | 715 | 0 | 0 | 189 | 0 | 10.81 | 1.23 |  | Categoría LIWC 'health': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_sexual | float64 | 715 | 0 | 0 | 69 | 0 | 7.32 | 0.22 |  | Categoría LIWC 'sexual': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_ingest | float64 | 715 | 0 | 0 | 101 | 0 | 8.33 | 0.38 |  | Categoría LIWC 'ingest': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_drives | float64 | 715 | 0 | 0 | 385 | 0 | 33.33 | 7.74 |  | Categoría LIWC 'drives': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_affiliation | float64 | 715 | 0 | 0 | 276 | 0 | 19.05 | 2.63 |  | Categoría LIWC 'affiliation': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_achieve | float64 | 715 | 0 | 0 | 203 | 0 | 16.67 | 1.29 |  | Categoría LIWC 'achieve': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_power | float64 | 715 | 0 | 0 | 265 | 0 | 11.11 | 2.47 |  | Categoría LIWC 'power': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_reward | float64 | 715 | 0 | 0 | 188 | 0 | 9.68 | 1.35 |  | Categoría LIWC 'reward': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_risk | float64 | 715 | 0 | 0 | 149 | 0 | 6.67 | 0.73 |  | Categoría LIWC 'risk': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focuspast | float64 | 715 | 0 | 0 | 370 | 0 | 19.51 | 5.09 |  | Categoría LIWC 'focuspast': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focuspresent | float64 | 715 | 0 | 0 | 460 | 0 | 30.95 | 12.26 |  | Categoría LIWC 'focuspresent': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_focusfuture | float64 | 715 | 0 | 0 | 187 | 0 | 8.33 | 1.15 |  | Categoría LIWC 'focusfuture': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_relativ | float64 | 715 | 0 | 0 | 440 | 0 | 36.76 | 14.5 |  | Categoría LIWC 'relativ': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_motion | float64 | 715 | 0 | 0 | 234 | 0 | 13.51 | 1.98 |  | Categoría LIWC 'motion': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_space | float64 | 715 | 0 | 0 | 368 | 0 | 22.06 | 6.33 |  | Categoría LIWC 'space': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_time | float64 | 715 | 0 | 0 | 373 | 0 | 24.29 | 6.42 |  | Categoría LIWC 'time': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_work | float64 | 715 | 0 | 0 | 235 | 0 | 22.22 | 1.77 |  | Categoría LIWC 'work': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_leisure | float64 | 715 | 0 | 0 | 151 | 0 | 11.54 | 0.77 |  | Categoría LIWC 'leisure': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_home | float64 | 715 | 0 | 0 | 129 | 0 | 7.41 | 0.57 |  | Categoría LIWC 'home': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_money | float64 | 715 | 0 | 0 | 133 | 0 | 16.67 | 0.72 |  | Categoría LIWC 'money': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_relig | float64 | 715 | 0 | 0 | 49 | 0 | 9.68 | 0.13 |  | Categoría LIWC 'relig': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_death | float64 | 715 | 0 | 0 | 54 | 0 | 3.9 | 0.14 |  | Categoría LIWC 'death': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_informal | float64 | 715 | 0 | 0 | 150 | 0 | 14.29 | 0.82 |  | Categoría LIWC 'informal': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_swear | float64 | 715 | 0 | 0 | 79 | 0 | 5.26 | 0.25 |  | Categoría LIWC 'swear': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_netspeak | float64 | 715 | 0 | 0 | 64 | 0 | 6.67 | 0.22 |  | Categoría LIWC 'netspeak': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_assent | float64 | 715 | 0 | 0 | 58 | 0 | 3.57 | 0.13 |  | Categoría LIWC 'assent': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_nonflu | float64 | 715 | 0 | 0 | 45 | 0 | 2.94 | 0.11 |  | Categoría LIWC 'nonflu': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_filler | float64 | 715 | 0 | 0 | 24 | 0 | 3.33 | 0.05 |  | Categoría LIWC 'filler': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_AllPunc | float64 | 715 | 0 | 0 | 458 | 4.65 | 166.1 | 16.73 |  | Categoría LIWC 'AllPunc': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Period | float64 | 715 | 0 | 0 | 289 | 0 | 33.33 | 6.2 |  | Categoría LIWC 'Period': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Comma | float64 | 715 | 0 | 0 | 300 | 0 | 22.58 | 3.57 |  | Categoría LIWC 'Comma': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Colon | float64 | 715 | 0 | 0 | 58 | 0 | 9.52 | 0.19 |  | Categoría LIWC 'Colon': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_SemiC | float64 | 715 | 0 | 0 | 40 | 0 | 8.33 | 0.1 |  | Categoría LIWC 'SemiC': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_QMark | float64 | 715 | 0 | 0 | 105 | 0 | 8.57 | 0.46 |  | Categoría LIWC 'QMark': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Exclam | float64 | 715 | 0 | 0 | 47 | 0 | 9.38 | 0.16 |  | Categoría LIWC 'Exclam': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Dash | float64 | 715 | 0 | 0 | 100 | 0 | 48.08 | 0.47 |  | Categoría LIWC 'Dash': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Quote | float64 | 715 | 0 | 0 | 82 | 0 | 14.29 | 0.43 |  | Categoría LIWC 'Quote': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Apostro | float64 | 715 | 0 | 0 | 293 | 0 | 18.18 | 3.33 |  | Categoría LIWC 'Apostro': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_Parenth | float64 | 715 | 0 | 0 | 117 | 0 | 16.67 | 0.74 |  | Categoría LIWC 'Parenth': % de palabras del texto en esa categoría psicolingüística |
| lex_liwc_OtherP | float64 | 715 | 0 | 0 | 135 | 0 | 152.54 | 1.1 |  | Categoría LIWC 'OtherP': % de palabras del texto en esa categoría psicolingüística |
| lex_dal_max_pleasantness | float64 | 715 | 0 | 0 | 28 | 2.3 | 3 | 2.8 |  | Índice DAL 'max_pleasantness' (Dictionary of Affect in Language) |
| lex_dal_max_activation | float64 | 715 | 0 | 0 | 39 | 2.11 | 3 | 2.71 |  | Índice DAL 'max_activation' (Dictionary of Affect in Language) |
| lex_dal_max_imagery | float64 | 715 | 0 | 0 | 6 | 2 | 3 | 2.94 |  | Índice DAL 'max_imagery' (Dictionary of Affect in Language) |
| lex_dal_min_pleasantness | float64 | 715 | 0 | 0 | 22 | 1 | 1.78 | 1.08 |  | Índice DAL 'min_pleasantness' (Dictionary of Affect in Language) |
| lex_dal_min_activation | float64 | 715 | 0 | 0 | 17 | 1 | 1.78 | 1.12 |  | Índice DAL 'min_activation' (Dictionary of Affect in Language) |
| lex_dal_min_imagery | float64 | 715 | 0 | 0 | 2 | 1 | 1.2 | 1 |  | Índice DAL 'min_imagery' (Dictionary of Affect in Language) |
| lex_dal_avg_activation | float64 | 715 | 0 | 0 | 700 | 1.57 | 1.95 | 1.72 |  | Índice DAL 'avg_activation' (Dictionary of Affect in Language) |
| lex_dal_avg_imagery | float64 | 715 | 0 | 0 | 644 | 1.28 | 2.04 | 1.53 |  | Índice DAL 'avg_imagery' (Dictionary of Affect in Language) |
| lex_dal_avg_pleasantness | float64 | 715 | 0 | 0 | 703 | 1.72 | 2.14 | 1.88 |  | Índice DAL 'avg_pleasantness' (Dictionary of Affect in Language) |
| social_upvote_ratio | float64 | 715 | 0 | 0 | 63 | 0.2 | 1 | 0.86 |  | Metadato social del post: upvote_ratio |
| social_num_comments | int64 | 715 | 0 | 0 | 53 | 0 | 128 | 8.95 |  | Número de comentarios |
| syntax_fk_grade | float64 | 715 | 0 | 0 | 685 | -2.32 | 18.53 | 5.5 |  | Índice de legibilidad Flesch-Kincaid |
| sentiment | float64 | 715 | 0 | 0 | 602 | -1 | 0.8 | 0.05 |  | Sentimiento del texto (polaridad, -1 a 1) |

## B3_DepressionStudent

| Depression Student Dataset (prajwalg26, GitHub) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 502 filas × 11 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Gender | str | 502 | 0 | 0 | 2 |  |  |  | Male (267); Female (235) | Género |
| Age | int64 | 502 | 0 | 0 | 17 | 18 | 34 | 26.24 |  | Edad |
| Academic Pressure | float64 | 502 | 0 | 0 | 5 | 1 | 5 | 3 |  | Presión académica (1-5) |
| Study Satisfaction | float64 | 502 | 0 | 0 | 5 | 1 | 5 | 3.08 |  | Satisfacción con los estudios (1-5) |
| Sleep Duration | str | 502 | 0 | 0 | 4 |  |  |  | 7-8 hours (128); More than 8 hours (128); 5-6 hours (123) | Duración del sueño (categórica) |
| Dietary Habits | str | 502 | 0 | 0 | 3 |  |  |  | Moderate (172); Unhealthy (169); Healthy (161) | Hábitos alimentarios |
| Have you ever had suicidal thoughts ? | str | 502 | 0 | 0 | 2 |  |  |  | Yes (260); No (242) | Pensamientos suicidas (Yes/No) |
| Study Hours | int64 | 502 | 0 | 0 | 13 | 0 | 12 | 6.4 |  | Horas de estudio diarias |
| Financial Stress | int64 | 502 | 0 | 0 | 5 | 1 | 5 | 2.93 |  | Estrés financiero (1-5) |
| Family History of Mental Illness | str | 502 | 0 | 0 | 2 |  |  |  | No (265); Yes (237) | Antecedentes familiares (Yes/No) |
| Depression | str | 502 | 0 | 0 | 2 |  |  |  | Yes (252); No (250) | VARIABLE OBJETIVO: depresión (Yes/No) |

## B4_DASS42

| DASS-42 (lucasgreenwell, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 39775 filas × 172 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Q1A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.62 |  | Respuesta al ítem 1 del DASS-42 (1-4) |
| Q1I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.56 |  | Posición del ítem 1 en el orden aleatorio del test |
| Q1E | int64 | 39775 | 0 | 0 | 10879 | 180 | 12102282 | 6970.59 |  | Tiempo de respuesta del ítem 1 (milisegundos) |
| Q2A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.17 |  | Respuesta al ítem 2 del DASS-42 (1-4) |
| Q2I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.25 |  | Posición del ítem 2 en el orden aleatorio del test |
| Q2E | int64 | 39775 | 0 | 0 | 10325 | 176 | 2161057 | 5332.38 |  | Tiempo de respuesta del ítem 2 (milisegundos) |
| Q3A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.23 |  | Respuesta al ítem 3 del DASS-42 (1-4) |
| Q3I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.58 |  | Posición del ítem 3 en el orden aleatorio del test |
| Q3E | int64 | 39775 | 0 | 0 | 11110 | -10814 | 28582689 | 7426.45 |  | Tiempo de respuesta del ítem 3 (milisegundos) |
| Q4A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.95 |  | Respuesta al ítem 4 del DASS-42 (1-4) |
| Q4I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 4 en el orden aleatorio del test |
| Q4E | int64 | 39775 | 0 | 0 | 11510 | 176 | 9488330 | 7128.73 |  | Tiempo de respuesta del ítem 4 (milisegundos) |
| Q5A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.52 |  | Respuesta al ítem 5 del DASS-42 (1-4) |
| Q5I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.49 |  | Posición del ítem 5 en el orden aleatorio del test |
| Q5E | int64 | 39775 | 0 | 0 | 10142 | 178 | 9467497 | 5919.31 |  | Tiempo de respuesta del ítem 5 (milisegundos) |
| Q6A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.54 |  | Respuesta al ítem 6 del DASS-42 (1-4) |
| Q6I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.56 |  | Posición del ítem 6 en el orden aleatorio del test |
| Q6E | int64 | 39775 | 0 | 0 | 9944 | 178 | 5426858 | 5724.1 |  | Tiempo de respuesta del ítem 6 (milisegundos) |
| Q7A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.92 |  | Respuesta al ítem 7 del DASS-42 (1-4) |
| Q7I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.53 |  | Posición del ítem 7 en el orden aleatorio del test |
| Q7E | int64 | 39775 | 0 | 0 | 10403 | 178 | 74124488 | 9776.97 |  | Tiempo de respuesta del ítem 7 (milisegundos) |
| Q8A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.48 |  | Respuesta al ítem 8 del DASS-42 (1-4) |
| Q8I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.57 |  | Posición del ítem 8 en el orden aleatorio del test |
| Q8E | int64 | 39775 | 0 | 0 | 8977 | 179 | 2103626 | 4444.63 |  | Tiempo de respuesta del ítem 8 (milisegundos) |
| Q9A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.67 |  | Respuesta al ítem 9 del DASS-42 (1-4) |
| Q9I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.58 |  | Posición del ítem 9 en el orden aleatorio del test |
| Q9E | int64 | 39775 | 0 | 0 | 15012 | 177 | 279772213 | 18330.83 |  | Tiempo de respuesta del ítem 9 (milisegundos) |
| Q10A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.45 |  | Respuesta al ítem 10 del DASS-42 (1-4) |
| Q10I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.42 |  | Posición del ítem 10 en el orden aleatorio del test |
| Q10E | int64 | 39775 | 0 | 0 | 10177 | -19695 | 74471124 | 9157.49 |  | Tiempo de respuesta del ítem 10 (milisegundos) |
| Q11A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.8 |  | Respuesta al ítem 11 del DASS-42 (1-4) |
| Q11I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.43 |  | Posición del ítem 11 en el orden aleatorio del test |
| Q11E | int64 | 39775 | 0 | 0 | 9684 | 180 | 6201142 | 5490.15 |  | Tiempo de respuesta del ítem 11 (milisegundos) |
| Q12A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.43 |  | Respuesta al ítem 12 del DASS-42 (1-4) |
| Q12I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.49 |  | Posición del ítem 12 en el orden aleatorio del test |
| Q12E | int64 | 39775 | 0 | 0 | 10256 | 177 | 28535639 | 6570.47 |  | Tiempo de respuesta del ítem 12 (milisegundos) |
| Q13A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.78 |  | Respuesta al ítem 13 del DASS-42 (1-4) |
| Q13I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 13 en el orden aleatorio del test |
| Q13E | int64 | 39775 | 0 | 0 | 8596 | 177 | 4095293 | 3931.87 |  | Tiempo de respuesta del ítem 13 (milisegundos) |
| Q14A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.58 |  | Respuesta al ítem 14 del DASS-42 (1-4) |
| Q14I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.57 |  | Posición del ítem 14 en el orden aleatorio del test |
| Q14E | int64 | 39775 | 0 | 0 | 13297 | 180 | 75366349 | 10348.75 |  | Tiempo de respuesta del ítem 14 (milisegundos) |
| Q15A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.83 |  | Respuesta al ítem 15 del DASS-42 (1-4) |
| Q15I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 15 en el orden aleatorio del test |
| Q15E | int64 | 39775 | 0 | 0 | 9862 | -8195 | 6211384 | 5243.59 |  | Tiempo de respuesta del ítem 15 (milisegundos) |
| Q16A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.52 |  | Respuesta al ítem 16 del DASS-42 (1-4) |
| Q16I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.46 |  | Posición del ítem 16 en el orden aleatorio del test |
| Q16E | int64 | 39775 | 0 | 0 | 10505 | -493 | 18593374 | 6446.74 |  | Tiempo de respuesta del ítem 16 (milisegundos) |
| Q17A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.66 |  | Respuesta al ítem 17 del DASS-42 (1-4) |
| Q17I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 17 en el orden aleatorio del test |
| Q17E | int64 | 39775 | 0 | 0 | 9771 | 177 | 8804235 | 5197.92 |  | Tiempo de respuesta del ítem 17 (milisegundos) |
| Q18A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.48 |  | Respuesta al ítem 18 del DASS-42 (1-4) |
| Q18I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.53 |  | Posición del ítem 18 en el orden aleatorio del test |
| Q18E | int64 | 39775 | 0 | 0 | 10890 | 179 | 43266690 | 7293.52 |  | Tiempo de respuesta del ítem 18 (milisegundos) |
| Q19A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.95 |  | Respuesta al ítem 19 del DASS-42 (1-4) |
| Q19I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.55 |  | Posición del ítem 19 en el orden aleatorio del test |
| Q19E | int64 | 39775 | 0 | 0 | 13648 | 180 | 53230195 | 11244.46 |  | Tiempo de respuesta del ítem 19 (milisegundos) |
| Q20A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.32 |  | Respuesta al ítem 20 del DASS-42 (1-4) |
| Q20I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.52 |  | Posición del ítem 20 en el orden aleatorio del test |
| Q20E | int64 | 39775 | 0 | 0 | 9734 | 177 | 4950647 | 4965.48 |  | Tiempo de respuesta del ítem 20 (milisegundos) |
| Q21A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.35 |  | Respuesta al ítem 21 del DASS-42 (1-4) |
| Q21I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.57 |  | Posición del ítem 21 en el orden aleatorio del test |
| Q21E | int64 | 39775 | 0 | 0 | 9445 | -5125 | 29328385 | 5596.29 |  | Tiempo de respuesta del ítem 21 (milisegundos) |
| Q22A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.34 |  | Respuesta al ítem 22 del DASS-42 (1-4) |
| Q22I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.52 |  | Posición del ítem 22 en el orden aleatorio del test |
| Q22E | int64 | 39775 | 0 | 0 | 11219 | 178 | 3464030 | 6865.09 |  | Tiempo de respuesta del ítem 22 (milisegundos) |
| Q23A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.56 |  | Respuesta al ítem 23 del DASS-42 (1-4) |
| Q23I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.48 |  | Posición del ítem 23 en el orden aleatorio del test |
| Q23E | int64 | 39775 | 0 | 0 | 9295 | 177 | 1609274 | 4603.33 |  | Tiempo de respuesta del ítem 23 (milisegundos) |
| Q24A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.44 |  | Respuesta al ítem 24 del DASS-42 (1-4) |
| Q24I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.53 |  | Posición del ítem 24 en el orden aleatorio del test |
| Q24E | int64 | 39775 | 0 | 0 | 11543 | 176 | 49175189 | 8142.97 |  | Tiempo de respuesta del ítem 24 (milisegundos) |
| Q25A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.18 |  | Respuesta al ítem 25 del DASS-42 (1-4) |
| Q25I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.56 |  | Posición del ítem 25 en el orden aleatorio del test |
| Q25E | int64 | 39775 | 0 | 0 | 15398 | 180 | 65356830 | 14082.9 |  | Tiempo de respuesta del ítem 25 (milisegundos) |
| Q26A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.66 |  | Respuesta al ítem 26 del DASS-42 (1-4) |
| Q26I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.45 |  | Posición del ítem 26 en el orden aleatorio del test |
| Q26E | int64 | 39775 | 0 | 0 | 9725 | 179 | 10010729 | 5336.94 |  | Tiempo de respuesta del ítem 26 (milisegundos) |
| Q27A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.61 |  | Respuesta al ítem 27 del DASS-42 (1-4) |
| Q27I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.53 |  | Posición del ítem 27 en el orden aleatorio del test |
| Q27E | int64 | 39775 | 0 | 0 | 10568 | 176 | 60807360 | 8448.04 |  | Tiempo de respuesta del ítem 27 (milisegundos) |
| Q28A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.22 |  | Respuesta al ítem 28 del DASS-42 (1-4) |
| Q28I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 28 en el orden aleatorio del test |
| Q28E | int64 | 39775 | 0 | 0 | 8968 | 177 | 151281923 | 8183.67 |  | Tiempo de respuesta del ítem 28 (milisegundos) |
| Q29A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.65 |  | Respuesta al ítem 29 del DASS-42 (1-4) |
| Q29I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.46 |  | Posición del ítem 29 en el orden aleatorio del test |
| Q29E | int64 | 39775 | 0 | 0 | 10795 | 178 | 47570142 | 8493.56 |  | Tiempo de respuesta del ítem 29 (milisegundos) |
| Q30A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.39 |  | Respuesta al ítem 30 del DASS-42 (1-4) |
| Q30I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.45 |  | Posición del ítem 30 en el orden aleatorio del test |
| Q30E | int64 | 39775 | 0 | 0 | 13609 | -4328 | 34265188 | 9719.1 |  | Tiempo de respuesta del ítem 30 (milisegundos) |
| Q31A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.38 |  | Respuesta al ítem 31 del DASS-42 (1-4) |
| Q31I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.48 |  | Posición del ítem 31 en el orden aleatorio del test |
| Q31E | int64 | 39775 | 0 | 0 | 11899 | 177 | 9711339 | 7069.76 |  | Tiempo de respuesta del ítem 31 (milisegundos) |
| Q32A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.45 |  | Respuesta al ítem 32 del DASS-42 (1-4) |
| Q32I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.39 |  | Posición del ítem 32 en el orden aleatorio del test |
| Q32E | int64 | 39775 | 0 | 0 | 13430 | 180 | 39791945 | 12722 |  | Tiempo de respuesta del ítem 32 (milisegundos) |
| Q33A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.41 |  | Respuesta al ítem 33 del DASS-42 (1-4) |
| Q33I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.45 |  | Posición del ítem 33 en el orden aleatorio del test |
| Q33E | int64 | 39775 | 0 | 0 | 9765 | 179 | 8658903 | 5272.24 |  | Tiempo de respuesta del ítem 33 (milisegundos) |
| Q34A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.63 |  | Respuesta al ítem 34 del DASS-42 (1-4) |
| Q34I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.5 |  | Posición del ítem 34 en el orden aleatorio del test |
| Q34E | int64 | 39775 | 0 | 0 | 8977 | -1615 | 21328973 | 4871.68 |  | Tiempo de respuesta del ítem 34 (milisegundos) |
| Q35A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.3 |  | Respuesta al ítem 35 del DASS-42 (1-4) |
| Q35I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.57 |  | Posición del ítem 35 en el orden aleatorio del test |
| Q35E | int64 | 39775 | 0 | 0 | 16472 | 183 | 72970668 | 14105.87 |  | Tiempo de respuesta del ítem 35 (milisegundos) |
| Q36A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.27 |  | Respuesta al ítem 36 del DASS-42 (1-4) |
| Q36I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.4 |  | Posición del ítem 36 en el orden aleatorio del test |
| Q36E | int64 | 39775 | 0 | 0 | 8910 | 178 | 4133123 | 4335.75 |  | Tiempo de respuesta del ítem 36 (milisegundos) |
| Q37A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.37 |  | Respuesta al ítem 37 del DASS-42 (1-4) |
| Q37I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.56 |  | Posición del ítem 37 en el orden aleatorio del test |
| Q37E | int64 | 39775 | 0 | 0 | 11214 | -165 | 12710289 | 6811.02 |  | Tiempo de respuesta del ítem 37 (milisegundos) |
| Q38A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.39 |  | Respuesta al ítem 38 del DASS-42 (1-4) |
| Q38I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.53 |  | Posición del ítem 38 en el orden aleatorio del test |
| Q38E | int64 | 39775 | 0 | 0 | 8821 | -8921 | 59401008 | 5838.11 |  | Tiempo de respuesta del ítem 38 (milisegundos) |
| Q39A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.45 |  | Respuesta al ítem 39 del DASS-42 (1-4) |
| Q39I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.54 |  | Posición del ítem 39 en el orden aleatorio del test |
| Q39E | int64 | 39775 | 0 | 0 | 12134 | -144 | 31773217 | 8472.12 |  | Tiempo de respuesta del ítem 39 (milisegundos) |
| Q40A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.65 |  | Respuesta al ítem 40 del DASS-42 (1-4) |
| Q40I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.51 |  | Posición del ítem 40 en el orden aleatorio del test |
| Q40E | int64 | 39775 | 0 | 0 | 11988 | 178 | 56297555 | 10274.1 |  | Tiempo de respuesta del ítem 40 (milisegundos) |
| Q41A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 1.97 |  | Respuesta al ítem 41 del DASS-42 (1-4) |
| Q41I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.48 |  | Posición del ítem 41 en el orden aleatorio del test |
| Q41E | int64 | 39775 | 0 | 0 | 10035 | -159 | 8021110 | 5540.7 |  | Tiempo de respuesta del ítem 41 (milisegundos) |
| Q42A | int64 | 39775 | 0 | 0 | 4 | 1 | 4 | 2.68 |  | Respuesta al ítem 42 del DASS-42 (1-4) |
| Q42I | int64 | 39775 | 0 | 0 | 42 | 1 | 42 | 21.46 |  | Posición del ítem 42 en el orden aleatorio del test |
| Q42E | int64 | 39775 | 0 | 0 | 12492 | 178 | 7750098 | 8300.7 |  | Tiempo de respuesta del ítem 42 (milisegundos) |
| country | str | 39773 | 2 | 0 | 145 |  |  |  | MY (21605); US (8207); GB (1180) | Código ISO del país de conexión |
| source | int64 | 39775 | 0 | 0 | 3 | 0 | 2 | 0.91 |  | Cómo llegó al test (1=portada, 2=google, 0=otro) |
| introelapse | int64 | 39775 | 0 | 0 | 1858 | 0 | 20829735 | 2432.59 |  | Segundos en la página de inicio |
| testelapse | int64 | 39775 | 0 | 0 | 1912 | 12 | 20829721 | 2684.84 |  | Segundos en los 42 ítems DASS |
| surveyelapse | int64 | 39775 | 0 | 0 | 1662 | 1 | 20828454 | 4673.67 |  | Segundos en la encuesta demográfica |
| TIPI1 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 3.79 |  | Ítem 1 del inventario de personalidad TIPI (1-7) |
| TIPI2 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 4.19 |  | Ítem 2 del inventario de personalidad TIPI (1-7) |
| TIPI3 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 4.74 |  | Ítem 3 del inventario de personalidad TIPI (1-7) |
| TIPI4 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 5.17 |  | Ítem 4 del inventario de personalidad TIPI (1-7) |
| TIPI5 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 4.93 |  | Ítem 5 del inventario de personalidad TIPI (1-7) |
| TIPI6 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 4.85 |  | Ítem 6 del inventario de personalidad TIPI (1-7) |
| TIPI7 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 5.27 |  | Ítem 7 del inventario de personalidad TIPI (1-7) |
| TIPI8 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 4.28 |  | Ítem 8 del inventario de personalidad TIPI (1-7) |
| TIPI9 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 3.65 |  | Ítem 9 del inventario de personalidad TIPI (1-7) |
| TIPI10 | int64 | 39775 | 0 | 0 | 8 | 0 | 7 | 3.73 |  | Ítem 10 del inventario de personalidad TIPI (1-7) |
| VCL1 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.81 |  | Chequeo de vocabulario, palabra 1 (1=conoce, 0=no) |
| VCL2 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.58 |  | Chequeo de vocabulario, palabra 2 (1=conoce, 0=no) |
| VCL3 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.15 |  | Chequeo de vocabulario, palabra 3 (1=conoce, 0=no) |
| VCL4 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.87 |  | Chequeo de vocabulario, palabra 4 (1=conoce, 0=no) |
| VCL5 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.68 |  | Chequeo de vocabulario, palabra 5 (1=conoce, 0=no) |
| VCL6 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.04 |  | Chequeo de vocabulario, palabra 6 (1=conoce, 0=no) (palabra inexistente: control de validez) |
| VCL7 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.08 |  | Chequeo de vocabulario, palabra 7 (1=conoce, 0=no) |
| VCL8 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.17 |  | Chequeo de vocabulario, palabra 8 (1=conoce, 0=no) |
| VCL9 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.04 |  | Chequeo de vocabulario, palabra 9 (1=conoce, 0=no) (palabra inexistente: control de validez) |
| VCL10 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.87 |  | Chequeo de vocabulario, palabra 10 (1=conoce, 0=no) |
| VCL11 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.07 |  | Chequeo de vocabulario, palabra 11 (1=conoce, 0=no) |
| VCL12 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.08 |  | Chequeo de vocabulario, palabra 12 (1=conoce, 0=no) (palabra inexistente: control de validez) |
| VCL13 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.29 |  | Chequeo de vocabulario, palabra 13 (1=conoce, 0=no) |
| VCL14 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.57 |  | Chequeo de vocabulario, palabra 14 (1=conoce, 0=no) |
| VCL15 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.85 |  | Chequeo de vocabulario, palabra 15 (1=conoce, 0=no) |
| VCL16 | int64 | 39775 | 0 | 0 | 2 | 0 | 1 | 0.93 |  | Chequeo de vocabulario, palabra 16 (1=conoce, 0=no) |
| education | int64 | 39775 | 0 | 0 | 5 | 0 | 4 | 2.5 |  | Nivel educativo (1=<secundaria, 2=secundaria, 3=grado, 4=posgrado) |
| urban | int64 | 39775 | 0 | 0 | 4 | 0 | 3 | 2.22 |  | Entorno de infancia (1=rural, 2=suburbano, 3=urbano) |
| gender | int64 | 39775 | 0 | 0 | 4 | 0 | 3 | 1.79 |  | Género |
| engnat | int64 | 39775 | 0 | 0 | 3 | 0 | 2 | 1.64 |  | Inglés nativo (1=sí, 2=no) |
| age | int64 | 39775 | 0 | 0 | 79 | 13 | 1998 | 23.61 |  | Edad |
| screensize | int64 | 39775 | 0 | 0 | 2 | 1 | 2 | 1.27 |  | 1=pantalla pequeña, 2=grande |
| uniquenetworklocation | int64 | 39775 | 0 | 0 | 2 | 1 | 2 | 1.2 |  | 1=única respuesta desde esa red, 2=múltiples |
| hand | int64 | 39775 | 0 | 0 | 4 | 0 | 3 | 1.14 |  | Mano de escritura (1=diestra, 2=zurda, 3=ambas) |
| religion | int64 | 39775 | 0 | 0 | 13 | 0 | 12 | 7.56 |  | Religión (codificada 1-12) |
| orientation | int64 | 39775 | 0 | 0 | 6 | 0 | 5 | 1.64 |  | Orientación sexual (codificada 1-5) |
| race | int64 | 39775 | 0 | 0 | 7 | 10 | 70 | 31.31 |  | Raza (codificada) |
| voted | int64 | 39775 | 0 | 0 | 3 | 0 | 2 | 1.71 |  | Votó el último año (1=sí, 2=no) |
| married | int64 | 39775 | 0 | 0 | 4 | 0 | 3 | 1.16 |  | Estado civil (1=soltero, 2=casado, 3=previamente casado) |
| familysize | int64 | 39775 | 0 | 0 | 28 | 0 | 133 | 3.51 |  | Número de hijos de la madre (incl. respondente) |
| major | str | 28350 | 11425 | 28.7 | 5308 |  |  |  | English (1026); Psychology (850); Business (621) | Carrera universitaria (texto libre) |

## B4_MentalHealth

| Mental Health Dataset (chanchal24, Kaggle) |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 261328 filas × 17 columnas |  |  |  |  |  |  |  |  |  |  |
| Columna | Tipo | No nulos | Nulos | % nulos | Únicos | Mín | Máx | Media | Valores frecuentes (top 3) | Descripción / regla a vigilar |
| Gender | str | 261328 | 0 | 0 | 2 |  |  |  | Male (230614); Female (30714) | Género |
| Country | str | 261328 | 0 | 0 | 35 |  |  |  | USA (154478); UK (47878); Canada (14177) | País |
| Occupation | str | 261328 | 0 | 0 | 5 |  |  |  | Housewife (60081); Corporate (55622); Student (54207) | Ocupación (filtrar 'Student' para el TFM) |
| SelfEmployed | str | 256972 | 4356 | 1.7 | 2 |  |  |  | No (230404); Yes (26568) | Autónomo (Yes/No, 4.356 nulos) |
| FamilyHistory | str | 261328 | 0 | 0 | 2 |  |  |  | No (161981); Yes (99347) | Antecedentes familiares de enfermedad mental (Yes/No) |
| Treatment | str | 261328 | 0 | 0 | 2 |  |  |  | No (132958); Yes (128370) | VARIABLE OBJETIVO: buscó tratamiento (Yes/No) |
| DaysIndoors | str | 261328 | 0 | 0 | 5 |  |  |  | 1-14 days (57598); 31-60 days (54992); Go out Every day (52408) | Días sin salir de casa (categórico) |
| HabitsChange | str | 261328 | 0 | 0 | 3 |  |  |  | Yes (97687); Maybe (85081); No (78560) | Cambio de hábitos (Yes/No/Maybe) |
| MentalHealthHistory | str | 261328 | 0 | 0 | 3 |  |  |  | No (94027); Maybe (84989); Yes (82312) | Historial propio de salud mental (Yes/No/Maybe) |
| IncreasingStress | str | 261328 | 0 | 0 | 3 |  |  |  | Maybe (90697); Yes (88423); No (82208) | Estrés creciente (Yes/No/Maybe) |
| MoodSwings | str | 261328 | 0 | 0 | 3 |  |  |  | Medium (90215); Low (89193); High (81920) | Cambios de humor (Low/Medium/High) |
| SocialWeakness | str | 261328 | 0 | 0 | 3 |  |  |  | Maybe (93271); No (87946); Yes (80111) | Debilidad social percibida (Yes/No/Maybe) |
| CopingStruggles | str | 261328 | 0 | 0 | 2 |  |  |  | No (139251); Yes (122077) | Dificultad de afrontamiento (Yes/No) |
| WorkInterest | str | 261328 | 0 | 0 | 3 |  |  |  | No (94460); Maybe (90031); Yes (76837) | Interés en el trabajo/estudio (Yes/No/Maybe) |
| SocialWeakness.1 | str | 261328 | 0 | 0 | 3 |  |  |  | Maybe (93271); No (87946); Yes (80111) | DUPLICADO EXACTO de SocialWeakness (eliminar) |
| MentalHealthInterview | str | 261328 | 0 | 0 | 3 |  |  |  | No (205477); Maybe (47844); Yes (8007) | Hablaría de salud mental en una entrevista (Yes/No/Maybe) |
| CareOptions | str | 261328 | 0 | 0 | 3 |  |  |  | No (108972); Yes (84097); Not sure (68259) | Conoce opciones de atención (Yes/No/Not sure) |
