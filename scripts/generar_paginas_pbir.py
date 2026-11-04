"""Genera las 7 páginas del informe (formato PBIR: visuals, page.json y pages.json) y ajusta el modelo.

Uso (con Power BI Desktop CERRADO):
    python generar_paginas_pbir.py

Reescribe la carpeta visuals/ de cada página de TFM_Estres.Report y, en el modelo,
fija el orden de rango de edad / niveles y desactiva la suma automática de las
métricas de los modelos. Después se abre TFM_Estres.pbip y se revisa en Desktop.
"""
import hashlib
import json
import os
import re
import shutil
import stat
import time

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "powerbi"))
PAGINAS = os.path.join(RAIZ, "TFM_Estres.Report", "definition", "pages")
TABLAS = os.path.join(RAIZ, "TFM_Estres.SemanticModel", "definition", "tables")
ESQUEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
ANCHO, ALTO, M = 1280, 720, 16


# ---------------------------------------------------------------- expresiones
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def txt(s):
    return lit("'" + s.replace("'", "''") + "'")


def col(tabla, columna):
    return {"Column": {"Expression": {"SourceRef": {"Entity": tabla}}, "Property": columna}}


def med(tabla, medida):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": tabla}}, "Property": medida}}


def proy(campo, nombre=None):
    clave = "Column" if "Column" in campo else "Measure"
    t = campo[clave]["Expression"]["SourceRef"]["Entity"]
    p = campo[clave]["Property"]
    d = {"field": campo, "queryRef": f"{t}.{p}", "nativeQueryRef": p}
    if nombre:
        d["displayName"] = nombre
    return d


def excluir(tabla, columna, valores, tipo="texto"):
    """Filtro de objeto visual: columna NOT IN valores."""
    fmt = (lambda v: f"'{v}'") if tipo == "texto" else (lambda v: f"{v}D")
    return {
        "name": _id("f", tabla, columna, *map(str, valores)),
        "field": col(tabla, columna),
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": "t", "Entity": tabla, "Type": 0}],
            "Where": [{"Condition": {"Not": {"Expression": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": columna}}],
                "Values": [[{"Literal": {"Value": fmt(v)}}] for v in valores]}}}}}],
        },
    }


def incluir(tabla, columna, valores, tipo="texto"):
    """Filtro de objeto visual: columna IN valores."""
    fmt = (lambda v: f"'{v}'") if tipo == "texto" else (lambda v: f"{v}D")
    return {
        "name": _id("f", tabla, columna, *map(str, valores)),
        "field": col(tabla, columna),
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": "t", "Entity": tabla, "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": columna}}],
                "Values": [[{"Literal": {"Value": fmt(v)}}] for v in valores]}}}],
        },
    }


def _id(*partes):
    return hashlib.md5("|".join(partes).encode()).hexdigest()[:20]


# ---------------------------------------------------------------- objetos visuales
def contenedor(nombre, x, y, w, h, z, visual, filtros=None, titulo=None):
    v = {
        "$schema": ESQUEMA,
        "name": nombre,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": visual,
    }
    if titulo:
        visual.setdefault("visualContainerObjects", {})["title"] = [
            {"properties": {"show": lit("true"), "text": txt(titulo)}}]
    if filtros:
        v["filterConfig"] = {"filters": filtros}
    return v


def tarjetas(campos, colores=None):
    """colores: lista de (campo, "#RRGGBB") para colorear el valor de medidas concretas de la tarjeta."""
    # labelDisplayUnits = 1: número completo (319.318) en lugar de la abreviatura automática (319 mil)
    valor = [{"properties": {"labelDisplayUnits": lit("1D")}}]
    for campo, hex_ in colores or []:
        valor.append({"selector": {"metadata": proy(campo)["queryRef"]},
                      "properties": {"fontColor": color(hex_)}})
    return {"visualType": "cardVisual",
            "query": {"queryState": {"Data": {"projections": [proy(c, n) for c, n in campos]}}},
            "objects": {"value": valor}}


def segmentador(campo, nombre):
    return {"visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [proy(campo, nombre)]}}},
            "objects": {"data": [{"properties": {"mode": txt("Dropdown")}}]}}


