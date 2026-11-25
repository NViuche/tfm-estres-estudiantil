// Índice de trabajo de la memoria final del TFM (Word, A4 horizontal).
// Uso: node indice_memoria.js <salida.docx>
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, LevelFormat, BorderStyle, Footer, PageNumber, PageOrientation, VerticalAlign, HeadingLevel,
} = require("docx");

const [, , SALIDA] = process.argv;
const AZUL = "1F5C99", GRIS = "6B6B6B", TINTA = "222222";
const SERIF = "Times New Roman", SANS = "Arial";
const ANCHO = 13958; // A4 horizontal con márgenes de 2,54 cm

const t = (text, o = {}) => new TextRun({ text, font: SERIF, size: 21, color: TINTA, ...o });
const b = (text, o = {}) => t(text, { bold: true, ...o });
const p = (runs, o = {}) => new Paragraph({ spacing: { after: 100, line: 276 }, children: Array.isArray(runs) ? runs : [t(runs)], ...o });
const vi = (runs, nivel = 0, keepNext = false) => new Paragraph({ numbering: { reference: "vinetas", level: nivel }, keepNext, keepLines: true, spacing: { after: 50, line: 264 }, children: Array.isArray(runs) ? runs : [t(runs)] });
const num = (runs) => new Paragraph({ numbering: { reference: "numeros", level: 0 }, spacing: { after: 60, line: 264 }, children: Array.isArray(runs) ? runs : [t(runs)] });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });

// ------------------------------------------------------------------ tabla del índice
const COLS = [700, 2250, 4150, 3700, 1250, 650, 1258]; // suma = ANCHO
const ESTADO = {
  Reutilizar: { fill: "DCEFD9", nota: "El texto ya existe: se resume y se ajusta al tono de la memoria." },
  Adaptar: { fill: "FCEBC7", nota: "Hay material de partida, pero hay que reescribirlo o completarlo." },
  Redactar: { fill: "F6D5D3", nota: "No existe todavía: hay que escribirlo desde cero." },
};
const borde = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
const celda = (contenido, ancho, o = {}) => new TableCell({
  width: { size: ancho, type: WidthType.DXA }, borders: bordes, verticalAlign: VerticalAlign.CENTER,
  margins: { top: 50, bottom: 50, left: 90, right: 90 },
  shading: o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined,
  columnSpan: o.span,
  children: (Array.isArray(contenido) ? contenido : [contenido]).map((c) => typeof c === "string"
    ? new Paragraph({ spacing: { after: 0, line: 240 }, alignment: o.centro ? AlignmentType.CENTER : AlignmentType.LEFT,
        children: [t(c, { size: 18, bold: !!o.negrita, color: o.color || TINTA })] })
    : c),
});
const fuente = (lineas) => lineas.map((l) => new Paragraph({ spacing: { after: 30, line: 240 }, children: [t(l, { size: 17, color: "333333" })] }));
const cabecera = new TableRow({ tableHeader: true, children: ["Nº", "Apartado", "Qué debe contener", "De dónde sale (ruta desde Entrega\\)", "Estado", "Págs.", "Responsable"]
  .map((h, n) => celda(h, COLS[n], { fill: AZUL, color: "FFFFFF", negrita: true, centro: n !== 1 && n !== 2 && n !== 3 })) });
const seccion = (texto) => new TableRow({ cantSplit: true, children: [celda(texto, ANCHO, { span: 7, fill: "E4ECF5", negrita: true })] });
const fila = ([n, apartado, contenido, fuentes, estado, pags]) => new TableRow({ cantSplit: true, children: [
  celda(n, COLS[0], { centro: true, negrita: true }), celda(apartado, COLS[1], { negrita: true }), celda(contenido, COLS[2]),
  celda(fuente(fuentes), COLS[3]), celda(estado, COLS[4], { fill: ESTADO[estado].fill, centro: true }),
  celda(String(pags).replace(".", ","), COLS[5], { centro: true }), celda("", COLS[6]),
] });

const S1 = "Objetivo1\\Sintesis objetivo 1 Final.docx";
const D1 = "Objetivo1\\Objetivo1_Desarrollo_Completo.docx";
const R1 = "Objetivo1\\Respuesta_Retroalimentacion_EntregaI_v3.pdf";
const E2 = "Objetivo2\\Sintesis_Entrega2_ETL_KPIs.pdf";
const M2 = "Objetivo2\\Sintesis_Objetivo2_Modelado.pdf";
const S3 = "Objetivo3\\Sintesis_Entrega3_PowerBI.docx";
const INS = "Objetivo3\\insights\\Insights_PowerBI_TFM_Estres.docx";
const PROP = "..\\Plantilla propuesta proyectos_2604_2.pdf";
const PROB = "Repo: investigacion\\problema.md";
const SEG = "Repo: SEGUIMIENTO.md";

