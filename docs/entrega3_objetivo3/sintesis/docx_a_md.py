"""Transcribe la síntesis (.docx generado por sintesis3.js) a Markdown para el repo."""
import sys, zipfile, re
import xml.etree.ElementTree as ET

DOCX, SALIDA = sys.argv[1], sys.argv[2]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
z = zipfile.ZipFile(DOCX)
body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
FIGS = ["sintesis/arquitectura.png", "../../figuras/powerbi/p0_inicio.png", "../../figuras/powerbi/p7_explorar.png"]
nfig = 0


def texto_runs(el, md=True):
    out = []
    for nodo in el.iter():
        if nodo.tag == W + "hyperlink":
            pass
    for hijo in el:
        if hijo.tag == W + "r":
            out.append(run_md(hijo, md))
        elif hijo.tag == W + "hyperlink":
            txt = "".join(run_md(r, False) for r in hijo.findall(W + "r"))
            url = rels.get(hijo.get(R + "id"), txt)
            out.append(f"[{txt}]({url})" if md else txt)
    s = "".join(out)
    return re.sub(r"\*\*\s*\*\*", "", s)


def run_md(r, md):
    t = "".join(x.text or "" for x in r.findall(W + "t"))
    if not t or not md:
        return t
    rpr = r.find(W + "rPr")
    fuente = rpr.find(W + "rFonts") if rpr is not None else None
    if fuente is not None and fuente.get(W + "ascii") == "Consolas":
        return f"`{t}`"
    if rpr is not None and rpr.find(W + "b") is not None:
        n = len(t) - len(t.rstrip())
        return f"**{t.rstrip()}**" + " " * n if t.strip() else t
    if rpr is not None and rpr.find(W + "i") is not None and t.strip():
        return f"*{t.strip()}*" + (" " if t.endswith(" ") else "")
    return t


def tam(p):
    sz = p.find(f".//{W}sz")
    return int(sz.get(W + "val")) if sz is not None else 22


lineas, codigo = [], []
for el in body:
    if el.tag == W + "tbl":
        filas = el.findall(W + "tr")
        celdas = [[" ".join(texto_runs(p) for p in tc.findall(W + "p")).replace("|", "\\|").strip() for tc in tr.findall(W + "tc")] for tr in filas]
        cab = [re.sub(r"\*\*", "", c) for c in celdas[0]]
        lineas += ["", "| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(f) + " |" for f in celdas[1:]] + [""]
        continue
    if el.tag != W + "p":
        continue
    if el.find(f".//{W}drawing") is not None:
        lineas += ["", f"![Figura {nfig + 1}]({FIGS[nfig]})"]
        nfig += 1
        continue
    plano = texto_runs(el, md=False)
    if not plano.strip():
        continue
    pPr = el.find(W + "pPr")
    shd = pPr.find(W + "shd") if pPr is not None else None
    fuente = el.find(f".//{W}rFonts")
    if shd is not None and fuente is not None and fuente.get(W + "ascii") == "Consolas":
        codigo.append(plano)
        continue
    if codigo:
        lineas += ["", "```dax", *codigo, "```"]
        codigo = []
    s = tam(el)
    if s >= 36:
        lineas += ["", "# " + plano]
    elif s == 32:
        lineas += ["", "*Transcripción a texto de `Sintesis_Entrega3_PowerBI.pdf`. El PDF, con las figuras, es el entregable oficial; se genera con los scripts de [`sintesis/`](sintesis/).*", "",
                   "**TFM — Business Analytics e Inteligencia Artificial.**"]
    elif s == 30:
        lineas += ["", "## " + plano]
    elif s == 24 and el.find(f".//{W}b") is not None and pPr is not None and pPr.find(W + "keepNext") is not None:
        lineas += ["", "### " + plano]
    elif pPr is not None and pPr.find(W + "numPr") is not None:
        lineas.append("- " + texto_runs(el))
    elif plano.startswith("Figura "):
        lineas.append("*" + plano + "*")
    elif shd is not None:
        lineas += ["", "> " + texto_runs(el)]
    else:
        lineas += ["", texto_runs(el)]

md = "\n".join(lineas).strip() + "\n"
# título primero: la cabecera del documento va antes del título de la entrega
partes = md.split("\n# ", 1)
if len(partes) == 2:
    cab, resto = partes
    titulo, cuerpo = resto.split("\n", 1)
    md = "# " + titulo + "\n\n" + cab.strip() + "\n" + cuerpo
md = re.sub(r"\n{3,}", "\n\n", md)
md += "\n**Relacionado:** [README](../../README.md) · [Guía de Power BI](guia_power_bi.md) · [Documento de insights](insights/README.md) · [Síntesis ETL y KPIs](../entrega2_objetivo2/02_sintesis_entrega2_etl_kpis.md) · [Pruebas](../../tests/pruebas.md)\n"
open(SALIDA, "w", encoding="utf-8", newline="\n").write(md)
print("ok", SALIDA, nfig, "figuras", len(md), "caracteres")
