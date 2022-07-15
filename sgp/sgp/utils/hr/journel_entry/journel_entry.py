# from erpnext.erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
from dataclasses import fields
import json

from requests import delete
import frappe
from frappe.utils.data import flt
import erpnext
from frappe import _, delete_doc


@frappe.whitelist()
def create_journal_entry(self):
    self = json.loads(self)
    if self.get("payment_account") == "":
        frappe.throw("Kindly Select Payment Account") 
        return
    new_journel = frappe.new_doc("Journal Entry")
    new_journel.company = self.get("company")
    new_journel.posting_date = self.get("posting_date")
    new_journel.accounts =  [] 
    salary_slip = frappe.get_all("Salary Slip",filters={"payroll_entry": self.get("name"),"docstatus":1},fields=["gross_pay","employee"])  
    if len(salary_slip) == 0:
        frappe.throw("Kindly click submit salary slip button or create salary slip")
        return      
    employee_salary = {}
    for i in salary_slip:
          empaccount = frappe.get_value("Employee",i.employee,"contracter_expense_account")
          if empaccount:
              employee_salary[i.employee] = [empaccount,i.gross_pay]  
    total_debit = 0
    for j in employee_salary:
        new_journel.append("accounts",{"account":employee_salary[j][0],"credit_in_account_currency":flt(employee_salary[j][1])})
        total_debit += flt(employee_salary[j][1])
    new_journel.append("accounts",{"account":self.get("payment_account"),"debit_in_account_currency":total_debit})
    # new_journel.docstatus=1
    new_journel.submit()
    # new_journel.make_gl_entries()
    # frappe.delete_doc("Journal Entry",new_journel.get("name"),force=1)
    frappe.msgprint("Journel Entry Submitted")