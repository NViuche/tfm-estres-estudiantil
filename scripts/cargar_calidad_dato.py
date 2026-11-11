"""Carga en el DWH las tablas de calidad y gobierno del dato que usa la página «8 Calidad» del informe.

    dwh_calidad_reglas     las 49 reglas del notebook 05, con su dataset y su dimensión de calidad
    dwh_calidad_controles  registro de controles de validación (carga, ETL, migración, seguridad e informe)

Uso:
    python cargar_calidad_dato.py                 # CSV para Power BI + MySQL (si XAMPP está encendido) + Supabase
    python cargar_calidad_dato.py --solo csv      # o mysql / supabase
    python cargar_calidad_dato.py --reglas <ruta del CSV del notebook 05>

Origen de las reglas: el CSV que exporta notebooks/05_reglas_calidad_dato.ipynb (resultado_reglas_calidad.csv).
Los controles salen de los notebooks 07b y 08, de la migración y de las pruebas documentadas en tests/pruebas.md:
cada uno indica su origen. Credenciales de Supabase y MySQL en supabase/.env (nunca se imprimen).
"""
import argparse
import csv
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# Rutas válidas en la carpeta de trabajo (Objetivo3/local_xampp/scripts) y en el repositorio (scripts/)
CANDIDATOS_REGLAS = [os.path.join(AQUI, "..", "..", "..", "Objetivo1", "Reglas de Calidad", "resultado_reglas_calidad.csv"),
                     os.path.join(AQUI, "..", "salidas", "objetivo1", "Reglas de Calidad", "resultado_reglas_calidad.csv")]
CANDIDATOS_CSV = [os.path.join(AQUI, "..", "powerbi_csv"), os.path.join(AQUI, "..", "powerbi_csv")]
CANDIDATOS_ENV = [os.path.join(AQUI, "..", "..", "supabase", ".env"), os.path.join(AQUI, "..", "supabase", ".env")]
CANDIDATOS_SQL = [os.path.join(AQUI, "..", "..", "supabase", "sql", "05_calidad_dato.sql"),
                  os.path.join(AQUI, "..", "supabase", "sql", "05_calidad_dato.sql")]
MYSQL_EXE = r"C:\xampp\mysql\bin\mysql.exe"


def primero(rutas):
    return next((os.path.normpath(p) for p in rutas if os.path.exists(p)), None)


# Etiqueta del dataset en el notebook 05 → código de dim_dataset
DATASETS = {"B1.1 AcademicStress": "B1_ACADSTRESS", "B1.2 Anxiety": "B1_ANXIETY", "B1.3 MHSurvey": "B1_MHSURVEY",
            "B1.4 StudentHabits": "B1_HABITS", "B2.1 SocialMedia": "B2_SOCIALMEDIA", "B2.2 SMMH": "B2_SMMH",
            "B2.3 Lifestyle": "B2_LIFESTYLE", "B3.1 Dreaddit": "B3_DREADDIT_TR", "B3.2 DepressionStudent": "B3_DEPSTUDENT",
            "B4.1 DASS": "B4_DASS", "B4.2 MentalHealth": "B4_MENTALHEALTH"}
ID_DATASET = {"B1_ACADSTRESS": 1, "B1_ANXIETY": 2, "B1_MHSURVEY": 3, "B1_HABITS": 4, "B2_SOCIALMEDIA": 5, "B2_SMMH": 6,
              "B2_LIFESTYLE": 7, "B3_DREADDIT_TR": 8, "B3_DREADDIT_TE": 9, "B3_DEPSTUDENT": 10, "B4_DASS": 11,
              "B4_MENTALHEALTH": 12}


def dimension(regla):
    """Dimensión de calidad (DAMA) de cada regla, según lo que comprueba."""
    r = regla.lower()
    if "columna duplicada" in r or "distinto conjunto" in r or "distinto orden" in r or "suma de horas" in r:
        return "Consistencia"   # coherencia entre columnas o entre particiones
    if "duplicad" in r or "solapamiento" in r:
        return "Unicidad"
    if "nulo" in r or "vacio" in r or "nan semantico" in r:
        return "Completitud"
    if "espacios" in r or "formato" in r:
        return "Conformidad"    # formato o estructura esperados
    return "Validez"            # rangos, dominios, escalas y valores imposibles


def leer_reglas(ruta):
    filas = []
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        for i, r in enumerate(csv.DictReader(f), start=1):
            codigo = DATASETS[r["Dataset"]]
            if codigo == "B3_DREADDIT_TR" and r["Regla"].rstrip().endswith("en test"):
                codigo = "B3_DREADDIT_TE"   # la única regla de Dreaddit que solo mira la partición de test
            filas.append([i, ID_DATASET[codigo], r["Regla"].strip(), dimension(r["Regla"]), int(r["Evaluados"]),
                          int(r["Incumplen"]), round(float(r["% incumplen"]), 2), r["Estado"].strip(),
                          r["Accion"].strip(), "Antes de la carga"])
    return filas


