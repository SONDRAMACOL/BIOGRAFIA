"""List of Enclosures en Word, con la misma lista y numeración que el PDF. Uso: python3 build_list_docx.py <salida.docx>"""
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.path.insert(0, str(Path(__file__).parent))
from build_list_checklist import G

d = Document()
sec = d.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.9)
sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.7)
st = d.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(0)


def para(text="", bold=False, size=11, after=0, before=0):
    p = d.add_paragraph()
    p.paragraph_format.space_after, p.paragraph_format.space_before = Pt(after), Pt(before)
    if text:
        r = p.add_run(text); r.bold = bold; r.font.size = Pt(size)
    return p


def no_borders(t):
    tblPr = t._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        x = OxmlElement(f"w:{e}"); x.set(qn("w:val"), "nil"); b.append(x)
    tblPr.append(b)


para("CARLOS ELÍAS MAHECHA DÍAZ", bold=True, size=13)
para("200 Biscayne Boulevard Way, Apt. 3806, Miami, Florida 33131", after=12)
para("November ___, 2026", after=10)
para("U.S. Department of Justice, Civil Division, Torts Branch, Federal Tort Claims Act Staff")
para("U.S. Department of State, Bureau of Diplomatic Security (copy: Office of the Legal Adviser, L/CID)", after=10)
para("Re: List of enclosures — Administrative claim under the Federal Tort Claims Act of Carlos Elías Mahecha Díaz, "
     "United States v. Carlos Mahecha, Case No. 1:19-cr-20738 (S.D. Fla.)", bold=True, after=8)
para("The following documents are enclosed with my claim:", after=4)

k = 0
for title, _, items in G:
    h = para(title, bold=True, before=8, after=2)
    h.paragraph_format.keep_with_next = True
    t = d.add_table(rows=0, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    no_borders(t)
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed"); t._tbl.tblPr.append(layout)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), (Inches(0.4), Inches(4.4), Inches(1.9))):
        gc.set(qn("w:w"), str(int(w.twips)))
    for name, date, _ in items:
        k += 1
        cells = t.add_row().cells
        for cell, txt, w in zip(cells, (f"{k}.", name, date), (Inches(0.4), Inches(4.4), Inches(1.9))):
            cell.width = w
            cell.paragraphs[0].add_run(txt).font.size = Pt(10.5)

para("Respectfully submitted,", before=18, after=30)
para("_____________________________________")
para("CARLOS ELÍAS MAHECHA DÍAZ", bold=True)
para("Claimant")
d.save(sys.argv[1])
print(k)
