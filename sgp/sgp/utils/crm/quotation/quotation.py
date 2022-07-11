import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def quotation_customization():
    quotation_custom_field()
    quotation_property_setter()

def quotation_custom_field():
    custom_fields={
        "Quotation":[
            dict(
                fieldname= "supervisor",
                fieldtype= "Link",
                insert_after= "customer_name",
                label= "Supervisor",
                options= "Employee"
            ),
        ]
    }
    create_custom_fields(custom_fields)

def quotation_property_setter():
    pass