# Registro de controles: (fase, control, resultado, estado, origen)
CONTROLES = [
    ("Carga", "Objetos del modelo", "Existen las 11 tablas de hechos, las 7 dimensiones y las 6 vistas de la estrella", "OK", "notebook 07b"),
    ("Carga", "Filas por tabla", "Cada tabla tiene exactamente las filas cargadas: suman 334.318", "OK", "notebook 07b"),
    ("Carga", "Capa estrella", "Los 12 datasets aparecen en vw_hechos_estres; las 9 fuentes incluidas suman 319.318", "OK", "notebook 07b"),
    ("Carga", "Integridad referencial", "Sin claves naturales repetidas ni claves nulas o huérfanas hacia las dimensiones", "OK", "notebook 07b"),
    ("Carga", "Reglas aplicadas en la ingesta", "Textos corruptos de Dreaddit excluidos; edades del DASS en 13–90", "OK", "notebook 07b"),
    ("Carga", "Filtro global", "«Mujeres de 18–25 con estrés Alto» reproduce los 7.446 casos de la verificación", "OK", "notebook 07b"),
    ("Carga", "Género no informado en el DASS", "67 respondentes (0,17 %) quedaron como «Otro» en lugar de «No reportado»", "AVISO", "notebook 07"),
    ("Carga", "Respuestas por ítem del DASS", "b4_dass_item existe en el modelo pero está vacía: no se cargaron las respuestas por ítem", "AVISO", "notebook 07"),
    ("ETL", "Relaciones hecho-dimensión", "14 relaciones con 0 claves huérfanas", "OK", "notebook 08"),
    ("ETL", "Cuadre de registros", "334.318 − 15.000 sintéticos = 319.318 registros en el DWH", "OK", "notebook 08"),
    ("ETL", "Reproducibilidad de los KPIs", "3 ejecuciones guardadas con valores idénticos", "OK", "dwh_kpi_resultados"),
    ("Migración", "Filas por tabla", "17 de 17 tablas con las mismas filas en MySQL y Supabase", "OK", "migrar_mysql_a_supabase.py"),
    ("Migración", "Cifras de control", "7 de 7 cifras de control iguales en MySQL y Supabase", "OK", "migrar_mysql_a_supabase.py"),
    ("Migración", "Textos corregidos", "Tildes y «Sí» corregidos en Supabase; MySQL los mantiene como en origen", "AVISO", "03_correcciones_datos.sql"),
    ("Seguridad", "Usuario de solo lectura", "tfm_lector lee el esquema tfm y la escritura queda bloqueada", "OK", "probar_lector.py"),
    ("Seguridad", "API pública", "Solo lectura de vistas agregadas; la escritura falla y el esquema tfm no se expone", "OK", "publicar_api_lectura.py"),
    ("Informe", "Valores de control del informe", "Los valores de control de Power BI coinciden con SQL sobre MySQL", "OK", "tests/pruebas.md"),
]
COLS_REGLAS = ["id_regla", "id_dataset", "regla", "dimension", "evaluados", "incumplen", "pct_incumplen", "estado", "accion", "fase"]
COLS_CONTROLES = ["id_control", "fase", "control", "resultado", "estado", "origen"]

DDL_MYSQL = """
CREATE TABLE IF NOT EXISTS dwh_calidad_reglas (
  id_regla SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
  id_dataset TINYINT UNSIGNED NOT NULL,
  regla VARCHAR(160) NOT NULL,
  dimension ENUM('Completitud','Validez','Unicidad','Consistencia','Conformidad') NOT NULL,
  evaluados INT UNSIGNED NOT NULL,
  incumplen INT UNSIGNED NOT NULL,
  pct_incumplen DECIMAL(7,2) NOT NULL,
  estado ENUM('OK','AVISO','ERROR') NOT NULL,
  accion VARCHAR(200) NOT NULL,
  fase VARCHAR(30) NOT NULL,
  CONSTRAINT fk_calidad_dataset FOREIGN KEY (id_dataset) REFERENCES dim_dataset (id_dataset)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS dwh_calidad_controles (
  id_control SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
  fase VARCHAR(30) NOT NULL,
  control VARCHAR(80) NOT NULL,
  resultado VARCHAR(240) NOT NULL,
  estado ENUM('OK','AVISO','ERROR') NOT NULL,
  origen VARCHAR(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
TRUNCATE TABLE dwh_calidad_reglas;
TRUNCATE TABLE dwh_calidad_controles;
"""


