# Resultados del modelado (Objetivo 2)

Métricas de los modelos entrenados en `notebooks/09_modelado_objetivo2.ipynb`. `id_dataset` es la clave que relaciona cada fila con `dim_dataset` en el esquema estrella. Los modelos serializados están en [`modelos/`](../modelos/) y las figuras en [`figuras/modelado/`](../figuras/modelado/).

- **Protocolo:** validación cruzada 5x3 en datasets pequeños; hold-out 80/20 en los grandes; partición original train/test en Dreaddit.
- **brecha_acc:** diferencia de accuracy entre entrenamiento y validación (indicador de sobreajuste).
- **Alerta B3_DEPSTUDENT:** un AUC de 0,998 indica una posible etiqueta generada por fórmula; se reporta con cautela.

## Mejor modelo por dataset

| dataset | modelo | protocolo | n | accuracy | f1 | auc | auc_desv | brecha_acc | target | acc_baseline | mejora_vs_baseline | lectura_capa_armonizada | id_dataset |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B3_DEPSTUDENT | Regresion Logistica | CV 5x3 | 502 | 0.9788 | 0.9789 | 0.9984 | 0.0019 | 0.0124 | Depression (Yes/No) | 0.502 | 0.4768 | No = Bajo, Yes = Alto | 10 |
| B3_DREADDIT | Hibrido (TF-IDF + LIWC) + RegLog | Train/Test original | 3549 | 0.7483 | 0.7625 | 0.8383 |  | 0.0845 | label estres (0/1) | 0.5161 | 0.2322 | Etiqueta 0 = Bajo, 1 = Alto | 8 |
| B2_SMMH | Random Forest | CV 5x3 | 481 | 0.7318 | 0.7276 | 0.7966 | 0.0384 | 0.237 | Se siente deprimido/a >= 4 | 0.5405 | 0.1913 | Valor >= 4 equivale a nivel Alto | 6 |
| B1_MHSURVEY | XGBoost | CV 5x3 | 87 | 0.6251 | 0.5486 | 0.7854 | 0.0678 | 0.3749 | Depresion autoreportada (3 niveles) | 0.4484 | 0.1767 | Depresion 1-5 mapeada a Bajo / Moderado / Alto | 3 |
| B4_MENTALHEALTH | XGBoost | Hold-out 80/20 | 54207 | 0.7177 | 0.7285 | 0.7696 |  | -0.0028 | Ha buscado tratamiento (Yes/No) | 0.5059 | 0.2118 | Conducta de busqueda de ayuda (no es nivel de estres): alimenta el KPI de tratamiento | 12 |
| B1_ANXIETY | Regresion Logistica | Hold-out 80/20 | 9302 | 0.7297 | 0.4527 | 0.7645 |  | 0.0045 | GAD-7 >= 10 | 0.827 | -0.0973 | GAD-7 >= 10 equivale a nivel Alto | 2 |
| B4_DASS | XGBoost | Hold-out 80/20 | 23039 | 0.5779 | 0.5836 | 0.7628 |  | 0.0316 | Nivel de estres DASS-42 (baremos) | 0.357 | 0.2209 | Baremos DASS: <=28 Bajo, 29-39 Moderado, >=40 Alto | 11 |
| B1_ACADSTRESS | Random Forest | CV 5x3 | 140 | 0.381 | 0.4109 | 0.729 | 0.0371 | 0.3577 | Indice de estres academico (1-5) | 0.4 | -0.019 | Indice 1-5: 1-2 Bajo, 3 Moderado, 4-5 Alto | 1 |

## Todos los modelos evaluados

