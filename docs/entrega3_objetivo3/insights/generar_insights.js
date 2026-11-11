// Documento de insights de la Entrega 3 (Word). Uso: node insights.js <carpeta_figuras> <salida.docx>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, HeadingLevel, LevelFormat, BorderStyle, Footer, PageNumber, TableOfContents, PageBreak, ExternalHyperlink,
} = require("docx");

const [, , FIG, SALIDA] = process.argv;
const TEAL = "1F6F6B", INK = "264653", GRIS = "5B6B70", CORAL = "C8553D";
const FUENTE = "Arial";
const ANCHO = 9026; // A4 con márgenes de 2,54 cm
const URL_WEB = "https://claude.ai/artifact/7DuVNnNh38qLgELbcKAG8b";  // versión web interactiva del informe

// ---------------------------------------------------------------- piezas
const t = (text, o = {}) => new TextRun({ text, font: FUENTE, ...o });
const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 120, line: 288 }, ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(text)] });
const vineta = (runs) => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 60, line: 276 } });
const etiqueta = (nombre, texto) => p([t(nombre + ". ", { bold: true, color: TEAL }), ...(Array.isArray(texto) ? texto : [t(texto)])]);
const b = (text) => t(text, { bold: true });
const enlace = (url) => new ExternalHyperlink({ link: url, children: [t(url, { color: "1F6F6B", underline: {} })] });

let nFig = 0;
// Figura solo si la captura existe (p. ej., la página 8 hasta que se exporte el PDF del informe con ella)
const figuraSi = (archivo, pie) => fs.existsSync(path.join(FIG, archivo)) ? figura(archivo, pie) : [];
function figura(archivo, pie) {
  nFig += 1;
  const datos = fs.readFileSync(path.join(FIG, archivo));
  // Alto según la proporción real de la imagen (cabecera PNG): la página Explorar es más alta que las demás
  const alto = Math.round(600 * datos.readUInt32BE(20) / datos.readUInt32BE(16));
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data: datos, transformation: { width: 600, height: alto },
        altText: { title: pie, description: pie, name: archivo } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
      children: [t(`Figura ${nFig}. `, { bold: true, size: 18, color: GRIS }), t(pie, { italics: true, size: 18, color: GRIS })] }),
  ];
}

const borde = { style: BorderStyle.SINGLE, size: 4, color: "D9D2C7" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
function tabla(anchos, cabecera, filas) {
  const celda = (texto, w, cab, i) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: bordes, margins: { top: 60, bottom: 60, left: 100, right: 100 },
    shading: cab ? { type: ShadingType.CLEAR, fill: "2A7F7F", color: "auto" } : (i % 2 ? { type: ShadingType.CLEAR, fill: "F2F8F7", color: "auto" } : undefined),
    children: [new Paragraph({ spacing: { after: 0 }, children: [t(texto, { size: 19, bold: cab, color: cab ? "FFFFFF" : INK })] })],
  });
  return new Table({
    width: { size: anchos.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: anchos,
    rows: [new TableRow({ tableHeader: true, children: cabecera.map((c, j) => celda(c, anchos[j], true, 0)) }),
      ...filas.map((f, i) => new TableRow({ children: f.map((c, j) => celda(c, anchos[j], false, i)) }))],
  });
}

// ---------------------------------------------------------------- contenido
const portada = [
  new Paragraph({ spacing: { before: 2400, after: 120 }, children: [t("TFM · Análisis multidimensional del estrés estudiantil", { size: 24, color: TEAL, bold: true })] }),
  new Paragraph({ heading: HeadingLevel.TITLE, children: [t("Insights del informe de Power BI")] }),
  new Paragraph({ spacing: { after: 600 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: TEAL, space: 8 } },
    children: [t("Entrega 3 · Objetivo 3: explotación de los datos y descubrimiento de insights", { size: 26, color: GRIS })] }),
  p([b("Máster en Business Analytics e Inteligencia Artificial"), t(" · UNIE / INESDI")]),
  p([b("Equipo: "), t("Obed Isaí Alvarado Núñez, Roberto Mario Brochero López, Raúl Cervantes Iglesias, Andrés Francisco García Grajales, Santiago Nicolas Viuche Pinilla")]),
  p([b("Fichero Power BI: "), t("TFM_Estres_supabase.pbix (datos en Supabase, esquema tfm)")]),
  p([b("Versión web interactiva: "), enlace(URL_WEB)]),
  p([b("Fecha: "), t("noviembre de 2026")]),
  new Paragraph({ children: [new PageBreak()] }),
];

