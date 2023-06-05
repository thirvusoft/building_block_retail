import frappe

def cal_per_hour(doc, actions):
    validate_for_duplicate_item(doc)
    total_hour= 0
    total_net_hour = 0
    total_hour = doc.administrator_expense or 0 + total_hour
    total_net_hour = doc.hour_rate + total_net_hour
    doc.hour_rate = total_hour + total_net_hour
    if doc.item_template and doc.item_wise_production_capacity:
        for i in doc.item_template:
            for j in doc.item_wise_production_capacity:
                if (j.variant_of == i.template):
                    j.production_capacity=i.qty

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





@frappe.whitelist()
def item_list(items,template):
    print(template)
    item_group = []
    parent_grps = []  
    item_list=[]
    item_list1=[]
    final_list=[]
    items=json.loads(items)
    template=json.loads(template)
  
    settings_doc=frappe.get_doc("Manufacturing Settings","Manufacturing Settings")
    settings_item_format=frappe.db.get_single_value("Manufacturing Settings","get_items")
    for i in settings_doc.item_groups:
        parent_grps.append(i.item_group)


    for i in parent_grps:
        item_group.extend(frappe.get_all('Item Group', filters={'parent_item_group':['in', i]}, pluck='name'))      
        parent_grps.extend(frappe.get_all('Item Group', filters={'parent_item_group':['in', i], 'is_group':1}, pluck='name'))
    item_group=item_group + parent_grps
    if(settings_item_format == "Template"):
        item_list=frappe.get_list("Item",filters={"item_group":["in",item_group],"has_variants":1,"name":["not in",template],"disabled":0},fields=["item_code"])
        item_list1=frappe.get_list("Item",filters={"item_group":["in",item_group],"has_variants":0,"disabled":0,"name":["not in",items]},fields=["item_code","variant_of"])
        final_list.append(item_list)
        final_list.append(item_list1)
        return final_list

    else:
        item_list=frappe.get_list("Item",filters={"item_group":["in",item_group],"has_variants":0,"disabled":0,"name":["not in",items]},fields=["item_code","variant_of"])
        item_list.append({"item_format":"Variant"})
        return item_list