const filas = [
  ["sec", "PARTES INICIALES"],
  ["A", "Portada", "Título completo, los 5 autores, programa (Máster en Business Analytics e Inteligencia Artificial), Grupo LUHN y fecha de entrega.", [PROP + " (título y autores)", "Portadas de las síntesis"], "Adaptar", 1],
  ["B", "Resumen ejecutivo", "Una sola página: el reto y los objetivos, la metodología y las fuentes (11 datasets en 4 bloques), una referencia breve al marco conceptual y las conclusiones principales. Se escribe al final.", ["Se resume desde D, E y F", S3 + " §1 y §6 (cifras)"], "Redactar", 1],
  ["C", "Índice", "Tabla de contenido automática de Word, más índice de figuras y de tablas.", ["Se genera desde los estilos de título"], "Redactar", 2],
  ["sec", "D. INTRODUCCIÓN"],
  ["D.a", "Contexto del proyecto", "No hay empresa: se sustituye por el ámbito. El estrés estudiantil como problema, a quién sirve el análisis (universidades, servicios de bienestar) y la motivación del grupo.", [PROB + " (Problema)", PROP + " (motivación)"], "Adaptar", 1],
  ["D.b", "Problema planteado", "Qué se quiere entender y por qué hace falta combinar fuentes académicas, conductuales, textuales y clínicas.", [PROB + " (Problema, Enfoque)"], "Adaptar", 0.5],
  ["D.c", "Objetivos", "Los tres objetivos de la propuesta: análisis exploratorio, modelado con IA y NLP, y dashboards de BI.", [PROP, PROB + " (Objetivos)"], "Reutilizar", 0.5],
  ["D.d", "Fases del proyecto", "Las 4 fases del desarrollo (ver E.3) presentadas en un esquema.", [SEG], "Adaptar", 0.5],
  ["D.e", "Resultado final", "Qué se obtuvo: Power BI en local y en la nube, servicio web, 9 insights y modelos predictivos.", [S3 + " §1, §6 y §8", PROB + " (Hallazgos)"], "Adaptar", 0.5],
  ["sec", "E.1 DEFINICIÓN DEL PROYECTO Y ANÁLISIS DE LA VIABILIDAD"],
  ["E.1.i", "Marco conceptual", "Estrés académico; escalas DASS-42 y GAD-7; detección de estrés en texto (NLP, LIWC); BI y datawarehouse dimensional (Kimball). Con citas.", [D1 + " §1", R1 + " §3 (capa analítica global)", "Bibliografía candidata (este documento)"], "Redactar", 2],
  ["E.1.ii", "Análisis interno y externo", "DAFO del proyecto. Fortalezas: 11 fuentes y gobierno del dato. Debilidades: sin ID común, datos sintéticos, poblaciones no estudiantiles. Oportunidades y amenazas.", [SEG + " (Limitaciones)", S3 + " (Limitaciones)", "Objetivo1\\Retroalimentacion.txt"], "Redactar", 1.5],
  ["E.1.iii", "Explicación detallada", "Arquitectura completa: fuentes → MySQL → datawarehouse → modelos → Power BI, Supabase y web, con el diagrama de arquitectura.", [S3 + " §1", "Objetivo3\\recursos\\sintesis\\arquitectura.png"], "Reutilizar", 1],
  ["E.1.iv", "Objetivos generales y específicos", "Objetivo general y objetivos específicos medibles, enlazados con los 6 KPIs.", [PROP, "Objetivo2\\KPIs_TFM.docx"], "Adaptar", 0.5],
  ["sec", "E.2 PLANIFICACIÓN"],
  ["E.2.i", "Recursos económicos", "Coste de herramientas (todas gratuitas: Python, MySQL/XAMPP, Power BI Desktop, Supabase plan gratuito, GitHub) y coste estimado de horas de trabajo.", ["Nuevo"], "Redactar", 1],
  ["E.2.ii", "Recursos materiales", "Hardware y software utilizados, con versiones.", [S3 + " §3, §4 y §8", "Repo: README.md"], "Redactar", 0.5],
  ["E.2.iii", "Recursos humanos", "Los 5 integrantes, sus roles y el reparto real de tareas.", ["Nuevo: lo define el grupo"], "Redactar", 0.5],
  ["E.2.iv", "Recursos de tiempo", "Horas estimadas por fase y por persona.", ["Nuevo"], "Redactar", 0.5],
  ["E.2.v", "Cronograma", "Diagrama de Gantt con las fases y las fechas de las entregas parciales y final.", ["Cronograma del aula TFM", "Fechas de envío de las Entregas 1, 2 y 3"], "Redactar", 1],
  ["E.2.vi", "Alcance", "Qué entra y qué no: análisis en paralelo más capa global, sin diagnóstico clínico, sin deep learning y política para datos sintéticos.", [SEG + " (Limitaciones)", R1 + " §4", "..\\Rubricas\\Alcance TFM.pdf"], "Adaptar", 0.5],
  ["sec", "E.3 DESARROLLO · FASE 1: DATOS, CALIDAD Y MODELO RELACIONAL (Entrega 1)"],
  ["1.1", "Fuentes y bloques", "Los 11 datasets en 4 bloques: qué aporta cada uno, filas y columnas, y si es real o sintético.", [S1 + " (Bloques 1 a 4)", "Objetivo1\\Diccionario de datos.xlsx", "..\\Enlaces.txt"], "Reutilizar", 1.5],
  ["1.2", "Perfilado y análisis exploratorio", "Resumen del EDA por bloque y la síntesis transversal (4 hallazgos). Solo las gráficas clave; el resto, a anexos.", [D1 + " §1 a §6", S1 + " (Síntesis transversal)", "Objetivo1\\figurasObje1"], "Reutilizar", 2.5],
  ["1.3", "Calidad del dato", "Las 49 reglas de calidad, resultados y decisiones de preprocesamiento. Incluir como limitación la regla B1.3 (cgpa en texto-rango): depende de la versión de pandas y da 0/87 (OK) cuando debería dar 87/87 (aviso); se mantiene la cifra entregada.", [D1 + " §7", "Objetivo1\\Reglas de Calidad", S3 + " §9", SEG + " (Limitaciones)"], "Reutilizar", 1.5],
  ["1.4", "Modelo relacional y respuesta al tutor", "Modelo MySQL (20 tablas, modelo v2): claves renombradas, dimensiones conformes y capa en estrella, como respuesta a la retroalimentación de la Entrega 1.", [R1 + " §1 a §6", "Objetivo1\\Modelo MySQL"], "Reutilizar", 2.5],
  ["1.5", "Armonización", "Cómo se unifican edad, género y nivel educativo entre fuentes.", ["Objetivo1\\Armonizacion", "Notebook 06 (Respaldo Notebooks)"], "Adaptar", 1],
  ["sec", "E.3 DESARROLLO · FASE 2: ETL, DATAWAREHOUSE Y KPIs (Entrega 2)"],
  ["2.1", "Ingesta y transformaciones", "Proceso ETL en Python: limpieza, carga y transformaciones aplicadas.", [E2 + " §1 y §2", "Objetivo2\\Notebooks\\08_etl_transformaciones_kpis_v4.ipynb"], "Reutilizar", 2],
  ["2.2", "Datawarehouse en estrella", "Modelo del DWH (hechos unificados, dimensiones y constelación) con su diagrama.", ["Objetivo2\\PASO4_dwh_estrella.sql", "Objetivo2\\dwh_estrella_ERD.png", S3 + " §2"], "Reutilizar", 1.5],
  ["2.3", "KPIs", "Los 6 KPIs: definición, fórmula, resultado y tabla de trazabilidad.", ["Objetivo2\\KPIs_TFM.docx", E2 + " §3"], "Reutilizar", 1.5],
  ["2.4", "Verificación", "Controles de calidad de la carga.", [E2 + " §4"], "Reutilizar", 0.5],
  ["sec", "E.3 DESARROLLO · FASE 3: MODELADO PREDICTIVO Y NLP (Entrega 2)"],
  ["3.1", "Diseño metodológico", "Elección de métricas, prevención de fugas de datos, feature engineering y pipeline.", [M2 + " §1 a §3"], "Reutilizar", 1.5],
  ["3.2", "Modelos por dataset", "Resultados de los 7 modelos estructurados en una tabla comparativa con breve comentario.", [M2 + " §4", "Objetivo2\\resultados_modelado_resumen.csv"], "Reutilizar", 2.5],
  ["3.3", "NLP sobre Dreaddit", "Detección de estrés en texto.", [M2 + " §5"], "Reutilizar", 1],
  ["3.4", "Alerta Depression Student", "El AUC de 0,998 y la decisión final del grupo (mantener con alerta o excluir).", [M2 + " §6", SEG + " (Pendiente)"], "Adaptar", 0.5],
  ["3.5", "Comparativa y limitaciones", "Qué modelo funciona mejor y por qué; límites de los resultados.", [M2 + " §7 y §8"], "Reutilizar", 1],
  ["sec", "E.3 DESARROLLO · FASE 4: EXPLOTACIÓN CON POWER BI (Entrega 3)"],
  ["4.1", "Modelo semántico y Power BI local", "Conexión, modelo semántico, medidas DAX y correcciones.", [S3 + " §2 y §3"], "Reutilizar", 1.5],
  ["4.2", "Nube y servicio web", "Supabase (PostgreSQL), usuario de solo lectura, API pública y prototipo web.", [S3 + " §4 y §8", "Objetivo3\\supabase\\README.md"], "Reutilizar", 1],
  ["4.3", "Diseño del informe", "Menú, tema y las 11 páginas visibles, con 3 o 4 capturas (el resto en anexos).", [S3 + " §5", "Objetivo3\\insights (capturas p0–p10)"], "Reutilizar", 2],
  ["4.4", "Insights", "Los 9 insights: qué se observa, cómo se encontró y cautelas.", [INS + " §2 y §3"], "Reutilizar", 3],
  ["4.5", "Analítica avanzada", "Correlaciones y modelos integrados en el informe (parte opcional).", [S3 + " §7"], "Reutilizar", 0.5],
  ["4.6", "Gobierno y retroalimentación", "Gobierno del dato y cómo se atendió cada retroalimentación del tutor, incluida la de la Entrega 3.", [S3 + " §9 y §10", INS + " §4", "Retroalimentación de la Entrega 3 (pendiente)"], "Adaptar", 1],
  ["sec", "PARTES FINALES"],
  ["F", "Conclusiones", "Aportaciones principales, conclusión por objetivo, recomendaciones (para universidades) y trabajo futuro (datos longitudinales con ID común, RACI, glosario, monitorización de reglas y versiones de librerías fijadas).", [M2 + " §8", INS + " §5", PROB + " (Hallazgos)", SEG + " (Pendiente y Limitaciones)"], "Redactar", 2.5],
  ["G", "Bibliografía", "Formato APA 7: datasets (Kaggle y GitHub) y referencias académicas.", ["..\\Enlaces.txt", "Bibliografía candidata (este documento)"], "Redactar", 2],
];