const indice = [
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t("Contenido")] }),
  new TableOfContents("Contenido", { hyperlink: true, headingStyleRange: "1-2" }),
  p([t("Si el índice aparece vacío, en Word: clic derecho sobre él → Actualizar campos.", { italics: true, size: 18, color: GRIS })]),
  new Paragraph({ children: [new PageBreak()] }),
];

const resumen = [
  h1("1. Resumen"),
  p("El informe de Power BI reúne 12 datasets públicos sobre estrés estudiantil, organizados en 4 bloques (factores internos, hábitos digitales, percepción emocional y validación psicológica). Las 9 fuentes con señal real suman 319.318 registros; los 3 datasets sintéticos se excluyen de las medidas. Cada fuente se compara con las demás a través de un nivel de estrés común (Bajo / Moderado / Alto) y de las dimensiones conformes de género, edad y nivel educativo."),
  p("Explorando el informe encontramos ocho insights. Los cuatro primeros describen a quién afecta más el estrés y quién busca ayuda; los tres siguientes explican cómo deben leerse las cifras y hasta dónde llegan los modelos, y el último evalúa la calidad de los propios datos."),
  tabla([600, 4300, 2826, 1300], ["N.º", "Insight", "Dato clave", "Página"], [
    ["1", "Buscar ayuda depende de los antecedentes familiares, no del nivel de estrés", "≈ 72 % frente a ≈ 35 %, igual en los tres niveles", "4 Validación"],
    ["2", "Las mujeres reportan más estrés que los hombres en casi todas las fuentes", "39,1 % frente a 32,0 %; en 3 de 4 bloques", "2 Demografía y 4 Validación"],
    ["3", "El estrés Alto disminuye con la edad", "48,3 % (<18) → 18,0 % (>50)", "2 Demografía"],
    ["4", "A más nivel educativo, menos estrés Alto y severo", "34,2 % → 29,8 % → 26,4 %", "2 Demografía y 4 Validación"],
    ["5", "El lenguaje delata el estrés, sobre todo fuera de los foros de ansiedad", "Ratio LIWC 2,58; hasta 4,83 en r/stress", "3 Lenguaje"],
    ["6", "El porcentaje global lo marca una sola fuente: se comparan tendencias, no niveles", "Mental Health Dataset = 81,8 % de los registros", "1 Panorama y 6 KPIs"],
    ["7", "La señal predictiva es real pero moderada, y dos fuentes exigen cautela", "AUC medio 0,786; 2 datasets con alerta", "5 Modelos"],
    ["8", "Los datos de origen son de buena calidad, pero la completitud demográfica limita los cruces", "39 de 49 reglas OK, 0 errores; edad informada en el 20,7 %", "8 Calidad"],
  ]),
  p(""),
  p([b("Versión web interactiva. "), t("Los insights también pueden comprobarse desde el navegador, sin instalar Power BI: "), enlace(URL_WEB),
    t(". La versión web reproduce las páginas del informe con los mismos datos de Supabase, filtros y medidas; en la página Explorar, el botón «Ver ruta de ejemplo» carga la ruta del árbol de descomposición que se describe en el apartado 2, y un clic sobre cualquier dataset abre su ficha. Incluye además una pestaña con la arquitectura de los datos.")]),
];

