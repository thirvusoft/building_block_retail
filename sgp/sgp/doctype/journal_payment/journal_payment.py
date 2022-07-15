# Copyright (c) 2022, ts@info.in and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JournalPayment(Document):
    
	def create_gl_entry(doc,account,credit,debit):
		gl_doc=frappe.new_doc('GL Entry')
		gl_doc.posting_date=doc.date
		gl_doc.account=account
		# gl_doc.cost_center=doc.cost_center
		gl_doc.voucher_type=doc.doctype
		gl_doc.voucher_no=doc.name
		gl_doc.credit=credit
		gl_doc.debit=debit
		gl_doc.company=doc.company_name
		gl_doc.credit_in_account_currency=credit
		gl_doc.debit_in_account_cuurency=debit
		gl_doc.save()
		gl_doc.submit()
	def on_submit(self):
		empaccount  = frappe.get_value("Employee",self.party_name,"contracter_expense_account")
		self.create_gl_entry(self.account,credit=self.amount,debit=0)
		self.create_gl_entry(empaccount,credit=0,debit=self.amount)
  

