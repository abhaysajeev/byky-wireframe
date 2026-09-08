"""Credit Note Management.

Not an FSD module -- built from the client's own "RMS WEB" screenshots
(RMS WEB 07.09.2026-1.pdf, page 7: "Credit Note Management"), the same way
Fare & Schemes and Discount Card Management were built from mockups rather
than an FSD PDF. Those screenshots are captures of the client's live legacy
system -- real order numbers, real staff names -- not a data export we have
programmatic access to, so none of it is reproducible here. Every list below
therefore starts genuinely empty and nothing is invented (CLAUDE.md 12).

The 5% VAT credit-note split is real, working logic: Gross = Amount / (1 +
VAT), Tax = Amount - Gross. The source PDF's own worked example has an
arithmetic error -- it states "70 / 1.05 = 60.67", but 70 / 1.05 is actually
66.67 (so Tax = 70 - 66.67 = 3.33, not the PDF's 9.33). credit_note_split()
implements the mathematically correct formula, not the source's misstated
result -- noted here so nobody "corrects" this code to match the PDF's wrong
number later.
"""

VAT_RATE = 0.05


def credit_note_requests():
    """Credit note requests submitted through the customer app (RMS APK),
    awaiting approval. No source data -- honest empty list."""
    return []


def tax_invoices():
    """Closed rental invoices eligible for a credit note (the Results tab's
    grid). No source data -- honest empty list."""
    return []


def credit_note_split(amount):
    """Gross and tax portions of a credit note amount at the standard 5% VAT
    split (see module docstring re: the source PDF's arithmetic error)."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return None
    gross = round(amount / (1 + VAT_RATE), 2)
    tax = round(amount - gross, 2)
    return {"gross": gross, "tax": tax}
