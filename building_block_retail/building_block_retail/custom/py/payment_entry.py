import frappe
from frappe.utils.data import get_link_to_form

def validate_branch(self, event=None):
    if self.branch:
        for row in self.references:
            if row.reference_doctype and row.reference_name and frappe.get_meta(row.reference_doctype).has_field('branch'):
                if (branch := frappe.db.get_value(row.reference_doctype, row.reference_name, 'branch')) and branch != self.branch:
                    frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} branch {self.branch} is not same as {row.reference_doctype} {get_link_to_form(row.reference_doctype, row.reference_name)} at row {row.idx}  branch {branch}""")
