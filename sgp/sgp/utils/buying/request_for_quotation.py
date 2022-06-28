from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter




def request_for_quotation():
    custom_fields = {
        "Request for Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='naming_series', read_only=0,reqd=1),
            
        ],
     
    }
    create_custom_fields(custom_fields)