def eje_largo(objetos, margen=40):
    """Etiquetas de categoría largas (nombres de dataset): más espacio para el eje (maxMarginFactor, %)
    y sin el título del eje, que repite el título del objeto visual."""
    objetos["categoryAxis"] = [{"properties": {"maxMarginFactor": lit(f"{margen}L"),
                                               "showAxisTitle": lit("false")}}]
    return objetos


def barras(categoria, nombre_cat, medidas, serie=None, tipo="clusteredBarChart", orden=None, largo=False):
    estado = {"Category": {"projections": [proy(categoria, nombre_cat)]},
              "Y": {"projections": [proy(c, n) for c, n in medidas]}}
    if serie:
        estado["Series"] = {"projections": [proy(*serie)]}
    v = {"visualType": tipo, "query": {"queryState": estado},
         "objects": {"labels": [{"properties": {"show": lit("true")}}]}}
    if largo:
        eje_largo(v["objects"], 40 if largo is True else largo)
    campo_orden = orden if orden is not None else medidas[0][0]
    v["query"]["sortDefinition"] = {"sort": [{"field": campo_orden,
                                              "direction": "Ascending" if orden is not None else "Descending"}]}
    return v


def barras100(categoria, nombre_cat, medida, serie, colores_serie):
    """Barras horizontales apiladas al 100 %; colores_serie: {valor de la serie: "#RRGGBB"}."""
    col_serie = serie[0]["Column"]
    puntos = [{"properties": {"fill": color(hex_)},
               "selector": {"data": [{"scopeId": {"Comparison": {
                   "ComparisonKind": 0,
                   "Left": {"Column": col_serie},
                   "Right": {"Literal": {"Value": f"'{valor}'"}}}}}]}}
              for valor, hex_ in colores_serie.items()]
    return {"visualType": "hundredPercentStackedBarChart",
            "query": {"queryState": {"Category": {"projections": [proy(categoria, nombre_cat)]},
                                     "Series": {"projections": [proy(*serie)]},
                                     "Y": {"projections": [proy(*medida)]}}},
            "objects": eje_largo({
                # 1 decimal en las etiquetas (10,7 % en lugar de 10,71 %)
                "labels": [{"properties": {"show": lit("true"), "labelPrecision": lit("1L")}}],
                "dataPoint": puntos,
                # el eje de valores (0-100 %) sobra: cada tramo ya muestra su porcentaje, y sin él caben
                # los 9 datasets sin barra de desplazamiento
                "valueAxis": [{"properties": {"show": lit("false"), "showAxisTitle": lit("false")}}]})}


def tabla(campos, totales=False, anchos=None):
    """anchos: {campo: px}. Con anchos fijos y ajuste de texto, la tabla cabe sin barra horizontal."""
    v = {"visualType": "tableEx",
         "query": {"queryState": {"Values": {"projections": [proy(c, n) for c, n in campos]}}},
         "objects": {}}
    if not totales:
        v["objects"]["total"] = [{"properties": {"totals": lit("false")}}]
    if anchos:
        v["objects"]["columnHeaders"] = [{"properties": {"autoSizeColumnWidth": lit("false"),
                                                         "wordWrap": lit("true")}}]
        v["objects"]["values"] = [{"properties": {"wordWrap": lit("true")}}]
        v["objects"]["columnWidth"] = [{"selector": {"metadata": proy(c)["queryRef"]},
                                        "properties": {"value": lit(f"{px}D")}} for c, px in anchos]
    return v


def matriz(filas, columnas, valores, totales=True, ancho_valor=None):
    """totales=False quita la fila y la columna «Total»; ancho_valor fija el ancho (px) de cada columna de valor."""
    v = {"visualType": "pivotTable",
         "query": {"queryState": {
             "Rows": {"projections": [proy(*filas)]},
             "Columns": {"projections": [proy(*columnas)]},
             "Values": {"projections": [proy(c, n) for c, n in valores]}}}}
    obj = {}
    if not totales:
        obj["subTotals"] = [{"properties": {"rowSubtotals": lit("false"), "columnSubtotals": lit("false")}}]
    if ancho_valor:
        obj["columnHeaders"] = [{"properties": {"autoSizeColumnWidth": lit("false"), "wordWrap": lit("true")}}]
        obj["columnWidth"] = [{"selector": {"metadata": proy(c)["queryRef"]},
                               "properties": {"value": lit(f"{ancho_valor}D")}} for c, _ in valores]
    if obj:
        v["objects"] = obj
    return v


