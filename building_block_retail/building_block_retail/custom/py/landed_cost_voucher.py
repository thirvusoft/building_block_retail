import frappe
def on_submit(doc,action):
    for i in doc.items:
        items =''
        if i.receipt_document_type == "Purchase Invoice":
            items = "Purchase Invoice Item"
        elif i.receipt_document_type == "Purchase Receipt":
            items = "Purchase Receipt Item"
        if items:
            purchased_uom = frappe.get_value(items,i.purchase_receipt_item,"uom")
            stock_uom = frappe.get_value(items,i.purchase_receipt_item,"stock_uom")
            conversion_factor = frappe.get_value(items,i.purchase_receipt_item,"conversion_factor")
            get_item_pl = frappe.get_all("Item Price",{'item_code':i.item_code,'buying':1})
            total_amount = i.rate+(i.applicable_charges/i.qty)
            conv = frappe.get_value("UOM Conversion Detail", {'parent':i.item_code, 'uom':purchased_uom}, 'conversion_factor') or 1
            stock_uom_rate = total_amount/conv
            	
            for j in get_item_pl:
                pl = frappe.get_doc("Item Price",j.name)
                conv = frappe.get_value("UOM Conversion Detail", {'parent':pl.item_code, 'uom':pl.uom}, 'conversion_factor') or 1
                pl.price_list_rate = stock_uom_rate * conv
                pl.save()

           