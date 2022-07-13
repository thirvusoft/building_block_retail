import frappe
from frappe import _
from frappe.model.document import Document

def create_docs():
    if(not frappe.db.exists("User", "admin@gmail.com")):
        create_docs = frappe.get_doc(
            {
                "doctype": "User",
                "first_name": "Admin",
                "email": "admin@gmail.com",
                "username": "admin@gmail.com",
                "send_welcome_email": 0
            }
        )
        create_docs.insert()
    if(not frappe.db.exists("UOM","bundle")):
        create_docs = frappe.get_doc(
            {
                "doctype": "UOM",
                "enabled": 1,
                "uom_name": "bundle",
                "must_be_whole_number": 1
            }
        )
        create_docs.insert()
    if(not frappe.db.exists("Item Group","Pavers")):
        create_docs = frappe.get_doc(
            {
                "doctype": "Item Group",
                "item_group_name": "Pavers"
            }
        )
        create_docs.insert()
    if(not frappe.db.exists("Item Group","Compound Walls")):
        create_docs = frappe.get_doc(
            {
                "doctype": "Item Group",
                "item_group_name": "Compound Walls"
            }
        )
        create_docs.insert()