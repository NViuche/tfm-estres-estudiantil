// Plantilla de Word para la memoria final del TFM (estructura A–H de la guía del TFM).
// Uso: node plantilla_memoria.js <salida.docx>
// Los textos en gris cursiva (estilo «Instrucciones») son indicaciones para quien redacta: se borran antes de entregar.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, LevelFormat, HeadingLevel, Footer, Header, PageNumber, TableOfContents, SequentialIdentifier,
  SectionType, VerticalAlign, PageBreak,
} = require("docx");

const [, , SALIDA] = process.argv;
// En el repositorio, los logos se leen desde la raíz (3 niveles por encima de esta carpeta).
const ENTREGA = path.resolve(__dirname, "..", "..", "..");
const AZUL = "1F5C99", GRIS = "6B6B6B", TINTA = "222222", NOTA_FONDO = "F3F3F3";
const SERIF = "Times New Roman", SANS = "Arial";
const ANCHO = 9070; // A4 con márgenes de 2,5 cm
const TITULO = "Análisis multidimensional del estrés estudiantil mediante Business Analytics e Inteligencia Artificial con datos académicos, conductuales y textuales";
const INTEGRANTES = ["Andrés Francisco García Grajales", "Obed Isaí Alvarado Núñez", "Roberto Mario Brochero López",
  "Raúl Cervantes Iglesias", "Santiago Nicolas Viuche Pinilla"];

// ------------------------------------------------------------------ piezas
const t = (text, o = {}) => new TextRun({ text, ...o });
const p = (text, o = {}) => new Paragraph({ children: [t(text)], ...o });
const h1 = (text, salto = true) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: salto, children: [t(text)] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(text)] });
const h3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t(text)] });
// Indicación para quien redacta (se borra antes de entregar)
const ind = (texto) => new Paragraph({ style: "Instrucciones", children: [t("[" + texto + "]")] });
// Indicación de un apartado: qué va, de dónde sale y extensión orientativa
const guia = (contenido, fuente, paginas) => ind(`Qué va aquí: ${contenido} Fuente: ${fuente}. Extensión orientativa: ${paginas}. Responsable: ________.`);
const vi = (texto) => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, children: [t(texto)] });
const pie = (tipo, texto) => new Paragraph({ style: "Caption", children: [t(`${tipo} `), new SequentialIdentifier(tipo), t(`. ${texto}`)] });
const fuente = (texto) => new Paragraph({ style: "Fuente", children: [t("Fuente: " + texto)] });

