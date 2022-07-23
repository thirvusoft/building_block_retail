import frappe
from frappe.utils.data import get_link_to_form

def before_save(doc,action):
    item=frappe.get_doc("Item",doc.production_item)
    if(not item.employee_rate):
        link = get_link_to_form('Item', doc.production_item)
        frappe.throw(f"Manufacturing expense for <b>{doc.production_item} is 0</b>. Please set Employee Rate field > 0 in <b>{link}</b>.")
    doc.total_expanse = item.employee_rate