const metodo = [
  h1("2. Cómo se exploró el informe"),
  p("El informe tiene nueve páginas en el menú: Inicio (menú principal con los 6 KPIs del DWH), Panorama, Demografía, Lenguaje, Validación, Modelos, KPIs, Explorar y Calidad (reglas de calidad, completitud por dataset y registro de controles). Además, cada dataset tiene una ficha a la que se llega con clic derecho → Obtener detalles, y al pasar el ratón por las barras de Panorama aparece un resumen del dataset o bloque. Cada insight se obtuvo con el mismo procedimiento, que también sirve para reproducirlo:"),
  vineta([b("Detectar. "), t("Un patrón llama la atención en un gráfico o una tarjeta: una diferencia grande entre categorías o una tendencia que se repite.")]),
  vineta([b("Aislar. "), t("Con los segmentadores (bloque, género, rango de edad y nivel educativo), sincronizados entre Panorama, Demografía y Explorar, y con los filtros cruzados de Power BI se comprueba si el patrón se mantiene en cada subgrupo o desaparece. El árbol de descomposición de la página Explorar permite encadenar esos cortes (por ejemplo, bloque → género → edad) y su opción «Valor alto» busca por sí sola el corte con más estrés Alto.")]),
  vineta([b("Descartar el efecto composición. "), t("Como las fuentes tienen tamaños muy distintos, un patrón global puede deberse solo a qué fuente aporta cada grupo. Por eso cada insight se verificó también dentro de cada dataset.")]),
  vineta([b("Contrastar. "), t("Se cruzó con las tablas del DWH, los KPIs, los modelos del Objetivo 2 y los influenciadores clave de la página Explorar, que estiman qué valores multiplican la probabilidad de estrés Alto. Todas las cifras de este documento coinciden con las calculadas en SQL sobre MySQL y sobre Supabase.")]),
  etiqueta("Cómo leer las cifras", "Cada fuente define «Alto» con su propio criterio nativo (por ejemplo, GAD-7 ≥ 10 o un índice 4–5 sobre 5), mapeado al constructo común. Por eso el informe compara tendencias dentro de cada fuente, no niveles absolutos entre fuentes (insight 6)."),
  ...figura("p0_inicio.png", "Página Inicio: menú principal, los 6 KPIs del DWH y los 4 bloques analíticos."),
  p([t("La página Explorar reúne los dos visuales de inteligencia artificial de Power BI. En el árbol de descomposición, la ruta Bloque = Validación psicológica (34,1 %) → Género = Femenino (39,0 %) → Rango de edad = 18-25 (37,6 %) → Nivel educativo muestra en una sola vista tres de los insights de este documento: más estrés en mujeres, que baja con la edad y con los estudios (de 40,4 % en secundaria a 35,0 % en posgrado). Los influenciadores clave, con «Alto» elegido, ordenan los factores que más elevan su probabilidad.")]),
  ...figura("p7_explorar.png", "Página 7 (Explorar): árbol de descomposición con la ruta Validación psicológica → Femenino → 18-25 → Nivel educativo, e influenciadores clave del estrés Alto."),
];

