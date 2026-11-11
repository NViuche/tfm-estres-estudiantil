"""Migra la capa estrella, el DWH y los resultados del modelado de MySQL (XAMPP) a Supabase.

Uso (con XAMPP/MySQL encendido):
    python migrar_mysql_a_supabase.py

Pasos: 1) crea el esquema tfm (01_esquema.sql; si ya existe, lo borra y lo rehace) y las tablas
de calidad del dato (05_calidad_dato.sql), 2) copia los datos tabla a tabla con COPY, 3) crea las
vistas (02_vistas.sql), 4) aplica las correcciones de datos (03_correcciones_datos.sql), 5) crea o
actualiza el usuario de solo lectura y vuelve a publicar las vistas de lectura pública de la API
(04_api_lectura_publica.sql; el DROP SCHEMA del paso 1 las borra) y 6) valida filas y cifras de
control contra MySQL. Las tablas de calidad deben estar antes en MySQL (local_xampp/scripts/cargar_calidad_dato.py).

Credenciales: ../.env (nunca se imprimen). Requiere psycopg2 y python-dotenv.
"""
import csv
import io
import os
import subprocess
import sys

import psycopg2
from dotenv import load_dotenv

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
SQL = os.path.join(RAIZ, "sql")
load_dotenv(os.path.join(RAIZ, ".env"))
E = os.environ.get

MYSQL_EXE = next((p for p in (r"C:\xampp\mysql\bin\mysql.exe", "mysql") if p == "mysql" or os.path.exists(p)))

# Orden de carga (respeta las claves foráneas). Origen MySQL → destino Supabase.
TABLAS = [
    ("dim_bloque", "dim_bloque"), ("dim_dataset", "dim_dataset"), ("dim_genero", "dim_genero"),
    ("dim_mapeo_estres", "dim_mapeo_estres"), ("dim_nivel_educativo", "dim_nivel_educativo"),
    ("dim_nivel_estres", "dim_nivel_estres"), ("dim_rango_edad", "dim_rango_edad"),
    ("dim_subreddit", "dim_subreddit"),
    ("vw_hechos_estres", "hechos_estres"),
    ("dwh_hechos_estres_unificado", "dwh_hechos_estres_unificado"),
    ("dwh_agg_prevalencia", "dwh_agg_prevalencia"), ("dwh_brecha_tratamiento", "dwh_brecha_tratamiento"),
    ("dwh_dass_severidad", "dwh_dass_severidad"), ("dwh_kpi_catalogo", "dwh_kpi_catalogo"),
    ("dwh_kpi_resultados", "dwh_kpi_resultados"), ("dwh_modelo_resultados", "dwh_modelo_resultados"),
    ("dwh_nlp_senales", "dwh_nlp_senales"),
    ("dwh_calidad_reglas", "dwh_calidad_reglas"), ("dwh_calidad_controles", "dwh_calidad_controles"),
]


def faltan(*claves):
    vacias = [k for k in claves if not E(k)]
    if vacias:
        sys.exit("Faltan en .env: " + ", ".join(vacias))


def mysql(sql):
    """Ejecuta una consulta con el cliente de XAMPP y devuelve (columnas, filas). NULL → None."""
    cmd = [MYSQL_EXE, "-h", E("MYSQL_HOST", "localhost"), "-P", E("MYSQL_PORT", "3306"), "-u", E("MYSQL_USER", "root"),
           "--batch", "--default-character-set=utf8mb4", E("MYSQL_DB"), "-e", sql]
    if E("MYSQL_PASSWORD"):
        cmd.insert(-3, "-p" + E("MYSQL_PASSWORD"))
    out = subprocess.run(cmd, capture_output=True, check=True).stdout.decode("utf-8")
    lineas = out.replace("\r\n", "\n").split("\n")
    if lineas and lineas[-1] == "":
        lineas.pop()

    def valor(v):
        if v == "NULL":
            return None
        return v.replace("\\t", "\t").replace("\\n", "\n").replace("\\0", "\0").replace("\\\\", "\\")

    cols = lineas[0].split("\t")
    return cols, [[valor(v) for v in l.split("\t")] for l in lineas[1:]]


def conectar():
    return psycopg2.connect(host=E("SUPABASE_DB_HOST"), port=E("SUPABASE_DB_PORT", "5432"),
                            dbname=E("SUPABASE_DB_NAME", "postgres"), user=E("SUPABASE_DB_USER"),
                            password=E("SUPABASE_DB_PASSWORD"), sslmode="require", connect_timeout=20)


def ejecutar_archivo(cur, nombre):
    cur.execute(open(os.path.join(SQL, nombre), encoding="utf-8").read())
    print(f"  {nombre}")


def copiar(cur, origen, destino):
    cols, filas = mysql(f"SELECT * FROM {origen}")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for f in filas:
        w.writerow(["\\N" if v is None else v for v in f])
    buf.seek(0)
    cur.copy_expert(f"COPY tfm.{destino} ({', '.join(cols)}) FROM STDIN WITH (FORMAT csv, NULL '\\N')", buf)
    return len(filas)