const borde = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
const celda = (txt, ancho, cab) => new TableCell({
  width: { size: ancho, type: WidthType.DXA }, borders: bordes, verticalAlign: VerticalAlign.CENTER,
  margins: { top: 50, bottom: 50, left: 90, right: 90 },
  shading: cab ? { type: ShadingType.CLEAR, color: "auto", fill: AZUL } : undefined,
  children: [new Paragraph({ style: "TextoTabla", children: [t(txt, cab ? { bold: true, color: "FFFFFF" } : {})] })],
});
const tabla = (cabecera, filas, cols) => new Table({
  width: { size: cols.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: cols,
  rows: [new TableRow({ tableHeader: true, children: cabecera.map((h, n) => celda(h, cols[n], true)) }),
    ...filas.map((f) => new TableRow({ cantSplit: true, children: f.map((x, n) => celda(x, cols[n], false)) }))],
});

const pngTam = (f) => { const x = fs.readFileSync(f); return { w: x.readUInt32BE(16), h: x.readUInt32BE(20) }; };
const logo = (rel, alto) => {
  const f = path.join(ENTREGA, rel);
  if (!fs.existsSync(f)) return t("");
  const { w, h } = pngTam(f);
  return new ImageRun({ type: "png", data: fs.readFileSync(f), transformation: { width: Math.round(alto * w / h), height: alto } });
};

// ------------------------------------------------------------------ cómo usar la plantilla (se borra)
const comoUsar = [
  new Paragraph({ style: "Instrucciones", spacing: { after: 160 }, children: [t("CÓMO USAR ESTA PLANTILLA · BORRAR ESTA PÁGINA ANTES DE ENTREGAR", { bold: true, size: 26 })] }),
  ind("Esta plantilla tiene ya la estructura A–H que pide la guía del TFM, los estilos y la numeración. Escribid encima de las indicaciones en gris y borradlas cuando el apartado esté terminado. Para encontrar las que queden: Inicio → Estilos → clic derecho en «Instrucciones» → Seleccionar todas las instancias."),
  ind("Formato: A4, márgenes de 2,5 cm, Times New Roman 12 con interlineado 1,5 y texto justificado; títulos en Arial azul. No cambiéis la fuente a mano: usad los estilos «Título 1», «Título 2», «Título 3», «Normal», «Descripción» (pies de figura y tabla) y «Bibliografía»."),
  ind("Extensión: unas 50 páginas a una cara (unas 25.000 palabras) sin contar los anexos, que pueden ocupar hasta 50 páginas más. Las extensiones de cada apartado son orientativas y vienen del índice de trabajo (Entrega\\Memoria\\Indice_Memoria_TFM.docx)."),
  ind("Figuras y tablas: cada una lleva un pie con su número automático (Referencias → Insertar título, o copiad un pie de ejemplo) y, debajo, la fuente. Los pies de figura van debajo de la figura; los de tabla, encima de la tabla. Citad cada figura y tabla en el texto antes de que aparezca («como muestra la Figura 3…»)."),
  ind("Cifras: usad siempre las de .memoria\\cifras.md (o el Anexo A de la guía de defensa), con coma decimal y los mismos redondeos. Escribid en primera persona del plural («analizamos», «decidimos»)."),
  ind("Citas en APA 7: en el texto, (Autor, año) o Autor (año); con dos autores, (Lovibond y Lovibond, 1995). Cada cita del texto debe estar en la bibliografía y al revés. Los datasets se citan también."),
  ind("Índices: el índice general, el de figuras y el de tablas se rellenan solos. Si aparecen vacíos o desactualizados: clic derecho sobre ellos → Actualizar campos → Actualizar toda la tabla. Hacedlo siempre justo antes de exportar a PDF."),
  ind("Trabajo en grupo: cada integrante redacta su capítulo en una copia de esta plantilla (por ejemplo, Memoria_Fase2_Nombre.docx) y el coordinador lo pega en el documento principal con «Pegar → Combinar formato». Así se evitan conflictos de OneDrive al editar el mismo archivo a la vez. Anotad cada versión en el registro de .memoria."),
  ind("Entrega: Archivo → Exportar → Crear PDF. El tutor debe aprobar la memoria antes de la defensa."),
];

// ------------------------------------------------------------------ A. Portada
const portada = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 600 },
    children: [logo("powerbi/imagenes/logo_unie.png", 55), t("          "), logo("powerbi/imagenes/logo_inesdi.png", 55)] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [t("TRABAJO FINAL DE MÁSTER", { font: SANS, size: 24, bold: true, color: GRIS })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 700, line: 300 }, children: [t(TITULO, { font: SANS, size: 36, bold: true, color: AZUL })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [t("Autores", { font: SANS, size: 22, bold: true, color: GRIS })] }),
  ...INTEGRANTES.map((n) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [t(n, { size: 24 })] })),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 500, after: 60 }, children: [t("Grupo: ", { bold: true }), t("Grupo LUHN")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t("Programa: ", { bold: true }), t("Máster en Business Analytics e Inteligencia Artificial")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t("INESDI Business Techschool · UNIE Universidad")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t("Tutor académico: ", { bold: true }), t("________________")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t("Fecha de entrega: ", { bold: true }), t("__ de ________ de 2026")] }),
];

// ------------------------------------------------------------------ B y C
const resumenEjecutivo = [
  h1("Resumen ejecutivo", false),
  guia("una sola página. (1) El reto y los objetivos; (2) la metodología, los pasos y las fuentes de datos (11 datasets en 4 bloques, 334.318 registros); (3) una referencia breve al marco conceptual; (4) las conclusiones principales. Se escribe al final, cuando el resto esté cerrado.",
    "Guía de defensa, «El proyecto en dos minutos»; síntesis de las tres entregas", "1 página"),
  p("Escribid aquí el resumen ejecutivo."),
  h2("Palabras clave"),
  p("Estrés estudiantil; Business Analytics; inteligencia artificial; procesamiento del lenguaje natural; Power BI; calidad del dato."),
];

const indices = [
  new Paragraph({ pageBreakBefore: true, style: "TituloIndice", children: [t("Índice")] }),
  new TableOfContents("Índice", { hyperlink: true, headingStyleRange: "1-3" }),
  new Paragraph({ pageBreakBefore: true, style: "TituloIndice", children: [t("Índice de figuras")] }),
  new TableOfContents("Índice de figuras", { hyperlink: true, captionLabelIncludingNumbers: "Figura" }),
  new Paragraph({ spacing: { before: 400 }, style: "TituloIndice", children: [t("Índice de tablas")] }),
  new TableOfContents("Índice de tablas", { hyperlink: true, captionLabelIncludingNumbers: "Tabla" }),
];

