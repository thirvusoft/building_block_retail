from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def bank_account_customization():
    create_custom_field()
    create_property_setter()
    
def create_custom_field():
    custom_fields = {
        "Bank Account": [
            dict(
                fieldname= "branch",
                fieldtype= "Data",
                insert_after= "iban",
                label= "Branch",
            ),
        ]
    }
    create_custom_fields(custom_fields)
    
def create_property_setter():
    pass