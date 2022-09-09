from warnings import filters
from building_block_retail.building_block_retail.custom.py.vehicle_log import notification
import frappe


@frappe.whitelist()
def get_permission_for_attachment(user):
    user = frappe.get_all("Has Role", filters={'parent':user, 'role':'Supervisor'}, pluck='role')
    if(len(user)):return False
    return True

def workflow_quotation(doc,action):
    if doc.workflow_state == "Waiting for Approval":
        user_list = frappe.get_all("Has Role",pluck="parent",filters={"role":"Admin","parent":['!=', 'Administrator']})
        for i in user_list:
            notification = frappe.new_doc("Notification Log")
            notification.update({
                "subject" : f"{doc.name} Quotation has been waiting for your approval",
                "email_content" : f"{doc.name} Quotation has been waiting for your approval",
                "document_type" : "Quotation",
                "document_name" : doc.name,
                "for_user" : i,
                "from_user" : doc.owner,
                "type" : "Energy Point"
            })
            notification.insert(ignore_permissions=True)

