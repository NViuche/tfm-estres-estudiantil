# Síntesis de la Entrega 3: cómo se genera

| Archivo | Qué hace |
|---|---|
| `arquitectura.py` | Dibuja `arquitectura.png` (figura 1: recorrido de los datos) con Pillow |
| `sintesis3.js` | Genera el Word de la síntesis con la librería `docx` de Node, con el formato de las síntesis de las entregas 1 y 2 |
| `docx_a_md.py` | Transcribe el Word a Markdown ([`01_sintesis_entrega3_powerbi.md`](../01_sintesis_entrega3_powerbi.md)) |

Pasos (desde esta carpeta):

```
python arquitectura.py arquitectura.png
node sintesis3.js ../../../figuras/powerbi arquitectura.png Sintesis_Entrega3_PowerBI.docx
python docx_a_md.py Sintesis_Entrega3_PowerBI.docx ../01_sintesis_entrega3_powerbi.md
```

El PDF ([`Sintesis_Entrega3_PowerBI.pdf`](../Sintesis_Entrega3_PowerBI.pdf)) se exporta desde Word (*Archivo → Exportar → PDF*). El Word no se versiona: es la fuente editable y se regenera con estos pasos.

**Relacionado:** [Síntesis](../01_sintesis_entrega3_powerbi.md) · [Guía de Power BI](../guia_power_bi.md) · [README](../../../README.md)
