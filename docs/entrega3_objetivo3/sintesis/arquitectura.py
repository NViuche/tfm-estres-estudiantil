"""Figura de arquitectura de la Entrega 3: de los CSV a MySQL, Supabase, Power BI y el servicio web."""
import sys
from PIL import Image, ImageDraw, ImageFont

SAL = sys.argv[1]
W, H = 2400, 1180
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
F = r"C:\Windows\Fonts"
fb = lambda s: ImageFont.truetype(F + r"\arialbd.ttf", s)
fr = lambda s: ImageFont.truetype(F + r"\arial.ttf", s)

AZUL, AZUL_C = (31, 92, 153), (226, 236, 247)
VERDE, VERDE_C = (46, 125, 110), (223, 241, 236)
NARANJA, NARANJA_C = (196, 110, 36), (251, 236, 220)
GRIS, GRIS_C = (90, 98, 110), (238, 240, 243)
MORADO, MORADO_C = (110, 76, 160), (237, 231, 247)


def caja(x, y, w, h, color, fondo, titulo, lineas, tam=26):
    d.rounded_rectangle((x, y, x + w, y + h), 18, fill=fondo, outline=color, width=4)
    d.rounded_rectangle((x, y, x + w, y + 58), 18, fill=color)
    d.rectangle((x, y + 40, x + w, y + 58), fill=color)
    d.text((x + w / 2, y + 29), titulo, font=fb(28), fill="white", anchor="mm")
    yy = y + 78
    for ln in lineas:
        negrita = ln.startswith("*")
        ln = ln.lstrip("*")
        d.text((x + 20, yy), ln, font=(fb if negrita else fr)(tam), fill=(40, 40, 40))
        yy += tam + 12
    return (x, y, w, h)


def flecha(x1, y1, x2, y2, texto=None, color=(80, 80, 80), dx=0, dy=-22):
    d.line((x1, y1, x2, y2), fill=color, width=5)
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    p = [(x2, y2), (x2 - 24 * math.cos(a - 0.4), y2 - 24 * math.sin(a - 0.4)), (x2 - 24 * math.cos(a + 0.4), y2 - 24 * math.sin(a + 0.4))]
    d.polygon(p, fill=color)
    if texto:
        d.text(((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy), texto, font=fr(23), fill=(60, 60, 60), anchor="mm")


d.text((W / 2, 36), "Arquitectura de la Entrega 3: un mismo modelo de datos, en local y en la nube", font=fb(38), fill=AZUL, anchor="mm")

# Columna 1: fuentes y Python
c1 = caja(40, 110, 470, 300, GRIS, GRIS_C, "12 datasets públicos",
          ["CSV de Kaggle y GitHub", "4 bloques analíticos", "*334.318 registros", "3 sintéticos: excluidos", "   de las medidas"])
c1b = caja(40, 500, 470, 300, GRIS, GRIS_C, "Python (notebooks)",
           ["Perfilado y calidad (05)", "Ingesta y ETL (07, 08)", "Modelado ML (09)", "*49 reglas de calidad", "*6 KPIs con histórico"])
flecha(275, 410, 275, 500)

# Columna 2: MySQL
c2 = caja(620, 250, 560, 420, AZUL, AZUL_C, "MySQL local (XAMPP)",
          ["*Modelo v2: 20 tablas", "  8 dimensiones y 12 de hechos", "*Capa estrella: 6 vistas vw_*", "  hechos + 5 dimensiones", "  conformes", "*DWH: 10 tablas dwh_*", "  T1–T5, KPIs, modelos y calidad",
           "*vw_modelo_resultados y vw_fuentes"])
flecha(510, 650, 620, 560, "carga", dx=-5, dy=-32)

# Rama local
c3 = caja(1300, 110, 500, 240, AZUL, AZUL_C, "18 CSV para Power BI",
          ["exportar_mysql_cli.py", "UTF-8, coma y punto decimal", "Se regeneran si cambia MySQL"])
flecha(1180, 360, 1300, 250)
c4 = caja(1900, 110, 460, 240, AZUL, AZUL_C, "Power BI local",
          ["TFM_Estres_local.pbix", "*Respaldo", "Parámetro Fuente = CSV"])
flecha(1800, 230, 1900, 230)

# Rama nube
c5 = caja(1300, 470, 500, 330, VERDE, VERDE_C, "Supabase (PostgreSQL)",
          ["Esquema tfm", "*19 tablas + 8 vistas", "Tildes y «Sí» corregidos", "Usuario tfm_lector", "  (solo lectura)", "Validado: 7/7 cifras"])
flecha(1180, 620, 1300, 620, "migración", dy=-24)
c6 = caja(1900, 470, 460, 240, VERDE, VERDE_C, "Power BI en la nube",
          ["TFM_Estres_supabase.pbix", "*Entregable", "Conector PostgreSQL"])
flecha(1800, 590, 1900, 590)

# API y web
c7 = caja(1300, 880, 500, 250, NARANJA, NARANJA_C, "API REST pública",
          ["4 vistas agregadas", "datasets, KPIs, modelos", "y reglas de calidad", "*Clave anon: solo SELECT"])
flecha(1550, 800, 1550, 880)
c8 = caja(1900, 790, 460, 340, NARANJA, NARANJA_C, "Servicio web (v12)",
          ["Prototipo HTML del informe", "Mismas páginas y medidas", "Datos de Supabase", "  incrustados", "*Público: enlace web", "Enlaces a datos en vivo"])
flecha(1800, 1000, 1900, 1000)
flecha(1800, 700, 1950, 790)

# Repositorio
c9 = caja(40, 880, 1140, 250, MORADO, MORADO_C, "Repositorio GitHub (público) · NViuche/tfm-estres-estudiantil",
          ["SQL, scripts, notebooks, proyectos .pbip, prototipo v1–v12, documentación y pruebas", "Ramas por entrega fusionadas en main · CITATION.cff",
           "GitHub Actions: consulta Supabase 2 veces por semana para que no se pause", "*No se suben: CSV, .pbix, .env ni contraseñas"], tam=25)

img.save(SAL, dpi=(200, 200))
print("ok", SAL)
