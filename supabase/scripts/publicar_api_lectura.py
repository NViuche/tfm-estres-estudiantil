"""Publica las vistas de lectura pública (sql/04_api_lectura_publica.sql) y comprueba la API REST.

Uso:  python publicar_api_lectura.py            aplica el SQL y prueba la API
      python publicar_api_lectura.py --probar   solo prueba la API

Necesita en .env: las variables de conexión de administrador, SUPABASE_URL y SUPABASE_ANON_KEY
(la clave pública anon/publishable: Project Settings → API Keys). La clave anon está pensada para
ser pública; la de servicio (service_role / secret) nunca se usa aquí.
"""
import json
import os
import sys
import urllib.error
import urllib.request

import psycopg2
from dotenv import load_dotenv

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
load_dotenv(os.path.join(RAIZ, ".env"))
E = os.environ.get
VISTAS = ("tfm_datasets", "tfm_kpis", "tfm_modelos", "tfm_calidad")

if "--probar" not in sys.argv:
    sql = open(os.path.join(RAIZ, "sql", "04_api_lectura_publica.sql"), encoding="utf-8").read()
    con = psycopg2.connect(host=E("SUPABASE_DB_HOST"), port=E("SUPABASE_DB_PORT", "5432"), dbname=E("SUPABASE_DB_NAME", "postgres"),
                           user=E("SUPABASE_DB_USER"), password=E("SUPABASE_DB_PASSWORD"), sslmode="require", connect_timeout=20)
    with con, con.cursor() as cur:
        cur.execute(sql)
        for v in VISTAS:
            cur.execute(f"SELECT count(*) FROM public.{v}")
            cur2 = con.cursor()
            cur2.execute("SELECT string_agg(privilege_type, ',' ORDER BY privilege_type) FROM information_schema.role_table_grants "
                         "WHERE table_schema='public' AND table_name=%s AND grantee='anon'", (v,))
            print(f"  {v}: {cur.fetchone()[0]} filas · permisos de anon: {cur2.fetchone()[0]}")
    con.close()

url, clave = (E("SUPABASE_URL") or "").rstrip("/"), E("SUPABASE_ANON_KEY")
if not (url and clave):
    sys.exit("Falta SUPABASE_URL o SUPABASE_ANON_KEY en .env: no se prueba la API")


def peticion(metodo, ruta, cuerpo=None):
    req = urllib.request.Request(f"{url}/rest/v1/{ruta}", method=metodo, data=cuerpo,
                                 headers={"apikey": clave, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


for v in VISTAS:
    estado, cuerpo = peticion("GET", f"{v}?select=*")
    print(f"  GET {v}: {estado} · {len(json.loads(cuerpo)) if estado == 200 else cuerpo[:120]}")
estado, _ = peticion("POST", "tfm_datasets", json.dumps({"codigo": "X"}).encode())
print(f"  POST tfm_datasets: {estado} ({'escritura bloqueada: correcto' if estado >= 400 else 'AVISO: revisar permisos'})")
estado, _ = peticion("DELETE", "tfm_datasets?codigo=eq.X")
print(f"  DELETE tfm_datasets: {estado} ({'escritura bloqueada: correcto' if estado >= 400 else 'AVISO: revisar permisos'})")
estado, _ = peticion("GET", "hechos_estres?select=*&limit=1")
print(f"  GET tabla interna hechos_estres: {estado} ({'no expuesta: correcto' if estado != 200 else 'AVISO: expuesta'})")
