import frappe
import json

@frappe.whitelist()
def add_supplier_to_default_supplier_in_item(doc, action=None):
    if(type(doc)==str):
        doc=json.loads(doc)
    for i in doc.get('default_items'):
        if(not frappe.db.exists("Item Supplier", {'parent': i.get('item'),'parentfield': 'supplier_items','parenttype' : 'Item','supplier' : doc.get('supplier_name')})):
            default = frappe.new_doc('Item Supplier')
            default.update({
                'parent': i.get('item'),
                'parentfield': 'supplier_items',
                'parenttype' : 'Item',
                'supplier' : doc.get('supplier_name')
            })
            default.save(ignore_permissions = True)
            
@frappe.whitelist()
def remove_default_supplier_from_items(doc):
    doc = json.loads(doc)
    if(type(doc)==list):
        for i in doc:
            dn=frappe.get_value('Item Supplier', {'parent':i['item'],'parentfield': 'supplier_items','parenttype' : 'Item','supplier' : i['parent']}, 'name')
            frappe.delete_doc_if_exists('Item Supplier', dn)
    else:
        dn=frappe.get_value('Item Supplier', {'parent':doc['item'],'parentfield': 'supplier_items','parenttype' : 'Item','supplier' : doc['parent']}, 'name')
        frappe.delete_doc_if_exists('Item Supplier', dn)