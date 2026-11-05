# Base de datos en la nube (Supabase)

Versión en la nube de la base de datos del TFM: PostgreSQL en Supabase, esquema `tfm`. Contiene lo que consumen el informe de Power BI y el prototipo web: 8 dimensiones, las 8 tablas del DWH y los hechos de la capa estrella (`hechos_estres`, 334.318 filas), con las 7 vistas `vw_*`. Las tablas originales de cada dataset (`b1_*` … `b4_*`) se quedan en MySQL.

| Carpeta | Contenido |
|---|---|
| `sql/` | `01_esquema.sql` (tablas en PostgreSQL), `02_vistas.sql` (vistas `vw_*`), `03_correcciones_datos.sql` (tildes y «Yes» → «Sí», solo en Supabase) |
| `scripts/` | `migrar_mysql_a_supabase.py` (migración y validación), `probar_lector.py` (prueba del usuario de solo lectura), `preparar_powerbi_supabase.py` (genera `powerbi/`) |
| `powerbi/` | El informe de Power BI conectado a Supabase con el conector PostgreSQL |

## Uso

1. Copia `.env.ejemplo` como `.env` y rellena las credenciales del proyecto de Supabase (nunca se versiona).
2. Con MySQL encendido: `python scripts/migrar_mysql_a_supabase.py`. Crea el esquema, copia los datos, aplica las correcciones, crea el usuario `tfm_lector` y compara filas y cifras de control con MySQL.
3. `python scripts/preparar_powerbi_supabase.py` (con Power BI cerrado) y abre `powerbi/TFM_Estres.pbip` con el usuario `tfm_lector.<ref del proyecto>`.

Validación de la migración (05/11/2026): 17 de 17 tablas con las mismas filas que MySQL y 7 de 7 cifras de control iguales (319.318 registros, 33,68 % de estrés Alto, 17,0 % de cobertura, 49,41 % de tratamiento, 3.549 posts, AUC 0,786 y 2 datasets con alerta).

Detalles en la [guía de Power BI](../docs/entrega3_objetivo3/guia_power_bi.md#9-versión-en-la-nube-supabase).
