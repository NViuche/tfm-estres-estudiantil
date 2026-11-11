"""Incrusta en prototipo_estres.html los datos agregados que usa el informe de Power BI.

Uso:
    python construir_prototipo.py                 # lee de Supabase (versión en la nube, por defecto)
    python construir_prototipo.py --fuente csv    # lee los CSV del Power BI local (MySQL de XAMPP)

Supabase: se conecta con el usuario de solo lectura (tfm_lector) de supabase/.env y lee el esquema
tfm, el mismo que usa el Power BI de supabase/powerbi. CSV: lee powerbi_csv (local_xampp/powerbi_csv en la
carpeta de trabajo), los mismos
archivos que el Power BI local. En los dos casos agrega los datos y reescribe el bloque
<script id="datos"> del HTML: el prototipo no necesita conexión, todo va dentro del archivo.
"""
import argparse
import csv
import json
import os
import re
import time
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
# Funciona en la carpeta de trabajo (Objetivo3/prototipo/vN) y en el repositorio (prototipo/vN)
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
CSV = next((p for p in (os.path.join(RAIZ, "local_xampp", "powerbi_csv"), os.path.join(RAIZ, "powerbi_csv"))
            if os.path.isdir(p)), os.path.join(RAIZ, "powerbi_csv"))
HTML = os.path.join(AQUI, "prototipo_estres.html")
ENV = os.path.join(RAIZ, "supabase", ".env")
PG = None  # conexión a Supabase cuando --fuente supabase


