"""Exporta la estructura del modelo (tablas, columnas, claves y filas) para la pestaña «Arquitectura» del prototipo.

Uso (con XAMPP/MySQL encendido):
    python exportar_arquitectura.py

Lee information_schema de MySQL (tfm_estres_estudiantil_2), cuenta las filas exactas de cada tabla y
reescribe el bloque <script id="arquitectura"> de prototipo_estres.html. Solo hace falta repetirlo si
cambia la estructura de la base de datos (no los datos).
"""
import json
import os
import re
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(AQUI, "prototipo_estres.html")
MYSQL = r"C:\xampp\mysql\bin\mysql.exe"
BD = "tfm_estres_estudiantil_2"
# Tablas que existen en Supabase (esquema tfm); vw_hechos_estres está materializada como hechos_estres
EN_SUPABASE = {"dim_bloque", "dim_dataset", "dim_genero", "dim_mapeo_estres", "dim_nivel_educativo", "dim_nivel_estres",
               "dim_rango_edad", "dim_subreddit", "dwh_hechos_estres_unificado", "dwh_agg_prevalencia",
               "dwh_brecha_tratamiento", "dwh_dass_severidad", "dwh_kpi_catalogo", "dwh_kpi_resultados",
               "dwh_modelo_resultados", "dwh_nlp_senales"}


def consulta(sql):
    out = subprocess.run([MYSQL, "-u", "root", "--batch", "-N", "--default-character-set=utf8mb4", BD, "-e", sql],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return [l.split("\t") for l in out.replace("\r\n", "\n").split("\n") if l]


def main():
    tablas = [t for (t,) in consulta("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE() "
                                     "AND table_type = 'BASE TABLE' ORDER BY table_name")]
    cols = {}
    for t, c, k in consulta("SELECT table_name, column_name, column_key FROM information_schema.columns "
                            "WHERE table_schema = DATABASE() ORDER BY table_name, ordinal_position"):
        cols.setdefault(t, []).append([c, k])
    fks = consulta("SELECT table_name, column_name, referenced_table_name FROM information_schema.key_column_usage "
                   "WHERE table_schema = DATABASE() AND referenced_table_name IS NOT NULL")
    fk_cols = {(t, c) for t, c, _ in fks}
    filas = dict(consulta(" UNION ALL ".join(f"SELECT '{t}', COUNT(*) FROM {t}" for t in tablas + ["vw_hechos_estres"])))

    def entrada(t):
        return {"columnas": [[c, "PK" if k == "PRI" else "FK" if (t, c) in fk_cols else ""] for c, k in cols[t]],
                "filas": int(filas[t]), "supabase": t in EN_SUPABASE}

    arq = {t: entrada(t) for t in tablas}
    arq["vw_hechos_estres"] = {"columnas": [[c, "FK" if c.startswith("id_") and c != "id_registro" else
                                             "PK" if c in ("id_registro", "tabla_origen") else ""] for c, _ in cols["vw_hechos_estres"]],
                               "filas": int(filas["vw_hechos_estres"]), "supabase": True, "vista": True}
    for v in ("vw_dim_dataset", "vw_dim_genero", "vw_dim_rango_edad", "vw_dim_nivel_educativo", "vw_dim_nivel_estres",
              "vw_modelo_resultados"):
        arq[v] = {"columnas": [[c, "PK" if i == 0 else ""] for i, (c, _) in enumerate(cols[v])], "vista": True, "supabase": True}
    datos = {"tablas": arq, "relaciones": [[t, c, r] for t, c, r in fks]}

    bloque = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    html = open(HTML, encoding="utf-8").read()
    html, n = re.subn(r'(<script id="arquitectura" type="application/json">).*?(</script>)',
                      lambda m: m.group(1) + bloque + m.group(2), html, count=1, flags=re.S)
    assert n == 1, "No se encontró <script id=\"arquitectura\"> en el HTML"
    open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    print(f"Arquitectura: {len(tablas)} tablas, {len(fks)} claves foráneas, vw_hechos_estres {int(filas['vw_hechos_estres']):,} filas"
          .replace(",", "."))


if __name__ == "__main__":
    main()
