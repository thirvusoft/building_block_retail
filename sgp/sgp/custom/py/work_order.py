import frappe
def before_save(doc,action):
    for d in doc.get("operations"):
        ws=frappe.get_doc("Workstation",d.workstation)
        doc.total_expanse = ws.expanse_per_piece