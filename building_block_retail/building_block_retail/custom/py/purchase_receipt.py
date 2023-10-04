import frappe
from frappe.utils.data import get_link_to_form

def validate_branch(self, event=None):
    if self.branch:
        for row in self.items:
            if row.purchase_order:
                if (branch := frappe.db.get_value('Purchase Order', row.purchase_order, 'branch')) and branch != self.branch:
                    frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} branch {self.branch} is not same as Purchase Order {get_link_to_form('Purchase Order', row.purchase_order)} branch {branch}""")
            
            if row.purchase_invoice:
                if (branch := frappe.db.get_value('Purchase Invoice', row.purchase_invoice, 'branch')) and branch != self.branch:
                    frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} branch {self.branch} is not same as Purchase Invoice {get_link_to_form('Purchase Invoice', row.purchase_invoice)} branch {branch}""")
