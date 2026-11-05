# Guía Power BI — Entrega 3 (Objetivo 3)

El informe está en `powerbi/` como proyecto de Power BI (`TFM_Estres.pbip`): modelo semántico en TMDL, 32 medidas DAX, tema de colores «Bienestar» y 7 páginas (Inicio + 6 de análisis). Los datos se leen de 15 CSV exportados del MySQL local (`powerbi_csv/`, no se versionan).


## 1. Preparar los datos

1. En MySQL (XAMPP) deben existir las vistas `vw_*` (`sql/esquema_estrella_powerbi.sql`), las tablas `dwh_*` (`sql/dwh_estrella.sql` + notebook 08) y los resultados del modelado (notebook 09: `dwh_modelo_resultados` y `vw_modelo_resultados`).
2. Con MySQL encendido: `python scripts\exportar_mysql_cli.py`. Genera los 15 CSV en `powerbi_csv/` (UTF-8, coma, punto decimal, nulos como celda vacía). Solo necesita Python y el `mysql.exe` de XAMPP. Hay que repetirlo cada vez que cambien los datos en MySQL.

¿Por qué CSV y no MySQL directo? El origen `MySQL` del modelo existe (parámetro `Fuente = "MySQL"`), pero no funciona con el MySQL de XAMPP. Al conectar sin cifrado, Power BI pide el modo SSL `None`, que el conector actual ya no admite (error *No se puede encontrar el valor solicitado 'None'*).

## 2. Abrir el informe

1. Power BI Desktop actualizado (probado con la versión 2.159, octubre de 2026). Abre `powerbi/TFM_Estres.pbip`.
2. *Transformar datos → Parámetros*:
   - `Fuente` = `CSV`;
   - `RutaCSV` = **ruta absoluta** de la carpeta `powerbi_csv/` en tu equipo. Power Query no admite rutas relativas, así que hay que actualizarla si se mueve la carpeta.
3. *Inicio → Actualizar*. Deben cargar 15 tablas.
4. Comprobación rápida, sin filtros: `Registros` = 319.318 y `% Estrés Alto` = 33,7 %. Si no coinciden, prevalece MySQL y hay que revisar la exportación.

Para ver los números con formato español (319.318 y 33,7 %): *Archivo → Opciones y configuración → Opciones → Configuración regional (Archivo actual) → Configuración regional de cadena de formato = Español (España)*.

## 3. Regenerar las páginas

Los objetos visuales de las 7 páginas los escribe `scripts/generar_paginas_pbir.py` en formato PBIR, junto con `pages.json` (orden del menú, Inicio como página de apertura). Además fija en el modelo el orden de rangos de edad y niveles, quita la suma automática de las métricas de los modelos y muestra `fecha_ejecucion` de los KPIs sin segundos (`dd/mm/yyyy hh:nn`).

- Ejecútalo **con Power BI cerrado**: `python scripts\generar_paginas_pbir.py`.
- **Rehace todos los objetos visuales desde cero:** los ajustes manuales hechos en Desktop se pierden. Úsalo solo para reconstruir el informe.

## 4. Modelo

| Tabla | Rol |
|---|---|
| `vw_hechos_estres` | Hechos: 1 fila = 1 registro de cualquiera de los 12 datasets |
| `vw_dim_dataset`, `vw_dim_genero`, `vw_dim_rango_edad`, `vw_dim_nivel_educativo`, `vw_dim_nivel_estres` | Dimensiones conformes |
| `dim_bloque`, `dim_subreddit` | Dimensiones auxiliares |
| `dwh_agg_prevalencia` (T2), `dwh_nlp_senales` (T3), `dwh_dass_severidad` (T4), `dwh_brecha_tratamiento` (T5) | Hechos agregados |
| `dwh_kpi_catalogo`, `dwh_kpi_resultados` | Definición e histórico de KPIs |
| `vw_modelo_resultados` | Resultados del Objetivo 2 (última ejecución) |

Relaciones (todas uno a varios, con filtro desde la dimensión hacia los hechos):

| Dimensión (1) | Hechos (*) |
|---|---|
| `vw_dim_dataset[id_dataset]` | `vw_hechos_estres`, `vw_modelo_resultados` |
| `vw_dim_genero[id_genero]` | `vw_hechos_estres`, `dwh_agg_prevalencia`, `dwh_dass_severidad` |
| `vw_dim_rango_edad[id_rango_edad]` | `vw_hechos_estres`, `dwh_agg_prevalencia`, `dwh_dass_severidad` |
| `vw_dim_nivel_educativo[id_nivel_educativo]` | `vw_hechos_estres`, `dwh_dass_severidad` |
| `vw_dim_nivel_estres[id_nivel_estres]` | `vw_hechos_estres`, `dwh_nlp_senales`, `dwh_brecha_tratamiento` |
| `dim_bloque[id_bloque]` | `dwh_agg_prevalencia` |
| `dim_subreddit[id_subreddit]` | `dwh_nlp_senales` |
| `dwh_kpi_catalogo[id_kpi]` | `dwh_kpi_resultados` |

