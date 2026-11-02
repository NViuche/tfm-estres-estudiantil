# Datasets del TFM, organizados por bloque

Fichas de los 12 CSV originales (Dreaddit viene en dos archivos, train y test). Los CSV no se publican en este repositorio (~52 MB); se descargan desde las fuentes enlazadas en el [README](../../README.md#fuentes-de-datos). Cada ficha recoge estructura, tipos, nulos, estadísticos y una muestra. Los 3 datasets sintéticos (excluidos del modelado) son Student Habits, Social Media/Sleep y Mental Health Lifestyle.

Todo lo de esta carpeta se calculó con pandas sobre los CSV originales; no se modificó ningún dato.

## Bloque 1
| Dataset | Ficha | Filas | Cols | MB |
|---|---|---|---|---|
| 1 Student Academic Stress Real World Dataset | `bloque1/1_student_academic_stress_real_world_dataset.md` | 140 | 9 | 0.01 |
| 1 Student Mental Health Survey | `bloque1/1_student_mental_health_survey.md` | 87 | 21 | 0.01 |
| 1 Student anxiety dataset | `bloque1/1_student_anxiety_dataset.md` | 13,464 | 55 | 4.26 |
| 1 Student-Habits-vs-Academic-Performance | `bloque1/1_student_habits_vs_academic_performance.md` | 1,000 | 16 | 0.07 |

## Bloque 2
| Dataset | Ficha | Filas | Cols | MB |
|---|---|---|---|---|
| 2 Mental_Health_Lifestyle GITHUB | `bloque2/2_mental_health_lifestyle_github.md` | 3,000 | 12 | 0.19 |
| 2 Social Media Usage vs Sleep, Stress & Productivity | `bloque2/2_social_media_usage_vs_sleep_stress_productivity.md` | 11,000 | 10 | 0.56 |
| 2 Social Media and Mental Health | `bloque2/2_social_media_and_mental_health.md` | 481 | 21 | 0.08 |

## Bloque 3
| Dataset | Ficha | Filas | Cols | MB |
|---|---|---|---|---|
| 3 Stress Analysis in Social Media (dreaddit-test) | `bloque3/3_dreaddit_test.md` | 715 | 116 | 0.76 |
| 3 Stress Analysis in Social Media (dreaddit-train) | `bloque3/3_dreaddit_train.md` | 2,838 | 116 | 2.72 |
| 3 Student_Mental_Health_Analysis GITHUB | `bloque3/3_student_mental_health_analysis_github.md` | 502 | 11 | 0.03 |

## Bloque 4
| Dataset | Ficha | Filas | Cols | MB |
|---|---|---|---|---|
| 4 Depression Anxiety Stress Scales Responses | `bloque4/4_depression_anxiety_stress_scales_responses.md` | 39,775 | 172 | 20.78 |
| 4 Mental Health Dataset | `bloque4/4_mental_health_dataset.md` | 261,328 | 17 | 22.67 |

Bloque 4 incluye además `bloque4/codebook_dass_original.md` (diccionario original de DASS).

Nota: el DASS tiene 39.775 filas en bruto; la ingesta usa 39.767 tras el filtro de edad 13–90 (cifra de los documentos del Objetivo 2). Verificado sobre el CSV: 39.767 filas con edad entre 13 y 90.
