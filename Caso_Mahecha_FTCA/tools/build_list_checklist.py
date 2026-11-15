"""Genera la carta con la lista de anexos (inglés) y el checklist de armado (español) con la misma numeración.

Uso: python3 build_list_checklist.py <carpeta_salida>
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from xml.sax.saxutils import escape as X

OUT = sys.argv[1]

# (título del grupo, separadora para el checklist, [(documento, fecha, nota del checklist)])
G = [
 ("Claim documents", None, [
  ("Cover letter", "November ___, 2026", "Firma, fecha y lugar en tinta"),
  ("Standard Form 95, Claim for Damage, Injury, or Death", "November ___, 2026", "Firma 13a y fecha 14 en tinta"),
  ("Addendum to Standard Form 95", "November ___, 2026", "Firma y fecha en tinta"),
 ]),
 ("Exhibit 1", "EXHIBIT 1", [("Indictment, United States v. Carlos Mahecha, Case No. 1:19-cr-20738 (S.D. Fla.)", "November 5, 2019", "")]),
 ("Exhibit 2", "EXHIBIT 2", [("Affidavit of AUSA Sean Paul Cronin in support of extradition", "March 16, 2021", ""),
                ("Affidavit of Special Agent Seth Toensing in support of extradition", "March 16, 2021", "")]),
 ("Exhibit 3", "EXHIBIT 3", [("Docket sheet, Case No. 1:19-cr-20738 (S.D. Fla.)", "November 5, 2019 - December 2, 2024", "PACER")]),
 ("Exhibit 4", "EXHIBIT 4", [("Minute Order setting bond (DE 15)", "May 9, 2023", ""),
                ("Order Directing Defendant's Release (DE 16)", "May 9, 2023", "PACER"),
                ("$3,000,000 10% Bond (DE 21)", "May 12, 2023", "PACER"),
                ("$500,000 Corporate Surety Bond (DE 22)", "May 17, 2023", "PACER"),
                ("Order granting removal of GPS ankle monitor (DE 32)", "August 24, 2023", "PACER (entrada del docket)")]),
 ("Exhibit 5", "EXHIBIT 5", [("Jury Verdict (DE 128)", "November 21, 2024", "PACER"),
                ("Judgment of Acquittal (DE 136)", "November 22, 2024", ""),
                ("Order granting disbursement of bond (DE 138)", "November 25, 2024", "PACER (entrada del docket)")]),
 ("Exhibit 6", "EXHIBIT 6", [("Itemized schedule of attorneys' fees and defense costs", "November ___, 2026", "Versión con pago 24-1123 del 6-ene-2025")]),
 ("Exhibit 7-A: Piñera-Vazquez Law Firm, P.A.", "EXHIBIT 7 + EXHIBIT 7-A", [
  ("Invoice", "March 8, 2021", ""),
  ("Statement of legal fees and expenses", "July 16, 2024", ""),
  ("Statement of legal fees and expenses", "August 28, 2024", "")]),
 ("Exhibit 7-B: Salazar Law, LLP", "EXHIBIT 7-B", [
  ("Invoice 6384", "April 30, 2024", ""),
  ("E-mail correspondence on fee agreement", "March 27 - April 3, 2024", "")]),
 ("Exhibit 7-C: Cooper Strategic Solutions, LLC", "EXHIBIT 7-C", [
  ("E-mail with payment schedule", "September 20, 2024", ""),
  ("Invoice 1002", "September 20, 2024", ""),
  ("Invoice 1003", "October 31, 2024", "")]),
 ("Exhibit 7-D: The FairWay, LLC", "EXHIBIT 7-D", [
  ("Invoice #23-032", "April 6, 2023", ""),
  ("Invoice #23-042", "July 8, 2023", ""),
  ("Invoice #24-313", "March 13, 2024", ""),
  ("Invoice 24-1015", "October 18, 2024", ""),
  ("Engagement letter, Mahecha trial", "November 3, 2024", ""),
  ("Invoice 24-1123", "November 23, 2024", "")]),
 ("Exhibit 7-F: Carlton Fields, P.A. (Matter 13390-36114)", "EXHIBIT 7-E (intentionally omitted) + EXHIBIT 7-F", [
  ("Engagement letter", "January 9, 2019", ""),
  ("Invoice 1012558", "May 22, 2019", ""), ("Invoice 1014921", "June 17, 2019", ""),
  ("Invoice 1019377", "July 19, 2019", ""), ("Invoice 1023833", "August 27, 2019", ""),
  ("Invoice 1025587", "September 12, 2019", ""), ("Invoice 1029904", "October 11, 2019", ""),
  ("Invoice 1033079", "November 8, 2019", ""), ("Invoice 1038046", "December 1, 2019", ""),
  ("Invoice 1044363", "February 11, 2020", ""), ("Invoice 1048137", "March 9, 2020", ""),
  ("Invoice 1053502", "April 15, 2020", ""), ("Invoice 1058555", "May 20, 2020", ""),
  ("Invoice 1063082", "June 30, 2020", ""), ("Invoice 1066204", "July 21, 2020", ""),
  ("Invoice 1068269", "August 11, 2020", ""), ("Invoice 1074721", "September 22, 2020", ""),
  ("Invoice 1080049", "October 25, 2020", ""), ("Invoice 1084115", "November 29, 2020", ""),
  ("Invoice 1086994", "November 30, 2020", ""), ("Invoice 1090325", "January 20, 2021", ""),
  ("Invoice 1093037", "February 10, 2021", ""), ("Invoice 1098111", "March 16, 2021", "")]),
 ("Exhibit 7-G: K&L Gates LLP", "EXHIBIT 7-G", [
  ("Engagement letter", "December 8, 2017", ""),
  ("Invoice 3532701", "July 18, 2018", ""),
  ("Invoice 3556337", "September 24, 2018", ""),
  ("Invoice 3579758", "October 31, 2018", "")]),
 ("Exhibit 8: Proof of payment", "EXHIBIT 8 (y una separadora por cada 8-01 a 8-15)", [
  ("8-01  SWIFT FT2412308573, Trevanes Company Ltd. to Salazar Law, LLP", "May 2, 2024", ""),
  ("8-02  SWIFT FT2313104266, Lenaine Ltd. to Silvia B. Piñera-Vásquez, P.A.", "May 12, 2023", ""),
  ("8-03  E-mails of Silvia B. Piñera-Vázquez on application of returned bond funds", "December 23 and 30, 2024", ""),
  ("8-04  SWIFT FT2205589017, Trevanes Company Ltd. to Piñera-Vazquez Law Firm, P.A.", "February 24, 2022", ""),
  ("8-05  SWIFT FT2424000354, Lenaine Ltd. to Piñera-Vazquez Law Firm, P.A.", "August 27, 2024", ""),
  ("8-05  Truist wire confirmation 2671633 to Cooper Strategic Solutions, LLC", "August 28, 2024", ""),
  ("8-05  E-mails confirming payment to Cooper Strategic Solutions, LLC", "August 26 - 28, 2024", ""),
  ("8-06  Davivienda wire transfer to Piñera-Vazquez Law Firm, with certified English translation", "September 20, 2024", "Original + traducción"),
  ("8-06  E-mails confirming payment to Cooper Strategic Solutions, LLC", "September 20 - 24, 2024", ""),
  ("8-07  Truist wire confirmation 2885006 to Cooper Strategic Solutions, LLC", "December 9, 2024", ""),
  ("8-07  E-mail confirming final payment to Cooper Strategic Solutions, LLC", "December 9, 2024", ""),
  ("8-08  SWIFT FT2313065439, Trevanes Company Ltd. to The FairWay, LLC", "May 10, 2023", ""),
  ("8-09  SWIFT FT2320793007, Trevanes Company Ltd. to The FairWay, LLC", "July 26, 2023", ""),
  ("8-10  SWIFT FT2407929081, Trevanes Company Ltd. to The FairWay, LLC", "March 19, 2024", ""),
  ("8-11  SWIFT FT2408007298, Trevanes Company Ltd. to The FairWay, LLC", "March 20, 2024", ""),
  ("8-12  Bank of America statement of Camilo E. Mahecha, showing withdrawal of US$25,000 on October 31, 2024", "October 10 - November 6, 2024", "Una sola copia (docs. 73 y 74 de Camilo son el mismo)"),
  ("8-12/8-13  E-mail of R.W. Simpson confirming receipt of payments of US$25,000 and US$10,260", "October 21, 2026", ""),
  ("8-14  Banco de Bogotá foreign exchange declaration, US$150,000 to Carlton Fields, P.A., with certified English translation", "June 18, 2019", "Original + traducción"),
  ("8-14  Bank of America transfer to Carlton Fields, P.A. trust account", "July 28, 2020", ""),
  ("8-15  Banco de Bogotá foreign exchange declaration, US$161,525 to K&L Gates LLP, with statement of account and certified English translation", "June 18, 2019", "Original + traducción")]),
 ("Exhibit 9", "EXHIBIT 9", [
  ("Forensic accounting report of Tanya M. Cooper, CPA", "October 31, 2024", ""),
  ("Trial minute entries (DE 110 - DE 126)", "November 4 - 21, 2024", "PACER (entradas del docket)")]),
 ("Exhibit 10", "EXHIBIT 10", [
  ("Independent forensic psychological evaluation by Gustavo R. Benejam, Psy.D.", "November 12, 2026", "21 páginas, incluye Attachment 1"),
  ("License verification of Gustavo R. Benejam, Psy.D., Florida Department of Health (License PY7387)", "November 10, 2026", "")]),
]

T, TB, F, FB = "Times-Roman", "Times-Bold", "Helvetica", "Helvetica-Bold"


# ------------------------------------------------------------------ carta (inglés)
def enclosures():
    n = ParagraphStyle("n", fontName=T, fontSize=11, leading=14)
    b = ParagraphStyle("b", parent=n, fontName=TB)
    h = ParagraphStyle("h", fontName=TB, fontSize=11, leading=14, spaceBefore=8, spaceAfter=2)
    it = ParagraphStyle("i", fontName=T, fontSize=10.5, leading=13)
    story = [
        Paragraph("CARLOS ELÍAS MAHECHA DÍAZ", ParagraphStyle("t", fontName=TB, fontSize=13, leading=16)),
        Paragraph("200 Biscayne Boulevard Way, Apt. 3806, Miami, Florida 33131", n), Spacer(1, 14),
        Paragraph("November ___, 2026", n), Spacer(1, 10),
        Paragraph("U.S. Department of Justice, Civil Division, Torts Branch, Federal Tort Claims Act Staff", n),
        Paragraph("U.S. Department of State, Bureau of Diplomatic Security (copy: Office of the Legal Adviser, L/CID)", n),
        Spacer(1, 10),
        Paragraph("Re: List of enclosures — Administrative claim under the Federal Tort Claims Act of Carlos Elías Mahecha Díaz, "
                  "United States v. Carlos Mahecha, Case No. 1:19-cr-20738 (S.D. Fla.)", b), Spacer(1, 8),
        Paragraph("The following documents are enclosed with my claim:", n),
    ]
    k = 0
    for title, _, items in G:
        rows = []
        for name, date, _ in items:
            k += 1
            rows.append([Paragraph(f"{k}.", it), Paragraph(X(name), it), Paragraph(X(date), it)])
        t = Table(rows, colWidths=[24, 340, 140])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                               ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        story += [KeepTogether([Paragraph(X(title), h), t])] if len(rows) < 8 else [Paragraph(X(title), h), t]
    story += [Spacer(1, 18), KeepTogether([
        Paragraph("Respectfully submitted,", n), Spacer(1, 36), Paragraph("_____________________________________", n),
        Paragraph("CARLOS ELÍAS MAHECHA DÍAZ", b), Paragraph("Claimant", n)])]

    def footer(cv, doc):
        cv.setFont(T, 8)
        cv.drawCentredString(306, 22, f"List of enclosures — FTCA claim of Carlos Elías Mahecha Díaz — page {doc.page}")
    SimpleDocTemplate(f"{OUT}/List_of_Enclosures_FTCA_Mahecha.pdf", pagesize=letter, leftMargin=54, rightMargin=54,
                      topMargin=54, bottomMargin=44, title="List of enclosures - FTCA claim Mahecha"
                      ).build(story, onFirstPage=footer, onLaterPages=footer)
    return k


# ------------------------------------------------------------------ checklist (español)
class Box(Flowable):
    def wrap(self, aw, ah): return 10, 10
    def draw(self): self.canv.setLineWidth(0.9); self.canv.rect(0, 0, 10, 10)


def checklist():
    c = ParagraphStyle("c", fontName=F, fontSize=8, leading=9.6)
    cb = ParagraphStyle("cb", fontName=FB, fontSize=8, leading=9.6)
    sec = ParagraphStyle("sec", fontName=FB, fontSize=9, leading=11, textColor=colors.white)
    sm = ParagraphStyle("s", fontName=F, fontSize=8, leading=10)
    head = [Paragraph(h, cb) for h in ("N.º", "Documento (nombre y fecha como en la lista de anexos)", "A<br/>DOJ", "B<br/>State", "C<br/>L/CID", "Nota")]
    data, st = [head], [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 0), (4, -1), "CENTER")]
    k = 0
    for title, sep, items in G:
        i = len(data)
        data.append([Paragraph(X(title.upper()), sec), "", "", "", "", ""])
        st += [("SPAN", (0, i), (-1, i)), ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#1F3864"))]
        if sep:
            i = len(data)
            data.append([Paragraph("Sep.", c), Paragraph(X(f"Hoja separadora: {sep}"), c), Box(), Box(), Box(), ""])
            st.append(("TEXTCOLOR", (0, i), (1, i), colors.HexColor("#595959")))
        for name, date, note in items:
            k += 1
            i = len(data)
            data.append([Paragraph(str(k), c), Paragraph(X(f"{name} — {date}"), c), Box(), Box(), Box(), Paragraph(X(note), c)])
            if note:
                st.append(("BACKGROUND", (5, i), (5, i), colors.HexColor("#FFF2CC")))
    tbl = Table(data, colWidths=[28, 296, 34, 34, 34, 126], repeatRows=1)
    tbl.setStyle(TableStyle(st))
    close = Table([[Paragraph(X(t), c), Box()] for t in [
        "Carta de presentación, SF-95 (recuadros 13a y 14), Addendum y lista de anexos firmados en tinta azul por el Dr. Mahecha en los tres juegos",
        "Fecha escrita a mano en: carta de presentación, SF-95 (recuadro 14), Addendum, lista de anexos y Exhibit 6",
        "Juego A en sobre al DOJ — FedEx: 175 N Street NE, Washington, DC 20002 · USPS: P.O. Box 888, Benjamin Franklin Station, Washington, DC 20044",
        "Juego B en sobre al Bureau of Diplomatic Security, U.S. Department of State, 2201 C Street NW, Washington, DC 20520",
        "Juego C en sobre a L/CID, Office of the Legal Adviser, U.S. Department of State, 2201 C Street NW, Washington, DC 20520",
        "Copia completa para el Dr. Mahecha y copia para la oficina",
        "FedEx Priority Overnight con firma de recibido + USPS certificado con acuse de recibo, a más tardar el lunes 16-nov-2026",
        "Guías y comprobantes guardados; confirmar entrega a más tardar el viernes 20-nov-2026",
    ]], colWidths=[518, 34])
    close.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, -1), "CENTER")]))
    story = [
        Paragraph("CHECKLIST DE ARMADO — RECLAMO FTCA DR. CARLOS ELÍAS MAHECHA DÍAZ", ParagraphStyle("t", fontName=FB, fontSize=13, leading=16)),
        Paragraph("Suma cierta US$2.326.652,15 · Juego A: Department of Justice · Juego B: Department of State (Diplomatic Security) · "
                  "Juego C: copia para L/CID. La numeración coincide con la lista de anexos (List of Enclosures).", sm),
        Spacer(1, 6), tbl, Spacer(1, 10),
        KeepTogether([Paragraph("CIERRE Y ENVÍO", ParagraphStyle("h", fontName=FB, fontSize=10, leading=13)), Spacer(1, 4), close]),
    ]

    def footer(cv, doc):
        cv.setFont(F, 7); cv.drawString(30, 18, "Checklist de armado FTCA Mahecha · versión final 15-nov-2026"); cv.drawRightString(582, 18, f"Página {doc.page}")
    SimpleDocTemplate(f"{OUT}/Checklist_Paquete_FTCA_Mahecha.pdf", pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30,
                      bottomMargin=32, title="Checklist armado FTCA Mahecha").build(story, onFirstPage=footer, onLaterPages=footer)
    return k


print(enclosures(), checklist())
