import frappe

def throw(from_doc, to_doc, msg=''):
    frappe.throw(f'You should create {frappe.bold(to_doc)} from {frappe.bold(from_doc)}. If you don\'t have enough permission to view {from_doc} contact your Manager. {msg}')

def get_follow_up_settings(doctype):
    settings = frappe.get_single('Document Settings')
    field = ''
    if(doctype == 'Opportunity'):
        field = 'lead_to_opportunity'
    elif(doctype == 'Quotation'):
        field = 'opportunity_to_quotation'
    elif(doctype == 'Sales Order'):
        field = 'quotation_to_sales_order'
    if(not field):return
    return settings.get(field)

def check_doc_follow_up(doc, event=None):
    validate = get_follow_up_settings(doc.doctype)
    if(not validate):return
    if(doc.doctype == 'Opportunity'):
        if(doc.opportunity_from == 'Lead' and not doc.party_name):
            throw('Lead', 'Opportunity')
    elif(doc.doctype == 'Quotation'):
        if(doc.quotation_to != 'Customer'):
            throw('Customer or Opportunity', 'Quotation')
    elif(doc.doctype == 'Sales Order'):
        if(doc.items):
            quotaion = sum([1 for i in doc.items if(i.prevdoc_docname)])
            if(not quotaion):
                throw('Quotation', 'Sales Order')

