# Prototipo web del informe

Versión web del informe de Power BI en un único HTML: las mismas 7 páginas con los mismos filtros y medidas. Los datos van incrustados en el archivo, así que se abre sin conexión.

Cada versión vive en su propia carpeta (`v1/`, `v2/`, …); las anteriores no se modifican. La versión final es **`v2/`**.

| Versión | Fecha | Contenido |
|---|---|---|
| `v1/` | 05/11/2026 | Primera versión: las 7 páginas del Power BI (Inicio, Panorama, Demografía, Lenguaje, Validación, Modelos y KPIs) con sus filtros. Datos de Supabase |
| `v2/` | 05/11/2026 | **Versión final.** Todo lo de la v1 más la pestaña «Arquitectura»: recorrido de los datos y los tres diagramas del modelo (modelo v2, capa de consumo y DWH) dibujados en SVG, con las columnas de cada tabla y las cifras verificadas (20 tablas, 334.318 y 319.318 filas) |

## Archivos de cada versión

| Archivo | Versiones | Qué hace |
|---|---|---|
| `prototipo_estres.html` | v1, v2 | El prototipo. Se abre con doble clic |
| `construir_prototipo.py` | v1, v2 | Vuelve a incrustar los datos. Por defecto lee de Supabase con el usuario de solo lectura (`../../supabase/.env`); con `--fuente csv` lee los CSV que usa el Power BI local |
| `exportar_arquitectura.py` | v2 | Vuelve a incrustar la estructura de tablas de la pestaña «Arquitectura» (columnas, claves y filas) leyendo MySQL. Solo hace falta si cambia la estructura de la base |
