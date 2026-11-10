# Prototipo web del informe

Versión web del informe de Power BI en un único HTML: las mismas páginas, filtros y medidas. Los datos van incrustados en el archivo, así que se abre sin conexión.

Cada versión vive en su propia carpeta (`v1/`, `v2/`, …); las anteriores no se modifican. La versión final es **`v8/`**.

**Versión publicada:** https://claude.ai/artifact/7DuVNnNh38qLgELbcKAG8b. Muestra la versión final (`v8/`); cada corrección o versión nueva se publica en este mismo enlace.

| Versión | Fecha | Contenido |
|---|---|---|
| `v1/` | 05/11/2026 | Primera versión: las 7 páginas del Power BI (Inicio, Panorama, Demografía, Lenguaje, Validación, Modelos y KPIs) con sus filtros. Datos de Supabase |
| `v2/` | 05/11/2026 | Todo lo de la v1 más la pestaña «Arquitectura»: recorrido de los datos y los tres diagramas del modelo (modelo v2, capa de consumo y DWH) dibujados en SVG, con las columnas de cada tabla y las cifras verificadas (20 tablas, 334.318 y 319.318 filas) |
| `v3/` | 10/11/2026 | Todo lo de la v2 más las mejoras del Power BI: logo, iconos de los bloques y fondo en Inicio; tooltip con el resumen del dataset o bloque; clic en un dataset → ficha del dataset con botón Volver (equivale a *Obtener detalles*); jerarquía bloque → dataset en Panorama; página **7 Explorar** con árbol de descomposición (incluye «Valor alto / bajo») e influenciadores clave, con el árbol a la izquierda y los influenciadores a la derecha |
| `v4/` | 10/11/2026 | La v3 con el árbol de descomposición a todo el ancho (caben la raíz y los 5 campos) y los influenciadores debajo; las instrucciones pasan al subtítulo, como en el Power BI |
| `v5/` | 10/11/2026 | La v4 con el árbol de descomposición abierto por defecto en la ruta representativa del `.pbix` y del PDF entregados: Validación psicológica (34,1 %) → Femenino (39,0 %) → 18-25 (37,6 %) → Nivel educativo. Muestra en una sola vista los insights 2, 3 y 4 |
| `v6/` | 10/11/2026 | El árbol vuelve a empezar sin desglosar, para que se vea que es una herramienta de exploración, y suma dos botones: **Ver ruta de ejemplo**, que carga en un clic la ruta de la v5 (la del `.pbix`, el PDF y la figura 2 del Word), y **Reiniciar**, que deja el árbol vacío |
| `v7/` | 10/11/2026 | La v6 con los logos de INESDI y UNIE en blanco en la banda de Inicio, separados por una línea fina, como en el Power BI |
| `v8/` | 10/11/2026 | **Versión final.** La v7 con los logos más grandes (INESDI 24 px y UNIE 44 px de alto) y el subtítulo de Inicio acortado a «TFM · Business Analytics e IA», como la banda del Power BI |

## Archivos de cada versión

| Archivo | Versiones | Qué hace |
|---|---|---|
| `prototipo_estres.html` | todas | El prototipo. Se abre con doble clic |
| `construir_prototipo.py` | todas | Vuelve a incrustar los datos. Por defecto lee de Supabase con el usuario de solo lectura (`../../supabase/.env`); con `--fuente csv` lee los CSV que usa el Power BI local. Desde la v3 también incrusta los iconos y el logo de `local_xampp/powerbi/imagenes` |
| `exportar_arquitectura.py` | v2 a v8 | Vuelve a incrustar la estructura de tablas de la pestaña «Arquitectura» (columnas, claves y filas) leyendo MySQL. Solo hace falta si cambia la estructura de la base |