// ------------------------------------------------------------------ D. Introducción
const introduccion = [
  h1("1. Introducción"),
  ind("Por qué elegimos este proyecto y presentación general. No hay empresa: el apartado de la empresa se sustituye por el contexto del estrés estudiantil."),
  h2("1.1 Contexto del proyecto"),
  guia("el estrés estudiantil como problema, a quién sirve el análisis (universidades, servicios de bienestar) y la motivación del grupo.", "Propuesta del proyecto; Respuesta a la retroalimentación de la Entrega 1", "1 página"),
  h2("1.2 Problema planteado"),
  guia("qué se quiere entender y por qué hace falta combinar fuentes académicas, conductuales, textuales y clínicas.", "Propuesta (Problema, Enfoque)", "0,5 páginas"),
  h2("1.3 Objetivos del proyecto"),
  guia("los tres objetivos: análisis exploratorio y calidad, modelos de IA y NLP, y dashboards de BI.", "Propuesta (Objetivos)", "0,5 páginas"),
  h2("1.4 Fases del proyecto"),
  guia("las 4 fases del desarrollo (capítulo 4) en un esquema.", "Repo: SEGUIMIENTO.md; guía de defensa, «El recorrido completo»", "0,5 páginas"),
  h2("1.5 Resumen del resultado final"),
  guia("qué se obtuvo: Power BI en local y en la nube, servicio web, 9 insights y modelos predictivos.", "Síntesis Entrega 3 §1, §6 y §8", "0,5 páginas"),
];

// ------------------------------------------------------------------ E. Núcleo
const viabilidad = [
  h1("2. Definición del proyecto y análisis de la viabilidad"),
  h2("2.1 Marco conceptual"),
  guia("estrés académico; escalas clínicas DASS-42 y GAD-7; detección de estrés en texto (NLP, LIWC); BI y datawarehouse dimensional (Kimball). Con citas en APA 7.",
    "Objetivo1_Desarrollo_Completo §1; bibliografía candidata del índice de trabajo (hay que verificarla)", "2 páginas"),
  p("Ejemplo de cita en el texto: la subescala de estrés del DASS-42 se interpreta con los baremos de sus autores (Lovibond y Lovibond, 1995)."),
  h2("2.2 Análisis interno y externo"),
  guia("DAFO del proyecto. Fortalezas: 11 fuentes, gobierno del dato. Debilidades: sin identificador común, datos sintéticos, poblaciones no estudiantiles. Oportunidades y amenazas.", "Repo: SEGUIMIENTO.md (Limitaciones)", "1 página"),
  pie("Tabla", "Análisis DAFO del proyecto."),
  tabla(["", "Factores positivos", "Factores negativos"], [
    ["Internos", "Fortalezas:", "Debilidades:"],
    ["Externos", "Oportunidades:", "Amenazas:"],
  ], [1500, 3785, 3785]),
  fuente("elaboración propia."),
  h2("2.3 Explicación detallada del proyecto"),
  guia("arquitectura completa: fuentes → MySQL → datawarehouse → modelos → Power BI, Supabase y web, con el diagrama de arquitectura.", "Síntesis Entrega 3 §1; Objetivo3\\recursos\\sintesis\\arquitectura.png", "1,5 páginas"),
  ind("Ejemplo de figura: insertad la imagen en un párrafo centrado y, debajo, el pie y la fuente."),
  pie("Figura", "Arquitectura del proyecto: de los 12 ficheros públicos a MySQL, Supabase, Power BI y el servicio web."),
  fuente("elaboración propia."),
  h2("2.4 Objetivos generales y específicos"),
  guia("objetivo general y objetivos específicos medibles, enlazados con los 6 KPIs.", "Propuesta; Objetivo2\\KPIs_TFM.docx", "0,5 páginas"),
];

