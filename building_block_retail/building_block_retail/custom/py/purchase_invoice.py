import frappe
import json

def remove_tax_percent_from_description(doc, event):
    for i in range(len(doc.taxes)):
        doc.taxes[i].description = doc.taxes[i].description.split("@")[0]
def create_landed_cost_voucher(doc,action):
    if doc.transporter=="Own Transporter":
        if doc.taxes_and_charges_in_landed:
            new_doc = frappe.new_doc("Landed Cost Voucher")
            new_doc.company = doc.company
            new_doc.distribute_charges_based_on = doc.get('distribute_charges_based_on')
            new_doc.append("purchase_receipts",dict(
                receipt_document_type = doc.doctype,
                receipt_document = doc.name
            ))
            for i in doc.taxes_and_charges_in_landed:
                new_doc.append("taxes",dict(
                    expense_account = i.expense_account,
                    description = i.description,
                    amount = i.amount
                ))
            new_doc.save()
            new_doc.submit()
        else:
            frappe.throw("Kindly Enter Applicable Charges")
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