const insights = [
  h1("3. Insights"),

  h2("Insight 1. Buscar ayuda depende de los antecedentes familiares, no del nivel de estrés"),
  etiqueta("Qué muestra", "Entre quienes tienen antecedentes familiares de salud mental, alrededor del 72 % ha buscado tratamiento; entre quienes no los tienen, alrededor del 35 %. Esa diferencia de unos 37 puntos es la misma en los tres niveles de estrés: 35,7 % / 34,6 % / 35,2 % sin antecedentes y 73,2 % / 71,8 % / 72,5 % con antecedentes (Bajo / Moderado / Alto). Sentir más estrés no aumenta la búsqueda de ayuda."),
  etiqueta("Cómo se encontró", "En la página 4 (Validación), la tarjeta «% búsqueda de tratamiento» marca un 49,4 % global. Al mirar el gráfico «Búsqueda de tratamiento por nivel de estrés y antecedentes familiares», las columnas de cada color tienen prácticamente la misma altura en Bajo, Moderado y Alto, mientras que entre colores la diferencia es enorme."),
  etiqueta("Comprobación", "La tabla dwh_brecha_tratamiento (54.207 respondentes del Mental Health Dataset) confirma que entre niveles de estrés la variación es menor de 1,1 puntos, y entre grupos con y sin antecedentes está entre 36 y 38 puntos."),
  etiqueta("Qué implica", "Hay una brecha entre malestar y ayuda: 7.751 personas con estrés Alto y sin antecedentes familiares no han buscado tratamiento. Las campañas de detección y orientación deberían dirigirse a ese grupo, que no tiene un referente cercano que normalice pedir ayuda."),
  etiqueta("Cautela", "El Mental Health Dataset es una encuesta amplia, no exclusivamente estudiantil, y su variable de estrés es autopercibida («estrés creciente»: sí / tal vez / no)."),
  ...figura("p4_validacion.png", "Página 4 (Validación psicológica): búsqueda de tratamiento por nivel de estrés y antecedentes, y estrés severo DASS-42 por estudios y género."),

  h2("Insight 2. Las mujeres reportan más estrés que los hombres en casi todas las fuentes"),
  etiqueta("Qué muestra", "El 39,1 % de los registros femeninos está en estrés Alto, frente al 32,0 % de los masculinos. En el DASS-42, la ansiedad media de las mujeres supera en 2,89 puntos a la de los hombres (31,0 frente a 28,1; KPI 2), y el porcentaje de estrés severo es mayor en las mujeres en los tres niveles educativos: 40,4 % frente a 28,2 % (secundaria), 35,8 % frente a 25,5 % (grado) y 35,0 % frente a 23,7 % (posgrado)."),
  etiqueta("Cómo se encontró", "En la página 2 (Demografía), el gráfico «% de estrés Alto por género». Después, aplicando el segmentador Bloque uno a uno, la diferencia se mantiene en Factores internos (35,1 % frente a 16,5 %), Hábitos digitales (53,2 % frente a 36,0 %) y Validación psicológica (39,0 % frente a 32,8 %). El gráfico de estrés severo por estudios y género de la página 4 lo confirma para el DASS-42."),
  etiqueta("Comprobación", "Dentro de cada dataset, las mujeres tienen más estrés Alto en 5 de las 6 fuentes con género informado (Student Anxiety GAD-7: 34 % frente a 16 %; DASS-42: 38 % frente a 27 %; Social Media and Mental Health: 53 % frente a 36 %; Mental Health Dataset: 40 % frente a 33 %; Student Mental Health Survey: 67 % frente a 37 %, con solo 87 registros). La única excepción es Depression Student (49 % frente a 52 %), en el bloque Percepción emocional. En la página Explorar, los influenciadores clave sitúan «Género es Otro» entre los factores que más elevan la probabilidad de estrés Alto (1,66x)."),
  etiqueta("Qué implica", "La perspectiva de género debe estar presente en cualquier programa de bienestar estudiantil, con atención especial a la ansiedad."),
  etiqueta("Cautela", "El 91 % de los registros masculinos procede del Mental Health Dataset, y la categoría «Otro» (49,3 %) tiene solo 677 registros. Los datos son autorreportados, y parte de la diferencia puede deberse a que las mujeres declaran más el malestar."),
  ...figura("p2_demografia.png", "Página 2 (Demografía): estrés Alto por género, rango de edad y nivel educativo, y matriz género × edad."),

  h2("Insight 3. El estrés Alto disminuye con la edad"),
  etiqueta("Qué muestra", "El porcentaje de estrés Alto baja de forma continua con la edad: 48,3 % en menores de 18, 29,7 % entre 18 y 25, 28,4 % entre 26 y 35, 25,5 % entre 36 y 50 y 18,0 % en mayores de 50."),
  etiqueta("Cómo se encontró", "En la página 2, el gráfico «% de estrés Alto por rango de edad» (figura 4). La matriz «Género × rango de edad» muestra que la caída se produce en mujeres (de 50,9 % a 20,2 %) y en hombres (de 36,6 % a 15,2 %)."),
  etiqueta("Comprobación", "Casi todos los menores de 18 (7.269 de 7.291) proceden del DASS-42, así que la comparación correcta es dentro de esa fuente. Con el segmentador Bloque = Validación psicológica, la tendencia se mantiene: 48,3 % → 35,5 % → 30,0 % → 26,1 % → 18,0 %. En Student Anxiety GAD-7 va en la misma dirección, aunque más suave (18 % entre 18 y 25, 15 % entre 26 y 35). Los influenciadores clave de la página Explorar lo confirman: «Rango de edad es <18» multiplica por 1,51 la probabilidad de estrés Alto. En el árbol de descomposición, la ruta Bloque = Validación psicológica → Rango de edad muestra el mismo gradiente."),
  etiqueta("Qué implica", "Los estudiantes más jóvenes son el grupo prioritario. La etapa preuniversitaria y los primeros cursos concentran el mayor riesgo."),
  etiqueta("Cautela", "Solo el 17 % de los registros informa a la vez género y edad (KPI de cobertura demográfica), y la tendencia se apoya sobre todo en una fuente (el DASS-42, una muestra en línea)."),

  h2("Insight 4. A más nivel educativo, menos estrés Alto y severo"),
  etiqueta("Qué muestra", "El estrés Alto baja con el nivel de estudios: 34,2 % (secundaria o menos), 29,8 % (grado universitario) y 26,4 % (posgrado). En el DASS-42, el estrés severo también baja de nivel en nivel, tanto en mujeres como en hombres."),
  etiqueta("Cómo se encontró", "En la página 2, el gráfico «% de estrés Alto por nivel educativo» (figura 4), y en la página 4, el gráfico «DASS-42: % de estrés severo por estudios y género» (figura 3)."),
  etiqueta("Comprobación", "La tendencia se repite dentro de las dos fuentes con más registros educativos: DASS-42 (41 % → 32 % → 28 %) y Student Anxiety GAD-7 (18 % → 15 % → 13 %). No es un efecto de mezcla de fuentes."),
  etiqueta("Qué implica", "Las primeras etapas formativas son las más expuestas; el refuerzo en la transición a la universidad es un punto de intervención claro."),
  etiqueta("Cautela", "Nivel educativo y edad están relacionados (a más edad, más estudios), y con los datos disponibles no se pueden separar sus efectos."),

  h2("Insight 5. El lenguaje delata el estrés, sobre todo fuera de los foros de ansiedad"),
  etiqueta("Qué muestra", "En los 3.549 posts de Reddit de Dreaddit, los posts con estrés usan 2,58 veces más vocabulario de ansiedad (LIWC) que los posts sin estrés (KPI 5). La diferencia es mucho mayor en comunidades que no tratan sobre la ansiedad: r/stress (4,83), r/food_pantry (4,45) y r/assistance (4,27), frente a r/anxiety (1,91) y r/almosthomeless (1,80)."),
  etiqueta("Cómo se encontró", "En la página 3 (Lenguaje), el gráfico «Vocabulario de ansiedad (LIWC) por subreddit» muestra que en r/anxiety incluso los posts sin estrés usan mucho vocabulario de ansiedad (1,27), mientras que en el resto ese valor base está entre 0,15 y 0,58. La tabla «Detalle por subreddit» ordenada por ratio lo cuantifica."),
  etiqueta("Comprobación", "El modelo híbrido TF-IDF + LIWC del Objetivo 2 alcanza un AUC de 0,838 en Dreaddit, el mejor de las fuentes sin alertas (página 5): la señal del lenguaje es aprovechable. El sentimiento medio, en cambio, es casi neutro (0,042) y separa peor."),
  etiqueta("Qué implica", "El vocabulario de ansiedad sirve como señal temprana de estrés justo donde no se espera, en foros de ayuda material o de relaciones, que es donde una alerta aporta más."),
  etiqueta("Cautela", "Algunos subreddits tienen pocos posts (r/stress 78, r/food_pantry 43), y los usuarios de Reddit no son necesariamente estudiantes."),
  ...figura("p3_lenguaje.png", "Página 3 (Lenguaje y estrés): vocabulario de ansiedad con y sin estrés por subreddit, y detalle con ratio, posts y sentimiento."),

  h2("Insight 6. El porcentaje global lo marca una sola fuente: se comparan tendencias, no niveles"),
  etiqueta("Qué muestra", "El Mental Health Dataset aporta 261.328 de los 319.318 registros (81,8 %), así que el 33,7 % de estrés Alto global coincide prácticamente con su propio valor (33,8 %). Entre fuentes, el porcentaje de estrés Alto va del 17,5 % (Student Anxiety GAD-7) al 63,6 % (Academic Stress)."),
  etiqueta("Cómo se encontró", "En la página 1 (Panorama), la tarjeta «% estrés Alto global» se compara con el gráfico «% de estrés Alto por dataset». En la página 6 (KPIs), las barras al 100 % muestran que Student Anxiety GAD-7 tiene un 55,3 % de registros en Bajo y Academic Stress solo un 10,7 %."),
  etiqueta("Comprobación", "La diferencia procede del criterio de cada fuente: GAD-7 usa un umbral clínico (≥ 10 puntos), mientras que Academic Stress usa un índice autopercibido (4–5 sobre 5). No es que unos estudiantes estén mucho más estresados que otros."),
  etiqueta("Qué implica", "Esto valida el diseño del proyecto: un constructo común para poder cruzar fuentes, pero leyendo cada fuente por separado. Para comparar grupos, el informe permite filtrar por bloque, bajar de bloque a dataset en Panorama y abrir la ficha de cada dataset con Obtener detalles."),
  etiqueta("Lo confirman los influenciadores clave", "En la página Explorar, los dos factores que más elevan la probabilidad de estrés Alto son «Género es No reportado» (1,70x) y «Bloque es Percepción emocional» (1,68x). No describen a las personas sino a las fuentes: las que no informan el género, o las del bloque de texto y NLP, tienen más estrés Alto según su propio criterio. Es el mismo efecto composición, y por eso los influenciadores se leen siempre junto al desglose por dataset."),
  etiqueta("Cautela", "Cualquier cifra global debe acompañarse de su desglose por fuente."),
  ...figura("p1_panorama.png", "Página 1 (Panorama): KPIs con segmentadores y % de estrés Alto por bloque y por dataset."),
  ...figura("p6_kpis.png", "Página 6 (KPIs): histórico y catálogo de los 6 KPIs y distribución Bajo / Moderado / Alto por dataset."),

  h2("Insight 7. La señal predictiva es real pero moderada, y dos fuentes exigen cautela"),
  etiqueta("Qué muestra", "En las seis fuentes sin alertas, el mejor modelo de cada una obtiene un AUC de entre 0,763 (DASS-42) y 0,838 (Dreaddit), con una media de 0,786. Dos fuentes tienen alerta: Depression Student (AUC 0,998) y Academic Stress (140 registros, cuyo accuracy no supera al baseline)."),
  etiqueta("Cómo se encontró", "En la página 5 (Modelos), la tarjeta «Datasets con alerta» aparece en color coral con un 2. El gráfico de AUC por dataset muestra a Depression Student muy por encima del resto, y la nota de alertas explica por qué."),
  etiqueta("Comprobación", "Un AUC de 0,998 en datos de encuesta no es creíble: apunta a que la etiqueta se generó con una fórmula a partir de las propias variables. Por eso el KPI 3 de riesgo crítico (72,69 %), calculado sobre Depression Student, se muestra con advertencia en la página 4. Los KPIs son reproducibles: las 3 ejecuciones guardadas dan los mismos valores (página 6)."),
  etiqueta("Qué implica", "Los modelos sirven para investigación y para priorizar, no para diagnóstico clínico. Este análisis cubre la parte opcional de la rúbrica (machine learning con Python, notebook 09)."),
  etiqueta("Cautela", "Tres tareas tienen menos de 600 registros, así que sus métricas varían mucho entre particiones."),
  ...figura("p5_modelos.png", "Página 5 (Modelos predictivos): AUC del mejor modelo por dataset, alertas y detalle de protocolo y métricas."),

  h2("Insight 8. Los datos de origen son de buena calidad, pero la completitud demográfica limita los cruces"),
  etiqueta("Qué muestra", "De las 49 reglas de calidad evaluadas sobre los 12 datasets antes de la carga, 39 se cumplen (79,6 %), 10 dan aviso y ninguna da error. Los avisos se concentran en validez (5) y completitud (4), y cada uno tiene un tratamiento documentado. De los 17 controles de carga, ETL, migración, seguridad e informe, 14 se superan y 3 quedan como avisos conocidos. El problema no está en la calidad de los valores sino en lo que cada fuente recoge: sobre los 334.318 registros, el género está informado en el 95,6 %, pero la edad solo en el 20,7 % y el nivel educativo en el 15,3 %."),
  etiqueta("Cómo se encontró", "En la página 8 (Calidad), las tarjetas resumen el resultado de las reglas y los controles, y el gráfico «Reglas por dimensión de calidad» muestra dónde se concentran los avisos. En la tabla «Completitud por dataset», la columna Edad del Mental Health Dataset marca un 0,0 %: esa fuente, que aporta el 78 % de los registros, no informa la edad ni los estudios."),
  etiqueta("Comprobación", "Explica el KPI de cobertura demográfica (17,0 %): para tener género y edad a la vez, un registro tiene que venir de una fuente que recoja los dos. Las reglas dejan además rastro en los datos: Dreaddit train tiene 2.838 filas de origen y 2.834 en los hechos, justo los 4 textos corruptos que detecta la regla R7 y que la carga excluye. Las cifras de completitud coinciden con las calculadas en SQL sobre Supabase."),
  etiqueta("Qué implica", "Las limitaciones de los cruces demográficos (insights 2 a 4) vienen del diseño de las fuentes, no de errores de calidad. Para ampliar el análisis por edad hay que priorizar fuentes que la recojan, y las reglas y los controles deben volver a ejecutarse cada vez que se añada una fuente."),
  etiqueta("Cautela", "Las reglas comprueban que los datos sean completos, válidos y coherentes, no que sean verdaderos: siguen siendo autorreportados. El aviso con más casos es el de validez del DASS-42: 5.192 respondentes (13,1 %) marcaron palabras inexistentes del control de vocabulario, una señal de respuesta poco atenta que se documenta pero no se excluye."),
  ...figuraSi("p8_calidad.png", "Página 8 (Calidad): reglas por dimensión y estado, completitud por dataset, reglas con aviso y registro de controles."),
];

