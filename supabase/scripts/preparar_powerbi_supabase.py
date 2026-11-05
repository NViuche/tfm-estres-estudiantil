"""Crea (o rehace) la copia del Power BI que lee de Supabase a partir del Power BI local.

Uso (con Power BI Desktop CERRADO):
    python preparar_powerbi_supabase.py

Copia el Power BI local (local_xampp/powerbi, o powerbi/ en el repositorio) → supabase/powerbi (sin la caché .pbi ni los PDF) y aplica:
  - Fuente = "Supabase"; Servidor = host:puerto del pooler (de ../.env); BaseDatos = postgres
  - fnTabla con la rama de Supabase (conector PostgreSQL, esquema tfm, mismos tipos que la rama CSV)
  - medida «% Tratamiento con antecedentes»: «Yes» → «Sí» (corrección de datos de Supabase)
Las páginas, el tema y las medidas son las mismas que en el informe local.
"""
import os
import re
import shutil
import stat
import sys

from dotenv import load_dotenv

AQUI = os.path.dirname(os.path.abspath(__file__))
SUPA = os.path.normpath(os.path.join(AQUI, ".."))
# Power BI de origen: local_xampp/powerbi en la carpeta de trabajo, powerbi/ en el repositorio
ORIGEN = next(p for p in (os.path.normpath(os.path.join(SUPA, "..", "local_xampp", "powerbi")),
                         os.path.normpath(os.path.join(SUPA, "..", "powerbi"))) if os.path.isdir(p))
DESTINO = os.path.join(SUPA, "powerbi")
load_dotenv(os.path.join(SUPA, ".env"))


def largo(p):
    return "\\\\?\\" + os.path.abspath(p)


def sololectura(f, p, _):
    os.chmod(p, stat.S_IWRITE)
    f(p)


def reemplazar(ruta, cambios):
    t = open(ruta, encoding="utf-8", newline="").read()
    for patron, nuevo in cambios:
        t, n = re.subn(patron, lambda m: nuevo, t, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"No se encontró el patrón en {os.path.basename(ruta)}: {patron[:60]}")
    open(ruta, "w", encoding="utf-8", newline="").write(t)


RAMA_SUPABASE = '''				if Fuente = "Supabase" then
					let
						Pg = PostgreSQL.Database(Servidor, BaseDatos),
						Datos = Pg{[Schema = "tfm", Item = nombre]}[Data],
						Tipos = List.Transform(Table.ColumnNames(Datos), each {_, if _ = "fecha_ejecucion" then type datetime else if List.Contains(TextoCols, _) then type text else type number}),
						Final = Table.TransformColumnTypes(Datos, Tipos)
					in
						Final
				else if Fuente = "MySQL" then'''


def main():
    host, puerto = os.environ.get("SUPABASE_DB_HOST"), os.environ.get("SUPABASE_DB_PORT", "5432")
    if not host:
        sys.exit("Falta SUPABASE_DB_HOST en .env")
    # Solo se rehacen las carpetas del proyecto PBIP; Entrega/ (los .pbix entregados) no se toca
    os.makedirs(DESTINO, exist_ok=True)
    for sub in ("TFM_Estres.Report", "TFM_Estres.SemanticModel"):
        d = os.path.join(DESTINO, sub)
        if os.path.exists(d):
            shutil.rmtree(largo(d), onexc=sololectura)
        shutil.copytree(largo(os.path.join(ORIGEN, sub)), largo(d),
                        ignore=shutil.ignore_patterns(".pbi"))
    for f in ("TFM_Estres.pbip", ".gitignore", "TFM_Estres_tema_bienestar.json"):
        shutil.copy2(os.path.join(ORIGEN, f), os.path.join(DESTINO, f))

    defin = os.path.join(DESTINO, "TFM_Estres.SemanticModel", "definition")
    reemplazar(os.path.join(defin, "expressions.tmdl"), [
        (r'expression Fuente = "[^"]*"', 'expression Fuente = "Supabase"'),
        (r'expression Servidor = "[^"]*"', f'expression Servidor = "{host}:{puerto}"'),
        (r'expression BaseDatos = "[^"]*"', 'expression BaseDatos = "postgres"'),
        (r'\t\t\t\tif Fuente = "MySQL" then', RAMA_SUPABASE),
    ])
    reemplazar(os.path.join(defin, "tables", "dwh_brecha_tratamiento.tmdl"), [
        (r'(antecedentes_familiares\] = )"Yes"', r'antecedentes_familiares] = "Sí"'),
    ])
    print(f"Power BI para Supabase listo en {DESTINO}")
    print("Ábrelo, actualiza y usa el usuario tfm_lector.<ref del proyecto> (Base de datos) al pedir credenciales.")


if __name__ == "__main__":
    main()
