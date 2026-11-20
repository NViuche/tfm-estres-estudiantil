// Guía de defensa del TFM (Word, A4 vertical), dividida en 5 partes, una por integrante.
// Uso: node guia_defensa.js <salida.docx>
// Las imágenes se leen de las carpetas de cada entrega (rutas relativas a este script).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, LevelFormat, BorderStyle, Footer, PageNumber, HeadingLevel, TableOfContents, VerticalAlign,
  ExternalHyperlink,
} = require("docx");

const [, , SALIDA] = process.argv;
// En el repositorio, las figuras se leen desde la raíz (3 niveles por encima de esta carpeta).
const ENTREGA = path.resolve(__dirname, "..", "..", "..");
const AZUL = "1F5C99", GRIS = "6B6B6B", TINTA = "222222", TEAL = "2E7D7A", CORAL = "B5523B";
const SERIF = "Times New Roman", SANS = "Arial";
const ANCHO = 9070; // A4 con márgenes de 2,5 cm
const URL_WEB = "https://claude.ai/artifact/7DuVNnNh38qLgELbcKAG8b";
const URL_REPO = "https://github.com/NViuche/tfm-estres-estudiantil";

// ------------------------------------------------------------------ piezas
const t = (text, o = {}) => new TextRun({ text, font: SERIF, size: 22, color: TINTA, ...o });
const b = (text, o = {}) => t(text, { bold: true, ...o });
const i = (text, o = {}) => t(text, { italics: true, ...o });
// Texto con **negritas** marcadas así
const md = (s, o = {}) => s.split(/(\*\*[^*]+\*\*|`[^`]+`)/).filter(Boolean).map((x) =>
  x.startsWith("**") ? b(x.slice(2, -2), o)
    : x.startsWith("`") ? t(x.slice(1, -1), { ...o, font: "Consolas", size: Math.round((o.size || 22) * 0.86) })
      : t(x, o));
const p = (s, o = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 276 }, children: typeof s === "string" ? md(s) : s, ...o });
const vi = (s, nivel = 0) => new Paragraph({ numbering: { reference: "vinetas", level: nivel }, spacing: { after: 60, line: 264 }, children: typeof s === "string" ? md(s) : s });
const num = (s, ref = "numeros") => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 60, line: 264 }, children: typeof s === "string" ? md(s) : s });
const h1 = (text, salto = true) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: salto, children: [new TextRun(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
const h3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
const enlace = (texto, url) => new ExternalHyperlink({ link: url, children: [t(texto, { color: AZUL, underline: {} })] });

// Recuadro de color (una celda) para mensajes clave, guion y transiciones
const caja = (titulo, contenido, fill = "E8F1F8", color = AZUL) => new Table({
  width: { size: ANCHO, type: WidthType.DXA }, columnWidths: [ANCHO],
  rows: [new TableRow({ cantSplit: true, children: [new TableCell({
    width: { size: ANCHO, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill },
    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      left: { style: BorderStyle.SINGLE, size: 24, color } },
    margins: { top: 100, bottom: 100, left: 200, right: 160 },
    children: [
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: titulo, font: SANS, size: 19, bold: true, color })] }),
      ...(Array.isArray(contenido) ? contenido : [contenido]).map((c) => typeof c === "string"
        ? new Paragraph({ spacing: { after: 60, line: 264 }, children: md(c, { size: 21 }) }) : c),
    ] })] })],
});
const espacio = () => new Paragraph({ spacing: { after: 80 }, children: [] });

// Tabla genérica: cabecera azul, columnas en DXA
const borde = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
const tabla = (cabecera, filas, cols, o = {}) => {
  const total = cols.reduce((a, c) => a + c, 0);
  const celda = (txt, n, extra = {}) => new TableCell({
    width: { size: cols[n], type: WidthType.DXA }, borders: bordes, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    shading: extra.fill ? { type: ShadingType.CLEAR, color: "auto", fill: extra.fill } : undefined,
    children: [new Paragraph({ spacing: { after: 0, line: 240 }, alignment: extra.centro ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: md(String(txt), { size: o.size || 18, color: extra.color || TINTA, bold: !!extra.negrita }) })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: cols,
    rows: [
      new TableRow({ tableHeader: true, children: cabecera.map((h, n) => celda(h, n, { fill: AZUL, color: "FFFFFF", negrita: true })) }),
      ...filas.map((f, k) => new TableRow({ cantSplit: true, children: f.map((x, n) => celda(x, n, {
        fill: (o.resaltar && o.resaltar(f)) || (k % 2 ? "F5F7FA" : undefined), negrita: o.primeraNegrita && n === 0,
        centro: o.centrar && o.centrar.includes(n) })) })),
    ],
  });
};
const nota = (s) => new Paragraph({ spacing: { before: 60, after: 160 }, children: [i(s, { size: 18, color: GRIS })] });

// Imagen PNG escalada al ancho indicado (en píxeles a 96 ppp)
const pngTam = (f) => { const x = fs.readFileSync(f); return { w: x.readUInt32BE(16), h: x.readUInt32BE(20) }; };
const imagen = (rel, ancho, pie) => {
  const f = path.join(ENTREGA, rel);
  if (!fs.existsSync(f)) return [p(`[Falta la imagen ${rel}]`)];
  const { w, h } = pngTam(f);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 40 },
      children: [new ImageRun({ type: "png", data: fs.readFileSync(f), transformation: { width: ancho, height: Math.round(ancho * h / w) } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [i(pie, { size: 18, color: GRIS })] }),
  ];
};

// Preguntas probables del tribunal: pregunta en negrita y respuesta debajo
const preguntas = (lista) => lista.flatMap(([q, r]) => [
  new Paragraph({ keepNext: true, spacing: { before: 100, after: 30 }, children: [new TextRun({ text: "P. " + q, font: SANS, size: 20, bold: true, color: TEAL })] }),
  new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { left: 280 }, spacing: { after: 80, line: 264 }, children: md("R. " + r) }),
]);

// Cabecera de cada parte: banda con número, título, integrante y tiempo
const portadaParte = (n, titulo, entrega, minutos, objetivo) => [
  new Paragraph({ pageBreakBefore: true, heading: HeadingLevel.HEADING_1, spacing: { after: 60 },
    children: [new TextRun(`Parte ${n}. ${titulo}`)] }),
  new Table({ width: { size: ANCHO, type: WidthType.DXA }, columnWidths: [3023, 3023, 3024], rows: [new TableRow({ children:
    [["Integrante", "______________________"], ["Corresponde a", entrega], ["Tiempo en la defensa", `${minutos} minutos`]].map(([k, v]) =>
      new TableCell({ width: { size: 3023, type: WidthType.DXA }, borders: bordes, shading: { type: ShadingType.CLEAR, color: "auto", fill: "F5F7FA" },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ spacing: { after: 0 }, children: [t(k, { size: 16, color: GRIS })] }),
          new Paragraph({ spacing: { after: 0 }, children: [b(v, { size: 20 })] })] })) })] }),
  espacio(),
  caja("Qué tiene que quedar claro al terminar esta parte", objetivo),
  espacio(),
];

// ------------------------------------------------------------------ contenido
const hoy = new Date().toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" });
const INTEGRANTES = ["Andrés Francisco García Grajales", "Obed Isaí Alvarado Núñez", "Roberto Mario Brochero López",
  "Raúl Cervantes Iglesias", "Santiago Nicolas Viuche Pinilla"];

