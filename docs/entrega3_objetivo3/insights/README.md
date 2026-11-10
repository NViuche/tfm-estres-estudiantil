# Documento de insights (Entrega 3)

| Archivo | Qué es |
|---|---|
| `Insights_PowerBI_TFM_Estres.docx` | **Entregable de la Entrega 3**: el documento Word con los insights que pide la rúbrica. 12 páginas: resumen, método de exploración (con la página Explorar del informe), 7 insights (qué muestran, cómo se encontraron, comprobación, implicación y cautela, con capturas del informe), limitaciones y un anexo para reproducirlos. Enlaza la versión web interactiva del informe (https://claude.ai/artifact/7DuVNnNh38qLgELbcKAG8b) |
| `generar_insights.js` | Genera el `.docx` con la librería `docx` de Node. Solo hace falta si cambian las cifras o el texto |

Los 7 insights:
1. Buscar ayuda depende de los antecedentes familiares, no del nivel de estrés.
2. Las mujeres reportan más estrés que los hombres en casi todas las fuentes.
3. El estrés Alto disminuye con la edad.
4. A más nivel educativo, menos estrés Alto y severo.
5. El lenguaje delata el estrés, sobre todo fuera de los foros de ansiedad.
6. El porcentaje global lo marca una sola fuente: se comparan tendencias, no niveles.
7. La señal predictiva es real pero moderada, y dos fuentes exigen cautela.

Todas las cifras se comprobaron con los datos del informe (Supabase), también dentro de cada dataset para descartar efectos de composición.

## Regenerarlo

Con Node y la librería `docx` instalada (`npm install docx`), desde esta carpeta:

```
node generar_insights.js ../../../figuras/powerbi Insights_PowerBI_TFM_Estres.docx
```

Las capturas (`figuras/powerbi/p0_inicio.png` … `p7_explorar.png`) salen del PDF del informe entregado ([`../informe_powerbi_TFM_Estres.pdf`](../informe_powerbi_TFM_Estres.pdf)), con la ruta de ejemplo desplegada en Explorar. Al abrir el `.docx` en Word, si el índice aparece vacío: clic derecho → *Actualizar campos*.

---
<!-- relacionado -->
**Relacionado:** [README](../../../README.md) · [Guía de Power BI](../guia_power_bi.md) · [Seguimiento](../../../SEGUIMIENTO.md) · [Prototipo web](../../../prototipo/README.md)