const tabla = new Table({
  width: { size: ANCHO, type: WidthType.DXA }, columnWidths: COLS,
  rows: [cabecera, ...filas.map((f) => (f[0] === "sec" ? seccion(f[1]) : fila(f)))],
});
const total = filas.filter((f) => f[0] !== "sec").reduce((s, f) => s + f[5], 0);

// ------------------------------------------------------------------ anexos
const COLS_A = [700, 4200, 6100, 1700, 1258];
const tablaAnexos = new Table({
  width: { size: ANCHO, type: WidthType.DXA }, columnWidths: COLS_A,
  rows: [
    new TableRow({ tableHeader: true, children: ["Nº", "Anexo", "De dónde sale (ruta desde Entrega\\)", "Estado", "Responsable"].map((h, n) => celda(h, COLS_A[n], { fill: AZUL, color: "FFFFFF", negrita: true, centro: n === 0 || n >= 3 })) }),
    ...[
      ["H.1", "Diccionario de datos completo", "Objetivo1\\Diccionario de datos.xlsx", "Reutilizar"],
      ["H.2", "Catálogo de las 49 reglas de calidad", "Objetivo1\\Reglas de Calidad", "Reutilizar"],
      ["H.3", "Fichas de los 6 KPIs", "Objetivo2\\KPIs_TFM.docx", "Reutilizar"],
      ["H.4", "Resultados completos del modelado", "Objetivo2\\resultados_modelado_completo.csv", "Reutilizar"],
      ["H.5", "Diagramas: modelo relacional y estrella", "Objetivo1\\Modelo MySQL · Objetivo2\\dwh_estrella_ERD.png", "Reutilizar"],
      ["H.6", "Capturas de las 11 páginas del informe", "Objetivo3\\insights (capturas)", "Reutilizar"],
      ["H.7", "Reproducibilidad: repositorio, orden de ejecución y guía de Power BI", R1 + " §8 · Objetivo3\\local_xampp\\guia_power_bi.md · Repo: README.md", "Adaptar"],
      ["H.8", "Respuestas completas a las retroalimentaciones", R1 + " · " + S3 + " §10", "Reutilizar"],
    ].map(([n, a, f, e]) => new TableRow({ cantSplit: true, children: [
      celda(n, COLS_A[0], { centro: true, negrita: true }), celda(a, COLS_A[1], { negrita: true }), celda(fuente([f]), COLS_A[2]),
      celda(e, COLS_A[3], { fill: ESTADO[e].fill, centro: true }), celda("", COLS_A[4])] })),
  ],
});

