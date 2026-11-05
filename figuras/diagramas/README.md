# Diagramas del modelo de datos

| Diagrama | Qué muestra |
|---|---|
| `modelo_datos_ERD.png` | Modelo v2 en MySQL: 8 dimensiones (4 conformes ★) y 12 tablas de hechos, una o dos por dataset |
| `esquema_estrella_powerbi_ERD.png` | Capa de consumo para Power BI: vistas `vw_*` en estrella (1 hecho + 5 dimensiones) |
| `dwh_estrella_ERD.png` | DWH del notebook 08: hechos derivados por KPI, catálogo y resultados de los KPIs y del modelado |

## Carpetas

- **`entregados/`**: los diagramas tal como se presentaron en las Entregas 1 y 2. No se modifican.
- **`corregidos/`**: la versión vigente. Solo cambia el texto erróneo; el resto de la imagen es idéntico:

| Diagrama | Decía | Dice | Comprobación |
|---|---|---|---|
| `modelo_datos_ERD.png` | 19 tablas | **20 tablas** | `sql/modelo_datos_mysql.sql` tiene 20 `CREATE TABLE`: 8 dimensiones y 12 tablas de hechos |
| `esquema_estrella_powerbi_ERD.png` | 320.318 filas | **334.318 filas** | `vw_hechos_estres` devuelve 334.318 filas en MySQL y en Supabase (12 datasets, sintéticos incluidos) |
| `dwh_estrella_ERD.png` | — | sin cambios | Sus 319.318 filas son correctas: el DWH solo incluye los 9 datasets con señal real |