def texto(parrafos, color=None):
    """parrafos: lista de (texto, tamaño_pt, negrita); color opcional para todo el texto (#RRGGBB)."""
    return {"visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [
                {"textRuns": [{"value": t, "textStyle": {"fontSize": f"{pt}pt",
                                                         **({"fontWeight": "bold"} if b else {}),
                                                         **({"color": color} if color else {})}}]}
                for t, pt, b in parrafos]}}]}}


def color(hex_):
    return {"solid": {"color": {"expr": {"Literal": {"Value": f"'{hex_}'"}}}}}


def banda(visual, fondo=None):
    """Fondo de color sólido (o transparente si fondo=None), sin borde ni sombra del tema."""
    fondo_obj = ({"show": lit("true"), "color": color(fondo), "transparency": lit("0D")} if fondo
                 else {"show": lit("false")})
    visual.setdefault("visualContainerObjects", {}).update({
        "background": [{"properties": fondo_obj}],
        "border": [{"properties": {"show": lit("false")}}],
        "dropShadow": [{"properties": {"show": lit("false")}}],
    })
    return visual


def navegador():
    return {"visualType": "pageNavigator"}


# ---------------------------------------------------------------- campos
H, DS, G, E, ED, NE = ("vw_hechos_estres", "vw_dim_dataset", "vw_dim_genero",
                       "vw_dim_rango_edad", "vw_dim_nivel_educativo", "vw_dim_nivel_estres")
NLP, SUB, DASS, TRAT = "dwh_nlp_senales", "dim_subreddit", "dwh_dass_severidad", "dwh_brecha_tratamiento"
KPI, KPIC, MOD = "dwh_kpi_resultados", "dwh_kpi_catalogo", "vw_modelo_resultados"


BANDA = "#2A7F7F"  # teal del tema «Bienestar» (TFM_Estres_tema_bienestar.json)


def cabecera(pid, titulo, subtitulo):
    # La caja del título ocupa todo el ancho como banda de color (68 px: título 16 pt + subtítulo 9 pt
    # sin barra de desplazamiento); el navegador va encima, a la derecha, con ~150 px por botón
    x_nav = M + 480 + 12
    return [
        contenedor(_id(pid, "titulo"), 0, 0, ANCHO, 68, 0,
                   banda(texto([(titulo, 16, True), (subtitulo, 9, False)], color="#FFFFFF"), BANDA)),
        # Navegador sin el recuadro blanco que le da el tema: los botones quedan sobre la banda
        contenedor(_id(pid, "nav"), x_nav, 11, ANCHO - x_nav - M, 46, 1, banda(navegador())),
    ]


def segmentadores(pid, y=72):
    w = (ANCHO - 2 * M - 3 * 12) / 4
    campos = [(col(DS, "bloque"), "Bloque"), (col(G, "nombre"), "Género"),
              (col(E, "rango"), "Rango de edad"), (col(ED, "nivel"), "Nivel educativo")]
    # 80 px de alto: con menos, el título del segmentador tapa el desplegable
    return [contenedor(_id(pid, "seg", n), M + i * (w + 12), y, w, 80, 10 + i, segmentador(c, n))
            for i, (c, n) in enumerate(campos)]


# Etiquetas de ≤ 18 caracteres: las tarjetas miden ~200 px y cortaban los nombres largos
KPIS = [("KPI_ESTRES_ALTO", "Estrés Alto (%)"), ("KPI_BRECHA_GENERO", "Brecha M − H (pts)"),
        ("KPI_RIESGO_CRITICO", "Riesgo crítico (%)"), ("KPI_TASA_TRATAMIENTO", "Tratamiento (%)"),
        ("KPI_DISCRIMINANTE_LIWC", "Ratio LIWC"), ("KPI_COBERTURA_DEMO", "Cobertura (%)")]


