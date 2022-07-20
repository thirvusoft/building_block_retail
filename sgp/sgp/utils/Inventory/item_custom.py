from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_Customization():
    item_customization()

def item_customization():
    custom_fields={
        "Item":[
            dict(
                 fieldname  = "employee_rate",
                 fieldtype  = "Currency",
                 insert_after  = "standard_rate",
                 label = "Employee Rate",
                 description = "per qty"
            ),
        ],
    }
    create_custom_fields(custom_fields)