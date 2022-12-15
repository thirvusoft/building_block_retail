import frappe

def autoname(doc, event):
    doc.name = (doc.customer_name or '') +"-"+ (doc.mobile_no or doc.territory or '')