const planificacion = [
  h1("3. Planificación"),
  h2("3.1 Recursos económicos"),
  guia("coste de las herramientas (todas gratuitas: Python, MySQL/XAMPP, Power BI Desktop, Supabase plan gratuito, GitHub) y coste estimado de las horas de trabajo.", "Nuevo", "1 página"),
  h2("3.2 Recursos materiales"),
  guia("hardware y software utilizados, con sus versiones.", "Síntesis Entrega 3 §3, §4 y §8; Repo: README.md", "0,5 páginas"),
  h2("3.3 Recursos humanos"),
  guia("los 5 integrantes, sus perfiles, sus roles y el reparto real de tareas.", "Nuevo: lo define el grupo", "0,5 páginas"),
  pie("Tabla", "Integrantes, perfiles y responsabilidades."),
  tabla(["Integrante", "Perfil", "Responsabilidades principales"], INTEGRANTES.map((n) => [n, "", ""]), [3200, 2200, 3670]),
  fuente("elaboración propia."),
  h2("3.4 Recursos de tiempo"),
  guia("horas estimadas por fase y por persona.", "Nuevo: cada integrante aporta sus horas", "0,5 páginas"),
  h2("3.5 Cronograma"),
  guia("diagrama de Gantt con las fases y las fechas de las entregas parciales y de la final.", "Cronograma del aula TFM; fechas de envío de las Entregas 1, 2 y 3", "1 página"),
  h2("3.6 Alcance del proyecto"),
  guia("qué entra y qué no: análisis en paralelo más capa global, sin diagnóstico clínico, sin deep learning, y la política para los datos sintéticos.", "Repo: SEGUIMIENTO.md (Limitaciones); Rubricas\\Alcance TFM.pdf", "0,5 páginas"),
];

const desarrollo = [
  h1("4. Desarrollo del proyecto"),
  ind("Dividido según las fases de la planificación. Solo las gráficas clave en el texto; el resto, a los anexos."),
  h2("4.1 Fase 1: datos, calidad y modelo relacional (Entrega 1)"),
  h3("4.1.1 Fuentes y bloques"),
  guia("los 11 datasets en 4 bloques: qué aporta cada uno, filas y columnas, y si es real o sintético.", "Síntesis Objetivo 1 (Bloques 1 a 4); Diccionario de datos.xlsx; Enlaces.txt", "1,5 páginas"),
  h3("4.1.2 Perfilado y análisis exploratorio"),
  guia("resumen del EDA por bloque y los 4 hallazgos transversales.", "Objetivo1_Desarrollo_Completo §1 a §6; Síntesis Objetivo 1; figurasObje1", "4 páginas"),
  h3("4.1.3 Calidad del dato"),
  guia("las 49 reglas de calidad, sus resultados (39 OK, 10 avisos, 0 errores) y las decisiones de preprocesamiento. Incluir como limitación la regla B1.3.", "Reglas de Calidad; .memoria\\memoria-final-y-defensa.md (Limitaciones)", "2 páginas"),
  h3("4.1.4 Modelo relacional y respuesta al tutor"),
  guia("modelo MySQL v2 (20 tablas): claves renombradas, dimensiones conformes y capa en estrella, como respuesta a la retroalimentación de la Entrega 1.", "Respuesta_Retroalimentacion_EntregaI_v3 §1 a §6; Modelo MySQL", "3 páginas"),
  h3("4.1.5 Armonización"),
  guia("cómo se unifican edad, género y nivel educativo entre fuentes.", "Objetivo1\\Armonizacion; notebook 06", "1 página"),
  h2("4.2 Fase 2: ETL, datawarehouse y KPIs (Entrega 2)"),
  h3("4.2.1 Ingesta y transformaciones"),
  guia("el proceso ETL en Python: limpieza, carga y las transformaciones T1–T5.", "Síntesis Entrega 2 §1 y §2; notebook 08", "2 páginas"),
  h3("4.2.2 Datawarehouse en estrella"),
  guia("modelo del datawarehouse (hechos unificados, dimensiones y constelación) con su diagrama.", "PASO4_dwh_estrella.sql; dwh_estrella_ERD.png; Síntesis Entrega 3 §2", "1,5 páginas"),
  h3("4.2.3 KPIs"),
  guia("los 6 KPIs: definición, fórmula, resultado y trazabilidad.", "KPIs_TFM.docx; Síntesis Entrega 2 §3", "1,5 páginas"),
  h3("4.2.4 Verificación"),
  guia("controles de calidad de la carga (14 relaciones, 0 huérfanos).", "Síntesis Entrega 2 §4", "0,5 páginas"),
  h2("4.3 Fase 3: modelado predictivo y NLP (Objetivo 2)"),
  h3("4.3.1 Diseño metodológico"),
  guia("métricas, prevención de fugas de datos, feature engineering y pipeline.", "Síntesis del modelado §1 a §3", "1,5 páginas"),
  h3("4.3.2 Modelos por fuente"),
  guia("tabla comparativa de los resultados por fuente con un breve comentario.", "Síntesis del modelado §4; resultados_modelado_resumen.csv", "2,5 páginas"),
  h3("4.3.3 NLP sobre Dreaddit"),
  guia("detección de estrés en texto: LIWC, TF-IDF e híbrido.", "Síntesis del modelado §5", "1 página"),
  h3("4.3.4 Alerta de Depression Student"),
  guia("el AUC de 0,998 y la decisión final del grupo (mantener con alerta o excluir).", "Síntesis del modelado §6; SEGUIMIENTO.md (Pendiente)", "0,5 páginas"),
  h3("4.3.5 Comparativa y limitaciones"),
  guia("qué modelo funciona mejor y por qué, y los límites de los resultados.", "Síntesis del modelado §7 y §8", "1 página"),
  h2("4.4 Fase 4: explotación con Power BI (Entrega 3)"),
  h3("4.4.1 Modelo semántico y Power BI en local"),
  guia("conexión, modelo semántico, medidas DAX y correcciones.", "Síntesis Entrega 3 §2 y §3", "1,5 páginas"),
  h3("4.4.2 Nube y servicio web"),
  guia("Supabase (PostgreSQL), usuario de solo lectura, API pública y prototipo web.", "Síntesis Entrega 3 §4 y §8; Objetivo3\\supabase\\README.md", "1 página"),
  h3("4.4.3 Diseño del informe"),
  guia("menú, tema y las 11 páginas visibles, con 3 o 4 capturas (el resto, en los anexos).", "Síntesis Entrega 3 §5; capturas p0–p10", "2 páginas"),
  h3("4.4.4 Insights"),
  guia("los 9 insights: qué se observa, cómo se encontró y cautelas.", "Insights_PowerBI_TFM_Estres.docx §2 y §3", "3 páginas"),
  h3("4.4.5 Analítica avanzada"),
  guia("modelos y visuales de IA integrados en el informe (parte opcional de la rúbrica).", "Síntesis Entrega 3 §7", "0,5 páginas"),
  h3("4.4.6 Gobierno del dato y retroalimentación"),
  guia("gobierno del dato (DAMA-DMBOK) y cómo se atendió cada retroalimentación del tutor, incluida la de la Entrega 3.", "Síntesis Entrega 3 §9 y §10; Insights §4; retroalimentación de la Entrega 3 (pendiente)", "1 página"),
];

