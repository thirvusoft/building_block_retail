import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax
from erpnext.controllers.taxes_and_totals import get_itemised_taxable_amount
from frappe.utils.data import get_link_to_form
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

def validate_branch(self, event=None):
    if self.branch:
        for row in self.items:
            if row.sales_order:
                if (branch := frappe.db.get_value('Sales Order', row.sales_order, 'branch')) and branch != self.branch:
                    frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} branch {self.branch} is not same as Sales Order {get_link_to_form('Sales Order', row.sales_order)} branch {branch}""")
            
            if row.delivery_note:
                if (branch := frappe.db.get_value('Delivery Note', row.delivery_note, 'branch')) and branch != self.branch:
                    frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} branch {self.branch} is not same as Delivery Note {get_link_to_form('Delivery Note', row.delivery_note)} branch {branch}""")