Decisiones de modelado:
- `vw_hechos_estres` incluye los 3 datasets sintéticos, pero todas las medidas de volumen filtran `vw_dim_dataset[uso_modelado] = "incluido"`. No hay que excluirlos a mano.
- Las columnas `id_*` están ocultas.
- Rango de edad, nivel de estrés y nivel educativo se ordenan por su id, no alfabéticamente.

## 5. Medidas DAX principales

Todas están en `powerbi/TFM_Estres.SemanticModel/definition/tables/*.tmdl`.

```dax
Registros = CALCULATE ( COUNTROWS ( vw_hechos_estres ), vw_dim_dataset[uso_modelado] = "incluido" )
% Estrés Alto = DIVIDE ( [Registros estrés Alto], [Registros] )
Cobertura demográfica = DIVIDE ( CALCULATE ( [Registros], vw_dim_genero[id_genero] <> 0, vw_dim_rango_edad[id_rango_edad] <> 0 ), [Registros] )
Brecha de género en ansiedad (puntos) = [Ansiedad media DASS (mujeres)] - [Ansiedad media DASS (hombres)]
% Búsqueda de tratamiento = DIVIDE ( SUM ( dwh_brecha_tratamiento[n_con_tratamiento] ), SUM ( dwh_brecha_tratamiento[n_total] ) )
Ratio discriminante LIWC = DIVIDE ( [LIWC ansiedad (estrés Alto)], [LIWC ansiedad (estrés Bajo)] )
Modelos con alerta = CALCULATE ( COUNTROWS ( vw_modelo_resultados ), vw_modelo_resultados[es_mejor_modelo] = 1, vw_modelo_resultados[alerta] <> BLANK () )
```

## 6. Páginas

Tamaño 1280 × 720. En todas: banda superior con título y subtítulo y navegador de páginas como menú. Tema `TFM_Estres_tema_bienestar.json` (teal, arena y coral sobre fondo crema; tarjetas blancas con borde redondeado y sombra). Las tablas tienen anchos fijos con ajuste de texto para que todo se lea sin barras de desplazamiento.

| Página | Contenido |
|---|---|
| **Inicio** (menú principal) | Qué analiza el informe; los 6 KPIs del DWH en tarjetas (última ejecución); un recuadro por bloque con sus fuentes y su página principal; nota de lectura con las advertencias |
| **1 Panorama general** | Segmentadores (bloque, género, rango de edad, nivel educativo); tarjetas de registros, % estrés Alto, % global, cobertura y fuentes; % estrés Alto por bloque y por dataset |
| **2 Demografía** | Mismos segmentadores; % estrés Alto por género, edad y estudios (sin «No reportado»); matriz Género × Edad con % Alto y registros; nota de lectura |
| **3 Lenguaje (Dreaddit)** | Ratio LIWC, sentimiento y posts; vocabulario de ansiedad con y sin estrés por subreddit; tabla por subreddit. Sin filtros demográficos: Dreaddit no tiene género ni edad |
| **4 Validación psicológica** | Brecha de ansiedad M − H, % estrés severo DASS, % búsqueda de tratamiento y KPI 3; tratamiento por nivel de estrés × antecedentes familiares; estrés severo DASS por estudios × género; advertencia sobre Depression Student |
| **5 Modelos predictivos** | AUC medio sin alertas y datasets con alerta; AUC del mejor modelo por dataset; tabla del mejor modelo (protocolo, n, AUC, F1, accuracy) |
| **6 KPIs** | Histórico de los 6 KPIs por ejecución (matriz; las 3 ejecuciones del 22/10/2026 dan los mismos valores: cálculo reproducible); catálogo con unidad y definición; distribución Bajo / Moderado / Alto por dataset (barras al 100 %) |

Valores de control sin filtros (calculados también en SQL):

| Medida | Valor |
|---|---|
| Registros | 319.318 |
| % Estrés Alto | 33,7 % |
| Cobertura demográfica | 17,0 % |
| Brecha de ansiedad | 2,89 |
| Ratio LIWC | 2,58 |
| % Tratamiento | 49,4 % |
| AUC medio sin alertas | 0,786 |
| Datasets con alerta | 2 |
| KPI riesgo crítico (última ejecución) | 72,69 % |

## 7. Mejoras posibles (no hechas)