// ------------------------------------------------------------------ documento
const hoy = new Date().toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" });
const doc = new Document({
  creator: "Grupo LUHN", title: "Índice de trabajo de la memoria final",
  styles: {
    default: { document: { run: { font: SERIF, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 28, bold: true, color: AZUL }, paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 23, bold: true, color: TINTA }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "vinetas", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 260 } } } }] },
    { reference: "numeros", levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1200, bottom: 1200, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      t("Grupo LUHN · Índice de trabajo de la memoria · página ", { size: 16, color: GRIS }), new TextRun({ children: [PageNumber.CURRENT], font: SERIF, size: 16, color: GRIS })] })] }) },
    children: [
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Índice de trabajo de la memoria final", font: SANS, size: 40, bold: true, color: AZUL })] }),
      new Paragraph({ spacing: { after: 40 }, children: [t("Análisis multidimensional del estrés estudiantil mediante Business Analytics e Inteligencia Artificial", { size: 24, italics: true })] }),
      new Paragraph({ spacing: { after: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: AZUL, space: 6 } },
        children: [t(`Grupo LUHN · Máster en Business Analytics e Inteligencia Artificial · ${hoy}`, { size: 19, color: GRIS })] }),

      h1("1. Para qué sirve este documento"),
      p("Las tres entregas parciales ya están hechas. Queda la memoria final (80 % de la nota) y la defensa (20 %). Este índice sigue la estructura que pide la guía del TFM y, para cada apartado, indica qué debe contener, de qué archivo existente sale, si basta con reutilizarlo o hay que escribirlo, y cuántas páginas se le reservan. La columna «Responsable» está en blanco para repartir el trabajo en el grupo."),
      h2("Requisitos de la guía del TFM"),
      vi([b("Extensión: "), t("unas 50 páginas a una cara (unas 25.000 palabras), más un máximo de 50 páginas de anexos.")]),
      vi([b("Formato: "), t("documento Word guardado en PDF y subido al campus en la fecha fijada. Nunca una presentación.")]),
      vi([b("Estructura: "), t("A. Portada · B. Resumen ejecutivo · C. Índice · D. Introducción · E. Núcleo · F. Conclusiones · G. Bibliografía · H. Anexos.")]),
      vi([b("Aprobación: "), t("el tutor revisa la memoria y decide si el grupo puede defenderla.")]),
      vi([b("Evaluación del trabajo escrito (80 %): "), t("50 % calidad del documento final, 10 % entregas a tiempo, 10 % creatividad e innovación y 10 % nota individual.")]),
      h2("Leyenda de la columna «Estado»"),
      ...Object.entries(ESTADO).map(([k, v]) => new Paragraph({ spacing: { after: 50 }, children: [
        new TextRun({ text: `  ${k}  `, font: SERIF, size: 19, bold: true, shading: { type: ShadingType.CLEAR, color: "auto", fill: v.fill } }), t("  " + v.nota, { size: 19 })] })),
      p([t("Las rutas parten de la carpeta "), b("Documentacion y entrega\\Entrega\\"), t(". Las marcadas «Repo:» están en el repositorio de GitHub. Los «§» remiten a los apartados de cada documento.", {})], { spacing: { before: 100, after: 100 } }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("2. Índice de la memoria")] }),
      tabla,
      new Paragraph({ spacing: { before: 100, after: 100 }, children: [b(`Total estimado: ${total.toString().replace(".", ",")} páginas `), t("sin contar los anexos. El objetivo de la guía es unas 50: si una parte crece, se recorta otra o se pasa detalle a los anexos.")] }),

      h1("3. Anexos (H)"),
      p("Máximo 50 páginas. Aquí va el detalle que no cabe en el núcleo."),
      tablaAnexos,

      h1("4. Decisiones que hay que tomar antes de redactar"),
      num([b("Depression Student: "), t("decidir si se mantiene en el modelado con una alerta (AUC 0,998, posible etiqueta generada por fórmula) o se excluye. Afecta a 3.4, 4.4 y a las conclusiones.")]),
      num([b("Tabla b4_dass_item: "), t("existe en el modelo pero está vacía. Cargar las respuestas por ítem del DASS-42 o explicar por qué se deja fuera.")]),
      num([b("67 respondentes del DASS clasificados como «Otro»: "), t("corregirlo a «No reportado» o documentarlo como limitación (efecto de 0,02 puntos).")]),
      num([b("Retroalimentación de la Entrega 3: "), t("incorporarla en 4.6 y donde corresponda cuando llegue.")]),
      num([b("Fechas: "), t("fecha de entrega de la memoria y de la defensa, según el cronograma del aula TFM. Con ellas se arma el Gantt (E.2.v).")]),
      num([b("Formato común: "), t("una plantilla de Word con los mismos estilos de títulos, fuente, numeración de figuras y tablas, y citas en APA 7, para que las partes de cada persona encajen.")]),
      num([b("Reparto: "), t("rellenar la columna «Responsable» y fijar una fecha interna para tener un primer borrador completo.")]),

      h1("5. Cifras de referencia"),
      p("Para que todo el grupo use los mismos números en todos los apartados:"),
      vi("11 datasets organizados en 4 bloques: factores internos, hábitos digitales, percepción emocional y validación psicológica."),
      vi("Modelo relacional v2 de 20 tablas; en Supabase, 19 tablas y 8 vistas."),
      vi("334.318 registros de hechos, de los que 319.318 se incluyen en el modelado."),
      vi("33,68 % de estrés Alto sobre los registros incluidos."),
      vi("49 reglas de calidad, 6 KPIs y 9 insights."),
      vi("Reglas de calidad: 39 OK, 10 avisos y 0 errores. Es la cifra oficial; con la regla B1.3 bien evaluada serían 38 OK y 11 avisos (ver 1.3)."),
      vi("Informe de Power BI con 11 páginas visibles, en versión local y en la nube."),

      h1("6. Bibliografía candidata"),
      p("Referencias de partida para el marco conceptual. Hay que verificar cada una (edición, páginas, DOI) antes de citarla, y añadir las que use cada apartado."),
      vi("Lovibond, S. H., y Lovibond, P. F. (1995). Manual for the Depression Anxiety Stress Scales (2.ª ed.). Psychology Foundation of Australia."),
      vi("Spitzer, R. L., Kroenke, K., Williams, J. B. W., y Löwe, B. (2006). A brief measure for assessing generalized anxiety disorder: The GAD-7. Archives of Internal Medicine, 166(10), 1092-1097."),
      vi("Turcan, E., y McKeown, K. (2019). Dreaddit: A Reddit dataset for stress analysis in social media. Proceedings of the 10th International Workshop on Health Text Mining and Information Analysis (LOUHI)."),
      vi("Pennebaker, J. W., Boyd, R. L., Jordan, K., y Blackburn, K. (2015). The development and psychometric properties of LIWC2015. University of Texas at Austin."),
      vi("Kimball, R., y Ross, M. (2013). The data warehouse toolkit: The definitive guide to dimensional modeling (3.ª ed.). Wiley."),
      vi("Chapman, P., et al. (2000). CRISP-DM 1.0: Step-by-step data mining guide. SPSS."),
      vi("Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830."),
      vi("Los datasets de Kaggle y GitHub, con autor, año y URL (lista completa en Documentacion y entrega\\Enlaces.txt)."),

      h1("7. Después de la memoria: la defensa"),
      vi("Presentación (PowerPoint o similar) para 25 minutos de exposición, seguidos de 15 minutos de preguntas del tribunal (3 personas).", 0, true),
      vi("Asistencia obligatoria de los 5 integrantes, con cámara y micrófono encendidos durante toda la defensa.", 0, true),
      vi("El documento de alcance recomienda entregar la presentación junto con la memoria para que el tutor ayude a mejorarla.", 0, true),
      vi("Sirve de base para las diapositivas: el informe de Power BI, el prototipo web y el resumen ejecutivo."),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(SALIDA, buf); console.log("OK", SALIDA, `total ${total} págs`); });
