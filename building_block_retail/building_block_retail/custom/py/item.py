import frappe

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


@frappe.whitelist()
def item_list():
    item_group = []
    parent_grps = ['Products']   
    for i in parent_grps:
        item_group.extend(frappe.get_all('Item Group', filters={'parent_item_group':['in', i]}, pluck='name'))        
        parent_grps.extend(frappe.get_all('Item Group', filters={'parent_item_group':['in', i], 'is_group':1}, pluck='name'))
    item_group=item_group + parent_grps
    item_list=frappe.get_list("Item",filters={"item_group":["in",item_group],"has_variants":0,"disabled":0},fields=["item_code"])
    return item_list





   