const gobierno = [
  h1("4. Calidad y gobierno del dato"),
  p("La página 8 del informe hace visible el trabajo de calidad y gobierno del dato del proyecto. La tabla resume cómo se cubre cada área del marco DAMA-DMBOK y dónde está la evidencia:"),
  tabla([2300, 6726], ["Área", "Evidencia"], [
    ["Calidad del dato", "49 reglas antes de la carga (notebook 05), validación después de la carga (notebook 07b) y cifras de control que coinciden en MySQL, Supabase y Power BI. Tablas dwh_calidad_reglas y dwh_calidad_controles, visibles en la página 8"],
    ["Metadatos", "Diccionario y fichas técnicas por dataset, catálogo de KPIs con definición, unidad y fuente de cálculo, y guía del informe"],
    ["Linaje", "dim_dataset y tabla_origen identifican el origen de cada registro; dim_mapeo_estres documenta el criterio con el que cada fuente se lleva al nivel común"],
    ["Datos de referencia", "4 dimensiones conformes (género, edad, nivel educativo y nivel de estrés) con el miembro «No reportado» para los vacíos"],
    ["Seguridad y acceso", "Usuario tfm_lector de solo lectura; la API pública solo lee vistas agregadas; credenciales fuera del repositorio"],
    ["Control de cambios", "Versiones en git con ramas por entrega y rama principal protegida; las correcciones quedan trazadas"],
    ["Aptitud de uso", "Datasets sintéticos marcados y excluidos del modelado; alertas de modelos y cautelas declaradas en el informe"],
  ]),
  p(""),
  p("Quedan como trabajo futuro la asignación formal de roles (responsable y custodio de cada fuente), un glosario de negocio único y la monitorización periódica de las reglas. Los datos de salud mental son una categoría especial según el RGPD (art. 9): el proyecto usa solo fuentes públicas anonimizadas y publica únicamente datos agregados."),
];

