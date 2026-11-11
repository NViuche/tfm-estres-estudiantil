"""Exporta las 17 tablas/vistas del modelo Power BI a CSV usando el cliente mysql.exe de XAMPP.

Uso (con MySQL encendido en XAMPP):
    python exportar_mysql_cli.py                 # escribe en ..\\powerbi_csv
    python exportar_mysql_cli.py D:\\otra\\carpeta

No necesita sqlalchemy ni pymysql: solo Python y el mysql.exe de XAMPP. Formato
de salida: UTF-8, coma, punto decimal, NULL -> celda vacía. Conexión: root sin contraseña, base
tfm_estres_estudiantil_2 (cambia las constantes si tu XAMPP es distinto).
En Power BI: parámetro Fuente = CSV y RutaCSV = carpeta de salida.
"""
import csv
import os
import subprocess
import sys

MYSQL = r"C:\xampp\mysql\bin\mysql.exe"
DB = "tfm_estres_estudiantil_2"
DESTINO = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "powerbi_csv"))
OBJETOS = [
    "vw_hechos_estres", "vw_dim_dataset", "vw_dim_genero", "vw_dim_rango_edad",
    "vw_dim_nivel_educativo", "vw_dim_nivel_estres", "dim_bloque", "dim_subreddit",
    "dwh_agg_prevalencia", "dwh_nlp_senales", "dwh_dass_severidad",
    "dwh_brecha_tratamiento", "dwh_kpi_catalogo", "dwh_kpi_resultados",
    "vw_modelo_resultados", "dwh_calidad_reglas", "dwh_calidad_controles",
]
ESCAPES = {"n": "\n", "t": "\t", "\\": "\\", "0": "\0", "r": "\r"}


def desescapar(v):
    # El modo --batch de mysql escapa \n, \t, \\ y escribe los nulos como NULL
    if v in ("NULL", "\\N"):
        return ""
    out, i = [], 0
    while i < len(v):
        if v[i] == "\\" and i + 1 < len(v):
            out.append(ESCAPES.get(v[i + 1], v[i + 1]))
            i += 2
        else:
            out.append(v[i])
            i += 1
    return "".join(out)


os.makedirs(DESTINO, exist_ok=True)
for nombre in OBJETOS:
    r = subprocess.run(
        [MYSQL, "-u", "root", "--batch", "--default-character-set=utf8mb4", DB,
         "-e", f"SELECT * FROM {nombre}"],
        capture_output=True, check=True)
    # En Windows mysql.exe termina las líneas con \r\n
    lineas = r.stdout.decode("utf-8").replace("\r\n", "\n").split("\n")
    if lineas and lineas[-1] == "":
        lineas.pop()
    ruta = os.path.join(DESTINO, f"{nombre}.csv")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(lineas[0].split("\t"))
        for ln in lineas[1:]:
            w.writerow([desescapar(c) for c in ln.split("\t")])
    print(f"  {nombre:<26} {len(lineas) - 1:>8,} filas")
print("Listo:", DESTINO)
