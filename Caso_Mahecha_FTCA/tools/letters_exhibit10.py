"""Agrega el Exhibit 10 (evaluación psicológica forense) a las cartas de presentación."""
import copy, sys
from docx import Document

EX10 = ("Exhibit 10 — ", "Independent forensic psychological evaluation of the claimant by Gustavo R. Benejam, Psy.D., "
        "Licensed Clinical Psychologist (report of November 12, 2026), with the Florida Department of Health license "
        "verification of Dr. Benejam (License PY7387).")
REPL = [
    ("Supporting evidence, including a forensic psychological evaluation, will be supplemented.",
     "These injuries are documented in the independent forensic psychological evaluation enclosed as Exhibit 10."),
    ("(a) the forensic psychological evaluation now in progress; (b) declarations of family members; (c) written confirmation "
     "from counsel Luis Salazar regarding Invoice 6384; (d) the trust-account ledgers of Piñera-Vazquez Law Firm and Carlton "
     "Fields, and the bail bond agent's contract and receipts; (e) copies of three K&L Gates invoices that appear in its "
     "statement of account; (f) the documents evidencing my reimbursement obligations to those who paid on my behalf; and "
     "(g) relevant trial transcript excerpts.",
     "(a) declarations of family members; (b) written confirmation from counsel Luis Salazar regarding Invoice 6384; (c) the "
     "trust-account ledgers of Piñera-Vazquez Law Firm and Carlton Fields, and the bail bond agent's contract and receipts; "
     "(d) copies of three K&L Gates invoices that appear in its statement of account; (e) the documents evidencing my "
     "reimbursement obligations to those who paid on my behalf; and (f) relevant trial transcript excerpts."),
    ("Enclosures: SF-95 with Addendum; Exhibits 1 to 9.", "Enclosures: SF-95 with Addendum; Exhibits 1 to 10."),
]

for path in sys.argv[1:]:
    d = Document(path)
    done = {k: 0 for k, _ in REPL}
    ex9 = None
    for p in d.paragraphs:
        for r in p.runs:
            for old, new in REPL:
                if old in r.text:
                    r.text = r.text.replace(old, new); done[old] += 1
        if p.runs and p.runs[0].text.startswith("Exhibit 9 —"):
            ex9 = p
    assert all(v == 1 for v in done.values()), done
    assert ex9 is not None
    new = copy.deepcopy(ex9._p)
    ex9._p.addnext(new)
    from docx.text.paragraph import Paragraph
    np_ = Paragraph(new, ex9._parent)
    np_.runs[0].text, np_.runs[1].text = EX10
    for r in np_.runs[2:]:
        r.text = ""
    d.save(path)
    print("ok", path)
