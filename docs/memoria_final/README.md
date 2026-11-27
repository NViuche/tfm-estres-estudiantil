# Memoria final y defensa

Material de trabajo del grupo para la fase final del TFM, después de la Entrega 3: la memoria (unas 50 páginas, estructura A–H de la guía del TFM) y la defensa (25 minutos de presentación y 15 de preguntas).

| Archivo | Qué es |
|---|---|
| [`Indice_Memoria_TFM.docx`](Indice_Memoria_TFM.docx) | Índice de trabajo de la memoria (A4 horizontal, 7 páginas). Para cada apartado: qué debe contener, de qué documento sale, si se reutiliza, se adapta o se redacta, las páginas estimadas (50,5 en total) y el responsable. Incluye los anexos, las decisiones pendientes, las cifras de referencia, la bibliografía candidata y notas para la defensa |
| [`Plantilla_Memoria_TFM.docx`](Plantilla_Memoria_TFM.docx) | Plantilla de Word de la memoria final (22 páginas): estructura A–H con todos los apartados del índice, estilos comunes (Times New Roman 12, interlineado 1,5, títulos en Arial), índices automáticos de contenido, figuras y tablas, y bibliografía en APA 7. Cada apartado trae en gris qué va, de dónde sale y su extensión orientativa; esas indicaciones se borran antes de entregar |
| [`Guia_Defensa_TFM.pdf`](Guia_Defensa_TFM.pdf) ([Word](Guia_Defensa_TFM.docx)) | Guía de estudio para la defensa (43 páginas): guion de 25 minutos, el proyecto en dos minutos y el recorrido completo. Lo central son **5 partes, una por integrante**, en el orden en que se hizo el proyecto: datos, EDA y calidad, modelo y ETL con KPIs, modelado y NLP, y Power BI con nube e insights. Cada parte tiene su relato, las cifras que hay que memorizar, qué mostrar y las preguntas probables del tribunal con su respuesta. Cada concepto técnico o sigla lleva su definición en una **nota al pie** de la página donde aparece (la primera vez en cada parte), para quien no tiene perfil técnico. Al final: preguntas transversales, chuleta de cifras, glosario y dónde está cada documento |
| [`recursos/`](recursos/) | Generadores de los tres Word, en Node con la librería `docx`. Las definiciones de las notas al pie y del glosario están en `glosario_defensa.js` |

La guía de defensa es un documento interno de estudio y no forma parte de la memoria entregable.

## Cómo se regeneran

Desde `recursos/`, con la librería `docx` de Node instalada:

```
node indice_memoria.js ../Indice_Memoria_TFM.docx
node guia_defensa.js ../Guia_Defensa_TFM.docx
node plantilla_memoria.js ../Plantilla_Memoria_TFM.docx
```

`guia_defensa.js` toma las figuras del propio repositorio: `figuras/eda`, `figuras/diagramas/corregidos`, `figuras/modelado`, `figuras/powerbi` y `docs/entrega3_objetivo3/sintesis`. Después de generarla, abre el Word, actualiza el índice (clic derecho → *Actualizar campos*) y expórtalo a PDF (*Archivo → Exportar → PDF*).

**Relacionado:** [Síntesis de la Entrega 3](../entrega3_objetivo3/01_sintesis_entrega3_powerbi.md) · [Seguimiento](../../SEGUIMIENTO.md) · [README](../../README.md)
