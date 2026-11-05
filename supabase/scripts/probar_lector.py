"""Comprueba la conexión del usuario de solo lectura (el que usa el Power BI) y muestra los textos corregidos.

Uso:  python probar_lector.py
En el session pooler de Supabase el usuario va con la referencia del proyecto: tfm_lector.<ref>.
"""
import os

import psycopg2
from dotenv import load_dotenv

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
load_dotenv(os.path.join(RAIZ, ".env"))
E = os.environ.get

ref = E("SUPABASE_DB_USER").split(".", 1)[1]
usuario = f'{E("SUPABASE_LECTOR_USER", "tfm_lector")}.{ref}'
con = psycopg2.connect(host=E("SUPABASE_DB_HOST"), port=E("SUPABASE_DB_PORT", "5432"), dbname=E("SUPABASE_DB_NAME", "postgres"),
                       user=usuario, password=E("SUPABASE_LECTOR_PASSWORD"), sslmode="require", connect_timeout=20)
with con.cursor() as cur:
    print(f"Conectado como {E('SUPABASE_LECTOR_USER', 'tfm_lector')} (solo lectura)")
    for titulo, q in [("Bloques", "SELECT nombre FROM tfm.dim_bloque ORDER BY id_bloque"),
                      ("KPIs", "SELECT nombre FROM tfm.dwh_kpi_catalogo ORDER BY id_kpi"),
                      ("Antecedentes", "SELECT DISTINCT antecedentes_familiares FROM tfm.dwh_brecha_tratamiento ORDER BY 1"),
                      ("Modelos", "SELECT DISTINCT modelo FROM tfm.vw_modelo_resultados WHERE es_mejor_modelo = 1 ORDER BY 1")]:
        cur.execute(q)
        print(f"  {titulo}: " + " · ".join(r[0] for r in cur.fetchall()))
    try:
        cur.execute("CREATE TABLE tfm.prueba_escritura (x int)")
        print("  AVISO: el usuario puede escribir")
    except psycopg2.Error:
        print("  Escritura bloqueada: correcto")
con.close()
