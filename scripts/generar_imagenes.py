"""Genera las imágenes del informe: iconos de los 4 bloques y fondo de la página Inicio.

Uso:
    python generar_imagenes.py

Escribe los PNG en ../powerbi/imagenes/. El generador de páginas (generar_paginas_pbir.py) los copia a
StaticResources/RegisteredResources del informe y los registra en report.json.
Iconos: tipografía Segoe Fluent Icons de Windows (SegoeIcons.ttf, o Segoe MDL2 Assets como respaldo),
en blanco sobre un círculo con los colores del tema «Bienestar».
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.normpath(os.path.join(AQUI, "..", "powerbi", "imagenes"))
FUENTES = [r"C:\Windows\Fonts\SegoeIcons.ttf", r"C:\Windows\Fonts\segmdl2.ttf"]

# (archivo, glifo, color del círculo): colores del tema Bienestar
ICONOS = [
    ("icono_factores_internos.png", "\uE7BE", "#2A9D8F"),     # Education: presión académica
    ("icono_habitos_digitales.png", "\uE8EA", "#264653"),     # CellPhone: redes sociales y pantallas
    ("icono_percepcion_emocional.png", "\uE8BD", "#E76F51"),  # Message: texto y lenguaje
    ("icono_validacion_psicologica.png", "\uE95E", "#8AB17D"),  # Health: escalas clínicas
]


def hex_rgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def icono(glifo, color, lado=192):
    """Círculo de color con el glifo en blanco, a 4x y reducido para suavizar los bordes."""
    fuente_ttf = next(f for f in FUENTES if os.path.exists(f))
    g = lado * 4
    im = Image.new("RGBA", (g, g), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, g - 1, g - 1), fill=hex_rgb(color))
    f = ImageFont.truetype(fuente_ttf, int(g * 0.5))
    x0, y0, x1, y1 = d.textbbox((0, 0), glifo, font=f)
    d.text(((g - (x1 - x0)) / 2 - x0, (g - (y1 - y0)) / 2 - y0), glifo, font=f, fill=(255, 255, 255, 255))
    return im.resize((lado, lado), Image.LANCZOS)


def fondo(ancho=1280, alto=720):
    """Fondo crema del tema con formas suaves en teal y arena: decorativo, sin restar legibilidad."""
    base = Image.new("RGBA", (ancho, alto), hex_rgb("#FAF6F0"))
    capa = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.ellipse((-260, 380, 520, 1100), fill=hex_rgb("#2A9D8F", 34))
    d.ellipse((900, -320, 1560, 300), fill=hex_rgb("#A8DADC", 60))
    d.ellipse((1020, 470, 1480, 930), fill=hex_rgb("#E9C46A", 40))
    d.ellipse((420, 610, 760, 950), fill=hex_rgb("#E76F51", 18))
    capa = capa.filter(ImageFilter.GaussianBlur(40))
    return Image.alpha_composite(base, capa).convert("RGB")


# Logos de origen: Objetivo3/recursos/logos en la carpeta de trabajo, recursos/logos en el repositorio
LOGOS = next((p for p in (os.path.normpath(os.path.join(AQUI, "..", "..", "recursos", "logos")),
                          os.path.normpath(os.path.join(AQUI, "..", "recursos", "logos"))) if os.path.isdir(p)),
             os.path.normpath(os.path.join(AQUI, "..", "recursos", "logos")))


def logos():
    """Logos de recursos/logos: recorta el margen transparente y guarda la versión original y una en blanco
    (para fondos oscuros como la banda teal). El nombre de salida es logo_<nombre>.png y logo_<nombre>_blanco.png."""
    if not os.path.isdir(LOGOS):
        return
    for f in sorted(os.listdir(LOGOS)):
        base, ext = os.path.splitext(f)
        if ext.lower() not in (".png", ".webp", ".jpg", ".jpeg", ".avif"):
            continue
        im = Image.open(os.path.join(LOGOS, f)).convert("RGBA")
        alfa = im.split()[3]
        # Sin fondo transparente no se puede pasar a blanco (saldría un rectángulo): se descarta
        if sum(1 for a in alfa.getdata() if a < 20) < 0.05 * im.size[0] * im.size[1]:
            print(f"  (descartado {f}: no tiene fondo transparente)")
            continue
        caja = alfa.point(lambda a: 255 if a > 10 else 0).getbbox()
        if caja:
            im = im.crop(caja)
        clave = base.lower()
        nombre = ("logo_unie" if "unie" in clave else "logo_inesdi" if "inesdi" in clave
                  else "logo_" + clave.replace("logo-", "").replace("logo_", "").replace(" ", "_"))
        im.save(os.path.join(DESTINO, nombre + ".png"), optimize=True)
        blanco = Image.new("RGBA", im.size, (255, 255, 255, 0))
        blanco.putalpha(im.split()[3])
        Image.merge("RGBA", (*Image.new("RGB", im.size, (255, 255, 255)).split(), im.split()[3])).save(
            os.path.join(DESTINO, nombre + "_blanco.png"), optimize=True)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for archivo, glifo, color in ICONOS:
        icono(glifo, color).save(os.path.join(DESTINO, archivo), optimize=True)
    fondo().save(os.path.join(DESTINO, "fondo_inicio.png"), optimize=True)
    # Línea vertical blanca semitransparente que separa los dos logos en la banda
    Image.new("RGBA", (4, 60), (255, 255, 255, 170)).save(os.path.join(DESTINO, "separador_blanco.png"), optimize=True)
    logos()
    for f in sorted(os.listdir(DESTINO)):
        print(f"  {f}: {os.path.getsize(os.path.join(DESTINO, f)):,} bytes".replace(",", "."))


if __name__ == "__main__":
    main()