| dataset | modelo | protocolo | n | accuracy | f1 | auc | auc_desv | brecha_acc | target | id_dataset |
|---|---|---|---|---|---|---|---|---|---|---|
| B1_ACADSTRESS | Baseline (clase mayoritaria) | CV 5x3 | 140 | 0.4 | 0.1143 | 0.5 | 0.0 | 0.0 | Indice de estres academico (1-5) | 1 |
| B1_ACADSTRESS | Regresion Logistica | CV 5x3 | 140 | 0.35 | 0.338 | 0.7153 | 0.056 | 0.1839 | Indice de estres academico (1-5) | 1 |
| B1_ACADSTRESS | Random Forest | CV 5x3 | 140 | 0.381 | 0.4109 | 0.729 | 0.0371 | 0.3577 | Indice de estres academico (1-5) | 1 |
| B1_ACADSTRESS | XGBoost | CV 5x3 | 140 | 0.3786 | 0.3677 | 0.6795 | 0.0529 | 0.5577 | Indice de estres academico (1-5) | 1 |
| B1_ANXIETY | Baseline (clase mayoritaria) | Hold-out 80/20 | 9302 | 0.827 | 0.0 | 0.5 |  | 0.0001 | GAD-7 >= 10 | 2 |
| B1_ANXIETY | Regresion Logistica | Hold-out 80/20 | 9302 | 0.7297 | 0.4527 | 0.7645 |  | 0.0045 | GAD-7 >= 10 | 2 |
| B1_ANXIETY | Random Forest | Hold-out 80/20 | 9302 | 0.7512 | 0.4102 | 0.7457 |  | 0.1578 | GAD-7 >= 10 | 2 |
| B1_ANXIETY | XGBoost | Hold-out 80/20 | 9302 | 0.8318 | 0.3091 | 0.7559 |  | 0.0374 | GAD-7 >= 10 | 2 |
| B1_MHSURVEY | Baseline (clase mayoritaria) | CV 5x3 | 87 | 0.4484 | 0.2063 | 0.5 | 0.0 | -0.0001 | Depresion autoreportada (3 niveles) | 3 |
| B1_MHSURVEY | Regresion Logistica | CV 5x3 | 87 | 0.6211 | 0.5716 | 0.7707 | 0.0687 | 0.2248 | Depresion autoreportada (3 niveles) | 3 |
| B1_MHSURVEY | Random Forest | CV 5x3 | 87 | 0.6068 | 0.534 | 0.775 | 0.0821 | 0.3837 | Depresion autoreportada (3 niveles) | 3 |
| B1_MHSURVEY | XGBoost | CV 5x3 | 87 | 0.6251 | 0.5486 | 0.7854 | 0.0678 | 0.3749 | Depresion autoreportada (3 niveles) | 3 |
| B2_SMMH | Baseline (clase mayoritaria) | CV 5x3 | 481 | 0.5405 | 0.0 | 0.5 | 0.0 | -0.0 | Se siente deprimido/a >= 4 | 6 |
| B2_SMMH | Regresion Logistica | CV 5x3 | 481 | 0.736 | 0.7257 | 0.792 | 0.037 | 0.0328 | Se siente deprimido/a >= 4 | 6 |
| B2_SMMH | Random Forest | CV 5x3 | 481 | 0.7318 | 0.7276 | 0.7966 | 0.0384 | 0.237 | Se siente deprimido/a >= 4 | 6 |
| B2_SMMH | XGBoost | CV 5x3 | 481 | 0.7013 | 0.6797 | 0.7745 | 0.0439 | 0.2971 | Se siente deprimido/a >= 4 | 6 |
| B3_DEPSTUDENT | Baseline (clase mayoritaria) | CV 5x3 | 502 | 0.502 | 0.6684 | 0.5 | 0.0 | 0.0 | Depression (Yes/No) | 10 |
| B3_DEPSTUDENT | Regresion Logistica | CV 5x3 | 502 | 0.9788 | 0.9789 | 0.9984 | 0.0019 | 0.0124 | Depression (Yes/No) | 10 |
| B3_DEPSTUDENT | Random Forest | CV 5x3 | 502 | 0.9004 | 0.9022 | 0.973 | 0.0129 | 0.0991 | Depression (Yes/No) | 10 |
| B3_DEPSTUDENT | XGBoost | CV 5x3 | 502 | 0.9343 | 0.935 | 0.9875 | 0.0074 | 0.0657 | Depression (Yes/No) | 10 |
| B4_DASS | Baseline (clase mayoritaria) | Hold-out 80/20 | 23039 | 0.357 | 0.1754 | 0.5 |  | 0.0001 | Nivel de estres DASS-42 (baremos) | 11 |
| B4_DASS | Regresion Logistica | Hold-out 80/20 | 23039 | 0.5686 | 0.5667 | 0.7621 |  | -0.003 | Nivel de estres DASS-42 (baremos) | 11 |
| B4_DASS | Random Forest | Hold-out 80/20 | 23039 | 0.5642 | 0.5659 | 0.7535 |  | 0.3796 | Nivel de estres DASS-42 (baremos) | 11 |
| B4_DASS | XGBoost | Hold-out 80/20 | 23039 | 0.5779 | 0.5836 | 0.7628 |  | 0.0316 | Nivel de estres DASS-42 (baremos) | 11 |
| B4_MENTALHEALTH | Baseline (clase mayoritaria) | Hold-out 80/20 | 54207 | 0.5059 | 0.0 | 0.5 |  | 0.0 | Ha buscado tratamiento (Yes/No) | 12 |
| B4_MENTALHEALTH | Regresion Logistica | Hold-out 80/20 | 54207 | 0.7032 | 0.708 | 0.7654 |  | -0.0034 | Ha buscado tratamiento (Yes/No) | 12 |
| B4_MENTALHEALTH | Random Forest | Hold-out 80/20 | 54207 | 0.6969 | 0.7109 | 0.7284 |  | 0.0223 | Ha buscado tratamiento (Yes/No) | 12 |
| B4_MENTALHEALTH | XGBoost | Hold-out 80/20 | 54207 | 0.7177 | 0.7285 | 0.7696 |  | -0.0028 | Ha buscado tratamiento (Yes/No) | 12 |
| B3_DREADDIT | Baseline (clase mayoritaria) | Train/Test original | 3549 | 0.5161 | 0.6808 | 0.5 |  | 0.0083 | label estres (0/1) | 8 |
| B3_DREADDIT | LIWC + Regresion Logistica | Train/Test original | 3549 | 0.7441 | 0.757 | 0.8346 |  | 0.0421 | label estres (0/1) | 8 |
| B3_DREADDIT | LIWC + Random Forest | Train/Test original | 3549 | 0.7622 | 0.7745 | 0.8329 |  | 0.2364 | label estres (0/1) | 8 |
| B3_DREADDIT | LIWC + XGBoost | Train/Test original | 3549 | 0.7343 | 0.7532 | 0.8345 |  | 0.2322 | label estres (0/1) | 8 |
| B3_DREADDIT | TF-IDF + Regresion Logistica | Train/Test original | 3549 | 0.7161 | 0.7332 | 0.8215 |  | 0.2172 | label estres (0/1) | 8 |
| B3_DREADDIT | TF-IDF + SVM lineal | Train/Test original | 3549 | 0.7315 | 0.7447 | 0.8201 |  | 0.265 | label estres (0/1) | 8 |
| B3_DREADDIT | TF-IDF + Naive Bayes | Train/Test original | 3549 | 0.7189 | 0.766 | 0.8311 |  | 0.225 | label estres (0/1) | 8 |
| B3_DREADDIT | Hibrido (TF-IDF + LIWC) + RegLog | Train/Test original | 3549 | 0.7483 | 0.7625 | 0.8383 |  | 0.0845 | label estres (0/1) | 8 |

---
<!-- relacionado -->
**Relacionado:** [README](../README.md) · [Síntesis del modelado](../docs/entrega2_objetivo2/01_sintesis_objetivo2_modelado.md) · [Pruebas](../tests/pruebas.md)
