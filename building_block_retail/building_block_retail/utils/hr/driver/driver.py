import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def driver_customization():
    driver_custom_field()
    driver_property_setter()

def driver_custom_field():
    custom_fields={
        "Driver":[
            dict(
               fieldname= "employee_categories",
                fieldtype= "Link",
                insert_after= "address",
                label= "Employee Categories",
                options = "Designation"
            ),
            
        ]
    }
    create_custom_fields(custom_fields)

def driver_property_setter():
    doctype = "driver"
    make_property_setter(doctype, 'transporter', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'cell_number', 'reqd', '1', 'Check')