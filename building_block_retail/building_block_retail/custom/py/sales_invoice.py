import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax
from erpnext.controllers.taxes_and_totals import get_itemised_taxable_amount
def update_customer(self,event):
    cus=self.customer
    for row in self.items:
        so=row.sales_order
        if(so):
            doc=frappe.get_doc('Sales Order', so)
            if(cus!=doc.customer):
                frappe.db.set(doc, "customer", cus)


def validate_tax_inclusive(doc, event=None):
    for i in (doc.taxes or []):
        i.included_in_print_rate = doc.set_inclusive_tax

def validate(doc, event=None):
    get_measured_qty(doc)

def get_measured_qty(doc):
    if doc.site_work:
        doc.measured_qty = frappe.db.get_value("Site Work", doc.site_work, "measured_qty")
    else:
        doc.measured_qty = 0