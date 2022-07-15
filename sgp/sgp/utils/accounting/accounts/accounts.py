from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def account_customization():
    create_custom_field()
    create_property_setter()
    
def create_custom_field():
    custom_fields = {
        "Account": [
            dict(
                fieldname= "employee",
                fieldtype= "Link",
                insert_after= "company",
                label= "Employee",
                options = "Employee",
                description = "Employee or Contractor for this account to add Manufacturing Cost"
            ),
        ]
    }
    create_custom_fields(custom_fields)
    
def create_property_setter():
    make_property_setter('Account','quick_entry','quick_entry',1,'Check',for_doctype=True)