import frappe
import json

def remove_tax_percent_from_description(doc, event):
    for i in range(len(doc.taxes)):
        doc.taxes[i].description = doc.taxes[i].description.split("@")[0]

@frappe.whitelist()
def make_vehicle_log(doc, data, vehicles):
    if isinstance(doc, str):
        doc = json.loads(doc)
    if isinstance(data, str):
        data = json.loads(data)
    if isinstance(vehicles, str):
        vehicles = eval(vehicles)
    doc = frappe.get_doc(doc)
    docnames = []
    for count, vehicle in enumerate(vehicles):
        qty = sum([i.qty for i in doc.items if(i.item_group=='Fuel' and i.vehicle == vehicle)])
        rate = sum([i.rate for i in doc.items if(i.item_group=='Fuel' and i.vehicle == vehicle)])
        amount = sum([i.amount for i in doc.items if(i.item_group=='Fuel' and i.vehicle == vehicle)])
        vl = frappe.new_doc('Vehicle Log')
        vl.update({
            'license_plate':vehicle,
            'employee':data[f'employee{count}'],
            'date':doc.posting_date,
            'odometer':data[f'odd{count}'],
            'select_purpose':'Fuel',
            'ts_total_cost':amount,
            'fuel_qty':qty,
            'fuel_price':rate,
            'invoice':doc.name,
            'supplier':doc.supplier
        })
        vl.flags.ignore_permissions = True
        vl.insert()
        vl.submit()
        docnames.append(vl.name)
    return docnames