def pagina0():
    p = "p0"
    v = cabecera(p, "Análisis multidimensional del estrés estudiantil",
                 "TFM Business Analytics e IA · UNIE / INESDI")
    v.append(contenedor(_id(p, "intro"), M, 84, 600, 212, 10, texto([
        ("Qué analiza este informe", 13, True),
        ("12 datasets públicos organizados en 4 bloques analíticos. Cada fuente se estudia por separado y se "
         "compara con las demás mediante un nivel de estrés común (Bajo / Moderado / Alto) y dimensiones "
         "conformes de género, edad y nivel educativo.", 10, False),
        ("319.318 registros en las 9 fuentes con señal real; los 3 datasets sintéticos quedan fuera de las medidas.",
         10, False),
        ("Navega con el menú superior. Las tarjetas de la derecha son los 6 KPIs guardados en el DWH "
         "(última ejecución).", 10, False)])))
    w = (632 - 2 * 12) / 3
    for i, (codigo, nombre) in enumerate(KPIS):
        x, y = 648 + (i % 3) * (w + 12), 84 + (i // 3) * 112
        v.append(contenedor(_id(p, "kpi", codigo), x, y, w, 100, 20 + i,
                            tarjetas([(med(KPI, "Valor KPI (última ejecución)"), nombre)]),
                            filtros=[incluir(KPIC, "codigo", [codigo])]))
    bloques = [
        ("1 · Factores internos", "Academic Stress, Student Anxiety (GAD-7), Student Mental Health Survey. "
         "Student Habits es sintético.", "Panorama y Demografía"),
        ("2 · Hábitos digitales", "Social Media and Mental Health. Social Media vs Sleep y Mental Health "
         "Lifestyle son sintéticos.", "Panorama y Demografía"),
        ("3 · Percepción emocional", "Dreaddit (train y test), texto de Reddit con NLP; Depression Student.",
         "Lenguaje"),
        ("4 · Validación psicológica", "DASS-42 y Mental Health Dataset (búsqueda de tratamiento).",
         "Validación")]
    wb = (ANCHO - 2 * M - 3 * 12) / 4
    for i, (titulo, fuentes, pagina) in enumerate(bloques):
        v.append(contenedor(_id(p, "bloque", titulo), M + i * (wb + 12), 312, wb, 200, 30 + i, texto([
            (titulo, 12, True), (fuentes, 10, False), ("Página principal: " + pagina, 10, True)])))
    v.append(contenedor(_id(p, "nota"), M, 528, ANCHO - 2 * M, 138, 40, texto([
        ("Cómo leer el informe", 12, True),
        ("Cada fuente define «Alto» con su propio criterio nativo, mapeado a un constructo común (GAD-7 y DASS con "
         "baremos clínicos): compara tendencias, no niveles absolutos entre fuentes.", 10, False),
        ("Los segmentadores de Panorama y Demografía filtran por bloque, género, edad y nivel educativo. "
         "Solo el 17 % de los registros informa a la vez género y edad. Modelos y KPIs cubren los cuatro bloques.",
         10, False),
        ("Advertencias: Depression Student (AUC ≈ 1, posible etiqueta generada por fórmula) y Academic Stress "
         "(n = 140) se leen con cautela.", 10, False)])))
    return v


def pagina6():
    p = "p6"
    # La nota de reproducibilidad va en el subtítulo de la banda: así las barras ganan alto y no se desplazan
    # Subtítulo corto: el navegador tapa todo lo que pase de ~380 px
    v = cabecera(p, "KPIs y niveles de estrés", "3 ejecuciones con valores idénticos: cálculo reproducible")
    w_h = 560                         # nombre del KPI (~210 px) + 3 ejecuciones de 100 px
    w_c = ANCHO - 2 * M - 16 - w_h    # 672 px
    alto = 298                        # 6 filas de 2 líneas en el catálogo sin barra vertical
    v.append(contenedor(_id(p, "historico"), M, 84, w_h, alto, 20,
                        matriz((col(KPIC, "nombre"), "KPI"), (col(KPI, "fecha_ejecucion"), "Ejecución"),
                               [(med(KPI, "Valor KPI (última ejecución)"), "Valor")],
                               totales=False, ancho_valor=100),
                        titulo="Histórico de los KPIs por ejecución"))
    v.append(contenedor(_id(p, "catalogo"), M + w_h + 16, 84, w_c, alto, 21,
                        tabla([(col(KPIC, "nombre"), "KPI"), (col(KPIC, "unidad"), "Unidad"),
                               (col(KPIC, "descripcion"), "Definición")],
                              anchos=[(col(KPIC, "nombre"), 168), (col(KPIC, "unidad"), 64),
                                      (col(KPIC, "descripcion"), 395)]),
                        titulo="Catálogo de KPIs"))
    v.append(contenedor(_id(p, "niveles"), M, 84 + alto + 12, ANCHO - 2 * M, 704 - (84 + alto + 12), 30,
                        barras100(col(DS, "dataset"), "Dataset", (med(H, "Registros"), "Registros"),
                                  (col(NE, "nivel"), "Nivel de estrés"),
                                  {"Bajo": "#2A9D8F", "Moderado": "#E9C46A", "Alto": "#E76F51"}),
                        filtros=[incluir(NE, "nivel", ["Bajo", "Moderado", "Alto"])],
                        titulo="Distribución del nivel de estrés por dataset (% de registros)"))
    return v


def pagina1():
    p = "p1"
    v = cabecera(p, "Panorama general del estrés estudiantil",
                 "9 fuentes con señal real · sin los 3 datasets sintéticos")
    v += segmentadores(p)
    v.append(contenedor(_id(p, "kpis"), M, 164, ANCHO - 2 * M, 100, 20, tarjetas([
        (med(H, "Registros"), "Registros"), (med(H, "% Estrés Alto"), "% estrés Alto"),
        (med(H, "% Estrés Alto global (sin filtros)"), "% estrés Alto global"),
        (med(H, "Cobertura demográfica"), "Cobertura demográfica"),
        (med(H, "Fuentes en la selección"), "Fuentes")])))
    w = (ANCHO - 2 * M - 16) / 2
    v.append(contenedor(_id(p, "bloque"), M, 276, w, 390, 30,
                        barras(col(DS, "bloque"), "Bloque", [(med(H, "% Estrés Alto"), "% estrés Alto")]),
                        titulo="% de estrés Alto por bloque analítico"))
    v.append(contenedor(_id(p, "dataset"), M + w + 16, 276, w, 390, 31,
                        barras(col(DS, "dataset"), "Dataset", [(med(H, "% Estrés Alto"), "% estrés Alto")], largo=True),
                        titulo="% de estrés Alto por dataset"))
    v.append(contenedor(_id(p, "nota"), M, 674, ANCHO - 2 * M, 38, 40, texto([(
        "Cada fuente define «Alto» con su propio criterio (escala nativa mapeada a Bajo / Moderado / Alto en "
        "dim_mapeo_estres; GAD-7 y DASS con baremos clínicos). Compara tendencias, no niveles absolutos entre fuentes.",
        9, False)])))
    return v


def pagina2():
    p = "p2"
    v = cabecera(p, "Demografía", "Estrés Alto por género, edad y nivel educativo")
    v += segmentadores(p)
    w = (ANCHO - 2 * M - 2 * 12) / 3
    for i, (c, n, t) in enumerate([(col(G, "nombre"), "Género", G), (col(E, "rango"), "Rango de edad", E),
                                   (col(ED, "nivel"), "Nivel educativo", ED)]):
        prop = c["Column"]["Property"]
        v.append(contenedor(_id(p, "barra", n), M + i * (w + 12), 164, w, 240, 20 + i,
                            barras(c, n, [(med(H, "% Estrés Alto"), "% estrés Alto")],
                                   tipo="clusteredColumnChart", orden=c),
                            filtros=[excluir(t, prop, ["No reportado"])],
                            titulo=f"% de estrés Alto por {n.lower()}"))
    v.append(contenedor(_id(p, "matriz"), M, 416, 920, 250, 30,
                        matriz((col(G, "nombre"), "Género"), (col(E, "rango"), "Rango de edad"),
                               [(med(H, "% Estrés Alto"), "% Alto"), (med(H, "Registros"), "Registros")]),
                        filtros=[excluir(G, "nombre", ["No reportado"]), excluir(E, "rango", ["No reportado"])],
                        titulo="Género × rango de edad"))
    v.append(contenedor(_id(p, "nota"), M + 936, 416, ANCHO - 2 * M - 936, 250, 31, texto([
        ("Cómo leer esta página", 12, True),
        ("Solo el 17 % de los registros informa género y edad a la vez: los filtros demográficos "
         "reducen mucho la muestra.", 10, False),
        ("El 91 % de «Masculino» procede del Mental Health Dataset.", 10, False),
        ("«Otro»: solo 677 registros, leer con cautela.", 10, False),
        ("«No reportado» no se muestra.", 10, False)])))
    return v


def pagina3():
    p = "p3"
    v = cabecera(p, "Lenguaje y estrés (Dreaddit)",
                 "Señales LIWC y sentimiento en posts de Reddit")
    v.append(contenedor(_id(p, "kpis"), M, 72, ANCHO - 2 * M, 110, 20, tarjetas([
        (med(NLP, "Ratio discriminante LIWC"), "Ratio LIWC ansiedad (Alto / Bajo)"),
        (med(NLP, "Sentimiento medio"), "Sentimiento medio"),
        (med(NLP, "Posts analizados"), "Posts analizados")])))
    v.append(contenedor(_id(p, "liwc"), M, 194, 780, 472, 30,
                        barras(col(SUB, "nombre"), "Subreddit",
                               [(med(NLP, "LIWC ansiedad (estrés Alto)"), "Con estrés"),
                                (med(NLP, "LIWC ansiedad (estrés Bajo)"), "Sin estrés")]),
                        titulo="Vocabulario de ansiedad (LIWC) por subreddit"))
    v.append(contenedor(_id(p, "tabla"), M + 796, 194, ANCHO - 2 * M - 796, 472, 31,
                        tabla([(col(SUB, "nombre"), "Subreddit"),
                               (med(NLP, "Ratio discriminante LIWC"), "Ratio"),
                               (med(NLP, "Posts analizados"), "Posts"),
                               (med(NLP, "Sentimiento medio"), "Sentimiento")]),
                        titulo="Detalle por subreddit"))
    v.append(contenedor(_id(p, "nota"), M, 674, ANCHO - 2 * M, 38, 40, texto([(
        "Dreaddit no incluye género ni edad: esta página no usa filtros demográficos. Un ratio > 1 indica más "
        "vocabulario de ansiedad en los posts con estrés.", 9, False)])))
    return v


def pagina4():
    p = "p4"
    v = cabecera(p, "Validación psicológica",
                 "DASS-42 (18-25 años) y búsqueda de tratamiento")
    v.append(contenedor(_id(p, "kpis"), M, 72, 900, 110, 20, tarjetas([
        (med(DASS, "Brecha de género en ansiedad (puntos)"), "Brecha ansiedad M − H (pts)"),
        (med(DASS, "% Estrés severo DASS"), "% estrés severo DASS"),
        (med(TRAT, "% Búsqueda de tratamiento"), "% búsqueda de tratamiento")])))
    v.append(contenedor(_id(p, "kpi3"), M + 916, 72, ANCHO - 2 * M - 916, 110, 21,
                        tarjetas([(med(KPI, "Valor KPI (última ejecución)"), "Riesgo crítico, KPI 3 (%)")]),
                        filtros=[incluir(KPIC, "codigo", ["KPI_RIESGO_CRITICO"])]))
    w = (ANCHO - 2 * M - 16) / 2
    v.append(contenedor(_id(p, "trat"), M, 194, w, 370, 30,
                        barras(col(NE, "nivel"), "Nivel de estrés",
                               [(med(TRAT, "% Búsqueda de tratamiento"), "% busca tratamiento")],
                               serie=(col(TRAT, "antecedentes_familiares"), "Antecedentes familiares"),
                               tipo="clusteredColumnChart", orden=col(NE, "nivel")),
                        filtros=[incluir(NE, "nivel", ["Bajo", "Moderado", "Alto"])],
                        titulo="Búsqueda de tratamiento por nivel de estrés y antecedentes familiares"))
    v.append(contenedor(_id(p, "dass"), M + w + 16, 194, w, 370, 31,
                        barras(col(ED, "nivel"), "Nivel educativo",
                               [(med(DASS, "% Estrés severo DASS"), "% estrés severo")],
                               serie=(col(G, "nombre"), "Género"),
                               tipo="clusteredColumnChart", orden=col(ED, "nivel")),
                        filtros=[excluir(ED, "nivel", ["No reportado"]),
                                 excluir(G, "nombre", ["No reportado", "Otro"])],
                        titulo="DASS-42: % de estrés severo por estudios y género"))
    v.append(contenedor(_id(p, "nota"), M, 576, ANCHO - 2 * M, 90, 40, texto([
        ("Lectura", 11, True),
        ("La búsqueda de tratamiento depende de los antecedentes familiares (≈72 % con antecedentes frente a ≈35 % "
         "sin ellos), no del nivel de estrés percibido: brecha entre malestar y ayuda.", 10, False),
        ("Advertencia: el KPI 3 se calcula sobre Depression Student, cuyo modelo obtuvo AUC 0,998 (posible etiqueta "
         "generada por fórmula). Interpretar con cautela.", 10, False)])))
    return v


def pagina5():
    p = "p5"
    v = cabecera(p, "Modelos predictivos (Objetivo 2)",
                 "Mejor modelo por dataset · CV 5x3 u hold-out según tamaño")
    v.append(contenedor(_id(p, "kpis"), M, 72, 620, 110, 20, tarjetas([
        (med(MOD, "AUC medio sin alertas"), "AUC medio (sin alertas)"),
        (med(MOD, "Modelos con alerta"), "Datasets con alerta")],
        colores=[(med(MOD, "Modelos con alerta"), "#E76F51")])))  # coral del tema: es una advertencia
    v.append(contenedor(_id(p, "nota"), M + 636, 72, ANCHO - 2 * M - 636, 110, 21, texto([
        ("Alertas", 11, True),
        ("Academic Stress: n = 140, el accuracy no supera al baseline (exploratorio).", 10, False),
        ("Depression Student: AUC ≈ 1, posible etiqueta generada por fórmula.", 10, False)])))
    mejores = [incluir(MOD, "es_mejor_modelo", [1], tipo="num")]
    # La columna «alerta» no va en la tabla: su texto es largo y las alertas ya están en la nota de arriba
    v.append(contenedor(_id(p, "auc"), M, 194, 380, 472, 30,
                        barras(col(MOD, "dataset"), "Dataset", [(med(MOD, "AUC medio"), "AUC")], largo=55),
                        filtros=mejores, titulo="AUC del mejor modelo por dataset"))
    v.append(contenedor(_id(p, "tabla"), M + 396, 194, ANCHO - 2 * M - 396, 472, 31,
                        tabla([(col(MOD, "dataset"), "Dataset"), (col(MOD, "modelo"), "Modelo"),
                               (col(MOD, "protocolo"), "Protocolo"), (col(MOD, "n_registros"), "n"),
                               (col(MOD, "auc"), "AUC"), (col(MOD, "f1"), "F1"),
                               (col(MOD, "accuracy"), "Accuracy")]),
                        filtros=mejores, titulo="Detalle del mejor modelo"))
    return v


# ---------------------------------------------------------------- modelo
def ajustar_modelo():
    orden = {"vw_dim_rango_edad.tmdl": ("rango", "id_rango_edad"),
             "vw_dim_nivel_estres.tmdl": ("nivel", "id_nivel_estres"),
             "vw_dim_nivel_educativo.tmdl": ("nivel", "id_nivel_educativo")}
    for archivo, (columna, por) in orden.items():
        ruta = os.path.join(TABLAS, archivo)
        t = open(ruta, encoding="utf-8").read()
        if "sortByColumn" not in t:
            t = t.replace(f"\t\tsourceColumn: {columna}\n",
                          f"\t\tsourceColumn: {columna}\n\t\tsortByColumn: {por}\n", 1)
            open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    ruta = os.path.join(TABLAS, "vw_modelo_resultados.tmdl")
    t = open(ruta, encoding="utf-8").read()
    formatos = {"n_registros": "#,0", "accuracy": "0.000", "f1": "0.000", "auc": "0.000",
                "auc_desv": "0.000", "brecha_acc": "0.000", "es_mejor_modelo": None}
    for c, fmt in formatos.items():
        patron = re.compile(rf"(\tcolumn {c}\n(?:\t\t.*\n|\n)*?)(?=\tcolumn |\tpartition |\tmeasure )")

        def arreglar(m, fmt=fmt):
            b = (m.group(1).replace("summarizeBy: sum", "summarizeBy: none")
                 .replace("SummarizationSetBy = Automatic", "SummarizationSetBy = User"))
            if fmt and "formatString:" not in b:
                b = re.sub(r"(\t\tdataType: \w+\n)", rf"\1\t\tformatString: {fmt}\n", b, count=1)
            return b

        t = patron.sub(arreglar, t)
    open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    # Fecha de ejecución de los KPIs sin segundos (22/10/2026 13:36 en lugar de 22/10/2026 13:36:30)
    ruta = os.path.join(TABLAS, "dwh_kpi_resultados.tmdl")
    t = open(ruta, encoding="utf-8").read()
    t = re.sub(r"(\tcolumn fecha_ejecucion\n\t\tdataType: dateTime\n\t\tformatString: )[^\n]*",
               r"\1dd/mm/yyyy hh:nn", t, count=1)
    open(ruta, "w", encoding="utf-8", newline="\n").write(t)


# ---------------------------------------------------------------- escritura
def _quitar_solo_lectura(funcion, ruta, _exc):
    # OneDrive marca carpetas como solo lectura y Windows no deja borrarlas así
    os.chmod(ruta, stat.S_IWRITE)
    funcion(ruta)


def borrar(carpeta):
    # Además, OneDrive puede bloquear unos segundos una carpeta recién vaciada: reintentar
    for intento in range(10):
        try:
            shutil.rmtree(carpeta, onexc=_quitar_solo_lectura)
            return
        except PermissionError:
            if intento == 9:
                raise
            time.sleep(1)


def escribir(pagina, visuales):
    carpeta = os.path.join(PAGINAS, pagina, "visuals")
    if os.path.isdir(carpeta):
        borrar(carpeta)
    for v in visuales:
        d = os.path.join(carpeta, v["name"])
        os.makedirs(d)
        with open(os.path.join(d, "visual.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"  {pagina}: {len(visuales)} objetos visuales")


ESQUEMA_PAGINA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json"
ESQUEMA_PAGINAS = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"
# (carpeta, nombre en el menú, función). Nombres cortos: con 7 páginas el navegador da ~108 px por botón
PAGINAS_INFORME = [("p0_inicio", "Inicio", pagina0), ("p1_panorama", "1 Panorama", pagina1),
                   ("p2_demografia", "2 Demografía", pagina2), ("p3_lenguaje", "3 Lenguaje", pagina3),
                   ("p4_validacion", "4 Validación", pagina4), ("p5_modelos", "5 Modelos", pagina5),
                   ("p6_kpis", "6 KPIs", pagina6)]


def escribir_paginas():
    for carpeta, nombre, _ in PAGINAS_INFORME:
        os.makedirs(os.path.join(PAGINAS, carpeta), exist_ok=True)
        with open(os.path.join(PAGINAS, carpeta, "page.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"$schema": ESQUEMA_PAGINA, "name": carpeta, "displayName": nombre,
                       "displayOption": "FitToPage", "height": ALTO, "width": ANCHO}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PAGINAS, "pages.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"$schema": ESQUEMA_PAGINAS, "pageOrder": [c for c, _, _ in PAGINAS_INFORME],
                   "activePageName": PAGINAS_INFORME[0][0]}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    escribir_paginas()
    for pagina, _, f in PAGINAS_INFORME:
        escribir(pagina, f())
    ajustar_modelo()
    print("Modelo ajustado (orden de categorías y resumen de métricas).")