const limites = [
  h1("5. Limitaciones generales"),
  vineta("Las fuentes son independientes: no comparten personas, así que no se pueden seguir individuos de una a otra."),
  vineta("Varias poblaciones no son estrictamente estudiantiles (Reddit, encuestas generales de salud mental)."),
  vineta("Solo el 17 % de los registros informa a la vez género y edad, de modo que los cruces demográficos trabajan con una submuestra."),
  vineta("Los datos son autorreportados y cada fuente define «Alto» con su propio criterio."),
  vineta("Los 3 datasets sintéticos (distribuciones uniformes, correlaciones ≈ 0) se excluyen de todas las medidas."),
];

const anexo = [
  h1("Anexo. Cómo reproducir los insights"),
  p([t("El fichero "), b("TFM_Estres_supabase.pbix"), t(" lleva los datos dentro y se abre con Power BI Desktop. Para actualizarlo hace falta el usuario de solo lectura de Supabase (tfm_lector). Las mismas rutas pueden seguirse en la versión web ("), enlace(URL_WEB), t("), donde la ficha del dataset se abre con un clic. Ruta de cada insight:")]),
  tabla([700, 2300, 6026], ["Insight", "Página", "Visual y filtro"], [
    ["1", "4 Validación", "«Búsqueda de tratamiento por nivel de estrés y antecedentes familiares»"],
    ["2", "2 Demografía · 4 Validación", "«% de estrés Alto por género» con el segmentador Bloque; «DASS-42: % de estrés severo por estudios y género»"],
    ["3", "2 Demografía", "«% de estrés Alto por rango de edad»; Bloque = Validación psicológica; matriz «Género × rango de edad»"],
    ["4", "2 Demografía · 4 Validación", "«% de estrés Alto por nivel educativo»; gráfico DASS-42 por estudios"],
    ["5", "3 Lenguaje", "«Vocabulario de ansiedad (LIWC) por subreddit» y tabla «Detalle por subreddit»"],
    ["6", "1 Panorama · 6 KPIs", "«% estrés Alto global» frente a «% de estrés Alto por dataset»; barras al 100 %"],
    ["7", "5 Modelos · 4 Validación", "«Datasets con alerta», «AUC del mejor modelo por dataset» y tarjeta del KPI 3"],
    ["8", "8 Calidad", "Tarjetas de reglas y controles, «Reglas por dimensión de calidad» y columna Edad de «Completitud por dataset»"],
    ["2, 3 y 6", "7 Explorar", "Árbol de descomposición (Bloque → Género → Rango de edad, o «Valor alto») e influenciadores clave con «Alto» elegido"],
    ["Todos", "Detalle del dataset", "Clic derecho sobre un dataset → Obtener detalles: ficha con registros, distribución, demografía y mejor modelo"],
  ]),
  p(""),
  p([t("Las capturas proceden del informe entregado (versión Supabase, con tildes y «Sí» en los antecedentes familiares), con la ruta de ejemplo desplegada en el árbol de Explorar.", { italics: true, size: 19, color: GRIS })]),
];

// ---------------------------------------------------------------- documento
const doc = new Document({
  creator: "Equipo TFM estrés estudiantil", title: "Insights del informe de Power BI",
  description: "Entrega 3 (Objetivo 3): insights del informe de Power BI",
  styles: {
    default: { document: { run: { font: FUENTE, size: 22, color: INK } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: FUENTE, size: 56, bold: true, color: INK }, paragraph: { spacing: { before: 0, after: 160 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FUENTE, size: 32, bold: true, color: TEAL }, paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FUENTE, size: 25, bold: true, color: INK }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 1,
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: CORAL, space: 8 } } } },
    ],
  },
  numbering: { config: [{ reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  features: { updateFields: true },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      t("Insights del informe de Power BI · Entrega 3 · ", { size: 16, color: GRIS }), new TextRun({ children: [PageNumber.CURRENT], font: FUENTE, size: 16, color: GRIS })] })] }) },
    children: [...portada, ...indice, ...resumen, ...metodo, ...insights, ...gobierno, ...limites, ...anexo],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(SALIDA, buf); console.log("ok", SALIDA, buf.length, "bytes,", nFig, "figuras"); });
