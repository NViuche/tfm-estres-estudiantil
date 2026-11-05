# Prototipo web del informe

Versión web del informe de Power BI en un único HTML: las mismas 7 páginas con los mismos filtros y medidas, más una pestaña «Arquitectura» con los diagramas del modelo de datos. Los datos van incrustados en el archivo, así que se abre sin conexión.

Cada versión vive en su propia carpeta (`v1/`, `v2/`, …); las anteriores no se modifican.

| Versión | Fecha | Contenido |
|---|---|---|
| `v1/` | 05/11/2026 | 7 páginas del Power BI + «Arquitectura» (modelo v2, capa de consumo y DWH dibujados en SVG, con cifras verificadas). Datos de Supabase |

## Archivos de cada versión

| Archivo | Qué hace |
|---|---|
| `prototipo_estres.html` | El prototipo. Se abre con doble clic |
| `construir_prototipo.py` | Vuelve a incrustar los datos. Por defecto lee de Supabase con el usuario de solo lectura (`../../supabase/.env`); con `--fuente csv` lee los CSV que usa el Power BI local |
| `exportar_arquitectura.py` | Vuelve a incrustar la estructura de tablas (columnas, claves y filas) leyendo MySQL. Solo hace falta si cambia la estructura de la base |
