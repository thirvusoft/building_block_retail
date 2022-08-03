import frappe


@frappe.whitelist()
def get_permission_for_attachment(user):
    user = frappe.get_all("Has Role", filters={'parent':user, 'role':'Supervisor'}, pluck='role')
    if(len(user)):return False
    return True