# from erpnext.erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
from dataclasses import fields
import json
import frappe
from frappe.utils.data import flt
import erpnext
from frappe import _


@frappe.whitelist()
def create_journal_entry(self):
    print(self)
    self = json.loads(self)
    print(self.get("company"))
    new_journel = frappe.new_doc("Journal Entry")
    new_journel.company = self.get("company")
    new_journel.posting_date = self.get("posting_date")
    salary_slip = frappe.get_all("Salary Slip",filters={"payroll_entry": self.get("name")},fields=["gross_pay","employee"])          
    print(salary_slip)
    # new_journel.accounts =  [{"account": self.get("payment_account"),"credit_in_account_currency": },{"account": self.get("payroll_payable_account")}]
    # new_journel.payroll_payable_account =  [{"accounts": self.get("account")}]
    print(new_journel)
    new_journel.insert()
