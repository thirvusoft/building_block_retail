import frappe

def validate(doc, event):
    if(doc.buying == 1 and doc.is_new()):
        purchase_uom = frappe.get_value("Item", doc.item_code, 'purchase_uom')
        if(purchase_uom):
            conv = frappe.get_value("UOM Conversion Detail", {'parent':doc.item_code, 'uom':purchase_uom}, 'conversion_factor')
            doc.uom = purchase_uom
            doc.price_list_rate *= conv