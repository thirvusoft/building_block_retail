import frappe
from frappe.utils.data import get_link_to_form

def validate_branch(self, event=None):
    branch_credit_debit = {}
    for row in self.accounts:
        if row.branch:
            if row.reference_type and row.reference_name:
                validate_je_branch(self, row)

            if row.branch not in branch_credit_debit:
                branch_credit_debit[row.branch] = {
                    'credit': 0,
                    'debit': 0
                }
            branch_credit_debit[row.branch]['credit'] += (row.credit or 0)
            branch_credit_debit[row.branch]['debit'] += (row.debit or 0)
    
    for branch in branch_credit_debit:
        if branch_credit_debit[branch].get('credit') != branch_credit_debit[branch].get('debit'):
            frappe.throw(f"""For branch {branch} credit { branch_credit_debit[branch].get('credit')} and debit { branch_credit_debit[branch].get('debit')} are not equal.""")

def validate_je_branch(self, row):
    if frappe.get_meta(row.reference_type).has_field('branch'):
        if (branch := frappe.db.get_value(row.reference_type, row.reference_name, 'branch')) and branch != row.branch:
                frappe.throw(f"""{self.doctype} {get_link_to_form(self.doctype, self.name)} at row {row.idx} branch {row.branch} is not same as {row.reference_type} {get_link_to_form(row.reference_type, row.reference_name)} branch {branch}""")

def remove_unacc_entries(self, event=None):
    if frappe.local.site == 'vbprime.thirvusoft.com':
        accounts = []
        for row in self.accounts:
            if row.branch != 'SVPB1':
                accounts.append(row)

        self.update({
            'accounts': accounts
        })
