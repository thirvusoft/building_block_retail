from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe



def request_for_quotation():
    custom_fields = {
        "Request for Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='naming_series', read_only=0,reqd=1),
            
        ],
     
    }
    request_for_quotation=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Request For Quotation",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"more_info",
        "value":1
    })
    request_for_quotation.save()
    create_custom_fields(custom_fields)