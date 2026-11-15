"""Hojas separadoras de los exhibits (una por página). Uso: python3 build_separators.py <salida.pdf>"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

S = [
 ("EXHIBIT 1", "Indictment"),
 ("EXHIBIT 2", "Affidavits in support of extradition"),
 ("EXHIBIT 3", "Docket sheet"),
 ("EXHIBIT 4", "Bond, conditions of release and removal of GPS monitor"),
 ("EXHIBIT 5", "Jury Verdict, Judgment of Acquittal and disbursement of bond"),
 ("EXHIBIT 6", "Itemized schedule of attorneys' fees and defense costs"),
 ("EXHIBIT 7", "Engagement letters and invoices"),
 ("EXHIBIT 7-A", "Piñera-Vazquez Law Firm, P.A."),
 ("EXHIBIT 7-B", "Salazar Law, LLP"),
 ("EXHIBIT 7-C", "Cooper Strategic Solutions, LLC"),
 ("EXHIBIT 7-D", "The FairWay, LLC"),
 ("EXHIBIT 7-E", "Intentionally omitted"),
 ("EXHIBIT 7-F", "Carlton Fields, P.A. (Matter 13390-36114)"),
 ("EXHIBIT 7-G", "K&L Gates LLP"),
 ("EXHIBIT 8", "Proof of payment"),
 ("EXHIBIT 8-01", "Salazar Law, LLP — Invoice 6384"),
 ("EXHIBIT 8-02", "Piñera-Vazquez Law Firm, P.A. — Trial Representation Fee"),
 ("EXHIBIT 8-03", "Piñera-Vazquez Law Firm, P.A. — Fee balance and LexisNexis"),
 ("EXHIBIT 8-04", "Piñera-Vazquez Law Firm, P.A. — Invoice of March 2021"),
 ("EXHIBIT 8-05", "Cooper Strategic Solutions, LLC — US$102,525"),
 ("EXHIBIT 8-06", "Cooper Strategic Solutions, LLC — Invoice 1002"),
 ("EXHIBIT 8-07", "Cooper Strategic Solutions, LLC — Invoice 1003"),
 ("EXHIBIT 8-08", "The FairWay, LLC — Invoice #23-032"),
 ("EXHIBIT 8-09", "The FairWay, LLC — Invoice #23-042"),
 ("EXHIBIT 8-10", "The FairWay, LLC — Invoice #24-313"),
 ("EXHIBIT 8-11", "The FairWay, LLC — Second payment of March 2024"),
 ("EXHIBIT 8-12", "The FairWay, LLC — Invoice 24-1015"),
 ("EXHIBIT 8-13", "The FairWay, LLC — Invoice 24-1123"),
 ("EXHIBIT 8-14", "Carlton Fields, P.A. — Matter 13390-36114"),
 ("EXHIBIT 8-15", "K&L Gates LLP"),
 ("EXHIBIT 9", "Forensic accounting report and trial minute entries"),
 ("EXHIBIT 10", "Forensic psychological evaluation"),
]

c = canvas.Canvas(sys.argv[1], pagesize=letter)
c.setTitle("Exhibit separator sheets - FTCA claim Mahecha")
W, H = letter
for title, sub in S:
    c.setFont("Helvetica-Bold", 64 if len(title) <= 10 else 56)
    c.drawCentredString(W / 2, H / 2 + 20, title)
    c.setLineWidth(2); c.line(108, H / 2, W - 108, H / 2)
    c.setFont("Helvetica", 20)
    y = H / 2 - 40
    for ln in simpleSplit(sub, "Helvetica", 20, W - 200):
        c.drawCentredString(W / 2, y, ln); y -= 26
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 54, "FTCA administrative claim of Carlos Elías Mahecha Díaz — "
                        "United States v. Carlos Mahecha, Case No. 1:19-cr-20738 (S.D. Fla.)")
    c.showPage()
c.save()
print(len(S))
