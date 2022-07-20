import frappe
def before_save(doc,action):
    item=frappe.get_doc("Item",doc.production_item)
    doc.total_expanse = item.employee_rate
        
def validate(doc, event):
    if(doc.sales_order):
        so = doc.sales_order
        ordered_qty, warehouse, stock_uom = frappe.db.get_value("Sales Order Item",{'parent':so, 'item_code':doc.production_item},['stock_qty','warehouse','stock_uom'])
        res_qty, act_qty = frappe.db.get_value("Bin",{'warehouse':warehouse, 'item_code':doc.production_item, 'stock_uom':stock_uom},['reserved_qty','actual_qty'])
        qty = 0
        if(res_qty<act_qty):qty = qty = act_qty-res_qty
        print(qty)
        if(qty >0 and qty < doc.qty):
            doc.priority = "High Priority"
        doc.available_qty = qty
