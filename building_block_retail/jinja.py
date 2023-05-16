import frappe
from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_data
from frappe.utils.data import flt

jenvs = {
    "methods":[
    "tax:building_block_retail.jinja.tax"
    ]
}
def tax(doc):
    doc = frappe.get_doc("Sales Invoice", doc)
    itemised_tax, itemised_taxable_amount = get_itemised_tax_breakup_data(doc)
    print(itemised_tax)
    precision = doc.precision("tax_amount", "taxes") or 2
    for taxes in itemised_tax.values():
        for tax_account in taxes:
            if('TDS' in tax_account or 'TCS' in tax_account):
                taxes[tax_account]["tax_amount"] = round(taxes[tax_account]["tax_amount"])
            else:
                taxes[tax_account]["tax_amount"] = flt(taxes[tax_account]["tax_amount"], precision)
    tax_rates = {}
    originals = {}
    for i in itemised_tax:
        for j in itemised_tax[i]:
            if(not itemised_tax[i][j]['tax_rate']):
                continue
            if(not f"{j}{itemised_tax[i][j]['tax_rate']}" in tax_rates):
                originals[f"{j}{itemised_tax[i][j]['tax_rate']}"] = j
                tax_rates[f"{j}{itemised_tax[i][j]['tax_rate']}"] = [itemised_tax[i][j]['tax_rate'], itemised_tax[i][j]['tax_amount']]
            else:
                tax_rates[f"{j}{itemised_tax[i][j]['tax_rate']}"][1] += itemised_tax[i][j]['tax_amount']
    descriptions = []
    for i in tax_rates:
        desc = i
        if('sgst' in i.lower()):
            desc='SGST'
        elif('cgst' in i.lower()):
            desc='CGST'
        elif('igst' in i.lower()):
            desc='IGST'
        else:
            desc = originals[desc]
        descriptions.append({'description':desc, 'percent':tax_rates[i][0], 'tax_amount':tax_rates[i][1]})
    return descriptions