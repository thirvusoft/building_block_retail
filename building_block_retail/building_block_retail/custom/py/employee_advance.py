import frappe

def after_insert(doc,action):
    doc.remaining_amount = doc.advance_amount