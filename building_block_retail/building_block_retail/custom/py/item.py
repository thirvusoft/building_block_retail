import frappe
import json

def multiply(doc,action):
    return
    # doc.per_rack=36*doc.per_plate
    # doc.pieces_per_bundle=1000/doc.block_weight

@frappe.whitelist()
def get_parent_item_group(item_group):
    parent = ''
    while True:
        parent = frappe.db.get_value("Item Group", item_group, 'parent_item_group')
        if(not parent or parent == 'All Item Groups'):break
        else:item_group = parent
    return item_group
    
def item_validate(doc,action):
    doc.item_name=doc.item_code





   
       


   