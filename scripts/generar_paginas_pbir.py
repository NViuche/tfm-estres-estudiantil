"""Genera las páginas del informe (formato PBIR: visuals, page.json y pages.json) y ajusta el modelo.

8 páginas visibles (Inicio, 1 Panorama … 6 KPIs, 7 Explorar) y 2 ocultas: «Detalle del dataset» (drill-through)
y «Tooltip del dataset» (tooltip de página). Registra en report.json las imágenes de ../powerbi/imagenes
(generadas por generar_imagenes.py): iconos de los bloques y fondo de Inicio.

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


def tarjetas(campos, colores=None, tam=None):
    """colores: lista de (campo, "#RRGGBB") para colorear el valor de medidas concretas de la tarjeta.
    tam: tamaño del valor en pt (para tarjetas pequeñas, como las del tooltip)."""
    # labelDisplayUnits = 1: número completo (319.318) en lugar de la abreviatura automática (319 mil)
    props = {"labelDisplayUnits": lit("1D")}
    if tam:
        props["fontSize"] = lit(f"{tam}D")
    valor = [{"properties": props}]
    for campo, hex_ in colores or []:
        valor.append({"selector": {"metadata": proy(campo)["queryRef"]},
                      "properties": {"fontColor": color(hex_)}})
    objetos = {"value": valor}
    if tam:
        objetos["label"] = [{"properties": {"fontSize": lit("9D")}}]
    return {"visualType": "cardVisual",
            "query": {"queryState": {"Data": {"projections": [proy(c, n) for c, n in campos]}}},
            "objects": objetos}


def segmentador(campo, nombre):
    # syncGroup: el mismo segmentador en varias páginas comparte la selección (Panorama, Demografía, Explorar)
    return {"visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [proy(campo, nombre)]}}},
            "objects": {"data": [{"properties": {"mode": txt("Dropdown")}}]},
            "syncGroup": {"groupName": nombre, "fieldChanges": True, "filterChanges": True}}


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
    # Sin páginas ocultas (Detalle del dataset) ni de tooltip: solo se llega a ellas desde los gráficos
    return {"visualType": "pageNavigator",
            "objects": {"pages": [{"properties": {"showHiddenPages": lit("false"), "showTooltipPages": lit("false")}}]}}


# ---------------------------------------------------------------- imágenes y funciones avanzadas
def recurso(item):
    """Referencia a una imagen registrada en StaticResources/RegisteredResources (PackageType 1)."""
    return {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": item}}}


def imagen(item):
    return banda({"visualType": "image",
                  "objects": {"general": [{"properties": {"imageUrl": recurso(item)}}],
                              "imageScaling": [{"properties": {"imageScalingType": txt("Fit")}}]}})


def con_tooltip(visual, pagina_tooltip):
    """Asigna una página de tooltip (tipo «Canvas» = página del informe) a un objeto visual."""
    visual.setdefault("visualContainerObjects", {})["visualTooltip"] = [{"properties": {
        "show": lit("true"), "type": txt("Canvas"), "section": txt(pagina_tooltip)}}]
    return visual


def boton_volver():
    """Botón «Volver» de las páginas de obtención de detalles (drill-through)."""
    # Los botones guardan su formato por estado: sin el selector {"id": "default"} no se pintan ni icono ni texto
    defecto = {"id": "default"}
    v = {"visualType": "actionButton",
         "objects": {
             "icon": [{"selector": defecto, "properties": {"show": lit("true"), "shapeType": txt("back"),
                                                           "lineColor": color(BANDA), "horizontalAlignment": txt("left")}}],
             "text": [{"selector": defecto, "properties": {"show": lit("true"), "text": txt("Volver"),
                                                           "fontColor": color(BANDA), "fontSize": lit("11D")}}],
             "outline": [{"selector": defecto, "properties": {"show": lit("true"), "lineColor": color(BANDA)}}]},
         "visualContainerObjects": {"visualLink": [{"properties": {"show": lit("true"), "type": txt("Back")}}]}}
    return v


def colores_niveles(col_nivel):
    """Selectores de color por nivel de estrés (Bajo teal, Moderado arena, Alto coral)."""
    return [{"properties": {"fill": color(hex_)},
             "selector": {"data": [{"scopeId": {"Comparison": {"ComparisonKind": 0, "Left": {"Column": col_nivel},
                                                               "Right": {"Literal": {"Value": f"'{nivel}'"}}}}}]}}
            for nivel, hex_ in (("Bajo", "#2A9D8F"), ("Moderado", "#E9C46A"), ("Alto", "#E76F51"))]


def anillo(categoria, nombre_cat, medida):
    col_cat = categoria["Column"]
    return {"visualType": "donutChart",
            "query": {"queryState": {"Category": {"projections": [proy(categoria, nombre_cat)]},
                                     "Y": {"projections": [proy(*medida)]}}},
            "objects": {"dataPoint": colores_niveles(col_cat),
                        "labels": [{"properties": {"show": lit("true"), "labelStyle": txt("Percent of total")}}],
                        "legend": [{"properties": {"show": lit("true"), "position": txt("Top")}}]}}


def arbol(medida, explicar):
    """Árbol de descomposición: la medida se desglosa por los campos que el usuario elija, en el orden que quiera."""
    return {"visualType": "decompositionTreeVisual",
            "query": {"queryState": {"Analyze": {"projections": [proy(*medida)]},
                                     "ExplainBy": {"projections": [proy(c, n) for c, n in explicar]}}}}


def influenciadores(objetivo, explicar):
    """Influenciadores clave: qué valores elevan la probabilidad de cada nivel del objetivo.
    El objetivo es una columna de la tabla de hechos: el análisis se hace por registro (no admite «Expandir por»)."""
    return {"visualType": "keyDriversVisual",
            "query": {"queryState": {"Target": {"projections": [proy(*objetivo)]},
                                     "ExplainBy": {"projections": [proy(c, n) for c, n in explicar]}}}}


def barras_jerarquia(niveles, medida):
    """Barras con jerarquía (bloque → dataset): las flechas de obtención de detalles bajan de nivel."""
    proyecciones = [proy(c, n) for c, n in niveles]
    proyecciones[0]["active"] = True
    return {"visualType": "clusteredBarChart",
            "query": {"queryState": {"Category": {"projections": proyecciones},
                                     "Y": {"projections": [proy(*medida)]}},
                      "sortDefinition": {"sort": [{"field": medida[0], "direction": "Descending"}]}},
            "objects": {"labels": [{"properties": {"show": lit("true")}}]}}


# ---------------------------------------------------------------- campos
H, DS, G, E, ED, NE = ("vw_hechos_estres", "vw_dim_dataset", "vw_dim_genero",
                       "vw_dim_rango_edad", "vw_dim_nivel_educativo", "vw_dim_nivel_estres")
NLP, SUB, DASS, TRAT = "dwh_nlp_senales", "dim_subreddit", "dwh_dass_severidad", "dwh_brecha_tratamiento"
KPI, KPIC, MOD = "dwh_kpi_resultados", "dwh_kpi_catalogo", "vw_modelo_resultados"
CR, CC = "dwh_calidad_reglas", "dwh_calidad_controles"   # calidad del dato (cargar_calidad_dato.py)
COLORES_ESTADO = {"OK": "#2A9D8F", "AVISO": "#E9C46A", "ERROR": "#E76F51"}


def barras_apiladas(categoria, nombre_cat, medida, serie, colores_serie):
    """Barras horizontales apiladas (recuento) con un color fijo por valor de la serie."""
    col_serie = serie[0]["Column"]
    puntos = [{"properties": {"fill": color(hex_)},
               "selector": {"data": [{"scopeId": {"Comparison": {
                   "ComparisonKind": 0, "Left": {"Column": col_serie},
                   "Right": {"Literal": {"Value": f"'{valor}'"}}}}}]}}
              for valor, hex_ in colores_serie.items()]
    return {"visualType": "barChart",
            "query": {"queryState": {"Category": {"projections": [proy(categoria, nombre_cat)]},
                                     "Series": {"projections": [proy(*serie)]},
                                     "Y": {"projections": [proy(*medida)]}},
                      "sortDefinition": {"sort": [{"field": medida[0], "direction": "Descending"}]}},
            "objects": {"labels": [{"properties": {"show": lit("true")}}], "dataPoint": puntos,
                        "legend": [{"properties": {"show": lit("true"), "position": txt("Top")}}]}}


BANDA = "#2A7F7F"  # teal del tema «Bienestar» (TFM_Estres_tema_bienestar.json)


def cabecera(pid, titulo, subtitulo):
    # La caja del título ocupa todo el ancho como banda de color (68 px: título 16 pt + subtítulo 9 pt
    # sin barra de desplazamiento); el navegador va encima, a la derecha: 9 botones de ~94 px, así que los
    # títulos de la banda deben caber en ~400 px (16 pt) y los subtítulos en ~400 px (9 pt)
    x_nav = 420
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
    # Título corto: con 8 botones el menú empieza en x = 400
    # Subtítulo corto: no llega bajo los logos, que ya identifican a UNIE e INESDI
    v = cabecera(p, "Estrés estudiantil", "TFM · Business Analytics e IA")
    # Logos en blanco sobre la banda, centrados en su alto (generar_imagenes.py los crea desde recursos/logos).
    # Caben entre el título (~200 px) y el menú (x = 420); el subtítulo corto no llega hasta ellos
    hay = lambda f: os.path.exists(os.path.join(RAIZ, "imagenes", f))
    if hay("logo_inesdi_blanco.png") and hay("logo_unie_blanco.png"):
        v.append(contenedor(_id(p, "logo"), 212, 24, 120, 20, 2, imagen("logo_inesdi_blanco.png")))
        v.append(contenedor(_id(p, "logo_sep"), 340, 14, 3, 40, 2, imagen("separador_blanco.png")))
        v.append(contenedor(_id(p, "logo_unie"), 350, 15, 69, 38, 2, imagen("logo_unie_blanco.png")))
    elif hay("logo_inesdi_blanco.png"):
        v.append(contenedor(_id(p, "logo"), 216, 12, 150, 25, 2, imagen("logo_inesdi_blanco.png")))
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
         "Student Habits es sintético.", "Panorama y Demografía", "icono_factores_internos.png"),
        ("2 · Hábitos digitales", "Social Media and Mental Health. Social Media vs Sleep y Mental Health "
         "Lifestyle son sintéticos.", "Panorama y Demografía", "icono_habitos_digitales.png"),
        ("3 · Percepción emocional", "Dreaddit (train y test), texto de Reddit con NLP; Depression Student.",
         "Lenguaje", "icono_percepcion_emocional.png"),
        ("4 · Validación psicológica", "DASS-42 y Mental Health Dataset (búsqueda de tratamiento).",
         "Validación", "icono_validacion_psicologica.png")]
    wb = (ANCHO - 2 * M - 3 * 12) / 4
    for i, (titulo, fuentes, pagina, icono) in enumerate(bloques):
        x = M + i * (wb + 12)
        # Icono arriba y texto debajo: así el icono nunca tapa el título del bloque
        v.append(contenedor(_id(p, "bloque", titulo), x, 312, wb, 200, 30 + i, texto([
            (" ", 26, False), (titulo, 12, True), (fuentes, 10, False), ("Página principal: " + pagina, 10, True)])))
        v.append(contenedor(_id(p, "icono", titulo), x + 10, 318, 44, 44, 35 + i, imagen(icono)))
    v.append(contenedor(_id(p, "nota"), M, 528, ANCHO - 2 * M, 138, 40, texto([
        ("Cómo leer el informe", 12, True),
        ("Cada fuente define «Alto» con su propio criterio nativo, mapeado a un constructo común (GAD-7 y DASS con "
         "baremos clínicos): compara tendencias, no niveles absolutos entre fuentes.", 10, False),
        ("Los segmentadores de Panorama, Demografía y Explorar están sincronizados: la selección se mantiene al cambiar "
         "de página. Explorar desglosa el estrés Alto con un árbol de descomposición y los influenciadores clave. Clic "
         "derecho sobre un dataset → Obtener detalles abre su ficha; al pasar el ratón por las barras de Panorama se ve "
         "su resumen. Solo el 17 % de los registros informa a la vez género y edad.", 10, False),
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


EXPLORAR, DETALLE, TOOLTIP = "p7_explorar", "p8_detalle_dataset", "p9_tooltip_dataset"
CALIDAD = "p10_calidad"
ALTO_EXPLORAR = 1000
ALTO_CALIDAD = 1450
FILTRO_DETALLE = "filtro_detalle_dataset"
NIVELES = incluir(NE, "nivel", ["Bajo", "Moderado", "Alto"])
INCLUIDOS = incluir(DS, "uso_modelado", ["incluido"])


def pagina7():
    """Explorar: árbol de descomposición e influenciadores clave (visuales de IA de Power BI).
    El árbol ocupa todo el ancho: en 1248 px caben la raíz y los 5 campos de desglose (cada nivel mide ~137 px)."""
    p = "p7"
    v = cabecera(p, "Explorar el estrés Alto", "Árbol: «+» para desglosar · Influenciadores: elige «Alto»")
    v += segmentadores(p)
    # Página más alta (1000 px, «Ajustar al ancho»): el árbol y los influenciadores se ven completos con desplazamiento vertical
    v.append(contenedor(_id(p, "arbol"), M, 164, ANCHO - 2 * M, 400, 30,
                        arbol((med(H, "% Estrés Alto"), "% estrés Alto"),
                              [(col(DS, "bloque"), "Bloque"), (col(DS, "dataset"), "Dataset"), (col(G, "nombre"), "Género"),
                               (col(E, "rango"), "Rango de edad"), (col(ED, "nivel"), "Nivel educativo")]),
                        titulo="Árbol de descomposición: % de estrés Alto"))
    v.append(contenedor(_id(p, "influ"), M, 576, ANCHO - 2 * M, 410, 31,
                        influenciadores((col(H, "nivel_estres"), "Nivel de estrés"),
                                        [(col(G, "nombre"), "Género"), (col(E, "rango"), "Rango de edad"),
                                         (col(ED, "nivel"), "Nivel educativo"), (col(DS, "bloque"), "Bloque")]),
                        filtros=[incluir(H, "nivel_estres", ["Bajo", "Moderado", "Alto"]), INCLUIDOS],
                        titulo="Influenciadores clave del nivel de estrés"))
    return v


def pagina8():
    """Detalle del dataset: página de obtención de detalles (drill-through) sobre vw_dim_dataset[dataset]."""
    p = "p8"
    v = cabecera(p, "Detalle del dataset", "Ficha del dataset elegido · «Volver» regresa a la página anterior")
    v.append(contenedor(_id(p, "volver"), M, 80, 120, 34, 5, boton_volver()))
    v.append(contenedor(_id(p, "ficha"), M, 124, 560, 112, 10,
                        tabla([(col(DS, "dataset"), "Dataset"), (col(DS, "bloque"), "Bloque"),
                               (col(DS, "calidad"), "Calidad"), (col(DS, "uso_modelado"), "Modelado")],
                              anchos=[(col(DS, "dataset"), 220), (col(DS, "bloque"), 150),
                                      (col(DS, "calidad"), 75), (col(DS, "uso_modelado"), 75)]),
                        titulo="Ficha"))
    v.append(contenedor(_id(p, "kpis"), M + 576, 80, ANCHO - 2 * M - 576, 156, 11, tarjetas([
        (med(H, "Registros"), "Registros"), (med(H, "% Estrés Alto"), "% estrés Alto"),
        (med(H, "% Estrés Moderado"), "% Moderado"), (med(H, "Cobertura demográfica"), "Cobertura")])))
    w = (ANCHO - 2 * M - 2 * 12) / 3
    v.append(contenedor(_id(p, "anillo"), M, 248, w, 220, 20,
                        anillo(col(NE, "nivel"), "Nivel de estrés", (med(H, "Registros"), "Registros")),
                        filtros=[NIVELES], titulo="Distribución por nivel de estrés"))
    for i, (c, n, t) in enumerate([(col(G, "nombre"), "Género", G), (col(E, "rango"), "Rango de edad", E)]):
        prop = c["Column"]["Property"]
        v.append(contenedor(_id(p, "barra", n), M + (i + 1) * (w + 12), 248, w, 220, 21 + i,
                            barras(c, n, [(med(H, "% Estrés Alto"), "% estrés Alto")], tipo="clusteredColumnChart", orden=c),
                            filtros=[excluir(t, prop, ["No reportado"])], titulo=f"% de estrés Alto por {n.lower()}"))
    v.append(contenedor(_id(p, "educ"), M, 480, w, 224, 24,
                        barras(col(ED, "nivel"), "Nivel educativo", [(med(H, "% Estrés Alto"), "% estrés Alto")],
                               tipo="clusteredColumnChart", orden=col(ED, "nivel")),
                        filtros=[excluir(ED, "nivel", ["No reportado"])], titulo="% de estrés Alto por nivel educativo"))
    v.append(contenedor(_id(p, "modelo"), M + w + 12, 480, ANCHO - 2 * M - w - 12, 224, 25,
                        tabla([(col(MOD, "modelo"), "Modelo"), (col(MOD, "protocolo"), "Protocolo"),
                               (col(MOD, "n_registros"), "n"), (col(MOD, "auc"), "AUC"), (col(MOD, "f1"), "F1"),
                               (col(MOD, "accuracy"), "Accuracy"), (col(MOD, "alerta"), "Alerta")],
                              anchos=[(col(MOD, "modelo"), 200), (col(MOD, "protocolo"), 110), (col(MOD, "n_registros"), 60),
                                      (col(MOD, "auc"), 50), (col(MOD, "f1"), 50), (col(MOD, "accuracy"), 65),
                                      (col(MOD, "alerta"), 250)]),
                        filtros=[incluir(MOD, "es_mejor_modelo", [1], tipo="num")],
                        titulo="Mejor modelo del dataset (Objetivo 2)"))
    return v


def pagina9():
    """Tooltip del dataset (320 × 240): aparece al pasar el ratón por las barras de dataset y bloque."""
    p = "p9"
    v = [contenedor(_id(p, "kpis"), 6, 6, 308, 72, 1, tarjetas([
             (med(H, "Registros"), "Registros"), (med(H, "% Estrés Alto"), "% estrés Alto")], tam=16)),
         contenedor(_id(p, "anillo"), 6, 84, 308, 150, 2,
                    anillo(col(NE, "nivel"), "Nivel", (med(H, "Registros"), "Registros")), filtros=[NIVELES],
                    titulo="Nivel de estrés")]
    return v


def pagina10():
    """Calidad del dato: reglas del notebook 05, completitud por dataset y registro de controles (gobierno del dato).
    Página alta (1450 px, «Ajustar al ancho»): las tablas se ven completas, sin barra de desplazamiento propia."""
    p = "p10"
    v = cabecera(p, "Calidad del dato", "49 reglas de calidad y 17 controles de validación")
    v.append(contenedor(_id(p, "kpis"), M, 72, ANCHO - 2 * M, 100, 20, tarjetas([
        (med(CR, "Reglas"), "Reglas evaluadas"), (med(CR, "% reglas superadas"), "% reglas superadas"),
        (med(CR, "Reglas con aviso"), "Reglas con aviso"), (med(CR, "Reglas con error"), "Reglas con error"),
        (med(CC, "Controles superados"), "Controles superados"), (med(CC, "Controles con aviso"), "Controles con aviso")],
        colores=[(med(CR, "Reglas con aviso"), "#C9A227"), (med(CC, "Controles con aviso"), "#C9A227")])))
    w_dim = 420
    v.append(contenedor(_id(p, "dimension"), M, 184, w_dim, 350, 30,
                        barras_apiladas(col(CR, "dimension"), "Dimensión", (med(CR, "Reglas"), "Reglas"),
                                        (col(CR, "estado"), "Estado"), COLORES_ESTADO),
                        titulo="Reglas por dimensión de calidad"))
    v.append(contenedor(_id(p, "completitud"), M + w_dim + 16, 184, ANCHO - 2 * M - w_dim - 16, 350, 31,
                        tabla([(col(DS, "dataset"), "Dataset"), (med(H, "Registros (12 fuentes)"), "Registros"),
                               (med(H, "% género informado"), "Género"), (med(H, "% edad informada"), "Edad"),
                               (med(H, "% nivel educativo informado"), "Nivel educativo"),
                               (med(H, "% nivel de estrés asignado"), "Nivel de estrés")], totales=True,
                              anchos=[(col(DS, "dataset"), 250), (med(H, "Registros (12 fuentes)"), 90),
                                      (med(H, "% género informado"), 95), (med(H, "% edad informada"), 95),
                                      (med(H, "% nivel educativo informado"), 115),
                                      (med(H, "% nivel de estrés asignado"), 115)]),
                        titulo="Completitud por dataset (% de registros con el campo informado)"))
    v.append(contenedor(_id(p, "avisos"), M, 546, ANCHO - 2 * M, 400, 40,
                        tabla([(col(DS, "dataset"), "Dataset"), (col(CR, "regla"), "Regla"),
                               (col(CR, "dimension"), "Dimensión"), (col(CR, "incumplen"), "Incumplen"),
                               (col(CR, "pct_incumplen"), "% incumplen"), (col(CR, "accion"), "Tratamiento")],
                              anchos=[(col(DS, "dataset"), 190), (col(CR, "regla"), 360), (col(CR, "dimension"), 100),
                                      (col(CR, "incumplen"), 80), (col(CR, "pct_incumplen"), 85),
                                      (col(CR, "accion"), 400)]),
                        filtros=[incluir(CR, "estado", ["AVISO", "ERROR"])],
                        titulo="Reglas con aviso y su tratamiento (ninguna bloquea la carga)"))
    v.append(contenedor(_id(p, "controles"), M, 958, ANCHO - 2 * M, 480, 41,
                        tabla([(col(CC, "fase"), "Fase"), (col(CC, "control"), "Control"),
                               (col(CC, "resultado"), "Resultado"), (col(CC, "estado"), "Estado"),
                               (col(CC, "origen"), "Origen")],
                              anchos=[(col(CC, "fase"), 90), (col(CC, "control"), 220), (col(CC, "resultado"), 600),
                                      (col(CC, "estado"), 70), (col(CC, "origen"), 200)]),
                        titulo="Registro de controles de validación: carga, ETL, migración, seguridad e informe"))
    return v


def pagina1():
    p = "p1"
    v = cabecera(p, "Panorama del estrés estudiantil",
                 "9 fuentes con señal real · sin los 3 datasets sintéticos")
    v += segmentadores(p)
    v.append(contenedor(_id(p, "kpis"), M, 164, ANCHO - 2 * M, 100, 20, tarjetas([
        (med(H, "Registros"), "Registros"), (med(H, "% Estrés Alto"), "% estrés Alto"),
        (med(H, "% Estrés Alto global (sin filtros)"), "% estrés Alto global"),
        (med(H, "Cobertura demográfica"), "Cobertura demográfica"),
        (med(H, "Fuentes en la selección"), "Fuentes")])))
    w = (ANCHO - 2 * M - 16) / 2
    # Bloque → dataset: jerarquía con obtención de detalles; las dos gráficas llevan el tooltip de página del dataset
    v.append(contenedor(_id(p, "bloque"), M, 276, w, 390, 30,
                        con_tooltip(barras_jerarquia([(col(DS, "bloque"), "Bloque"), (col(DS, "dataset"), "Dataset")],
                                                     (med(H, "% Estrés Alto"), "% estrés Alto")), TOOLTIP),
                        titulo="% de estrés Alto por bloque (↓ baja a dataset)"))
    v.append(contenedor(_id(p, "dataset"), M + w + 16, 276, w, 390, 31,
                        con_tooltip(barras(col(DS, "dataset"), "Dataset", [(med(H, "% Estrés Alto"), "% estrés Alto")],
                                           largo=True), TOOLTIP),
                        titulo="% de estrés Alto por dataset"))
    v.append(contenedor(_id(p, "nota"), M, 674, ANCHO - 2 * M, 38, 40, texto([(
        "Compara tendencias, no niveles absolutos: cada fuente define «Alto» con su criterio (GAD-7 y DASS con baremos "
        "clínicos). Pasa el ratón por una barra para ver el resumen del dataset; clic derecho → Obtener detalles abre su ficha.",
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
    # Nivel de estrés como columna calculada de la tabla de hechos: los influenciadores clave analizan por fila de
    # la tabla del campo objetivo, así que el objetivo tiene que estar en los hechos (no en la dimensión)
    ruta = os.path.join(TABLAS, "vw_hechos_estres.tmdl")
    t = open(ruta, encoding="utf-8").read()
    if "column nivel_estres" not in t:
        columna = ("\tcolumn nivel_estres = RELATED ( vw_dim_nivel_estres[nivel] )\n"
                   "\t\tdataType: string\n"
                   "\t\tlineageTag: 6c1f0e2a-7d3b-4f6e-9a51-2b8f3c4d5e61\n"
                   "\t\tsummarizeBy: none\n\n"
                   "\t\tannotation SummarizationSetBy = Automatic\n\n")
        i = t.index("\tpartition ")
        t = t[:i] + columna + t[i:]
        open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    modelo_calidad()


# ---------------------------------------------------------------- modelo: calidad del dato
def _tag(*partes):
    """lineageTag estable (el mismo en cada ejecución) a partir del nombre del objeto."""
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "tfm-estres/" + "/".join(partes)))


def _tabla_tmdl(nombre, columnas, medidas):
    """columnas: [(nombre, "texto"|"numero", formato|None, oculta)]; medidas: [(nombre, DAX, formato)]."""
    def ident(n):
        return n if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", n) else "'" + n + "'"
    t = [f"table {nombre}", f"\tlineageTag: {_tag(nombre)}", ""]
    for m, dax, fmt in medidas:
        t += [f"\tmeasure {ident(m)} = {dax}", f"\t\tformatString: {fmt}", "\t\tdisplayFolder: Calidad del dato",
              f"\t\tlineageTag: {_tag(nombre, 'medida', m)}", ""]
    for c, tipo, fmt, oculta in columnas:
        t += [f"\tcolumn {c}", f"\t\tdataType: {'string' if tipo == 'texto' else 'double'}"]
        if fmt:
            t.append(f"\t\tformatString: {fmt}")
        if oculta:
            t.append("\t\tisHidden")
        t += [f"\t\tlineageTag: {_tag(nombre, c)}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: {c}", ""]
        if tipo != "texto" and not fmt:
            t += ['\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}', ""]
    t += [f"\tpartition {nombre} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
          f'\t\t\t\t\tOrigen = fnTabla("{nombre}")', "\t\t\t\tin", "\t\t\t\t\tOrigen", ""]
    return "\n".join(t) + "\n"


TABLAS_CALIDAD = {
    CR: ([("id_regla", "numero", None, True), ("id_dataset", "numero", None, True), ("regla", "texto", None, False),
          ("dimension", "texto", None, False), ("evaluados", "numero", "#,0", False), ("incumplen", "numero", "#,0", False),
          ("pct_incumplen", "numero", "0.00", False), ("estado", "texto", None, False), ("accion", "texto", None, False),
          ("fase", "texto", None, False)],
         [("Reglas", "COUNTROWS ( dwh_calidad_reglas )", "#,0"),
          ("Reglas OK", 'CALCULATE ( [Reglas], dwh_calidad_reglas[estado] = "OK" ) + 0', "#,0"),
          ("Reglas con aviso", 'CALCULATE ( [Reglas], dwh_calidad_reglas[estado] = "AVISO" ) + 0', "#,0"),
          ("Reglas con error", 'CALCULATE ( [Reglas], dwh_calidad_reglas[estado] = "ERROR" ) + 0', "#,0"),
          ("% reglas superadas", "DIVIDE ( [Reglas OK], [Reglas] )", "0.0%")]),
    CC: ([("id_control", "numero", None, True), ("fase", "texto", None, False), ("control", "texto", None, False),
          ("resultado", "texto", None, False), ("estado", "texto", None, False), ("origen", "texto", None, False)],
         [("Controles", "COUNTROWS ( dwh_calidad_controles )", "#,0"),
          ("Controles superados", 'CALCULATE ( [Controles], dwh_calidad_controles[estado] = "OK" ) + 0', "#,0"),
          ("Controles con aviso", 'CALCULATE ( [Controles], dwh_calidad_controles[estado] = "AVISO" ) + 0', "#,0")]),
}
# Completitud sobre los 12 datasets (sin filtrar uso_modelado): el id 0 es «No reportado» / «No aplica»
MEDIDAS_COMPLETITUD = [
    ("Registros (12 fuentes)", "COUNTROWS ( vw_hechos_estres )", "#,0"),
    ("% género informado", "DIVIDE ( CALCULATE ( COUNTROWS ( vw_hechos_estres ), vw_hechos_estres[id_genero] <> 0 ) + 0, COUNTROWS ( vw_hechos_estres ) )", "0.0%"),
    ("% edad informada", "DIVIDE ( CALCULATE ( COUNTROWS ( vw_hechos_estres ), vw_hechos_estres[id_rango_edad] <> 0 ) + 0, COUNTROWS ( vw_hechos_estres ) )", "0.0%"),
    ("% nivel educativo informado", "DIVIDE ( CALCULATE ( COUNTROWS ( vw_hechos_estres ), vw_hechos_estres[id_nivel_educativo] <> 0 ) + 0, COUNTROWS ( vw_hechos_estres ) )", "0.0%"),
    ("% nivel de estrés asignado", "DIVIDE ( CALCULATE ( COUNTROWS ( vw_hechos_estres ), vw_hechos_estres[id_nivel_estres] <> 0 ) + 0, COUNTROWS ( vw_hechos_estres ) )", "0.0%"),
]


def modelo_calidad():
    definicion = os.path.dirname(TABLAS)
    # 1. Tablas (se reescriben siempre: el generador es la fuente de verdad)
    for nombre, (columnas, medidas) in TABLAS_CALIDAD.items():
        open(os.path.join(TABLAS, nombre + ".tmdl"), "w", encoding="utf-8", newline="\n").write(
            _tabla_tmdl(nombre, columnas, medidas))
    # 2. Referencias y orden de consultas en model.tmdl
    ruta = os.path.join(definicion, "model.tmdl")
    t = open(ruta, encoding="utf-8").read()
    faltan = [n for n in TABLAS_CALIDAD if f"ref table {n}\n" not in t]
    if faltan:
        t = t.replace("ref table vw_modelo_resultados\n",
                      "ref table vw_modelo_resultados\n" + "".join(f"ref table {n}\n" for n in faltan), 1)
    faltan = [n for n in TABLAS_CALIDAD if f'"{n}"' not in t]
    if faltan:
        t = t.replace('"vw_modelo_resultados",', '"vw_modelo_resultados",' + "".join(f'"{n}",' for n in faltan), 1)
    open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    # 3. Relación reglas → dataset
    ruta = os.path.join(definicion, "relationships.tmdl")
    t = open(ruta, encoding="utf-8").read()
    if f"fromColumn: {CR}.id_dataset" not in t:
        t = t.rstrip("\n") + f"\n\nrelationship {_tag('rel', CR, 'id_dataset')}\n\tfromColumn: {CR}.id_dataset\n\ttoColumn: {DS}.id_dataset\n"
        open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    # 4. Columnas de texto del origen CSV (fnTabla tipa el resto como número)
    ruta = os.path.join(definicion, "expressions.tmdl")
    t = open(ruta, encoding="utf-8").read()
    nuevas = [c for c in ("regla", "dimension", "estado", "accion", "fase", "control", "resultado", "origen")
              if f'"{c}"' not in t.split("TextoCols = {", 1)[1].split("}", 1)[0]]
    if nuevas:
        t = t.replace('"tarea_modelado"}', '"tarea_modelado",' + ",".join(f'"{c}"' for c in nuevas) + "}", 1)
        open(ruta, "w", encoding="utf-8", newline="\n").write(t)
    # 5. Medidas de completitud en la tabla de hechos
    ruta = os.path.join(TABLAS, "vw_hechos_estres.tmdl")
    t = open(ruta, encoding="utf-8").read()
    bloque = ""
    for m, dax, fmt in MEDIDAS_COMPLETITUD:
        if f"measure '{m}'" in t:   # ya existe: se actualiza su expresión (el generador es la fuente de verdad)
            t = re.sub(rf"(\tmeasure '{re.escape(m)}' = )[^\n]*", lambda x: x.group(1) + dax, t, count=1)
            open(ruta, "w", encoding="utf-8", newline="\n").write(t)
        else:
            bloque += (f"\tmeasure '{m}' = {dax}\n\t\tformatString: {fmt}\n\t\tdisplayFolder: 6 Calidad del dato\n"
                       f"\t\tlineageTag: {_tag('vw_hechos_estres', 'medida', m)}\n\n")
    if bloque:
        i = t.index("\tmeasure ")
        t = t[:i] + bloque + t[i:]
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
# (carpeta, nombre en el menú, función). Nombres cortos: con 8 páginas visibles el navegador da ~96 px por botón.
# Las dos últimas están ocultas: el navegador no las muestra (drill-through y tooltip)
PAGINAS_INFORME = [("p0_inicio", "Inicio", pagina0), ("p1_panorama", "1 Panorama", pagina1),
                   ("p2_demografia", "2 Demografía", pagina2), ("p3_lenguaje", "3 Lenguaje", pagina3),
                   ("p4_validacion", "4 Validación", pagina4), ("p5_modelos", "5 Modelos", pagina5),
                   ("p6_kpis", "6 KPIs", pagina6), (EXPLORAR, "7 Explorar", pagina7),
                   (CALIDAD, "8 Calidad", pagina10),
                   (DETALLE, "Detalle del dataset", pagina8), (TOOLTIP, "Tooltip del dataset", pagina9)]

IMAGENES = os.path.normpath(os.path.join(RAIZ, "imagenes"))
RECURSOS = os.path.join(RAIZ, "TFM_Estres.Report", "StaticResources", "RegisteredResources")
REPORTE = os.path.join(RAIZ, "TFM_Estres.Report", "definition", "report.json")


def config_pagina(carpeta):
    """Propiedades extra de page.json: fondo de Inicio, drill-through y tooltip."""
    if carpeta == "p0_inicio":
        return {"objects": {"background": [{"properties": {
            "image": {"image": {"name": txt("fondo_inicio.png"), "url": recurso("fondo_inicio.png"),
                                "scaling": txt("Fill")}},
            "transparency": lit("0D")}}]}}
    if carpeta == EXPLORAR:
        return {"displayOption": "FitToWidth", "height": ALTO_EXPLORAR}
    if carpeta == CALIDAD:
        return {"displayOption": "FitToWidth", "height": ALTO_CALIDAD}
    if carpeta == DETALLE:
        campo = col(DS, "dataset")
        return {"type": "Drillthrough", "visibility": "HiddenInViewMode",
                "pageBinding": {"name": "detalle_dataset", "type": "Drillthrough",
                                "parameters": [{"name": "detalle_dataset_param", "boundFilter": FILTRO_DETALLE,
                                                "fieldExpr": campo}]},
                "filterConfig": {"filters": [{"name": FILTRO_DETALLE, "field": campo, "type": "Categorical",
                                              "howCreated": "Drillthrough"}]}}
    if carpeta == TOOLTIP:
        return {"type": "Tooltip", "visibility": "HiddenInViewMode", "width": 320, "height": 240,
                "pageBinding": {"name": "tooltip_dataset", "type": "Tooltip"}}
    return {}


def escribir_paginas():
    for carpeta, nombre, _ in PAGINAS_INFORME:
        os.makedirs(os.path.join(PAGINAS, carpeta), exist_ok=True)
        pagina = {"$schema": ESQUEMA_PAGINA, "name": carpeta, "displayName": nombre,
                  "displayOption": "FitToPage", "height": ALTO, "width": ANCHO}
        pagina.update(config_pagina(carpeta))
        with open(os.path.join(PAGINAS, carpeta, "page.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(pagina, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PAGINAS, "pages.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"$schema": ESQUEMA_PAGINAS, "pageOrder": [c for c, _, _ in PAGINAS_INFORME],
                   "activePageName": PAGINAS_INFORME[0][0]}, f, ensure_ascii=False, indent=2)


def registrar_imagenes():
    """Copia powerbi/imagenes/*.png a StaticResources/RegisteredResources y las registra en report.json."""
    if not os.path.isdir(IMAGENES):
        print("  (sin imágenes: ejecuta antes generar_imagenes.py)")
        return
    os.makedirs(RECURSOS, exist_ok=True)
    archivos = sorted(f for f in os.listdir(IMAGENES) if f.lower().endswith(".png"))
    for f in archivos:
        shutil.copy2(os.path.join(IMAGENES, f), os.path.join(RECURSOS, f))
    rep = json.load(open(REPORTE, encoding="utf-8"))
    paquete = next(pq for pq in rep["resourcePackages"] if pq["type"] == "RegisteredResources")
    ya = {it["name"] for it in paquete["items"]}
    paquete["items"] += [{"name": f, "path": f, "type": "Image"} for f in archivos if f not in ya]
    with open(REPORTE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=2)
    print(f"  imágenes registradas: {len(archivos)}")


if __name__ == "__main__":
    registrar_imagenes()
    escribir_paginas()
    for pagina, _, f in PAGINAS_INFORME:
        escribir(pagina, f())
    ajustar_modelo()
    print("Modelo ajustado (orden de categorías y resumen de métricas).")