const portada = [
  new Paragraph({ spacing: { before: 1800, after: 120 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "TRABAJO FINAL DE MÁSTER", font: SANS, size: 22, bold: true, color: GRIS })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [new TextRun({ text: "Guía del proyecto para la defensa", font: SANS, size: 48, bold: true, color: AZUL })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
    children: [i("Análisis multidimensional del estrés estudiantil mediante Business Analytics e Inteligencia Artificial con datos académicos, conductuales y textuales", { size: 26 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [b("Grupo LUHN", { size: 28, color: AZUL })] }),
  ...INTEGRANTES.map((n) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [t(n, { size: 23 })] })),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 40 }, children: [t("Máster en Business Analytics e Inteligencia Artificial", { size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [t("INESDI Business Techschool · UNIE", { size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [t(hoy, { size: 22, color: GRIS })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900 }, children: [i("Documento interno de estudio del grupo. No forma parte de la memoria entregable.", { size: 18, color: GRIS })] }),
];

const indice = [
  new Paragraph({ pageBreakBefore: true, spacing: { after: 200 }, children: [new TextRun({ text: "Contenido", font: SANS, size: 32, bold: true, color: AZUL })] }),
  new TableOfContents("Contenido", { hyperlink: true, headingStyleRange: "1-2" }),
  p("Si el índice aparece vacío al abrir el Word, haz clic derecho sobre él y elige «Actualizar campos».", { spacing: { before: 200 } }),
];

// ---------------- Cómo usar la guía
const comoUsar = [
  h1("Cómo usar esta guía"),
  p("Esta guía cuenta el proyecto completo en el orden en que se hizo: desde la elección de los datasets hasta el informe de Power BI en la nube. Está dividida en **cinco partes, una por integrante**, para que cada persona domine a fondo un tramo del proyecto y lo exponga en la defensa, pero conviene que **todo el grupo lea las cinco**: el tribunal puede preguntar cualquier cosa a cualquiera."),
  p("Cada parte sigue la misma estructura:"),
  vi("**Qué tiene que quedar claro:** la idea que el tribunal debe llevarse."),
  vi("**Qué se hizo, paso a paso:** el relato detallado, con las decisiones y su porqué."),
  vi("**Cifras para memorizar:** los números que hay que decir sin dudar."),
  vi("**Qué mostrar en pantalla:** la figura o la página del informe que apoya la explicación."),
  vi("**Preguntas probables del tribunal:** con una respuesta preparada."),
  vi("**Transición:** la frase que da paso a la siguiente parte."),
  h2("Requisitos de la defensa"),
  vi("**25 minutos** de exposición y después **15 minutos** de preguntas de un tribunal de 3 personas (dos docentes y la dirección del programa)."),
  vi("**Asistencia obligatoria** de los 5 integrantes, con **cámara y micrófono encendidos** toda la sesión, por la videoconferencia del aula TFM."),
  vi("La defensa vale el **20 %** de la nota: 10 % calidad de la exposición, ajuste al tiempo y material de apoyo, y 10 % respuesta a las preguntas. Si se pasan los 25 minutos, el tribunal puede cortar la presentación."),
  h2("Guion de tiempos propuesto"),
  tabla(["Bloque", "Contenido", "Minutos", "Quién"], [
    ["Apertura", "Presentación del grupo, el problema y el recorrido de la exposición", "1", "Parte 1"],
    ["Parte 1", "El problema, los objetivos y la elección de los datos", "4", "Integrante 1"],
    ["Parte 2", "Análisis exploratorio y calidad del dato (Entrega 1)", "4", "Integrante 2"],
    ["Parte 3", "Modelo de datos, retroalimentación del tutor, ETL y KPIs (Entregas 1 y 2)", "5", "Integrante 3"],
    ["Parte 4", "Modelado predictivo y NLP (Objetivo 2)", "5", "Integrante 4"],
    ["Parte 5", "Power BI, nube, servicio web e insights (Entrega 3)", "5", "Integrante 5"],
    ["Cierre", "Conclusiones, limitaciones y trabajo futuro", "1", "Parte 5"],
    ["**Total**", "", "**25**", ""],
  ], [1500, 4870, 1100, 1600], { centrar: [2] }),
  h2("Consejos para la exposición"),
  vi("**Ensayad con cronómetro:** mejor terminar en 23 minutos que pasarse; el margen absorbe los cambios de turno y cualquier problema técnico."),
  vi("Cada parte debe abrir con **una frase que diga qué problema resuelve** y cerrar con **una cifra o un hallazgo**."),
  vi("Hablad de **decisiones**, no solo de tareas: «elegimos X porque Y» demuestra dominio; «hicimos X» no."),
  vi("Reconoced las limitaciones antes de que las señale el tribunal: el proyecto las tiene documentadas, y eso es una fortaleza."),
  vi("Para la demostración del Power BI tened **plan B**: el PDF del informe y el servicio web abiertos en otra pestaña."),
  vi("Usad siempre las mismas cifras (anexo «Chuleta de cifras»). Un número distinto entre dos integrantes resta credibilidad."),
];

// ---------------- El proyecto en dos minutos
const resumen = [
  h1("El proyecto en dos minutos", false),
  p("**El problema.** El estrés estudiantil depende de factores académicos, conductuales, digitales y emocionales que casi nunca se miden juntos. Los datos públicos están dispersos: cada fuente recoge una faceta, con escalas, poblaciones y calidades distintas. Una sola fuente da una visión parcial."),
  p("**La propuesta.** Analizar el estrés desde **cuatro ángulos** a la vez, con **11 datasets públicos** (12 ficheros, porque Dreaddit viene en entrenamiento y prueba) organizados en cuatro bloques: factores internos, hábitos digitales, percepción emocional (texto) y validación psicológica (escalas clínicas). En total, **334.318 registros**."),
  p("**La idea central.** Las fuentes no comparten un identificador de persona, así que **no se fusionan**: cada una se analiza por separado (análisis en paralelo), pero todas se llevan a un **constructo común**, el nivel de estrés Bajo / Moderado / Alto, y a **dimensiones conformes** (género, rango de edad y nivel educativo). Así un mismo filtro, como «mujeres de 18 a 25 años», actúa sobre todas las fuentes."),
  p("**Los tres objetivos y lo que se obtuvo:**"),
  tabla(["Objetivo", "Qué se hizo", "Resultado principal"], [
    ["1. Análisis exploratorio y calidad", "EDA de los 12 ficheros, 49 reglas de calidad, diccionario de datos, modelo relacional en MySQL", "4 patrones transversales; 3 datasets detectados como sintéticos y excluidos del análisis"],
    ["2. Modelos de IA y NLP", "ETL y datawarehouse en estrella, 6 KPIs, 8 tareas de clasificación y NLP sobre texto de Reddit", "Señal real pero moderada: AUC de 0,73 a 0,84; el lenguaje delata el estrés"],
    ["3. Dashboards de BI", "Informe de Power BI de 11 páginas en local y en la nube (Supabase), servicio web público", "9 insights documentados; mismas cifras en MySQL, Supabase, Power BI y web"],
  ], [2300, 3700, 3070], { primeraNegrita: true }),
  ...imagen("docs/entrega3_objetivo3/sintesis/arquitectura.png", 590, "Figura 1. Recorrido de los datos: de los 12 CSV públicos a MySQL, y de ahí al Power BI local, a Supabase (Power BI en la nube y API) y al servicio web."),
  caja("Si solo pudiéramos decir una frase", "Combinando fuentes muy distintas en un mismo modelo de datos, mostramos que **la presión académica y el aislamiento** son el eje del estrés, que **el lenguaje lo delata**, y que **más estrés no lleva a pedir más ayuda**: lo que la mueve son los antecedentes familiares."),
];

// ---------------- Línea de tiempo
const lineaTiempo = [
  h1("Cómo se hizo: el recorrido completo"),
  p("El proyecto avanzó en fases que se apoyan unas en otras. Cada una tomó como base la anterior y se corrigió con la retroalimentación del tutor. Esta es la historia que cuentan, juntas, las cinco partes de la defensa:"),
  tabla(["Fase", "Qué se hizo", "Entregable", "Parte"], [
    ["Propuesta", "Tema, objetivos y tres datasets iniciales (estrés académico, redes sociales y sueño, Dreaddit)", "Plantilla de propuesta", "1"],
    ["Selección de datos", "Ampliación a 11 datasets en 4 bloques para cubrir el fenómeno desde cuatro ángulos", "Inventario de fuentes", "1"],
    ["Entrega 1 (a)", "Perfilado y análisis exploratorio con una plantilla común de 5 pasos; 49 reglas de calidad; diccionario de datos", "Notebooks 01-05, diccionario en Excel, síntesis", "2"],
    ["Entrega 1 (b)", "Modelo relacional en MySQL (v1, 15 tablas)", "SQL y diagrama ERD", "3"],
    ["Retroalimentación 1", "El tutor señala silos, claves poco legibles, falta de constructo común y riesgo de los sintéticos", "—", "3"],
    ["Corrección", "Modelo v2 (20 tablas), dimensiones conformes, constructo Bajo/Moderado/Alto, capa en estrella, carga de 334.318 registros", "Respuesta a la retroalimentación v3", "3"],
    ["Entrega 2", "ETL en Python (T1-T5), datawarehouse en estrella, 6 KPIs con histórico", "Notebook 08, KPIs en Word, síntesis", "3"],
    ["Objetivo 2", "8 tareas de clasificación y NLP, serialización de modelos y carga de resultados al DWH", "Notebook 09, síntesis del modelado", "4"],
    ["Retroalimentación 2", "El tutor valora la entrega como sobresaliente", "—", "4"],
    ["Entrega 3", "Power BI local y en la nube, servicio web, 9 insights, calidad y gobierno del dato", "Dos .pbix, Word de insights, síntesis", "5"],
  ], [1700, 4350, 2200, 820], { primeraNegrita: true, centrar: [3] }),
  nota("Todo el código, el SQL y la documentación están versionados en el repositorio público del proyecto en GitHub."),
];

// ---------------- PARTE 1
const parte1 = [
  ...portadaParte(1, "El problema, los objetivos y la elección de los datos", "Propuesta y selección de datos", 4 + 1,
    ["Que el estrés estudiantil es **multidimensional** y que por eso el proyecto combina **11 datasets de naturaleza distinta** en **4 bloques**.",
      "Que no se fusionan registros entre fuentes, sino que se **comparan a través de un constructo común**.",
      "Que **no todos los datos son fiables**: detectar 3 datasets sintéticos fue un resultado del proyecto."]),
  h2("1.1 Apertura (1 minuto)"),
  p("Presentar al grupo (Grupo LUHN, cinco integrantes), el título y el recorrido de la exposición: problema y datos → exploración y calidad → modelo de datos y KPIs → modelos de IA → Power BI e insights."),
  h2("1.2 El problema"),
  p("El estrés en estudiantes depende a la vez de la **presión académica**, del **entorno social**, de los **hábitos digitales** y del **estado emocional**. Cada estudio o encuesta pública mide solo una parte: unas usan escalas clínicas, otras preguntas de opinión, otras el texto que la gente escribe en redes. Si se analiza una sola fuente, se ve una parte del fenómeno."),
  p("La motivación del proyecto, tal como se planteó en la propuesta, es **comprender mejor qué factores influyen en el estrés** y **demostrar que combinar varias fuentes de datos da una visión más completa** para tomar decisiones (por ejemplo, en servicios de bienestar universitarios)."),
  h2("1.3 Los tres objetivos"),
  num("**Objetivo 1 — Análisis exploratorio y descriptivo** de los datasets por bloque, evaluando la calidad de cada fuente e identificando patrones entre variables académicas, conductuales y el nivel de estrés.", "obj"),
  num("**Objetivo 2 — Modelos de inteligencia artificial** para predecir el estrés y detectar patrones: clasificación sobre datos estructurados y procesamiento de lenguaje natural (NLP) sobre texto, con un análisis independiente por dataset.", "obj"),
  num("**Objetivo 3 — Dashboards de Business Intelligence** en Power BI que muestren los indicadores de cada bloque de forma comparativa e interactiva.", "obj"),
  h2("1.4 De tres datasets a once: la elección de los datos"),
  p("La propuesta inicial partía de **tres datasets** de naturaleza distinta: uno académico (Academic Stress), uno conductual (Social Media Usage vs Sleep, Stress & Productivity) y uno textual (Dreaddit, posts de Reddit). Al formular el Objetivo 1, el alcance se amplió a **cuatro bloques analíticos**, para mirar el mismo fenómeno desde cuatro ángulos complementarios:"),
  tabla(["Bloque", "Qué aporta", "Datasets"], [
    ["1. Factores internos", "Presión académica, ansiedad, salud mental y hábitos personales", "Academic Stress · Student Anxiety (GAD-7) · Student Mental Health Survey · Student Habits vs Performance*"],
    ["2. Hábitos digitales", "Uso de redes sociales, sueño y estilo de vida", "Social Media and Mental Health (SMMH) · Social Media / Sleep / Productivity* · Mental Health Lifestyle*"],
    ["3. Percepción emocional", "El estrés expresado en el lenguaje (texto) y un perfil de riesgo", "Dreaddit (entrenamiento y prueba) · Depression Student"],
    ["4. Validación psicológica", "Escalas clínicas validadas y búsqueda de ayuda", "DASS-42 · Mental Health Dataset"],
  ], [2000, 3000, 4070], { primeraNegrita: true }),
  nota("* Datasets que el análisis exploratorio identificó como sintéticos (ver 1.6)."),
  p("Todos los datasets son **públicos** (Kaggle y GitHub; los enlaces están en Documentacion y entrega\\Enlaces.txt). Al explicar la selección conviene destacar tres ideas: (1) **diversidad de naturaleza** — encuestas, escalas clínicas y texto libre; (2) **diversidad de tamaño** — desde 87 hasta 261.328 registros; (3) **relación directa con el malestar psicológico** en estudiantes o jóvenes, aunque no siempre en población estrictamente estudiantil (ver 1.7)."),
  h2("1.5 Inventario de las fuentes"),
  tabla(["Id", "Dataset (autor en Kaggle/GitHub)", "Bloque", "Registros", "Variable objetivo nativa", "Uso"], [
    ["1", "Academic Stress (poushal02)", "1", "140", "Índice de estrés 1-5", "Incluido"],
    ["2", "Student Anxiety GAD-7 (petalme)", "1", "13.464", "GAD-7 total 0-21", "Incluido"],
    ["3", "Mental Health Survey (abdullahashfaqvirk)", "1", "87", "Depresión 1-5", "Incluido"],
    ["4", "Student Habits vs Performance (abhi88377)", "1", "1.000", "Salud mental 1-10", "Excluido*"],
    ["5", "Social Media / Sleep / Productivity (jayjoshi37)", "2", "11.000", "Estrés en 3 niveles", "Excluido*"],
    ["6", "Social Media and Mental Health (souvikahmed071)", "2", "481", "Sentirse deprimido 1-5", "Incluido"],
    ["7", "Mental Health Lifestyle (datafit17)", "2", "3.000", "Estrés en 3 niveles", "Excluido*"],
    ["8-9", "Dreaddit, entrenamiento y prueba (payaldhokane)", "3", "2.834 + 715", "Etiqueta estrés 0/1", "Incluido"],
    ["10", "Depression Student (prajwalg26)", "3", "502", "Depresión Sí/No", "Incluido, con alerta"],
    ["11", "DASS-42 (lucasgreenwell)", "4", "39.767", "Subescala de estrés 14-56", "Incluido"],
    ["12", "Mental Health Dataset (chanchal24)", "4", "261.328", "Estrés creciente; tratamiento", "Incluido"],
    ["", "**Total**", "", "**334.318**", "", "9 incluidos"],
  ], [500, 3150, 750, 1150, 2120, 1400], { centrar: [0, 2, 3] }),
  nota("Dreaddit se cuenta como un dataset con dos ficheros (ids 8 y 9). El DASS-42 tenía 39.775 respuestas: se eliminaron 8 con edades imposibles. Dreaddit tenía 2.838 textos de entrenamiento: se excluyeron 4 corruptos («#NAME?»)."),
  h2("1.6 Datos reales y datos sintéticos"),
  p("Un resultado importante de la fase exploratoria fue detectar que **tres datasets son sintéticos**, es decir, generados por un programa y no recogidos de personas reales. Las pistas fueron:"),
  vi("**Distribuciones uniformes perfectas:** la salud mental de Student Habits se reparte igual en los 10 valores; las cinco condiciones de Mental Health Lifestyle tienen casi la misma frecuencia (≈ 570-630 cada una)."),
  vi("**Clases exactamente equilibradas:** en Social Media / Sleep, los tres niveles de estrés tienen ≈ 33 % cada uno, algo que no ocurre en poblaciones reales."),
  vi("**Correlaciones nulas** (entre −0,02 y +0,02) donde la evidencia clínica espera relación, por ejemplo entre sueño y estrés."),
  p("**Decisión:** se cargan en la base de datos (sirven como caso de estudio de calidad del dato y para la capa descriptiva), pero **se excluyen de todo el análisis y del modelado**. La política queda grabada en el propio modelo (columna `uso_modelado` = «excluido»), así que es auditable. Esta decisión responde además a una advertencia del tutor: entrenar modelos con datos sintéticos «resta validez científica»."),
  h2("1.7 Enfoque metodológico: análisis en paralelo con un constructo común"),
  p("Las fuentes **no comparten un identificador de persona**: no hay forma de saber que el autor de un post de Reddit es el mismo que respondió una encuesta. Por eso no se fusionan registros. En su lugar:"),
  vi("Cada dataset se analiza y se modela **por separado**, con su propia variable objetivo."),
  vi("Todas las variables objetivo se llevan a un **constructo común: el nivel de estrés Bajo / Moderado / Alto**, con un criterio explícito por fuente (por ejemplo, GAD-7 ≥ 10 es Alto; en el DASS-42, 40-56 es Alto)."),
  vi("Todas las fuentes comparten **dimensiones conformes**: género, rango de edad y nivel educativo, con un valor «No reportado» para las que no recogen el dato."),
  p("Ese diseño, que se detalla en la Parte 3, es lo que convierte once análisis sueltos en **un único análisis multidimensional**."),
  p("**Poblaciones:** no todas son estrictamente estudiantiles, y así se reconoce. Anxiety viene de jugadores online (se filtran los estudiantes: 9.302); el DASS-42 es población general (se usa la franja de 18-25 años como aproximación: 23.039); Mental Health Dataset se filtra a estudiantes (54.207); Dreaddit es texto de Reddit."),
  h2("Cifras para memorizar"),
  tabla(["Cifra", "Qué es"], [
    ["11 datasets · 12 ficheros", "Dreaddit viene en entrenamiento y prueba"],
    ["4 bloques", "Factores internos, hábitos digitales, percepción emocional, validación psicológica"],
    ["334.318", "Registros cargados en total"],
    ["319.318", "Registros de las 9 fuentes con señal real (sin los 15.000 sintéticos)"],
    ["3 sintéticos", "Student Habits, Social Media/Sleep y Mental Health Lifestyle"],
    ["Bajo / Moderado / Alto", "Constructo común de nivel de estrés"],
  ], [2700, 6370], { primeraNegrita: true }),
  h2("Qué mostrar en pantalla"),
  vi("Diapositiva con los 4 bloques y sus datasets (tabla 1.4)."),
  vi("Diagrama de arquitectura (Figura 1) para anticipar el recorrido."),
  vi("En el Power BI: página **9 Fuentes**, que muestra los 12 ficheros, su calidad, su uso y el criterio con que cada uno define Bajo / Moderado / Alto."),
  h2("Preguntas probables del tribunal"),
  ...preguntas([
    ["¿Por qué tantos datasets y no uno solo, más completo?", "Porque no existe una fuente pública que mida a la vez lo académico, lo digital, lo emocional y lo clínico. Cada bloque aporta un ángulo distinto del mismo fenómeno, y el valor del proyecto está en contrastarlos. Además, varias fuentes permiten comprobar si un patrón se repite (por ejemplo, la brecha de género aparece en 5 de 6 fuentes)."],
    ["¿Por qué no unir los datasets en una sola tabla?", "Porque no comparten identificador de persona: unir registros de distintas fuentes sería inventar relaciones. Se integran de forma correcta, por dimensiones comunes (género, edad, nivel educativo) y por un constructo común de nivel de estrés, sin mezclar personas."],
    ["¿Cómo supisteis que los tres datasets eran sintéticos?", "Por tres señales estadísticas: distribuciones uniformes perfectas, clases exactamente equilibradas y correlaciones prácticamente nulas (|r| ≤ 0,02) donde la literatura clínica espera relación, como entre sueño y estrés. No lo dice la fuente: lo detectamos nosotros en el análisis exploratorio."],
    ["Si son sintéticos, ¿por qué los cargasteis?", "Porque su detección es un resultado legítimo de calidad del dato y sirven para la capa descriptiva, siempre rotulados. Pero ninguna medida de análisis ni ningún modelo los usa: la exclusión está en la propia base de datos (uso_modelado = «excluido»)."],
    ["¿Son realmente estudiantes?", "No en todas las fuentes, y lo documentamos como limitación. Filtramos estudiantes donde la fuente lo permite (Anxiety, Mental Health Dataset), usamos la franja de 18-25 años como aproximación en el DASS-42, y advertimos que Dreaddit es texto de Reddit sobre temas sobre todo relacionales y clínicos."],
  ]),
  caja("Transición a la Parte 2", "«Con los datos elegidos, el primer paso fue entenderlos: ¿qué dice cada fuente y cuánto podemos fiarnos de ella? Eso es lo que hicimos en el análisis exploratorio y de calidad.»", "EAF4F3", TEAL),
];

// ---------------- PARTE 2
const parte2 = [
  ...portadaParte(2, "Análisis exploratorio y calidad del dato", "Entrega 1 · Objetivo 1", 4,
    ["Que el análisis exploratorio se hizo con **una misma plantilla en todas las fuentes**, para que los resultados sean comparables.",
      "Los **cuatro patrones** que aparecen en varias fuentes a la vez.",
      "Que la calidad del dato se trató como un **resultado**: **49 reglas** ejecutables, sin errores, y decisiones documentadas para cada incidencia."]),
  h2("2.1 Cómo se hizo: una plantilla común de cinco pasos"),
  p("Todo el análisis se programó en **Python** (pandas, matplotlib y seaborn), con un notebook por bloque y otro para las reglas de calidad. A cada dataset se le aplicó la misma plantilla:"),
  num("**Carga e inventario:** filas, columnas, tipos de variable y particularidades de lectura (codificación, separadores).", "pasos"),
  num("**Calidad de datos:** nulos, duplicados, valores anómalos y columnas redundantes, con una decisión documentada para cada incidencia.", "pasos"),
  num("**Análisis univariante:** distribución de la variable objetivo (estrés, depresión o ansiedad) y de las explicativas principales.", "pasos"),
  num("**Análisis bivariante:** correlaciones de Pearson y tablas de contingencia frente a la variable de malestar.", "pasos"),
  num("**Síntesis:** de tres a cinco conclusiones por dataset, incluida su calidad y su valor explicativo.", "pasos"),
  p("Para el texto de Dreaddit, los pasos 3 y 4 se adaptaron: equilibrio de clases, longitud de los posts, subreddit de origen y comparación de señales del lenguaje (sentimiento y categorías del diccionario psicolingüístico **LIWC**) entre posts con y sin estrés."),
  tabla(["Notebook", "Contenido"], [
    ["01 · Bloque 1", "EDA de 4 datasets de factores internos (4 figuras)"],
    ["02 · Bloque 2", "EDA de 3 datasets de hábitos digitales (3 figuras)"],
    ["03 · Bloque 3", "EDA textual de Dreaddit y perfil de Depression Student (3 figuras)"],
    ["04 · Bloque 4", "Subescalas del DASS-42 según su manual oficial, desglose demográfico y búsqueda de tratamiento (3 figuras)"],
    ["05 · Reglas de calidad", "49 reglas como código, con estado OK / AVISO / ERROR y acción correctiva; exporta el resultado a CSV"],
  ], [2300, 6770], { primeraNegrita: true }),
  h2("2.2 Hallazgos por bloque"),
  h3("Bloque 1 — Factores internos"),
  vi("**Academic Stress (140):** más del 60 % se sitúa en los niveles de estrés 4-5; la mediana es 4 en todas las etapas educativas."),
  vi("**Anxiety GAD-7 (9.302 estudiantes):** la ansiedad se relaciona con menos satisfacción vital (r = −0,40) y más ansiedad social (r = +0,44), un patrón coherente con la literatura clínica."),
  vi("**Mental Health Survey (87):** el **aislamiento social** es el predictor más fuerte de la depresión de todo el proyecto (**r = 0,71**), seguido de la inseguridad ante el futuro (0,47) y la carga académica (0,38)."),
  vi("**Student Habits (1.000):** salud mental con distribución uniforme perfecta → sintético."),
  h3("Bloque 2 — Hábitos digitales"),
  vi("**SMMH (481):** no importa cuánto tiempo se pasa en redes, sino **cómo se usan**: preocupación (r = 0,59), dificultad de concentración (0,51), comparación social (0,42)."),
  vi("**Social Media/Sleep (11.000)** y **Lifestyle (3.000):** correlaciones ≈ 0 y clases equilibradas → sintéticos."),
  ...imagen("figuras/eda/b2_2_smmh_corr.png", 470, "Figura 2. SMMH: correlación de cada comportamiento digital con «sentirse deprimido/a». Manda el patrón de uso ansioso, no el tiempo."),
  h3("Bloque 3 — Percepción emocional"),
  vi("**Dreaddit (2.838 + 715 textos):** clases casi equilibradas (1.488 con estrés, 1.350 sin estrés). Los posts con estrés usan **2,5 veces más vocabulario de ansiedad** (LIWC 1,28 frente a 0,51) y tienen un tono más negativo (sentimiento −0,02 frente a +0,10)."),
  vi("**Depression Student (502):** el 73 % de quienes reportan pensamientos suicidas presenta depresión, frente al 26 % de quienes no; la presión académica es un 57 % mayor en el grupo con depresión."),
  h3("Bloque 4 — Validación psicológica"),
  vi("**DASS-42 (23.039 de 18-25 años):** medias de 35,0 en depresión, 30,4 en ansiedad y 35,2 en estrés (escala 14-56), es decir, malestar moderado-alto. Las mujeres puntúan más en ansiedad (31,0 frente a 28,1) y a menor nivel educativo, más malestar."),
  vi("**Mental Health Dataset (54.207 estudiantes):** buscar tratamiento **no depende del estrés** (48-51 % en todos los niveles), pero **sí de los antecedentes familiares** (72,4 % frente a 35,1 %)."),
  h2("2.3 Los cuatro patrones transversales"),
  p("El análisis en paralelo permitió encontrar patrones que se repiten en varias fuentes, sin necesidad de fusionarlas:"),
  tabla(["Patrón", "Evidencia"], [
    ["1. La presión académica es el eje del estrés", "Más del 60 % en niveles altos (Bloque 1); +57 % de presión en el grupo con depresión (Bloque 3); malestar moderado-alto en una escala clínica (Bloque 4)"],
    ["2. El aislamiento y el uso ansioso de redes median el malestar", "Aislamiento r = 0,71 (Bloque 1); preocupación r = 0,59 y comparación social r = 0,42 (Bloque 2)"],
    ["3. El lenguaje refleja el estrés", "2,5 veces más vocabulario de ansiedad y tono más negativo en los posts con estrés (Bloque 3)"],
    ["4. Hay una brecha entre malestar y búsqueda de ayuda", "Más estrés no aumenta la búsqueda de tratamiento; los antecedentes familiares la duplican (Bloque 4)"],
  ], [3300, 5770], { primeraNegrita: true }),
  caja("La historia que cuentan los cuatro patrones", "La presión académica genera malestar, que **se expresa en el lenguaje**, **se agrava con el aislamiento** y el uso problemático de redes, y **rara vez termina en una petición de ayuda**. De ahí el valor práctico del proyecto: detectar el estrés por vías indirectas (como el lenguaje) puede llegar donde la persona no pide ayuda."),
  espacio(),
  h2("2.4 Calidad del dato: 49 reglas"),
  p("Las incidencias del análisis exploratorio se convirtieron en **49 reglas de calidad ejecutables** en Python. Cada regla informa cuántos registros evalúa, cuántos incumplen, el porcentaje, el estado y la acción correctiva. Resultado: **39 reglas superadas, 10 avisos documentados y 0 errores**."),
  p("Las reglas encontraron dos problemas que el análisis exploratorio no había visto, ambos en Dreaddit: **4 textos corruptos** que decían literalmente «#NAME?» (un error de Excel heredado de la fuente), que se excluyen, y que los ficheros de entrenamiento y prueba tenían **las mismas 116 columnas en distinto orden**, lo que obliga a alinearlas por nombre."),
  tabla(["Dataset", "Incidencia", "Decisión"], [
    ["Anxiety", "Codificación latin1; población de jugadores online", "Lectura con latin1; filtro a estudiantes documentado"],
    ["Student Habits", "9,1 % de nulos en estudios de los padres; señal sintética", "Uso restringido a validación técnica"],
    ["Lifestyle", "19,8 % de nulos en la condición de salud mental", "Recodificados como «Ninguna»; uso técnico"],
    ["Dreaddit", "4 textos «#NAME?»; columnas en distinto orden", "Excluir los 4 textos (regla R7); alinear por nombre (R6)"],
    ["DASS-42", "Edades imposibles; separador tabulador", "Filtro 13-90 años (8 registros fuera); subescalas según el manual oficial"],
    ["Mental Health Dataset", "Columna duplicada; nulos en autoempleo", "Columna eliminada; filtro a estudiantes"],
  ], [2000, 3600, 3470], { primeraNegrita: true }),
  h2("2.5 Diccionario de datos"),
  p("Un Excel con **13 hojas**: un índice con el inventario de las fuentes (bloque, filas, columnas, nulos, duplicados, descripción) y una hoja por dataset con cada columna: tipo, nulos, valores únicos, mínimo, máximo, media, valores más frecuentes, significado y regla de calidad que la vigila. Las 172 columnas del DASS-42 y las 116 de Dreaddit quedan todas documentadas."),
  h2("Cifras para memorizar"),
  tabla(["Cifra", "Qué es"], [
    ["r = 0,71", "Aislamiento social y depresión: el predictor más fuerte del proyecto"],
    ["r = 0,59", "Preocupación y sentirse deprimido en redes sociales (patrón de uso)"],
    ["× 2,5", "Vocabulario de ansiedad en posts con estrés frente a sin estrés"],
    ["72 % frente a 35 %", "Búsqueda de tratamiento con y sin antecedentes familiares"],
    ["48-51 %", "Búsqueda de tratamiento en cualquier nivel de estrés (no cambia)"],
    ["49 reglas · 39 OK · 10 avisos · 0 errores", "Resultado de la calidad del dato"],
    ["13 hojas", "Diccionario de datos"],
  ], [3000, 6070], { primeraNegrita: true }),
  h2("Qué mostrar en pantalla"),
  vi("La figura de SMMH (Figura 2) o la de señales de Dreaddit, para ilustrar los patrones 2 y 3."),
  vi("La tabla de los cuatro patrones transversales."),
  vi("En el Power BI: página **8 Calidad** (reglas por dimensión y estado, completitud por dataset)."),
  h2("Preguntas probables del tribunal"),
  ...preguntas([
    ["¿Correlación implica causalidad? ¿Podéis decir que el aislamiento causa depresión?", "No. Son asociaciones en datos transversales, y así se presentan. Lo que sí podemos decir es que el patrón aparece de forma consistente en varias fuentes, lo que lo hace más robusto que un resultado aislado."],
    ["¿Qué es una regla de calidad? Poned un ejemplo.", "Una comprobación automática sobre los datos con un estado y una acción. Por ejemplo, R7 detecta los textos de Dreaddit que son «#NAME?» y los excluye; otra comprueba que la edad esté entre 13 y 90 años; otra acota las horas de juego a 112 por semana."],
    ["¿Por qué Pearson con escalas Likert?", "Para una primera exploración homogénea en todas las fuentes, tratando las escalas de 1 a 5 como ordinales aproximadamente continuas. Para las categóricas usamos tablas de contingencia. Los modelos del Objetivo 2 no dependen de ese supuesto."],
    ["¿Cuál es el hallazgo más relevante del análisis exploratorio?", "La brecha entre malestar y ayuda: tener más estrés no hace que se busque más tratamiento, pero tener antecedentes familiares lo duplica. Sugiere una barrera de acceso o estigma, y tiene implicaciones prácticas directas."],
    ["Si había avisos, ¿por qué decís que la calidad es buena?", "Porque ninguna regla dio error, y los 10 avisos son incidencias conocidas con un tratamiento decidido (por ejemplo, nulos que se recodifican o registros que se excluyen). La limitación real es otra: la completitud demográfica, que se trata en la Parte 3."],
  ]),
  caja("Transición a la Parte 3", "«Entender cada fuente por separado no basta: había que poder analizarlas juntas. Para eso diseñamos el modelo de datos, que además tuvimos que rehacer tras la retroalimentación del tutor.»", "EAF4F3", TEAL),
];

// ---------------- PARTE 3
const parte3 = [
  ...portadaParte(3, "Modelo de datos, retroalimentación, ETL y KPIs", "Entregas 1 y 2", 5,
    ["Cómo la **retroalimentación del tutor** transformó un modelo de silos en un modelo **integrado con dimensiones conformes**.",
      "Que gracias a ello un filtro como **«mujeres de 18 a 25 años con estrés Alto»** funciona sobre todas las fuentes a la vez.",
      "Que el **datawarehouse** y los **6 KPIs** se calculan con un ETL reproducible y con histórico."]),
  h2("3.1 Primer modelo relacional (v1)"),
  p("En la Entrega 1 la base de datos se implementó en **MySQL** (XAMPP, MariaDB y phpMyAdmin) con **15 tablas**: tres dimensiones de metadatos (bloque, dataset y subreddit) y una tabla de hechos por dataset. Dos decisiones de diseño: Dreaddit entrenamiento y prueba comparten tabla (con un campo de partición) y el DASS-42 se normaliza en dos tablas, respondente e ítem, con relación 1 a N. Las reglas de calidad pasaron al modelo como restricciones (CHECK y ENUM)."),
  p("Siguiendo el enfoque en paralelo, las tablas de hechos **solo se relacionaban con las dimensiones de metadatos**."),
  h2("3.2 La retroalimentación del tutor"),
  p("El tutor valoró la ambición del proyecto, pero señaló problemas serios de arquitectura:"),
  tabla(["Observación del tutor", "Qué significaba"], [
    ["Claves llamadas registro_id, poco legibles", "Los identificadores no decían qué entidad representaban"],
    ["Hechos vinculados solo a dimensiones de metadatos: «silos insalvables»", "Sin dimensiones comunes, «en Power BI será imposible aplicar un filtro global de Mujeres de 18 a 25 años»"],
    ["Riesgo de que el TFM se fragmente en 4 o 5 mini-proyectos", "Faltaba una arquitectura que explicara cómo conviven las fuentes"],
    ["Falta un planteamiento de qué se mide en la capa global", "Cada fuente tenía su propia escala de estrés"],
    ["Los datos sintéticos restan validez científica al modelado", "No se pueden usar para entrenar modelos"],
  ], [4200, 4870]),
  h2("3.3 La respuesta: modelo v2"),
  tabla(["Cambio", "Cómo se resolvió"], [
    ["Claves legibles", "Cada clave describe su entidad: id_encuesta_estres, id_respondente_dass, id_fragmento_post…"],
    ["Dimensiones conformes", "dim_genero, dim_rango_edad, dim_nivel_educativo y dim_nivel_estres, compartidas por las 12 tablas de hechos con claves foráneas reales. Un miembro «No reportado» (id 0) para las fuentes sin el dato, sin nulos"],
    ["Constructo común", "dim_nivel_estres (Bajo / Moderado / Alto) y la tabla de gobierno dim_mapeo_estres, que documenta el criterio de cada fuente"],
    ["Política de sintéticos", "Columna uso_modelado en dim_dataset: incluido / excluido, consultable y auditable"],
    ["Capa de consumo en estrella", "6 vistas que aplanan el modelo para Power BI: una tabla de hechos única (vw_hechos_estres, 334.318 filas) y 5 dimensiones"],
  ], [2300, 6770], { primeraNegrita: true }),
  p("El modelo v2 tiene **20 tablas: 8 dimensiones y 12 tablas de hechos**. El resultado es una arquitectura **hub-and-spoke** (centro y radios): cada fuente conserva su detalle, pero todas convergen en las mismas dimensiones y en el mismo constructo."),
  h3("Cómo se lleva cada fuente al nivel Bajo / Moderado / Alto"),
  tabla(["Fuente", "Variable nativa", "Criterio"], [
    ["Academic Stress", "Índice 1-5", "1-2 Bajo · 3 Moderado · 4-5 Alto"],
    ["Anxiety", "GAD-7 (0-21)", "0-4 · 5-9 · 10-21 (umbrales clínicos)"],
    ["MH Survey / SMMH", "Likert 1-5", "1-2 · 3 · 4-5"],
    ["Dreaddit", "Etiqueta 0/1", "0 Bajo · 1 Alto (etiquetado manual)"],
    ["Depression Student", "Sí / No", "No Bajo · Sí Alto"],
    ["DASS-42", "Estrés (14-56)", "14-28 · 29-39 · 40-56 (baremos DASS)"],
    ["Mental Health Dataset", "Estrés creciente", "No Bajo · Quizá Moderado · Sí Alto"],
  ], [2700, 2500, 3870], { primeraNegrita: true }),
  h3("La prueba: el filtro que el tutor decía imposible"),
  p("Con los datos cargados, una sola consulta sobre la vista de hechos devuelve las **mujeres de 18 a 25 años con estrés Alto en 7 fuentes de los 4 bloques: 7.446 casos** (6.799 de ellos del DASS-42). Las fuentes que faltan lo hacen por una razón documentada: Dreaddit es anónimo y el Mental Health Dataset no registra la edad."),
  ...imagen("figuras/diagramas/corregidos/esquema_estrella_powerbi_ERD.png", 560, "Figura 3. Capa de consumo en estrella: una tabla de hechos con los 12 ficheros y las dimensiones conformes compartidas."),
  h2("3.4 Ingesta: 334.318 registros"),
  p("El notebook 07 lee los 12 CSV, calcula fila a fila las claves de las dimensiones conformes (armonizando, por ejemplo, el género escrito en inglés, en códigos 1/2/3 o en texto libre), aplica las reglas de calidad y carga **334.318 registros**. Quitando los 15.000 de los sintéticos quedan **319.318**, la cifra base de todo el análisis."),
  h2("3.5 ETL y datawarehouse (Entrega 2)"),
  p("El notebook 08 lee de MySQL, transforma con pandas y escribe en **tablas nuevas del datawarehouse**. Al empezar vacía sus tablas, así que se puede relanzar sin duplicar datos. Son cinco transformaciones de tipos distintos:"),
  tabla(["#", "Transformación", "Tipo", "Filas", "Resultado destacado"], [
    ["T1", "Registros de las 9 fuentes reales", "Integración", "319.318", "La validación psicológica aporta el 94 % del volumen"],
    ["T2", "Prevalencia por bloque × género × edad", "Agregación", "49", "Estrés Alto entre 14,7 % y 52,3 % en los grupos grandes"],
    ["T3", "Señales del lenguaje por subreddit", "Resumen estadístico", "20", "En los 10 subreddits, más ansiedad y peor tono con estrés"],
    ["T4", "DASS 18-25 por género × estudios", "Pivote + umbral clínico", "12", "«Otro» con secundaria: 50 % en estrés severo"],
    ["T5", "Tratamiento por estrés × antecedentes", "Contingencia", "6", "≈ 35 % sin antecedentes frente a ≈ 72 % con ellos"],
  ], [500, 2900, 1700, 900, 3070], { centrar: [0, 3] }),
  p("El datawarehouse es un **esquema en estrella**: sus tablas de hechos solo guardan claves hacia las mismas dimensiones conformes y sus medidas. Las claves foráneas son restricciones reales de MySQL, así que no puede haber registros huérfanos (el notebook comprueba **14 relaciones con 0 huérfanos**)."),
  ...imagen("figuras/diagramas/corregidos/dwh_estrella_ERD.png", 590, "Figura 4. Datawarehouse en estrella de la Entrega 2."),
  h2("3.6 Los 6 KPIs"),
  p("Se calculan en Python y se guardan en `dwh_kpi_resultados` con su fecha: **cada ejecución añade una fila por KPI, nunca se sobrescribe**. Así hay histórico y trazabilidad (el tutor lo valoró en la Entrega 2). La definición de cada uno está en `dwh_kpi_catalogo` y en el Word de KPIs."),
  tabla(["KPI", "Valor", "Lectura"], [
    ["1. Tasa de estrés Alto global", "33,68 %", "Uno de cada tres registros está en estrés Alto"],
    ["2. Brecha de género en ansiedad (DASS, 18-25)", "2,89 puntos", "Mujeres 31,0 frente a hombres 28,1"],
    ["3. Índice de riesgo crítico", "72,69 %", "Con pensamientos suicidas, el 73 % presenta depresión (con nota de validez: Depression Student)"],
    ["4. Tasa de búsqueda de tratamiento", "49,41 %", "La mitad ha buscado tratamiento"],
    ["5. Poder discriminante LIWC", "2,58", "2,6 veces más vocabulario de ansiedad en textos con estrés"],
    ["6. Cobertura demográfica", "17,01 %", "Solo el 17 % de los registros tiene género y edad a la vez"],
  ], [3500, 1300, 4270], { primeraNegrita: true, centrar: [1] }),
  h2("Cifras para memorizar"),
  tabla(["Cifra", "Qué es"], [
    ["15 → 20 tablas", "Modelo v1 y modelo v2 (8 dimensiones + 12 hechos)"],
    ["4 dimensiones conformes", "Género, rango de edad, nivel educativo y nivel de estrés"],
    ["7.446", "Mujeres de 18-25 años con estrés Alto, en 7 fuentes, con una sola consulta"],
    ["334.318 → 319.318", "Registros cargados y registros de las fuentes reales"],
    ["T1-T5 · 14 relaciones · 0 huérfanos", "ETL y comprobación de integridad"],
    ["33,68 % · 17 %", "KPI de estrés Alto y KPI de cobertura demográfica"],
  ], [3200, 5870], { primeraNegrita: true }),
  h2("Qué mostrar en pantalla"),
  vi("Antes y después: diagrama del modelo v1 junto al de la capa en estrella (Figura 3)."),
  vi("La tabla de criterios Bajo / Moderado / Alto."),
  vi("En el Power BI: aplicar en vivo el filtro **Femenino + 18-25** con los segmentadores y ver cómo cambian todas las páginas; página **6 KPIs** con el histórico."),
  h2("Preguntas probables del tribunal"),
  ...preguntas([
    ["¿Qué es una dimensión conforme?", "Una dimensión que comparten varias tablas de hechos con el mismo significado y los mismos valores. Como todas las fuentes apuntan a la misma tabla de género, de edad y de nivel educativo, un filtro sobre ellas actúa a la vez sobre todas."],
    ["¿Para qué sirve el valor «No reportado»?", "Para que las fuentes que no recogen un dato (Dreaddit es anónimo, el Mental Health Dataset no tiene edad) puedan conformarse igual, sin nulos en las claves foráneas. Además, su porcentaje mide la cobertura real de cada dimensión."],
    ["¿Cómo comparáis el estrés si cada fuente lo mide distinto?", "Con un constructo común de tres niveles y un criterio explícito por fuente, basado en baremos clínicos cuando existen (GAD-7, DASS). Está documentado en la tabla dim_mapeo_estres. Por eso comparamos tendencias dentro de cada fuente y no niveles absolutos entre fuentes."],
    ["¿Por qué vistas para la estrella y no tablas nuevas?", "Porque la base de datos conserva su normalización (correcta para almacenar) y las vistas la aplanan para el consumo analítico sin duplicar datos. Power BI trabaja mejor con una estrella que con un copo de nieve."],
    ["¿Por qué la cobertura demográfica es solo del 17 %?", "Porque es exigente: cuenta los registros con género y edad a la vez, y la fuente más grande (Mental Health Dataset, 261.328) no registra la edad, y Dreaddit es anónimo. Es un KPI de calidad que advierte del alcance de los filtros demográficos."],
    ["¿Qué aporta guardar el histórico de los KPIs?", "Trazabilidad: cada ejecución del ETL queda registrada con su fecha. Las tres ejecuciones dan los mismos valores, lo que demuestra que el cálculo es reproducible; y con datos nuevos permitiría seguir la evolución."],
  ]),
  caja("Transición a la Parte 4", "«Con los datos integrados y los indicadores calculados, la siguiente pregunta era si se puede anticipar el estrés: ¿qué capacidad predictiva tienen estos datos?»", "EAF4F3", TEAL),
];

// ---------------- PARTE 4
const parte4 = [
  ...portadaParte(4, "Modelado predictivo y procesamiento del lenguaje", "Objetivo 2 (notebook 09)", 5,
    ["Que se modeló **con rigor**: métrica adecuada (AUC), comparación con un baseline, prevención de fugas de datos y sin sintéticos.",
      "Que hay **señal predictiva real pero moderada** (AUC 0,73-0,84) y que **un modelo simple basta**.",
      "Que un resultado **demasiado perfecto** (Depression Student) se trató como una **alerta**, no como un éxito."]),
  h2("4.1 Integración con el modelo de datos"),
  p("Cada dataset se modela por separado, pero el modelado está conectado con la estrella en tres puntos: (1) **la política se lee de la base de datos**: el notebook consulta `uso_modelado` y solo modela las fuentes «incluido»; (2) **los resultados vuelven al datawarehouse** (`dwh_modelo_resultados`); y (3) esa tabla es una **segunda tabla de hechos** que comparte la dimensión de dataset con los registros (una **constelación**), de modo que en Power BI un mismo filtro actúa sobre registros y modelos."),
  h2("4.2 Diseño metodológico"),
  tabla(["Decisión", "Qué se hizo", "Por qué"], [
    ["Fuentes", "9 fuentes «incluido» → 8 tareas (Dreaddit entrenamiento y prueba son una)", "Los sintéticos restan validez científica"],
    ["Algoritmos", "Baseline, Regresión Logística, Random Forest y XGBoost. En texto, además TF-IDF con Regresión Logística, SVM y Naive Bayes, y un híbrido con LIWC", "Del más simple al más complejo, para ver si la complejidad aporta"],
    ["Evaluación", "Menos de 1.000 filas: validación cruzada estratificada 5×3 (15 evaluaciones). 1.000 o más: hold-out 80/20. Dreaddit: su partición original", "Con 87 filas, una única partición es inestable"],
    ["Métrica principal", "AUC; F1 y Accuracy siempre frente al baseline", "El Accuracy engaña con clases desequilibradas"],
    ["Fuga de datos", "Fuera las variables que construyen el objetivo: ítems GAD-7 y DASS, «anxiety» en MH Survey, confidence y subreddit en Dreaddit", "Evita resultados triviales"],
    ["Ética", "Religión, orientación sexual y raza no se usan como predictores", "No modelar atributos sensibles"],
    ["Industrialización", "Pipeline completo (preprocesado + modelo) guardado en .pkl con su metadata", "Se puede puntuar datos nuevos sin reentrenar"],
  ], [1800, 4500, 2770], { primeraNegrita: true }),
  h3("Cómo leer las métricas"),
  vi("**AUC:** probabilidad de que el modelo puntúe más alto un caso positivo que uno negativo. 0,5 es el azar; 1, la separación perfecta."),
  vi("**F1:** equilibrio entre precisión y exhaustividad de la clase de interés."),
  vi("**Baseline:** predecir siempre la clase más frecuente. Es el suelo que cualquier modelo debe superar."),
  vi("**Brecha:** accuracy de entrenamiento menos accuracy de prueba. Por encima de ≈ 0,15 indica sobreajuste."),
  h2("4.3 Feature engineering"),
  p("En cada fuente se crearon variables derivadas con sentido de negocio, por ejemplo: `presion_total` (pares + hogar + competencia) en Academic Stress; `bienestar` (satisfacción − aislamiento) en MH Survey; `uso_ansioso` e `impacto_social` en SMMH; las cinco dimensiones de personalidad **Big Five** a partir del test TIPI en el DASS-42; `vulnerabilidad` (antecedentes + historial) en Mental Health Dataset. Varias de ellas quedaron entre las variables más importantes de su modelo."),
  h2("4.4 Resultados por fuente"),
  tabla(["Fuente", "Mejor modelo", "Accuracy", "Baseline", "AUC", "Brecha"], [
    ["Depression Student ⚠", "Regresión Logística", "0,979", "0,502", "0,998", "0,012"],
    ["Dreaddit (texto)", "Híbrido TF-IDF + LIWC", "0,748", "0,516", "0,838", "0,085"],
    ["SMMH", "Random Forest", "0,741", "0,540", "0,793", "0,233"],
    ["MH Survey", "XGBoost", "0,621", "0,448", "0,789", "0,379"],
    ["Mental Health Dataset", "XGBoost", "0,718", "0,506", "0,769", "−0,004"],
    ["Anxiety GAD-7", "Regresión Logística", "0,730", "0,827", "0,764", "0,004"],
    ["DASS-42", "XGBoost", "0,579", "0,357", "0,762", "0,032"],
    ["Academic Stress ⚠", "Random Forest", "0,395", "0,400", "0,730", "0,433"],
  ], [2300, 2300, 1100, 1100, 1100, 1170], { primeraNegrita: true, centrar: [2, 3, 4, 5], resaltar: (f) => f[0].includes("⚠") ? "FBEAE6" : undefined }),
  nota("⚠ Fuentes con alerta: Depression Student (resultado demasiado perfecto) y Academic Stress (140 registros, sobreajuste fuerte)."),
  ...imagen("figuras/modelado/resumen_auc_por_dataset.png", 520, "Figura 5. AUC del mejor modelo por fuente."),
  h3("Lo que dicen los modelos (y confirma el Objetivo 1)"),
  vi("**Anxiety:** la trampa del Accuracy. El baseline acierta el 83 % sin detectar un solo caso (F1 = 0). La Regresión Logística logra F1 0,45 y AUC 0,76 sin sobreajuste: **gana el modelo más simple**. Pesan la ansiedad social y la satisfacción vital."),
  vi("**MH Survey:** el aislamiento es la variable más importante, y `bienestar` la segunda."),
  vi("**SMMH:** ni el tiempo diario ni las plataformas están entre las variables principales: **importa el patrón de uso, no cuánto**."),
  vi("**DASS-42:** solo con perfil y personalidad, AUC 0,76; la **estabilidad emocional** pesa el triple que cualquier otro rasgo."),
  vi("**Mental Health Dataset:** los **antecedentes familiares** encabezan la importancia y el estrés creciente no aparece entre las primeras: el modelo reproduce la brecha de ayuda."),
  h2("4.5 NLP: detectar el estrés en el texto"),
  p("Sobre Dreaddit (2.834 textos de entrenamiento y 715 de prueba) se compararon tres enfoques: las **105 variables psicolingüísticas** ya calculadas (LIWC, afecto, legibilidad, sentimiento), **TF-IDF** de palabras y pares de palabras con tres clasificadores, y un **híbrido**. No se eliminaron las palabras vacías porque los pronombres («I», «me») son señal de estrés."),
  vi("Los tres enfoques rinden parecido: **AUC 0,82-0,84** frente a 0,50 del azar; el híbrido es el mejor (0,838), pero las diferencias de 0,01 no son concluyentes con 715 textos."),
  vi("El modelo detecta el **78 %** de los textos con estrés y descarta bien el 71 % de los que no lo tienen."),
  vi("Las palabras que más empujan hacia «estrés» son **me, my, feel, because, just, am**: lenguaje centrado en uno mismo, un marcador clásico de rumiación."),
  vi("**Despliegue:** LIWC es un diccionario con licencia, así que el mejor modelo no puede usarse sobre texto nuevo. Por eso se guardó también un modelo **solo con el texto** (TF-IDF + Regresión Logística, AUC 0,82)."),
  h2("4.6 La alerta: un resultado demasiado perfecto"),
  p("En Depression Student la Regresión Logística obtiene **AUC 0,998** y 98 % de acierto, algo no creíble en datos de encuesta. Para distinguir entre una fuga de datos y otra causa, se midió el AUC de cada variable por separado: **ninguna pasa de 0,77** (la presión académica), un árbol de profundidad 2 llega a 0,83 y uno de profundidad 4 a 0,90. Es decir, ninguna columna delata la etiqueta, pero **una combinación lineal la reproduce casi sin error**: el patrón típico de una etiqueta generada por una fórmula."),
  p("**Decisión:** no se afirma que el dataset sea sintético, pero se reporta **con cautela** y no se usa como evidencia sustantiva; queda marcado como alerta en el informe. Excluirlo solo requiere un cambio en la base de datos (uso_modelado = «excluido»), que se propaga a la estrella, a Power BI y al notebook. **Esta decisión está pendiente de cerrar con el tutor; revisad qué se decidió antes de la defensa.**"),
  h2("4.7 Conclusiones del modelado"),
  vi("**Señal real pero moderada:** AUC entre 0,73 y 0,84 en las fuentes fiables. Se puede anticipar el estrés mejor que el azar, no predecirlo con precisión individual."),
  vi("**Ningún algoritmo domina:** XGBoost gana 3 tareas, la Regresión Logística 3 y Random Forest 2, muchas veces dentro del ruido. La Regresión Logística queda a menos de 0,015 de AUC del mejor en todas y es la que menos sobreajusta en 7 de 8."),
  vi("**Un resultado demasiado bueno es una alerta**, no un éxito."),
  vi("**Limitaciones:** tres tareas con menos de 600 registros; poblaciones no siempre estudiantiles; sin deep learning, búsqueda de hiperparámetros ni ajuste de umbrales; **modelos de investigación, no de diagnóstico clínico**."),
  h2("Cifras para memorizar"),
  tabla(["Cifra", "Qué es"], [
    ["8 tareas · 9 fuentes", "Dreaddit entrenamiento y prueba forman una tarea"],
    ["AUC 0,73-0,84", "Rango del mejor modelo en las fuentes fiables"],
    ["0,786", "AUC medio sin las 2 fuentes con alerta"],
    ["0,838 · 0,82", "NLP: modelo híbrido · modelo solo texto"],
    ["0,998", "Depression Student: demasiado perfecto → alerta"],
    ["< 0,015", "Distancia de la Regresión Logística al mejor modelo"],
  ], [2700, 6370], { primeraNegrita: true }),
  h2("Qué mostrar en pantalla"),
  vi("La tabla de resultados por fuente o la Figura 5."),
  vi("En el Power BI: página **5 Modelos** (AUC por fuente, alertas y comparación de los tres algoritmos por AUC y sobreajuste)."),
  h2("Preguntas probables del tribunal"),
  ...preguntas([
    ["¿Por qué usáis el AUC y no el Accuracy?", "Porque el Accuracy engaña cuando una clase domina. En Anxiety, predecir siempre «no hay ansiedad alta» acierta el 83 % sin detectar ningún caso. El AUC mide si el modelo ordena bien los casos, independientemente del umbral."],
    ["¿Qué es una fuga de datos y cómo la evitasteis?", "Usar como predictor algo que contiene la respuesta. Por ejemplo, el total GAD-7 es la suma de sus ítems: si los ítems entran como variables, el modelo acierta trivialmente. Excluimos las variables que construyen el objetivo en cada fuente."],
    ["¿Por qué no usasteis deep learning?", "Con datos tabulares de 87 a 54.000 filas, la regresión y los árboles son el punto de partida estándar y, de hecho, el modelo más simple igualó a los complejos. El deep learning queda como línea futura, sobre todo para el texto."],
    ["¿Por qué validación cruzada en unas fuentes y hold-out en otras?", "Por el tamaño. Con menos de 1.000 filas, una única partición da resultados muy variables, así que repetimos 5 particiones 3 veces (15 evaluaciones). Con muchas filas, una partición 80/20 es estable."],
    ["Si Depression Student es sospechoso, ¿por qué no lo excluisteis?", "Porque tenemos un indicio, no una prueba: no podemos afirmar que sea sintético. Lo marcamos como alerta, no lo usamos como evidencia y propusimos al tutor decidir. Excluirlo es un único cambio en la base de datos que se propaga a todo."],
    ["¿Se podrían usar estos modelos para diagnosticar?", "No. Son modelos de investigación con señal moderada, sobre poblaciones no siempre estudiantiles y con datos autorreportados. Sirven para entender qué factores pesan y para priorizar, no para decidir sobre una persona."],
  ]),
  caja("Transición a la Parte 5", "«Todo este trabajo solo es útil si alguien puede explorarlo. La última fase fue convertirlo en un informe de Power BI accesible en local, en la nube y desde el navegador.»", "EAF4F3", TEAL),
];

// ---------------- PARTE 5
const INSIGHTS = [
  ["1", "Buscar ayuda depende de los antecedentes familiares, no del nivel de estrés", "≈ 72 % frente a ≈ 35 %, igual en los tres niveles", "4"],
  ["2", "Las mujeres reportan más estrés que los hombres en casi todas las fuentes", "39,1 % frente a 32,0 %; 5 de 6 fuentes", "2, 4, 10"],
  ["3", "El estrés Alto disminuye con la edad", "48,3 % (<18) → 18,0 % (>50)", "2, 10"],
  ["4", "A más nivel educativo, menos estrés Alto y severo", "34,2 % → 29,8 % → 26,4 %", "2, 4"],
  ["5", "El lenguaje delata el estrés, sobre todo fuera de los foros de ansiedad", "Ratio LIWC 2,58; 4,83 en r/stress", "3"],
  ["6", "El porcentaje global lo marca una sola fuente: se comparan tendencias, no niveles", "Una fuente = 81,8 % de los registros", "1, 6, 9"],
  ["7", "La señal predictiva es real pero moderada, y dos fuentes exigen cautela", "AUC medio 0,786; 2 con alerta", "5"],
  ["8", "Los datos son de buena calidad, pero la completitud demográfica limita los cruces", "39 de 49 reglas, 0 errores; edad en el 20,7 %", "8"],
  ["9", "Un modelo simple basta: la Regresión Logística iguala a los complejos", "A menos de 0,015 de AUC del mejor", "5"],
];
const parte5 = [
  ...portadaParte(5, "Power BI, nube, servicio web e insights", "Entrega 3 · Objetivo 3", 5 + 1,
    ["Que el informe va **más allá de un Excel con filtros**: menú, segmentadores sincronizados, detalle por clic, inteligencia artificial de Power BI.",
      "Que el mismo informe funciona **en local, en la nube (Supabase) y como web pública**, con **las mismas cifras** en todos.",
      "Los **9 insights** y cómo se encontraron, y las conclusiones del proyecto."]),
  h2("5.1 Arquitectura de la Entrega 3"),
  p("No se rehizo nada para Power BI: el informe consume la capa en estrella y el datawarehouse que ya existían. La versión en la nube es una copia de esas mismas tablas y vistas en PostgreSQL. Por eso las cifras coinciden en **MySQL, Supabase, los dos Power BI y el servicio web**."),
  tabla(["Capa", "Tecnología", "Papel"], [
    ["Origen", "12 ficheros públicos, 334.318 registros", "Sin cambios; los sintéticos se cargan pero las medidas los excluyen"],
    ["Base local", "MySQL (XAMPP): modelo v2, estrella y datawarehouse", "Fuente de verdad"],
    ["Base en la nube", "Supabase (PostgreSQL): 19 tablas y 8 vistas", "Fuente del Power BI entregado y del servicio web"],
    ["Visualización", "Power BI Desktop (proyecto .pbip guardado como .pbix)", "Informe de 11 páginas, en local y en la nube"],
    ["Servicio web", "HTML único con los datos incrustados y API de solo lectura", "Acceso público sin instalar nada"],
    ["Código", "Repositorio público en GitHub, ramas por entrega, GitHub Actions", "Reproducibilidad y mantenimiento"],
  ], [1700, 3700, 3670], { primeraNegrita: true }),
  h2("5.2 Power BI en local"),
  vi("Se construyó como **proyecto .pbip**: el modelo se guarda en TMDL y las páginas en PBIR, formatos de texto que se pueden versionar en git y generar con scripts (las 13 páginas, los iconos y el fondo se generan por código)."),
  vi("**Conexión:** el conector de Power BI no admite el MySQL de XAMPP sin cifrado (exige un modo SSL que ya no soporta). Solución: un script exporta **18 CSV** desde MySQL y el informe los lee. MySQL sigue siendo la fuente de verdad."),
  vi("**Modelo semántico:** 18 tablas, 18 relaciones uno a varios, **53 medidas DAX** y 2 columnas calculadas. Todas las medidas de volumen filtran `uso_modelado = \"incluido\"`, así que los sintéticos nunca cuentan."),
  vi("**Constelación:** la dimensión de dataset filtra a la vez registros, modelos, reglas de calidad y fuentes."),
  h2("5.3 Power BI en la nube (Supabase)"),
  vi("**Por qué:** para que el informe no dependa de un MySQL instalado en cada equipo. El entregable principal es **TFM_Estres_supabase.pbix**."),
  vi("**Migración automatizada:** un script crea el esquema en PostgreSQL con 6 ficheros SQL, copia los datos desde MySQL y crea el usuario de solo lectura. Se puede repetir siempre que cambien los datos."),
  vi("**Validación:** compara las filas de cada tabla y **7 cifras de control** con MySQL: 7 de 7, y 20 de 20 tablas y vistas con las mismas filas."),
  vi("**Textos corregidos:** en Supabase se añadieron las tildes y «Sí» en lugar de «Yes»; por eso el entregable es la versión de la nube."),
  vi("**Seguridad:** Power BI se conecta con el usuario **tfm_lector**, que solo puede leer; las credenciales están en un fichero .env que nunca se sube al repositorio."),
  vi("**Siempre activo:** el plan gratuito pausa los proyectos inactivos; una tarea de GitHub Actions consulta la base dos veces por semana."),
  vi("El .pbix **se abre con los datos incluidos, sin credenciales**; solo hacen falta para pulsar «Actualizar»."),
  h2("5.4 El informe: diseño y páginas"),
  tabla(["Criterio de la rúbrica", "Cómo se cubre"], [
    ["Diseño atractivo", "Página de Inicio como menú principal, con fondo propio, logos e icono por bloque; tema de colores propio «Bienestar»; banda de título y menú de 11 botones en todas las páginas"],
    ["Capacidad de explotación", "Segmentadores de bloque, género, edad y estudios sincronizados entre páginas; jerarquía bloque → dataset; tooltip de página; ficha de cada dataset con clic derecho → Obtener detalles; filtros cruzados"],
    ["Generación de insights", "Página Explorar con árbol de descomposición e influenciadores clave (inteligencia artificial de Power BI); notas de lectura y advertencias en cada página"],
  ], [2500, 6570], { primeraNegrita: true }),
  ...imagen("figuras/powerbi/p0_inicio.png", 560, "Figura 6. Página de Inicio: los 6 KPIs, los 4 bloques y el menú de navegación."),
  tabla(["Página", "Contenido"], [
    ["Inicio", "Qué analiza el informe, los 6 KPIs y un recuadro por bloque"],
    ["1 Panorama", "Registros, % de estrés Alto, cobertura y fuentes; estrés Alto por bloque y por dataset"],
    ["2 Demografía", "Estrés Alto por género, edad y estudios; matriz género × edad"],
    ["3 Lenguaje", "Dreaddit: vocabulario de ansiedad con y sin estrés por subreddit; sentimiento"],
    ["4 Validación", "Brecha de ansiedad, estrés severo DASS, búsqueda de tratamiento"],
    ["5 Modelos", "AUC por fuente, alertas y comparación de algoritmos"],
    ["6 KPIs", "Histórico de los 6 KPIs y su catálogo"],
    ["7 Explorar", "Árbol de descomposición e influenciadores clave"],
    ["8 Calidad", "Reglas por dimensión y estado, completitud, controles"],
    ["9 Fuentes", "Catálogo de los 12 ficheros y criterio de cada uno"],
    ["10 DASS-42", "Depresión, ansiedad y estrés por género y estudios"],
  ], [1800, 7270], { primeraNegrita: true }),
  h2("5.5 Los 9 insights"),
  p("Todos se obtuvieron con el mismo método: **detectar** un patrón en un gráfico, **aislarlo** con los segmentadores y el árbol de descomposición, **descartar el efecto composición** (comprobarlo dentro de cada fuente, porque tienen tamaños muy distintos) y **contrastarlo** con el datawarehouse, los KPIs, los modelos y el SQL."),
  tabla(["#", "Insight", "Dato clave", "Pág."], INSIGHTS, [400, 4500, 3270, 900], { centrar: [0, 3] }),
  caja("Cómo leer las cifras (insight 6)", "Cada fuente define «Alto» con su propio criterio, y la mayor (Mental Health Dataset) es el **81,8 %** de los registros. Por eso el 33,7 % global no es una prevalencia: el informe **compara tendencias dentro de cada fuente**, no niveles absolutos entre fuentes. Decirlo antes de que lo pregunte el tribunal demuestra dominio."),
  espacio(),
  ...imagen("figuras/powerbi/p7_explorar.png", 560, "Figura 7. Página Explorar: árbol de descomposición (Validación psicológica → Femenino → 18-25) e influenciadores clave."),
  h2("5.6 Analítica avanzada (parte opcional de la rúbrica)"),
  vi("Los modelos del Objetivo 2 se ven en la página 5, con sus alertas y la comparación de algoritmos por AUC y sobreajuste."),
  vi("Los **influenciadores clave** estiman qué valores multiplican la probabilidad de estrés Alto (por ejemplo, tener menos de 18 años: 1,51 veces)."),
  vi("El **árbol de descomposición** busca solo los cortes con más estrés."),
  h2("5.7 Servicio web y calidad del dato"),
  p([...md("El informe se publicó como **servicio web público** ("), enlace(URL_WEB, URL_WEB), ...md("): un único HTML que reproduce las 11 páginas con los mismos datos, filtros y medidas, sin instalar Power BI ni tener credenciales. Incluye una pestaña Arquitectura con los diagramas y 4 consultas en vivo a la API de Supabase (catálogo 12 filas, KPIs 6, modelos 8, reglas 49), que solo permite leer vistas agregadas.")], { alignment: AlignmentType.LEFT }),
  p("La **calidad y el gobierno del dato** se organizan según las áreas del marco **DAMA-DMBOK**: calidad (49 reglas y 17 controles), metadatos y linaje (página Fuentes, catálogo de KPIs), datos de referencia (dimensiones conformes, completitud medida: género 95,6 %, edad 20,7 %, estudios 15,3 %), seguridad (usuario de solo lectura, credenciales fuera del repositorio) y aptitud de uso (sintéticos excluidos, alertas visibles)."),
  h2("5.8 Cierre: conclusiones, limitaciones y trabajo futuro (1 minuto)"),
  h3("Conclusiones"),
  num("**La presión académica y el aislamiento** son el eje del estrés estudiantil, y en redes **importa el patrón de uso, no el tiempo**.", "concl"),
  num("**El lenguaje delata el estrés**: se detecta en texto con un AUC de 0,84.", "concl"),
  num("**Más estrés no lleva a pedir más ayuda**: lo que la mueve son los antecedentes familiares.", "concl"),
  num("**Mujeres, menores de 18 y personas con menos estudios** concentran más estrés Alto: son colectivos prioritarios.", "concl"),
  num("**La señal predictiva es real pero moderada**, y un modelo simple basta.", "concl"),
  num("Es posible **integrar fuentes heterogéneas sin identificador común** con dimensiones conformes y un constructo común, y llevarlo de una base local a la nube y a la web con las mismas cifras.", "concl"),
  h3("Limitaciones"),
  vi("Datos autorreportados y transversales: asociaciones, no causas."),
  vi("Poblaciones no siempre estudiantiles; cada fuente define el estrés con su criterio."),
  vi("Solo el 17 % de los registros tiene género y edad a la vez."),
  vi("Modelos de investigación, no de diagnóstico."),
  h3("Trabajo futuro"),
  vi("Datos longitudinales con un identificador común (por ejemplo, una encuesta propia en una universidad)."),
  vi("Cargar las respuestas por ítem del DASS-42 (`b4_dass_item` está vacía)."),
  vi("Deep learning para el texto y ajuste de umbrales; matriz de responsabilidades (RACI), glosario y monitorización automática de las reglas."),
  h2("Cifras para memorizar"),
  tabla(["Cifra", "Qué es"], [
    ["11 + 2 páginas", "Páginas visibles y ocultas (detalle y tooltip)"],
    ["18 tablas · 18 relaciones · 53 medidas", "Modelo semántico de Power BI"],
    ["18 CSV", "Exportados de MySQL para la versión local"],
    ["19 tablas · 8 vistas", "Esquema en Supabase"],
    ["7 de 7 · 20 de 20", "Cifras de control y tablas iguales entre MySQL y Supabase"],
    ["9 insights", "Documentados con su método y capturas"],
    ["81,8 %", "Peso de la mayor fuente en los registros (por qué no comparar niveles)"],
  ], [3300, 5770], { primeraNegrita: true }),
  h2("Qué mostrar en pantalla"),
  vi("**Demostración en vivo** del .pbix: Inicio → aplicar Femenino + 18-25 → página 7 Explorar → clic derecho en un dataset → Obtener detalles."),
  vi("Plan B: el **servicio web** o el PDF del informe abiertos en otra pestaña."),
  h2("Preguntas probables del tribunal"),
  ...preguntas([
    ["¿Qué aporta vuestro Power BI que no haga un Excel con filtros?", "Un modelo de datos en constelación con dimensiones compartidas, segmentadores sincronizados entre 11 páginas, jerarquías, detalle por clic, tooltips de página y visuales de inteligencia artificial (árbol de descomposición e influenciadores clave), sobre 319.318 registros de 9 fuentes."],
    ["¿Por qué Supabase y no publicar en Power BI Service?", "Para tener una base de datos real en la nube, independiente del equipo de cada persona, con un usuario de solo lectura y una API pública. El mismo modelo sirve al Power BI y al servicio web, y el plan gratuito basta para el proyecto."],
    ["¿Cómo garantizáis que las cifras son correctas?", "Con validaciones automáticas: 7 cifras de control y el número de filas de las 20 tablas y vistas coinciden entre MySQL y Supabase, y las mismas medidas dan los mismos valores en Power BI y en la web. Además, el histórico de KPIs muestra que el cálculo es reproducible."],
    ["¿Es seguro publicar los datos?", "El tutor accede con un usuario que solo puede leer; la API pública solo expone vistas agregadas, sin registros individuales; las credenciales nunca se suben al repositorio. Además, los datos de origen son públicos y anónimos."],
    ["¿Por qué el 33,7 % de estrés Alto no es la prevalencia real?", "Porque cada fuente define «Alto» con su propio criterio y una sola fuente aporta el 81,8 % de los registros. Por eso comparamos tendencias dentro de cada fuente (insight 6)."],
    ["¿Qué recomendaríais a una universidad?", "Priorizar a los colectivos con más estrés (mujeres, menores de 18, menos estudios), trabajar el aislamiento y el uso ansioso de redes, y acercar la ayuda a quien no tiene antecedentes familiares, porque es quien menos la pide aunque la necesite."],
  ]),
];

// ---------------- Preguntas transversales y anexos
const transversales = [
  h1("Preguntas transversales (para todo el grupo)"),
  p("Preguntas sobre el proyecto en conjunto, que puede responder cualquiera. Conviene acordar quién toma cada una."),
  ...preguntas([
    ["¿Qué es lo más original del proyecto?", "La integración de fuentes heterogéneas sin identificador común mediante dimensiones conformes y un constructo común, el tratamiento de la calidad del dato como resultado (detectar sintéticos y un dataset sospechoso) y la arquitectura completa: de MySQL local a la nube, al Power BI y a un servicio web, con las mismas cifras y todo versionado en GitHub."],
    ["¿Qué haríais diferente si empezarais de nuevo?", "Buscar o recoger datos con un identificador común y longitudinales, para estudiar causas y evolución; diseñar las dimensiones conformes desde el principio (llegaron tras la retroalimentación); y priorizar fuentes estrictamente estudiantiles."],
    ["¿Qué aprendisteis de la retroalimentación del tutor?", "Que sin dimensiones comunes un proyecto con muchas fuentes se fragmenta. La corrección (modelo v2, constructo común, política de sintéticos) es lo que permitió el informe unificado de la Entrega 3."],
    ["¿Cómo os organizasteis como grupo?", "Acordadlo antes y respondedlo con hechos: quién hizo qué parte, cómo se repartieron las entregas, cómo se revisó el trabajo y cómo se usó el repositorio."],
    ["¿Cuál es la utilidad práctica?", "Ayudar a servicios de bienestar universitarios a priorizar colectivos y factores, y apoyar la detección temprana por vías indirectas, como el lenguaje, justo donde la persona no pide ayuda."],
    ["¿Qué limitación os preocupa más?", "La comparabilidad entre fuentes: cada una mide el estrés a su manera y con poblaciones distintas. Lo mitigamos comparando tendencias dentro de cada fuente y documentando el criterio de cada una."],
  ]),
];

const chuleta = [
  h1("Anexo A. Chuleta de cifras"),
  p("Las cifras oficiales del proyecto. Usad siempre estas, con los mismos redondeos."),
  tabla(["Ámbito", "Cifra", "Qué es"], [
    ["Datos", "11 datasets · 12 ficheros · 4 bloques", "Dreaddit en entrenamiento y prueba"],
    ["Datos", "334.318 · 319.318", "Registros cargados · registros de las 9 fuentes reales"],
    ["Datos", "3 sintéticos (15.000 registros)", "Student Habits, Social Media/Sleep, Lifestyle"],
    ["Calidad", "49 reglas: 39 OK, 10 avisos, 0 errores", "Reglas de calidad del dato"],
    ["Calidad", "17 controles: 14 OK, 3 avisos", "Carga, ETL, migración, seguridad e informe"],
    ["Calidad", "Género 95,6 % · edad 20,7 % · estudios 15,3 %", "Completitud de las dimensiones"],
    ["Modelo", "20 tablas (8 dim. + 12 hechos)", "Modelo relacional v2 en MySQL"],
    ["Modelo", "6 vistas en estrella", "Capa de consumo para Power BI"],
    ["Modelo", "19 tablas + 8 vistas", "Esquema en Supabase"],
    ["Modelo", "7.446", "Mujeres 18-25 con estrés Alto, en 7 fuentes"],
    ["KPIs", "33,68 % · 2,89 · 72,69 % · 49,41 % · 2,58 · 17,01 %", "Estrés Alto · brecha ansiedad · riesgo crítico · tratamiento · LIWC · cobertura"],
    ["EDA", "r = 0,71 · 0,59 · 0,42", "Aislamiento–depresión · preocupación · comparación social"],
    ["EDA", "72,4 % frente a 35,1 %", "Tratamiento con y sin antecedentes familiares"],
    ["Modelos", "8 tareas · AUC 0,73-0,84 · media 0,786", "Rango y media sin las 2 alertas"],
    ["Modelos", "0,838 · 0,82 · 0,998", "NLP híbrido · NLP solo texto · Depression Student"],
    ["Power BI", "11 + 2 páginas · 18 tablas · 53 medidas", "Informe y modelo semántico"],
    ["Insights", "9 · 81,8 %", "Insights · peso de la mayor fuente"],
  ], [1400, 3800, 3870], { primeraNegrita: true }),
];

const glosario = [
  h1("Anexo B. Glosario"),
  tabla(["Término", "Significado"], [
    ["AUC", "Área bajo la curva ROC: probabilidad de que el modelo puntúe más alto un caso positivo que uno negativo (0,5 azar, 1 perfecto)"],
    ["Baseline", "Modelo de referencia que predice siempre la clase más frecuente"],
    ["Brecha (sobreajuste)", "Accuracy de entrenamiento menos accuracy de prueba; > 0,15 indica sobreajuste"],
    ["Constelación", "Varias tablas de hechos que comparten dimensiones"],
    ["Constructo común", "El nivel de estrés Bajo / Moderado / Alto al que se lleva la variable de cada fuente"],
    ["DAMA-DMBOK", "Marco de referencia de gestión y gobierno del dato"],
    ["DASS-42", "Escala clínica de 42 ítems para depresión, ansiedad y estrés (Lovibond y Lovibond, 1995)"],
    ["Dimensión conforme", "Dimensión compartida por varias tablas de hechos con el mismo significado"],
    ["Esquema en estrella", "Una tabla de hechos central rodeada de dimensiones planas"],
    ["ETL", "Extraer, transformar y cargar datos"],
    ["Fuga de datos", "Usar como predictor información que contiene la respuesta"],
    ["GAD-7", "Escala clínica de 7 ítems para la ansiedad generalizada (≥ 10: ansiedad moderada o más)"],
    ["Hold-out 80/20", "Separar el 80 % para entrenar y el 20 % para evaluar"],
    ["Hub-and-spoke", "Arquitectura de centro y radios: las fuentes conservan su detalle y convergen en dimensiones comunes"],
    ["LIWC", "Diccionario psicolingüístico que cuenta palabras por categoría (ansiedad, emoción negativa, pronombres…)"],
    ["NLP", "Procesamiento de lenguaje natural"],
    ["PBIP / TMDL / PBIR", "Formato de proyecto de Power BI en texto: modelo en TMDL y páginas en PBIR"],
    ["SPIN · SWL", "Escalas de ansiedad social y de satisfacción con la vida"],
    ["TF-IDF", "Representación del texto que pondera cada palabra por su frecuencia en el documento y su rareza en el corpus"],
    ["Validación cruzada 5×3", "5 particiones repetidas 3 veces: 15 evaluaciones del modelo"],
  ], [2300, 6770], { primeraNegrita: true }),
];

const fuentes = [
  h1("Anexo C. Dónde está cada cosa"),
  p("Rutas desde la carpeta **Documentacion y entrega\\Entrega\\**, para repasar el detalle de cada parte."),
  tabla(["Parte", "Documentos de referencia"], [
    ["1", "..\\Plantilla propuesta proyectos_2604_2.pdf · Objetivo1\\Diccionario de datos.xlsx · ..\\Enlaces.txt"],
    ["2", "Objetivo1\\Sintesis objetivo 1 Final.pdf · Objetivo1\\Objetivo1_Desarrollo_Completo.docx · Objetivo1\\figurasObje1 · Objetivo1\\Reglas de Calidad"],
    ["3", "Objetivo1\\Respuesta_Retroalimentacion_EntregaI_v3.pdf · Objetivo1\\Modelo MySQL · Objetivo2\\Sintesis_Entrega2_ETL_KPIs.pdf · Objetivo2\\KPIs_TFM.docx"],
    ["4", "Objetivo2\\Sintesis_Objetivo2_Modelado.pdf · Objetivo2\\Notebooks\\09_modelado_objetivo2.ipynb · Objetivo2\\figuras_modelado"],
    ["5", "Objetivo3\\Sintesis_Entrega3_PowerBI.pdf · Objetivo3\\insights\\Insights_PowerBI_TFM_Estres.docx · Objetivo3\\supabase\\powerbi\\Entrega\\TFM_Estres_supabase.pbix"],
    ["Todas", "Memoria\\Indice_Memoria_TFM.docx (índice de la memoria final)"],
  ], [900, 8170], { primeraNegrita: true, centrar: [0] }),
  p([t("Repositorio: "), enlace(URL_REPO, URL_REPO), t(" · Servicio web: "), enlace(URL_WEB, URL_WEB)], { alignment: AlignmentType.LEFT, spacing: { before: 160 } }),
];

// ------------------------------------------------------------------ documento
const doc = new Document({
  creator: "Grupo LUHN", title: "Guía del proyecto para la defensa",
  styles: {
    default: { document: { run: { font: SERIF, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 32, bold: true, color: AZUL }, paragraph: { spacing: { before: 120, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 25, bold: true, color: TINTA }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 22, bold: true, color: TEAL }, paragraph: { spacing: { before: 160, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "vinetas", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 260 } } } }] },
    ...["numeros", "obj", "pasos", "concl"].map((reference) => ({ reference, levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] })),
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1418, right: 1418 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      t("Grupo LUHN · Guía del proyecto para la defensa · ", { size: 16, color: GRIS }), new TextRun({ children: [PageNumber.CURRENT], font: SERIF, size: 16, color: GRIS })] })] }) },
    children: [...portada, ...indice, ...comoUsar, ...resumen, ...lineaTiempo, ...parte1, ...parte2, ...parte3, ...parte4, ...parte5,
      ...transversales, ...chuleta, ...glosario, ...fuentes],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(SALIDA, buf); console.log("OK", SALIDA); });
