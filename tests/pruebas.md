# Pruebas y validación

El proyecto no es una aplicación con tests unitarios: sus pruebas son **comprobaciones sobre los datos, sobre la carga en MySQL, sobre el informe de Power BI y sobre la migración a Supabase**. Hay cuatro niveles.

## 1. Reglas de calidad del dato (antes de la carga)

Notebook: [`notebooks/05_reglas_calidad_dato.ipynb`](../notebooks/05_reglas_calidad_dato.ipynb). Se evalúan 49 reglas sobre los 12 datasets originales (nombres de columna, nulos en el target, rangos válidos, duplicados, etc.).

**Resultado: 39 OK · 10 AVISO · 0 ERROR.** Los avisos no bloquean la carga; cada uno lleva su acción de tratamiento.

## 2. Validación de la carga (después de la ingesta)

Notebook: [`notebooks/07b_validacion_carga_datos.ipynb`](../notebooks/07b_validacion_carga_datos.ipynb). Abre la base de datos en modo solo lectura y cada comprobación termina en **OK** o **FALLA**.

| Bloque | Qué comprueba |
|---|---|
| Objetos | Existen las 11 tablas de hechos, las 7 dimensiones y las 6 vistas de la estrella |
| Filas por tabla | Cada tabla tiene exactamente las filas cargadas (suman 334.318) |
| Estrella | Los 12 datasets aparecen en `vw_hechos_estres`; las 9 fuentes incluidas suman 319.318 registros |
| Integridad | Sin claves naturales repetidas ni claves nulas o huérfanas hacia las dimensiones |
| Calidad | Reglas aplicadas en la ingesta: textos corruptos de Dreaddit excluidos, edades del DASS en 13–90 |
| Filtro global | «Mujeres de 18–25 con estrés Alto» reproduce los 7.446 casos de la verificación de la carga |

El notebook de ETL (`08_etl_transformaciones_kpis.ipynb`) añade dos controles: 14 relaciones hecho-dimensión con 0 claves huérfanas, y el cuadre 334.318 − 15.000 sintéticos = 319.318.

**Limitación conocida:** 67 de los 39.767 respondentes del DASS (0,17 %) no contestaron el género y quedaron como «Otro» en lugar de «No reportado» (efecto de 0,02 puntos en la cobertura demográfica).

## 3. Validación del informe de Power BI

Comprobaciones hechas antes de dar por bueno el informe ([`powerbi/`](../powerbi/)):

| Comprobación | Resultado |
|---|---|
| Exportación MySQL → CSV (`scripts/exportar_mysql_cli.py`) | 15 objetos; filas idénticas a MySQL; ningún nulo exportado como texto «NULL» |
| Columnas del modelo semántico frente a las cabeceras de los CSV | Coinciden en las 15 tablas |
| Modelo TMDL cargado con la biblioteca de Power BI Desktop | Sin errores: 32 medidas, sin conflictos de nombres ni referencias DAX rotas |
| Campos usados por los objetos visuales de las 10 páginas (informe local y de Supabase) | Todos existen en el modelo, incluida la columna calculada `vw_hechos_estres[nivel_estres]` |
| Posición de los objetos visuales | Todos caben en su página (1280 × 720; Explorar 1280 × 1000; tooltip 320 × 240) |
| Revisión en Power BI Desktop | Validado: menú sin páginas ocultas, logos, tooltip de página, *Obtener detalles* con botón Volver, filtros sincronizados, árbol de descomposición e influenciadores clave |
| KPIs de la página Inicio frente a `dwh_kpi_resultados` | Coinciden con la última ejecución; las 3 ejecuciones guardadas dan los mismos valores |

Valores de control, sin filtros, en el informe y en SQL sobre MySQL:

| Medida | Valor |
|---|---|
| Registros (9 fuentes incluidas) | 319.318 |
| % Estrés Alto | 33,7 % |
| Cobertura demográfica | 17,0 % |
| Brecha de género en ansiedad (DASS) | 2,89 |
| % Búsqueda de tratamiento | 49,4 % |
| AUC medio del mejor modelo, sin alertas | 0,786 |
| Datasets con alerta | 2 |

