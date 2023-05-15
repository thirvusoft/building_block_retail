import frappe

def cal_per_hour(doc, actions):
    validate_for_duplicate_item(doc)
    total_hour= 0
    total_net_hour = 0
    total_hour = doc.administrator_expense + total_hour
    total_net_hour = doc.hour_rate + total_net_hour
    doc.hour_rate = total_hour + total_net_hour

def validate_for_duplicate_item(doc):
    items = {}
    for i in doc.item_wise_production_capacity:
        if i.item_code in items:
            items[i.item_code][0] += 1
            items[i.item_code][1].append(str(i.idx))
        else:
            items[i.item_code] = [1, [str(i.idx)]]
    error_msg = ''
    for i in items:
        if(items[i][0]>1):
            error_msg+=f"<p>Item: <b>{i}</b> entered {items[i][0]} times in Rows: <b>{', '.join(items[i][1])}</b></p>"
    if(error_msg):
        frappe.throw(error_msg)