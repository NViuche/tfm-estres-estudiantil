# Problema y objetivos

## Problema

El estrés estudiantil depende de factores académicos, conductuales, digitales y emocionales que rara vez se miden juntos. Los datos públicos disponibles están dispersos: cada fuente recoge una faceta distinta, con escalas, poblaciones y calidades diferentes. Analizar una sola fuente da una visión parcial del fenómeno.

## Enfoque

Análisis **multidimensional en paralelo**: cada dataset se estudia por separado, sin fusionar registros entre fuentes (no comparten identificador de persona). La comparación entre fuentes se hace a través de un **constructo común de nivel de estrés (Bajo / Moderado / Alto)** y de dimensiones conformes (género, rango de edad, nivel educativo) en un modelo en estrella sobre MySQL. Para GAD-7 y DASS se usan los baremos clínicos de cada escala.

Los datasets se agrupan en cuatro bloques analíticos:

| Bloque | Enfoque | Fuentes |
|---|---|---|
| 1. Factores internos | Presión académica, ansiedad, hábitos | Academic Stress, Student Anxiety (GAD-7), Mental Health Survey, Student Habits* |
| 2. Hábitos digitales | Redes sociales, sueño, estilo de vida | Social Media and Mental Health, Social Media/Sleep*, Mental Health Lifestyle* |
| 3. Percepción emocional | Texto y NLP | Dreaddit (train/test), Depression Student |
| 4. Validación psicológica | Escalas clínicas y búsqueda de ayuda | DASS-42, Mental Health Dataset |

\* Datasets sintéticos (distribuciones uniformes, correlaciones ≈ 0): se usan solo en la capa descriptiva y como caso de calidad del dato, y se excluyen del modelado.

## Objetivos

1. **Análisis exploratorio y descriptivo** de los datasets por bloque, evaluando la calidad de cada fuente e identificando patrones entre variables académicas, conductuales y niveles de estrés.
2. **Modelos de IA** para predecir el estrés y detectar patrones: clasificación sobre datos estructurados y NLP sobre texto, con análisis independiente por dataset.
3. **Dashboards de Business Intelligence** (Power BI) que muestren los indicadores de cada bloque de forma comparativa e interactiva para apoyar la toma de decisiones.

## Hallazgos principales

- **La presión académica es el eje del estrés:** más del 60 % se sitúa en los niveles 4–5 (Academic Stress) y tiene una correlación r = 0,38 con la depresión (Mental Health Survey).
- **El aislamiento social es el predictor más fuerte** de la depresión (r = 0,71).
- **En redes sociales importa el patrón de uso, no el tiempo total:** preocupación (r = 0,59) y comparación social (r = 0,42).
- **El lenguaje refleja el estrés:** en Dreaddit, los posts con estrés usan el doble y medio de vocabulario de ansiedad; un modelo híbrido TF-IDF + LIWC alcanza un AUC de 0,84.
- **Existe una brecha entre malestar y ayuda:** más estrés no aumenta la búsqueda de tratamiento (48–51 %); tener antecedentes familiares sí (72 % frente a 35 %).
- **La señal predictiva es real pero moderada:** el AUC va de 0,73 a 0,84 en las fuentes con señal real. Los modelos sirven para investigación, no para diagnóstico clínico.

El desarrollo completo está en [`docs/`](../docs/).