## 4. Validación de la migración a Supabase

`supabase/scripts/migrar_mysql_a_supabase.py` compara Supabase con MySQL al terminar cada migración (05/11/2026):

| Comprobación | Resultado |
|---|---|
| Filas por tabla (17 tablas, incluida `hechos_estres` con 334.318) | 17 de 17 coinciden con MySQL |
| Cifras de control calculadas con SQL en las dos bases | 7 de 7 iguales: 319.318 registros, 33,68 % de estrés Alto, 17,0 % de cobertura, 49,41 % de tratamiento, 3.549 posts, AUC 0,786 y 2 datasets con alerta |
| Usuario `tfm_lector` (`probar_lector.py`) | Lee el esquema `tfm`; la escritura queda bloqueada |
| Correcciones de texto | Bloques, KPIs y modelos con tildes; antecedentes familiares «No / Sí» |
| Informe de Power BI conectado a Supabase | Mismos valores de control que el informe local |
| Prototipo web construido desde Supabase | Mismas cifras que el informe (319.318 registros, 33,7 % de estrés Alto) |
| Influenciadores clave del prototipo frente a Power BI | Mismo orden de factores (No reportado, Percepción emocional, Otro, <18, Hábitos digitales); valores algo menores porque Power BI aplica su propio modelo |
| Ruta de ejemplo del árbol (prototipo frente al PDF entregado) | Mismas cifras en cada nivel: 34,1 % → 39,0 % → 37,6 % → 40,4 / 35,8 / 35,2 / 35,0 % |
| API de lectura pública (`publicar_api_lectura.py`, 11/11/2026) | `tfm_datasets`, `tfm_kpis` y `tfm_modelos` responden con 12, 6 y 8 filas; crear, modificar o borrar por la API da error; la clave pública no accede al esquema `tfm` ni a sus tablas |

## 5. Revisión general del repositorio

Comprobaciones hechas sobre el repositorio antes de cerrar la Entrega 3 (11/11/2026):

| Comprobación | Resultado |
|---|---|
| Los dos modelos TMDL (`powerbi/` y `supabase/powerbi/`) cargados con la biblioteca de Power BI | Sin errores: 18 tablas, 18 relaciones, 32 medidas y la columna calculada `nivel_estres` |
| Campos y posición de los objetos visuales en los dos informes | Todos existen en el modelo y caben en su página |
| Scripts de Python (24) y ficheros JSON del informe (219) | Compilan y se leen sin errores |
| Prototipo final (`prototipo/v10`) | JavaScript válido; los tres bloques de datos incrustados (datos, imágenes y arquitectura) se leen bien; las 17 rutas del repositorio que enlaza existen y los 9 datasets de la ficha tienen su fuente |
| Imágenes del informe regeneradas con `scripts/generar_imagenes.py` | Idénticas a las del repositorio |
| Enlaces relativos entre los documentos Markdown | 118 enlaces, ninguno roto |
| Usuario `tfm_lector` en Supabase | Lee bloques, KPIs, antecedentes y modelos con tildes; la escritura sigue bloqueada |
| Ficheros que no deben subirse (CSV, `.env`, `.pbix`, caché de Power BI) y credenciales | Ninguno en el repositorio; los scripts leen las credenciales del `.env` local y los parámetros de conexión llevan valores de ejemplo |

## Detalle de las 49 reglas