def a_csv(carpeta, nombre, cols, filas):
    ruta = os.path.join(carpeta, nombre + ".csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(filas)
    print(f"  CSV {nombre}: {len(filas)} filas")


def sql_literal(v):
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def a_mysql(env, reglas, controles):
    if not os.path.exists(MYSQL_EXE):
        print("  MySQL: no se encuentra el cliente de XAMPP; se omite")
        return False
    inserts = [f"INSERT INTO {t} ({', '.join(c)}) VALUES " + ",".join("(" + ",".join(sql_literal(v) for v in f) + ")" for f in filas) + ";"
               for t, c, filas in (("dwh_calidad_reglas", COLS_REGLAS, reglas), ("dwh_calidad_controles", COLS_CONTROLES, controles))]
    cmd = [MYSQL_EXE, "-h", env.get("MYSQL_HOST", "localhost"), "-P", env.get("MYSQL_PORT", "3306"), "-u", env.get("MYSQL_USER", "root"),
           "--default-character-set=utf8mb4", env.get("MYSQL_DB", "tfm_estres_estudiantil_2")]
    if env.get("MYSQL_PASSWORD"):
        cmd.insert(-1, "-p" + env["MYSQL_PASSWORD"])
    r = subprocess.run(cmd, input=(DDL_MYSQL + "\n".join(inserts)).encode("utf-8"), capture_output=True)
    if r.returncode:
        print("  MySQL: no disponible (¿XAMPP apagado?); se omite. Vuelve a ejecutar con --solo mysql cuando esté encendido")
        return False
    print(f"  MySQL: dwh_calidad_reglas {len(reglas)} filas · dwh_calidad_controles {len(controles)} filas")
    return True


def a_supabase(env, reglas, controles):
    import psycopg2
    sql = primero(CANDIDATOS_SQL)
    con = psycopg2.connect(host=env.get("SUPABASE_DB_HOST"), port=env.get("SUPABASE_DB_PORT", "5432"),
                           dbname=env.get("SUPABASE_DB_NAME", "postgres"), user=env.get("SUPABASE_DB_USER"),
                           password=env.get("SUPABASE_DB_PASSWORD"), sslmode="require", connect_timeout=20)
    with con, con.cursor() as cur:
        cur.execute(open(sql, encoding="utf-8").read())
        for t, c, filas in (("dwh_calidad_reglas", COLS_REGLAS, reglas), ("dwh_calidad_controles", COLS_CONTROLES, controles)):
            cur.executemany(f"INSERT INTO tfm.{t} ({', '.join(c)}) VALUES ({', '.join(['%s'] * len(c))})", filas)
        lector = env.get("SUPABASE_LECTOR_USER", "tfm_lector")
        cur.execute(f'GRANT SELECT ON tfm.dwh_calidad_reglas, tfm.dwh_calidad_controles TO "{lector}"')
        cur.execute("SELECT (SELECT count(*) FROM tfm.dwh_calidad_reglas), (SELECT count(*) FROM tfm.dwh_calidad_controles)")
        n_r, n_c = cur.fetchone()
    con.close()
    print(f"  Supabase: dwh_calidad_reglas {n_r} filas · dwh_calidad_controles {n_c} filas")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--solo", choices=["csv", "mysql", "supabase"])
    ap.add_argument("--reglas", help="CSV de resultados del notebook 05")
    a = ap.parse_args()
    ruta = a.reglas or primero(CANDIDATOS_REGLAS)
    if not ruta:
        sys.exit("No se encuentra resultado_reglas_calidad.csv: ejecuta el notebook 05 o pasa --reglas")
    reglas = leer_reglas(ruta)
    controles = [[i, *c] for i, c in enumerate(CONTROLES, start=1)]
    estados = {e: sum(1 for r in reglas if r[7] == e) for e in ("OK", "AVISO", "ERROR")}
    print(f"Reglas: {len(reglas)} ({estados['OK']} OK · {estados['AVISO']} AVISO · {estados['ERROR']} ERROR) · controles: {len(controles)}")

    env = {}
    ruta_env = primero(CANDIDATOS_ENV)
    if ruta_env:
        from dotenv import dotenv_values
        env = {k: v for k, v in dotenv_values(ruta_env).items() if v}
    if a.solo in (None, "csv"):
        destino = primero(CANDIDATOS_CSV)
        if destino:
            a_csv(destino, "dwh_calidad_reglas", COLS_REGLAS, reglas)
            a_csv(destino, "dwh_calidad_controles", COLS_CONTROLES, controles)
        else:
            print("  CSV: no se encuentra la carpeta powerbi_csv; se omite")
    if a.solo in (None, "mysql"):
        a_mysql(env, reglas, controles)
    if a.solo in (None, "supabase"):
        if env.get("SUPABASE_DB_PASSWORD"):
            a_supabase(env, reglas, controles)
        else:
            print("  Supabase: faltan credenciales en supabase/.env; se omite")


if __name__ == "__main__":
    main()