def leer(tabla):
    """Filas de una tabla o vista como diccionarios de texto (mismo formato desde CSV y desde Supabase)."""
    if PG is None:
        with open(os.path.join(CSV, tabla + ".csv"), encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    with PG.cursor() as cur:
        cur.execute(f"SELECT * FROM tfm.{tabla}")
        cols = [c.name for c in cur.description]
        return [{c: "" if v is None else str(v) for c, v in zip(cols, fila)} for fila in cur.fetchall()]


def cubo_hechos(incluidos):
    """Recuento de registros por dataset × género × edad × educación × nivel de estrés."""
    cubo = Counter()
    if PG is None:
        with open(os.path.join(CSV, "vw_hechos_estres.csv"), encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                d = int(r["id_dataset"])
                if d in incluidos:
                    cubo[(d, int(r["id_genero"]), int(r["id_rango_edad"]),
                          int(r["id_nivel_educativo"]), int(r["id_nivel_estres"]))] += 1
        return cubo
    with PG.cursor() as cur:
        cur.execute("""SELECT id_dataset, id_genero, id_rango_edad, id_nivel_educativo, id_nivel_estres, COUNT(*)
                       FROM tfm.vw_hechos_estres GROUP BY 1, 2, 3, 4, 5""")
        for *k, n in cur.fetchall():
            if k[0] in incluidos:
                cubo[tuple(k)] = n
    return cubo


def completitud():
    """Por dataset (los 12): registros y registros con género, edad, nivel educativo y nivel de estrés informados (id ≠ 0)."""
    if PG is None:
        c = {}
        with open(os.path.join(CSV, "vw_hechos_estres.csv"), encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                t = c.setdefault(int(r["id_dataset"]), [0, 0, 0, 0, 0])
                t[0] += 1
                for i, k in enumerate(("id_genero", "id_rango_edad", "id_nivel_educativo", "id_nivel_estres"), start=1):
                    t[i] += r[k] != "0"
        return c
    with PG.cursor() as cur:
        cur.execute("""SELECT id_dataset, COUNT(*), COUNT(*) FILTER (WHERE id_genero <> 0), COUNT(*) FILTER (WHERE id_rango_edad <> 0),
                              COUNT(*) FILTER (WHERE id_nivel_educativo <> 0), COUNT(*) FILTER (WHERE id_nivel_estres <> 0)
                       FROM tfm.vw_hechos_estres GROUP BY 1""")
        return {d: list(v) for d, *v in cur.fetchall()}


def calidad(ds):
    """Página «8 Calidad»: reglas del notebook 05, registro de controles y completitud (cargar_calidad_dato.py)."""
    nombre = {int(d["id_dataset"]): d["dataset"] for d in ds}
    comp = completitud()
    return {
        "reglas": [{"ds": nombre[int(r["id_dataset"])], "regla": r["regla"], "dim": r["dimension"], "ev": int(float(r["evaluados"])),
                    "inc": int(float(r["incumplen"])), "pct": num(r["pct_incumplen"]), "estado": r["estado"], "accion": r["accion"]}
                   for r in sorted(leer("dwh_calidad_reglas"), key=lambda r: int(float(r["id_regla"])))],
        "controles": [{"fase": c["fase"], "control": c["control"], "resultado": c["resultado"], "estado": c["estado"],
                       "origen": c["origen"]} for c in sorted(leer("dwh_calidad_controles"), key=lambda c: int(float(c["id_control"])))],
        "completitud": [{"ds": nombre[d], "n": v[0], "gen": v[1], "edad": v[2], "educ": v[3], "nivel": v[4]}
                        for d, v in sorted(comp.items())],
    }


def imagenes():
    """Iconos de los bloques y logo del informe de Power BI (powerbi/imagenes), incrustados como data URI.
    Los iconos se reducen a 80 px: en el prototipo se ven a 40 px."""
    import base64
    import io
    from PIL import Image
    carpeta = next((p for p in (os.path.join(RAIZ, "local_xampp", "powerbi", "imagenes"), os.path.join(RAIZ, "powerbi", "imagenes"))
                    if os.path.isdir(p)), None)
    if not carpeta:
        return {}
    salida = {}
    for f in sorted(os.listdir(carpeta)):
        nombre, ext = os.path.splitext(f)
        if ext.lower() != ".png" or not (nombre.startswith("icono_") or nombre.endswith("_blanco")):
            continue
        im = Image.open(os.path.join(carpeta, f))
        if nombre.startswith("icono_"):
            im = im.resize((80, 80), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        salida[nombre] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return salida


def conectar_supabase():
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv(ENV)
    e = os.environ.get
    ref = e("SUPABASE_DB_USER", "").split(".", 1)[-1]
    return psycopg2.connect(host=e("SUPABASE_DB_HOST"), port=e("SUPABASE_DB_PORT", "5432"),
                            dbname=e("SUPABASE_DB_NAME", "postgres"), user=f'{e("SUPABASE_LECTOR_USER", "tfm_lector")}.{ref}',
                            password=e("SUPABASE_LECTOR_PASSWORD"), sslmode="require", connect_timeout=20)


def num(v):
    return None if v in ("", None) else float(v)


def enlaces_nube(html):
    """Rellena la constante NUBE (pestaña Arquitectura) con la URL de la API y la clave pública anon de supabase/.env.

    La clave anon es pública por diseño y solo permite leer las vistas de sql/04_api_lectura_publica.sql.
    Si el .env no está (por ejemplo, en el repositorio) se conservan los valores que ya tenga el HTML.
    """
    from dotenv import load_dotenv
    load_dotenv(ENV)
    url, clave = (os.environ.get("SUPABASE_URL") or "").rstrip("/"), os.environ.get("SUPABASE_ANON_KEY") or ""
    m = re.search(r"/\*nube\*/(.*?)/\*fin-nube\*/", html, flags=re.S)
    assert m, "No se encontró la constante NUBE en el HTML"
    nube = json.loads(m.group(1))
    if url and clave:
        nube.update(api=url, clave=clave)
    elif not nube.get("clave"):
        print("Aviso: faltan SUPABASE_URL o SUPABASE_ANON_KEY en supabase/.env; los enlaces a los datos en vivo quedan vacíos")
    nuevo = json.dumps(nube, ensure_ascii=False, separators=(",", ":"))
    return html[:m.start(1)] + nuevo + html[m.end(1):]


def main():
    global PG
    ap = argparse.ArgumentParser(description="Incrusta los datos en el prototipo HTML")
    ap.add_argument("--fuente", choices=["supabase", "csv"], default="supabase")
    ap.add_argument("--solo-enlaces", action="store_true", help="solo actualiza los enlaces a Supabase, sin tocar los datos")
    args = ap.parse_args()
    if args.solo_enlaces:
        html = enlaces_nube(open(HTML, encoding="utf-8").read())
        open(HTML, "w", encoding="utf-8", newline="\n").write(html)
        print("Enlaces a Supabase actualizados")
        return
    fuente = args.fuente
    if fuente == "supabase":
        PG = conectar_supabase()
    ds = leer("vw_dim_dataset")
    incluidos = {int(d["id_dataset"]) for d in ds if d["uso_modelado"] == "incluido"}

    # Cubo de hechos: solo los 9 datasets con señal real (las medidas de Power BI filtran uso_modelado = incluido)
    cubo = cubo_hechos(incluidos)

    if PG is None:
        fecha = time.localtime(os.path.getmtime(os.path.join(CSV, "vw_hechos_estres.csv")))
        origen = "MySQL local (XAMPP)"
    else:
        fecha, origen = time.localtime(), "Supabase (PostgreSQL, esquema tfm)"
    datos = {
        "fuente": origen,
        "exportado": time.strftime("%d/%m/%Y", fecha),
        "datasets": [{"id": int(d["id_dataset"]), "nombre": d["dataset"], "bloque": d["bloque"],
                      "id_bloque": int(d["id_bloque"]), "calidad": d["calidad"], "uso": d["uso_modelado"]}
                     for d in ds if int(d["id_dataset"]) in incluidos],
        "generos": {g["id_genero"]: g["nombre"] for g in leer("vw_dim_genero")},
        "edades": sorted(({"id": int(e["id_rango_edad"]), "nombre": e["rango"]} for e in leer("vw_dim_rango_edad")),
                         key=lambda x: x["id"]),
        "educacion": sorted(({"id": int(e["id_nivel_educativo"]), "nombre": e["nivel"]}
                             for e in leer("vw_dim_nivel_educativo")), key=lambda x: x["id"]),
        "niveles": {n["id_nivel_estres"]: n["nivel"] for n in leer("vw_dim_nivel_estres")},
        # [dataset, genero, edad, educacion, nivel, n]
        "cubo": [list(k) + [n] for k, n in sorted(cubo.items())],
        "subreddits": {s["id_subreddit"]: s["nombre"] for s in leer("dim_subreddit")},
        "nlp": [{"sub": int(r["id_subreddit"]), "nivel": int(r["id_nivel_estres"]), "posts": int(r["n_posts"]),
                 "sent": num(r["sentimiento_medio"]), "liwc": num(r["liwc_ansiedad_medio"])}
                for r in leer("dwh_nlp_senales")],
        "dass": [{"g": int(r["id_genero"]), "e": int(r["id_rango_edad"]), "ed": int(r["id_nivel_educativo"]),
                  "n": int(r["n_respondentes"]), "ans": num(r["ansiedad_media"]), "sev": num(r["pct_estres_severo"])}
                 for r in leer("dwh_dass_severidad")],
        "tratamiento": [{"nivel": int(r["id_nivel_estres"]), "ant": r["antecedentes_familiares"],
                         "n": int(r["n_total"]), "trat": int(r["n_con_tratamiento"])}
                        for r in leer("dwh_brecha_tratamiento")],
        "kpi_catalogo": [{"codigo": k["codigo"], "nombre": k["nombre"], "descripcion": k["descripcion"],
                          "unidad": k["unidad"]} for k in leer("dwh_kpi_catalogo")],
        "kpi_resultados": [{"codigo": k["codigo"], "valor": num(k["valor"]), "fecha": k["fecha_ejecucion"]}
                           for k in leer("dwh_kpi_resultados")],
        "modelos": [{"dataset": m["dataset"], "modelo": m["modelo"], "protocolo": m["protocolo"],
                     "n": int(m["n_registros"]), "auc": num(m["auc"]), "f1": num(m["f1"]),
                     "acc": num(m["accuracy"]), "alerta": m["alerta"] or None}
                    for m in leer("vw_modelo_resultados") if m["es_mejor_modelo"] == "1"],
        "calidad": calidad(ds),
    }

    bloque = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = open(HTML, encoding="utf-8").read()
    html, n = re.subn(r'(<script id="datos" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + bloque + m.group(2), html, count=1, flags=re.S)
    assert n == 1, "No se encontró el bloque <script id=\"datos\"> en el HTML"
    imgs = json.dumps(imagenes(), separators=(",", ":"))
    html, n = re.subn(r'(<script id="imagenes" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + imgs + m.group(2), html, count=1, flags=re.S)
    assert n == 1, "No se encontró el bloque <script id=\"imagenes\"> en el HTML"
    html = enlaces_nube(html)
    open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    if PG is not None:
        PG.close()
    total = sum(cubo.values())
    alto = sum(v for k, v in cubo.items() if k[4] == 3)
    print(f"Fuente: {origen}")
    print(f"Datos incrustados: {len(cubo)} celdas del cubo; {total:,} registros".replace(",", ".")
          + f"; % Alto {alto / total:.1%}".replace(".", ","))


if __name__ == "__main__":
    main()