| Dataset | Regla | Evaluados | Incumplen | % incumplen | Estado | Accion |
|---|---|---|---|---|---|---|
| B1.1 AcademicStress | R1: columnas sin espacios sobrantes en el nombre | 9 | 0 | 0.0 | OK | strip() aplicado a los nombres al cargar |
| B1.1 AcademicStress | R2: indice de estres nulo | 140 | 0 | 0.0 | OK | Excluir registro del analisis del target |
| B1.1 AcademicStress | R3: indice de estres fuera de rango [1,5] | 140 | 0 | 0.0 | OK | Ninguna necesaria si 0 |
| B1.1 AcademicStress | R4: registros duplicados completos | 140 | 0 | 0.0 | OK | Eliminar duplicados si aparecen |
| B1.2 Anxiety | R1: GAD_T nulo | 13464 | 0 | 0.0 | OK | Excluir del analisis de ansiedad |
| B1.2 Anxiety | R2: GAD_T fuera de rango [0,21] | 13464 | 0 | 0.0 | OK | Revisar calculo de la escala si >0 |
| B1.2 Anxiety | R3: Edad fuera de rango plausible [13,90] | 13464 | 0 | 0.0 | OK | Filtrar registros fuera de rango |
| B1.2 Anxiety | R4: Horas de juego semanales imposibles (>112) | 13434 | 10 | 0.07 | AVISO | Tratar como atipico/captura erronea (winsorizar o excluir) |
| B1.2 Anxiety | R5: Work nulo (impide filtrar estudiantes) | 13464 | 38 | 0.28 | AVISO | Los nulos quedan fuera del subset estudiantil |
| B1.3 MHSurvey | R: depression nulo | 87 | 0 | 0.0 | OK | Excluir del analisis si aparece |
| B1.3 MHSurvey | R: depression fuera de rango [1,5] | 87 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B1.3 MHSurvey | R: anxiety nulo | 87 | 0 | 0.0 | OK | Excluir del analisis si aparece |
| B1.3 MHSurvey | R: anxiety fuera de rango [1,5] | 87 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B1.3 MHSurvey | R: cgpa en formato texto-rango (no numerico) | 87 | 0 | 0.0 | OK | Recodificar a ordinal antes del modelado (Objetivo 2) |
| B1.4 StudentHabits | R1: parental_education_level nulo | 1000 | 91 | 9.1 | AVISO | Imputar por moda o excluir columna en el modelado |
| B1.4 StudentHabits | R2: exam_score fuera de rango [0,100] | 1000 | 0 | 0.0 | OK | Recortar a [0,100] si >0 |
| B1.4 StudentHabits | R3: suma de horas diarias imposible (>24h) | 1000 | 0 | 0.0 | OK | Marcar como inconsistencia de captura |
| B1.4 StudentHabits | R4: student_id duplicado | 1000 | 0 | 0.0 | OK | Debe ser clave unica (PK) |
| B2.1 SocialMedia | R1: user_id duplicado | 11000 | 0 | 0.0 | OK | Debe ser clave unica (PK) |
| B2.1 SocialMedia | R2: stress_level fuera del dominio {Low,Medium,High} | 11000 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B2.1 SocialMedia | R3: horas de pantalla fuera de rango [0,24] | 11000 | 0 | 0.0 | OK | Recortar o excluir si >0 |
| B2.1 SocialMedia | R4: sleep_hours fuera de rango [0,24] | 11000 | 0 | 0.0 | OK | Recortar o excluir si >0 |
| B2.2 SMMH | R: '9. How often do you find yourself using ...' fuera de escala Likert [1,5] | 481 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B2.2 SMMH | R: '10. How often do you get distracted by S...' fuera de escala Likert [1,5] | 481 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B2.2 SMMH | R: '11. Do you feel restless if you haven't ...' fuera de escala Likert [1,5] | 481 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B2.2 SMMH | R: edad no numerica o nula | 481 | 0 | 0.0 | OK | Excluir de analisis por edad |
| B2.3 Lifestyle | R1: Mental Health Condition nulo (NaN semantico) | 3000 | 595 | 19.83 | AVISO | Recodificar NaN -> 'Ninguna' (ausencia de diagnostico) |
| B2.3 Lifestyle | R2: Stress Level fuera del dominio {Low,Moderate,High} | 3000 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B2.3 Lifestyle | R3: Sleep Hours fuera de rango [0,24] | 3000 | 0 | 0.0 | OK | Recortar o excluir si >0 |
| B3.1 Dreaddit | R1: texto vacio o nulo (train) | 2838 | 0 | 0.0 | OK | Excluir del corpus NLP |
| B3.1 Dreaddit | R2: label fuera del dominio {0,1} (train) | 2838 | 0 | 0.0 | OK | Revisar etiquetado si >0 |
| B3.1 Dreaddit | R3: id duplicado (train) | 2838 | 0 | 0.0 | OK | Debe ser clave unica (PK) |
| B3.1 Dreaddit | R4: solapamiento de ids entre train y test | 715 | 0 | 0.0 | OK | Garantiza evaluacion sin fuga de datos (data leakage) |
| B3.1 Dreaddit | R5: train y test con distinto CONJUNTO de columnas | 1 | 0 | 0.0 | OK | Ambas particiones deben compartir esquema |
| B3.1 Dreaddit | R6: train y test con distinto ORDEN de columnas | 1 | 1 | 100.0 | AVISO | Mismo conjunto, distinto orden: alinear por nombre (pandas) o reordenar test con tr.columns antes de modelar |
| B3.1 Dreaddit | R7: texto = artefacto de Excel ('#NAME?', etc.) en train | 2838 | 4 | 0.14 | AVISO | Excluir del corpus NLP: son celdas corruptas de la fuente original |
| B3.1 Dreaddit | R8: texto = artefacto de Excel en test | 715 | 0 | 0.0 | OK | Excluir del corpus NLP |
| B3.2 DepressionStudent | R1: Depression fuera del dominio {Yes,No} | 502 | 0 | 0.0 | OK | Revisar codificacion si >0 |
| B3.2 DepressionStudent | R2: Academic Pressure fuera de rango [1,5] | 502 | 0 | 0.0 | OK | Revisar escala si >0 |
| B3.2 DepressionStudent | R3: Edad fuera de rango estudiantil [15,60] | 502 | 0 | 0.0 | OK | Revisar registros fuera de rango |
| B3.2 DepressionStudent | R4: registros duplicados completos | 502 | 0 | 0.0 | OK | Eliminar si aparecen |
| B4.1 DASS | R1: edad fuera de rango plausible [13,90] | 39775 | 8 | 0.02 | AVISO | Filtrar (valores tipo '1998' son anos de nacimiento mal capturados) |
| B4.1 DASS | R2: items DASS fuera de escala [1,4] (42 columnas) | 39775 | 0 | 0.0 | OK | Revisar registro completo si >0 |
| B4.1 DASS | R3: marca palabras inexistentes (VCL6/9/12) - validez dudosa | 39775 | 5192 | 13.05 | AVISO | Opcional: excluir o sensibilizar el analisis (control del codebook) |
| B4.1 DASS | R4: genero fuera del dominio {1,2,3} | 39775 | 67 | 0.17 | AVISO | Tratar como no informado |
| B4.2 MentalHealth | R1: columna duplicada SocialWeakness.1 == SocialWeakness | 1 | 0 | 0.0 | OK | Eliminar SocialWeakness.1 (duplicado exacto verificado) |
| B4.2 MentalHealth | R2: SelfEmployed nulo | 261328 | 4356 | 1.67 | AVISO | Imputar 'No' o categoria 'Desconocido' |
| B4.2 MentalHealth | R3: Treatment fuera del dominio {Yes,No} | 261328 | 0 | 0.0 | OK | Revisar si >0 |
| B4.2 MentalHealth | R4: Occupation fuera del dominio esperado | 261328 | 0 | 0.0 | OK | Revisar categorias nuevas si >0 |

---
<!-- relacionado -->
**Relacionado:** [README](../README.md) · [Seguimiento](../SEGUIMIENTO.md) · [Resultados del modelado](../resultados/README.md) · [Diccionario de datos](../docs/entrega1_objetivo1/03_diccionario_de_datos.md) · [Guía de Power BI](../docs/entrega3_objetivo3/guia_power_bi.md)