1. `dwh_modelo_resultados` no guarda el baseline de accuracy (está en `resultados/`). Para mostrarlo habría que añadir la columna `acc_baseline` a esa tabla.
2. Las medidas de T3 y T4 ponderan medias ya redondeadas, así que la segunda decimal puede variar ligeramente. Para exactitud, habría que guardar numerador y denominador por grupo.
3. Los nombres de los bloques y de los KPIs llegan sin tildes desde MySQL («Percepcion emocional», «Tasa de estres…»), y los antecedentes familiares como «No / Yes». **Resuelto en la versión Supabase** (sección 9); el informe local con CSV los mantiene como en MySQL.

## 8. Correcciones aplicadas al proyecto original

El proyecto inicial no abría en Desktop. Se corrigió lo siguiente:
- grupos de consultas `Parametros` y `Funciones` sin declarar;
- medidas `AUC`, `F1` y `Accuracy` que chocaban con columnas del mismo nombre (renombradas a `AUC medio`, `F1 medio` y `Accuracy media`);
- `MySql.Database` en lugar de `MySQL.Database`;
- `Modelos con alerta` contaba los 4 modelos de cada dataset con alerta: ahora cuenta solo el mejor.

## 9. Versión en la nube (Supabase)

La base de datos también está en Supabase (PostgreSQL), en el esquema `tfm`. Los archivos están en `supabase/`.

| Paso | Archivo | Qué hace |
|---|---|---|
| Esquema | `sql/01_esquema.sql` | Traduce a PostgreSQL las 8 dimensiones, las 8 tablas `dwh_*` y los hechos de `vw_hechos_estres`, que se guardan como tabla `hechos_estres` (las tablas originales `b1_*`…`b4_*` se quedan en MySQL) |
| Vistas | `sql/02_vistas.sql` | Vuelve a crear las 7 vistas `vw_*` con los mismos nombres y columnas |
| Correcciones | `sql/03_correcciones_datos.sql` | Pone las tildes en bloques, KPIs, modelos y descripciones, y cambia «Yes» por «Sí» en los antecedentes familiares. Solo en Supabase: MySQL queda igual |
| Migración | `scripts/migrar_mysql_a_supabase.py` | Ejecuta los tres SQL, copia los datos desde MySQL, crea el usuario de solo lectura `tfm_lector` y valida contra MySQL (17/17 tablas y 7/7 cifras de control) |
| Power BI | `scripts/preparar_powerbi_supabase.py` | Genera `supabase/powerbi/` a partir del Power BI local: `Fuente = "Supabase"`, conector PostgreSQL y la medida de antecedentes con «Sí» |

Credenciales: en `supabase/.env` (no se versiona; plantilla en `.env.ejemplo`). El esquema `tfm` no está expuesto en la API REST de Supabase.

Para abrir el informe de Supabase:
1. Abre `supabase/powerbi/TFM_Estres.pbip` y pulsa *Actualizar*.
2. Credenciales de PostgreSQL, pestaña *Base de datos*: usuario `tfm_lector.<ref del proyecto>` y la contraseña de solo lectura.
3. Si falla la conexión por el certificado: *Archivo → Opciones y configuración → Configuración del origen de datos → Editar permisos* y desmarca *Cifrar conexiones*. El conector de Power BI no valida el certificado del pooler de Supabase; el usuario es de solo lectura y los datos son agregados de datasets públicos.

Si cambia el informe local: ejecuta el generador de páginas y después `preparar_powerbi_supabase.py` (con Power BI cerrado). Si cambian los datos en MySQL: vuelve a ejecutar `migrar_mysql_a_supabase.py`, que rehace el esquema desde cero.

## 10. Ficheros de entrega (.pbix)

La rúbrica pide un fichero Power BI. Los proyectos `.pbip` son carpetas con muchos archivos, así que para entregar se guardan como `.pbix` (un único archivo con los datos dentro):

| Fichero | Carpeta | Uso |
|---|---|---|
| `TFM_Estres_supabase.pbix` | `supabase/powerbi/Entrega/` | **Entregable de la Entrega 3.** Versión final, textos corregidos; *Actualizar* pide el usuario `tfm_lector` |
| `TFM_Estres_local.pbix` | `powerbi/Entrega/` (local: `local_xampp/powerbi/Entrega/`) | Respaldo; *Actualizar* necesita los CSV de `RutaCSV` |

Para generarlos: abre el `.pbip`, *Inicio → Actualizar* y *Archivo → Guardar como → Archivos de Power BI (*.pbix)* en la carpeta `Entrega`. El `.pbix` es una copia fija: si el informe cambia, hay que volver a guardarlo. No se suben al repositorio (`*.pbix` está en `.gitignore`) porque llevan los datos dentro; se entregan aparte.
