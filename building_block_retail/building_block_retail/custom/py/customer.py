from erpnext.accounts.party import get_dashboard_info
import frappe
from frappe.utils.data import fmt_money

def autoname(doc, event):
    doc.name = (doc.customer_name or '') +"-"+ (doc.mobile_no or doc.territory or '')

@frappe.whitelist()
def customer_outstanding_amount(company, customer):
	info = get_dashboard_info("Customer", customer)
	for i in info:
		if(i.get("company") == company):
			return fmt_money(amount = i.get("total_unpaid"), currency=i.get('currency')) or 0