// ------------------------------------------------------------------ F, G y H
const conclusiones = [
  h1("5. Conclusiones"),
  guia("aportaciones principales, una conclusión por objetivo, recomendaciones de los autores (para universidades), limitaciones y trabajo futuro (datos longitudinales con identificador común, RACI, monitorización de reglas, versiones de librerías fijadas).",
    "Guía de defensa §5.8; SEGUIMIENTO.md (Pendiente y Limitaciones)", "2 páginas"),
  h2("5.1 Conclusiones por objetivo"),
  h2("5.2 Recomendaciones"),
  h2("5.3 Limitaciones y trabajo futuro"),
];

const bibliografia = [
  h1("Bibliografía"),
  guia("todas las referencias citadas, en APA 7 y por orden alfabético: artículos y libros, datasets (Kaggle y GitHub) y software. Usad el estilo «Bibliografía» (sangría francesa).", "Enlaces.txt; bibliografía candidata del índice de trabajo", "2 páginas"),
  ind("Ejemplos de formato (comprobad cada dato antes de usarlos):"),
  new Paragraph({ style: "Bibliografia", children: [t("Lovibond, S. H. y Lovibond, P. F. (1995). "), t("Manual for the Depression Anxiety Stress Scales", { italics: true }), t(" (2.ª ed.). Psychology Foundation.")] }),
  new Paragraph({ style: "Bibliografia", children: [t("Apellido, A. (año). "), t("Título del dataset", { italics: true }), t(" [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/autor/nombre")] }),
  new Paragraph({ style: "Bibliografia", children: [t("Apellido, A. y Apellido, B. (año). Título del artículo. "), t("Nombre de la revista, volumen", { italics: true }), t("(número), páginas. https://doi.org/xxxx")] }),
];

