"""Genera los objetos visuales de las 5 páginas del informe (formato PBIR) y ajusta el modelo.

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


def tarjetas(campos):
    # labelDisplayUnits = 1: número completo (319.318) en lugar de la abreviatura automática (319 mil)
    return {"visualType": "cardVisual",
            "query": {"queryState": {"Data": {"projections": [proy(c, n) for c, n in campos]}}},
            "objects": {"value": [{"properties": {"labelDisplayUnits": lit("1D")}}]}}


def segmentador(campo, nombre):
    return {"visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [proy(campo, nombre)]}}},
            "objects": {"data": [{"properties": {"mode": txt("Dropdown")}}]}}


def barras(categoria, nombre_cat, medidas, serie=None, tipo="clusteredBarChart", orden=None):
    estado = {"Category": {"projections": [proy(categoria, nombre_cat)]},
              "Y": {"projections": [proy(c, n) for c, n in medidas]}}
    if serie:
        estado["Series"] = {"projections": [proy(*serie)]}
    v = {"visualType": tipo, "query": {"queryState": estado},
         "objects": {"labels": [{"properties": {"show": lit("true")}}]}}
    campo_orden = orden if orden is not None else medidas[0][0]
    v["query"]["sortDefinition"] = {"sort": [{"field": campo_orden,
                                              "direction": "Ascending" if orden is not None else "Descending"}]}
    return v


def tabla(campos, totales=False):
    v = {"visualType": "tableEx",
         "query": {"queryState": {"Values": {"projections": [proy(c, n) for c, n in campos]}}}}
    if not totales:
        v["objects"] = {"total": [{"properties": {"totals": lit("false")}}]}
    return v


def matriz(filas, columnas, valores):
    return {"visualType": "pivotTable",
            "query": {"queryState": {
                "Rows": {"projections": [proy(*filas)]},
                "Columns": {"projections": [proy(*columnas)]},
                "Values": {"projections": [proy(c, n) for c, n in valores]}}}}


def texto(parrafos):
    """parrafos: lista de (texto, tamaño_pt, negrita)."""
    return {"visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [
                {"textRuns": [{"value": t, "textStyle": {"fontSize": f"{pt}pt",
                                                         **({"fontWeight": "bold"} if b else {})}}]}
                for t, pt, b in parrafos]}}]}}


def navegador():
    return {"visualType": "pageNavigator"}


# ---------------------------------------------------------------- campos
H, DS, G, E, ED, NE = ("vw_hechos_estres", "vw_dim_dataset", "vw_dim_genero",
                       "vw_dim_rango_edad", "vw_dim_nivel_educativo", "vw_dim_nivel_estres")
NLP, SUB, DASS, TRAT = "dwh_nlp_senales", "dim_subreddit", "dwh_dass_severidad", "dwh_brecha_tratamiento"
KPI, KPIC, MOD = "dwh_kpi_resultados", "dwh_kpi_catalogo", "vw_modelo_resultados"


def cabecera(pid, titulo, subtitulo):
    # Título de 480 px para dejar ~150 px por botón al navegador (nombres de página completos);
    # 66 px de alto para que título (16 pt) y subtítulo (9 pt) quepan sin barra de desplazamiento
    x_nav = M + 480 + 12
    return [
        contenedor(_id(pid, "titulo"), M, 4, 480, 66, 0,
                   texto([(titulo, 16, True), (subtitulo, 9, False)])),
        contenedor(_id(pid, "nav"), x_nav, 14, ANCHO - x_nav - M, 46, 1, navegador()),
    ]


def segmentadores(pid, y=72):
    w = (ANCHO - 2 * M - 3 * 12) / 4
    campos = [(col(DS, "bloque"), "Bloque"), (col(G, "nombre"), "Género"),
              (col(E, "rango"), "Rango de edad"), (col(ED, "nivel"), "Nivel educativo")]
    # 80 px de alto: con menos, el título del segmentador tapa el desplegable
    return [contenedor(_id(pid, "seg", n), M + i * (w + 12), y, w, 80, 10 + i, segmentador(c, n))
            for i, (c, n) in enumerate(campos)]


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
                        barras(col(DS, "dataset"), "Dataset", [(med(H, "% Estrés Alto"), "% estrés Alto")]),
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
        (med(MOD, "Modelos con alerta"), "Datasets con alerta")])))
    v.append(contenedor(_id(p, "nota"), M + 636, 72, ANCHO - 2 * M - 636, 110, 21, texto([
        ("Alertas", 11, True),
        ("Academic Stress: n = 140, el accuracy no supera al baseline (exploratorio).", 10, False),
        ("Depression Student: AUC ≈ 1, posible etiqueta generada por fórmula.", 10, False)])))
    mejores = [incluir(MOD, "es_mejor_modelo", [1], tipo="num")]
    # La columna «alerta» no va en la tabla: su texto es largo y las alertas ya están en la nota de arriba
    v.append(contenedor(_id(p, "auc"), M, 194, 380, 472, 30,
                        barras(col(MOD, "dataset"), "Dataset", [(med(MOD, "AUC medio"), "AUC")]),
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


if __name__ == "__main__":
    for pagina, f in [("p1_panorama", pagina1), ("p2_demografia", pagina2), ("p3_lenguaje", pagina3),
                      ("p4_validacion", pagina4), ("p5_modelos", pagina5)]:
        escribir(pagina, f())
    ajustar_modelo()
    print("Modelo ajustado (orden de categorías y resumen de métricas).")
