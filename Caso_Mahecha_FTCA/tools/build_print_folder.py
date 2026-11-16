"""Arma la carpeta Imprimir/ y el mapa de impresión de los 81 documentos.

Uso: python3 build_print_folder.py <carpeta_caso> <informe_benejam.pdf> <licencia_benejam.pdf> <correo_simpson.pdf> <extracto_bofa.pdf>
"""
import shutil, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from xml.sax.saxutils import escape as X

sys.path.insert(0, str(Path(__file__).parent))
from build_list_checklist import G  # misma lista y numeración

case = Path(sys.argv[1]); benejam, license_, simpson, bofa = map(Path, sys.argv[2:6])
out = case / "Imprimir"
if out.exists():
    shutil.rmtree(out)
out.mkdir()

def cp(src, name):
    shutil.copy(src, out / name)
    return name

def first_page(src, name):
    w = PdfWriter(); w.add_page(PdfReader(src).pages[0]); w.write(out / name)
    return name

F = {}
F["01A"] = cp(case / "Cartas/Cover_Letter_FTCA_DOJ_Mahecha.pdf", "01_Carta_presentacion_JUEGO-A_DOJ.pdf")
F["01B"] = cp(case / "Cartas/Cover_Letter_FTCA_Department_of_State_Mahecha.pdf", "01_Carta_presentacion_JUEGOS-B-y-C_State.pdf")
F["02A"] = cp(case / "SF95/SF95_Mahecha_DOJ_para_firma.pdf", "02-03_SF95_y_Addendum_JUEGO-A_DOJ.pdf")
F["02B"] = cp(case / "SF95/SF95_Mahecha_Estado_para_firma.pdf", "02-03_SF95_y_Addendum_JUEGOS-B-y-C_State.pdf")
F["LIST"] = cp(case / "Paquete/List_of_Enclosures_FTCA_Mahecha.pdf", "03b_List_of_Enclosures_TODOS-LOS-JUEGOS.pdf")
F["SEP"] = cp(case / "Paquete/Exhibit_Separator_Sheets_Mahecha.pdf", "00_Hojas_separadoras_32pag_TODOS-LOS-JUEGOS.pdf")
F["16"] = cp(case / "Paquete/Exhibit_6_Schedule_of_Defense_Costs.pdf", "16_Exhibit-6_Schedule_of_defense_costs.pdf")
F["73"] = cp(bofa, "73_Exhibit-8-12_BofA_statement_Camilo_Oct-Nov-2024.pdf")
F["74"] = cp(simpson, "74_Exhibit-8-12-13_Email_RW_Simpson_21-Oct-2026.pdf")
F["80"] = cp(benejam, "80_Exhibit-10_Forensic_psychological_evaluation_Benejam.pdf")
F["81"] = first_page(license_, "81_Exhibit-10_License_verification_Benejam.pdf")
cp(case / "Paquete/Checklist_Paquete_FTCA_Mahecha.pdf", "99_Checklist_de_armado_NO-VA-EN-EL-PAQUETE.pdf")

PACER = {7, 9, 10, 11, 12, 13, 15, 79}
OURS = {1: "01A / 01B (según el juego)", 2: "02-03 (según el juego), págs. 1-2", 3: "02-03 (según el juego), pág. 3",
        16: F["16"], 73: F["73"], 74: F["74"], 80: F["80"], 81: F["81"]}

def source(k):
    if k in OURS:
        return "Carpeta Imprimir", OURS[k]
    if k in PACER:
        return "PACER (descarga suya)", "Docket / DE indicado"
    camilo = k if k <= 72 else k + 1      # Camilo numeró con la lista del 11-nov (su doc. 74 era duplicado)
    return "Camilo (ZIP / PDF consolidado)", f"Su documento {camilo}"

c = ParagraphStyle("c", fontName="Helvetica", fontSize=7.5, leading=9)
cb = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=7.5, leading=9)
data = [[Paragraph(h, cb) for h in ("N.º", "Documento", "De dónde sale", "Archivo / referencia", "A", "B", "C")]]
st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
      ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
k = 0
for title, _, items in G:
    i = len(data)
    data.append([Paragraph(X(title.upper()), ParagraphStyle("s", parent=cb, textColor=colors.white)), "", "", "", "", "", ""])
    st += [("SPAN", (0, i), (-1, i)), ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#1F3864"))]
    for name, date, _ in items:
        k += 1
        who, ref = source(k)
        i = len(data)
        data.append([Paragraph(str(k), c), Paragraph(X(f"{name} — {date}"), c), Paragraph(X(who), c), Paragraph(X(ref), c), "", "", ""])
        colr = {"Carpeta Imprimir": "#E2EFDA", "PACER (descarga suya)": "#FFF2CC"}.get(who)
        if colr:
            st.append(("BACKGROUND", (2, i), (3, i), colors.HexColor(colr)))
t = Table(data, colWidths=[24, 236, 92, 150, 18, 18, 18], repeatRows=1)
t.setStyle(TableStyle(st))
sm = ParagraphStyle("sm", fontName="Helvetica", fontSize=8, leading=10)
story = [
    Paragraph("MAPA DE IMPRESIÓN — RECLAMO FTCA DR. CARLOS ELÍAS MAHECHA DÍAZ", ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=12, leading=15)),
    Paragraph("Verde: archivo listo en la carpeta Imprimir. Amarillo: descarga de PACER. Sin color: archivo de Camilo "
              "(ZIP en Drive \"DOCUMENTOS ADJUNTOS (2).zip\" o PDF consolidado del 12-nov). Camilo numeró con la lista del "
              "11-nov: sus documentos 1 a 73 coinciden; su 74 es un duplicado y NO se imprime; sus 75 a 79 son aquí 74 a 78. "
              "La lista de anexos (archivo 03b) va justo después del Addendum. Las hojas separadoras (archivo 00) se intercalan "
              "según el checklist. Columnas A, B, C para marcar cada juego.", sm),
    Spacer(1, 6), t]
SimpleDocTemplate(str(out / "00_Mapa_de_impresion_NO-VA-EN-EL-PAQUETE.pdf"), pagesize=letter, leftMargin=28, rightMargin=28,
                  topMargin=28, bottomMargin=28, title="Mapa de impresion FTCA Mahecha").build(story)
print(k, sorted(p.name for p in out.iterdir()))