const ANEXOS = [
  ["Anexo A. Diccionario de datos completo", "Objetivo1\\Diccionario de datos.xlsx"],
  ["Anexo B. Catálogo de las 49 reglas de calidad", "Objetivo1\\Reglas de Calidad"],
  ["Anexo C. Fichas de los 6 KPIs", "Objetivo2\\KPIs_TFM.docx"],
  ["Anexo D. Resultados completos del modelado", "Objetivo2\\resultados_modelado_completo.csv"],
  ["Anexo E. Diagramas del modelo relacional y de la estrella", "Objetivo1\\Modelo MySQL; Objetivo2\\dwh_estrella_ERD.png"],
  ["Anexo F. Capturas de las 11 páginas del informe", "Objetivo3\\insights\\capturas"],
  ["Anexo G. Reproducibilidad: repositorio, orden de ejecución y guía de Power BI", "Respuesta a la retroalimentación §8; guia_power_bi.md; Repo: README.md"],
  ["Anexo H. Respuestas completas a las retroalimentaciones", "Respuesta_Retroalimentacion_EntregaI_v3; Síntesis Entrega 3 §10"],
];
const anexos = [
  h1("Anexos"),
  ind("Máximo 50 páginas. Aquí va el detalle que no cabe en el núcleo. Citad cada anexo desde el texto («ver Anexo B»)."),
  ...ANEXOS.flatMap(([titulo, origen], k) => [
    new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: k > 0, children: [t(titulo)] }),
    ind(`Sale de: ${origen}. Responsable: ________.`),
  ]),
];

// ------------------------------------------------------------------ documento
const pagina = { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418, header: 709, footer: 709 } };
const piePagina = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
  new TextRun({ children: [PageNumber.CURRENT], font: SERIF, size: 20, color: GRIS })] })] });
const cabecera = new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF", space: 4 } },
  children: [t("Grupo LUHN · Trabajo Final de Máster", { font: SANS, size: 16, color: GRIS })] })] });

const doc = new Document({
  creator: "Grupo LUHN", title: "Memoria del Trabajo Final de Máster", description: TITULO,
  styles: {
    default: { document: { run: { font: SERIF, size: 24, color: TINTA }, paragraph: { spacing: { after: 120, line: 360 }, alignment: AlignmentType.JUSTIFIED } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 32, bold: true, color: AZUL }, paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 0, after: 240, line: 276 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 26, bold: true, color: AZUL }, paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 300, after: 120, line: 276 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 23, bold: true, color: TINTA }, paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 220, after: 100, line: 276 }, keepNext: true, outlineLevel: 2 } },
      { id: "Caption", name: "Caption", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SERIF, size: 20, bold: true, color: TINTA }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60, line: 240 }, keepNext: true } },
      { id: "Fuente", name: "Fuente de figura o tabla", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SERIF, size: 18, italics: true, color: GRIS }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 40, after: 240, line: 240 } } },
      { id: "TextoTabla", name: "Texto de tabla", basedOn: "Normal", quickFormat: true,
        run: { font: SERIF, size: 20 }, paragraph: { alignment: AlignmentType.LEFT, spacing: { before: 0, after: 0, line: 240 } } },
      { id: "Bibliografia", name: "Bibliografía", basedOn: "Normal", next: "Bibliografia", quickFormat: true,
        paragraph: { alignment: AlignmentType.LEFT, indent: { left: 709, hanging: 709 }, spacing: { after: 120, line: 360 } } },
      { id: "Instrucciones", name: "Instrucciones", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 19, italics: true, color: "7A7A7A" },
        paragraph: { alignment: AlignmentType.LEFT, spacing: { after: 120, line: 260 }, shading: { type: ShadingType.CLEAR, color: "auto", fill: NOTA_FONDO } } },
      { id: "TituloIndice", name: "Título de índice", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 32, bold: true, color: AZUL }, paragraph: { alignment: AlignmentType.LEFT, spacing: { after: 240 } } },
    ],
  },
  numbering: { config: [{ reference: "vinetas", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] }] },
  sections: [
    { properties: { page: pagina }, children: comoUsar },
    { properties: { page: pagina, type: SectionType.NEXT_PAGE }, children: portada },
    { properties: { page: { ...pagina, pageNumbers: { start: 1 } }, type: SectionType.NEXT_PAGE },
      headers: { default: cabecera }, footers: { default: piePagina },
      children: [...resumenEjecutivo, ...indices, ...introduccion, ...viabilidad, ...planificacion, ...desarrollo, ...conclusiones, ...bibliografia, ...anexos] },
  ],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(SALIDA, buf); console.log("OK", SALIDA); });
