from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe



def supplier_quotation():
    custom_fields = {
     
        "Supplier Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
            
        ],
    }
    create_custom_fields(custom_fields)