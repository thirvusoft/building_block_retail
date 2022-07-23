import frappe

def remove_tax_percent_from_description(doc, event):
    for i in range(len(doc.taxes)):
        doc.taxes[i].description = doc.taxes[i].description.split("@")[0]