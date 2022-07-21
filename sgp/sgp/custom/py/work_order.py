import frappe
def before_save(doc,action):
    item=frappe.get_doc("Item",doc.production_item)
    doc.total_expanse = item.employee_rate