def lector(cur):
    usuario, clave = E("SUPABASE_LECTOR_USER", "tfm_lector"), E("SUPABASE_LECTOR_PASSWORD")
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (usuario,))
    accion = "ALTER" if cur.fetchone() else "CREATE"
    cur.execute(f'{accion} ROLE "{usuario}" WITH LOGIN PASSWORD %s', (clave,))
    cur.execute(f'GRANT USAGE ON SCHEMA tfm TO "{usuario}"')
    cur.execute(f'GRANT SELECT ON ALL TABLES IN SCHEMA tfm TO "{usuario}"')
    cur.execute(f'ALTER ROLE "{usuario}" SET search_path = tfm')
    # El esquema tfm no se expone por la API REST: sin acceso para los roles de la API
    cur.execute("REVOKE ALL ON SCHEMA tfm FROM anon, authenticated, public")
    print(f"  usuario de solo lectura «{usuario}»: {'actualizado' if accion == 'ALTER' else 'creado'}")


# Cifras de control: misma definición que las medidas DAX del Power BI
CONTROL = {
    "Registros": "SELECT COUNT(*) FROM {s}vw_hechos_estres h JOIN {s}vw_dim_dataset d USING (id_dataset) WHERE d.uso_modelado = 'incluido'",
    "% Estrés Alto": "SELECT ROUND(100.0 * SUM(CASE WHEN h.id_nivel_estres = 3 THEN 1 ELSE 0 END) / COUNT(*), 2) FROM {s}vw_hechos_estres h JOIN {s}vw_dim_dataset d USING (id_dataset) WHERE d.uso_modelado = 'incluido'",
    "Cobertura demográfica": "SELECT ROUND(100.0 * SUM(CASE WHEN h.id_genero <> 0 AND h.id_rango_edad <> 0 THEN 1 ELSE 0 END) / COUNT(*), 2) FROM {s}vw_hechos_estres h JOIN {s}vw_dim_dataset d USING (id_dataset) WHERE d.uso_modelado = 'incluido'",
    "% Tratamiento": "SELECT ROUND(100.0 * SUM(n_con_tratamiento) / SUM(n_total), 2) FROM {s}dwh_brecha_tratamiento",
    "Posts analizados": "SELECT SUM(n_posts) FROM {s}dwh_nlp_senales",
    "AUC medio sin alertas": "SELECT ROUND(AVG(auc), 3) FROM {s}vw_modelo_resultados WHERE es_mejor_modelo = 1 AND alerta IS NULL",
    "Datasets con alerta": "SELECT COUNT(*) FROM {s}vw_modelo_resultados WHERE es_mejor_modelo = 1 AND alerta IS NOT NULL",
}


def a_num(v):
    return round(float(v), 3) if v is not None else None


def main():
    faltan("SUPABASE_DB_HOST", "SUPABASE_DB_USER", "SUPABASE_DB_PASSWORD", "SUPABASE_LECTOR_PASSWORD", "MYSQL_DB")
    print("Conectando a Supabase…")
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                print("1. Esquema"); ejecutar_archivo(cur, "01_esquema.sql"); ejecutar_archivo(cur, "05_calidad_dato.sql")
                print("2. Datos")
                cargadas = {}
                for origen, destino in TABLAS:
                    cargadas[destino] = copiar(cur, origen, destino)
                    print(f"  {destino:30s} {cargadas[destino]:>8,} filas".replace(",", "."))
                print("3. Vistas"); ejecutar_archivo(cur, "02_vistas.sql")
                print("4. Correcciones de datos"); ejecutar_archivo(cur, "03_correcciones_datos.sql")
                print("5. Permisos"); lector(cur); ejecutar_archivo(cur, "04_api_lectura_publica.sql")

        print("6. Validación contra MySQL")
        errores = 0
        with con.cursor() as cur:
            for origen, destino in TABLAS:
                cur.execute(f"SELECT COUNT(*) FROM tfm.{destino}")
                n_pg = cur.fetchone()[0]
                n_my = int(mysql(f"SELECT COUNT(*) FROM {origen}")[1][0][0])
                if n_pg != n_my:
                    errores += 1
                    print(f"  ERROR filas {destino}: MySQL {n_my} · Supabase {n_pg}")
            print(f"  filas: {len(TABLAS) - errores} de {len(TABLAS)} tablas coinciden")
            for nombre, q in CONTROL.items():
                cur.execute(q.format(s="tfm."))
                v_pg = a_num(cur.fetchone()[0])
                v_my = a_num(mysql(q.format(s=""))[1][0][0])
                ok = v_pg == v_my
                errores += not ok
                print(f"  {'OK ' if ok else 'ERROR'} {nombre:24s} MySQL {v_my} · Supabase {v_pg}")
        print("Migración completa." if not errores else f"Migración con {errores} diferencias: revisar.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
