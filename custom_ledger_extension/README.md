# Custom Ledger Extension — Odoo 19 Enterprise

Adds three native string columns to Partner Ledger, General Ledger, Aged Receivable and Aged Payable.

| Column | Source |
|---|---|
| Bill Number | account.move.name (invoice/bill/journal-entry number) |
| Supplier Reference | account.move.ref |
| Our Reference | account.move.x_studio_po_number (Studio PO number) |


## All accounting reports: loading indicator