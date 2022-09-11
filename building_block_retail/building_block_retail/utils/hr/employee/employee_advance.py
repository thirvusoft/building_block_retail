import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def employee_advance_customization():
    employee_advance_custom_fields()
    employee_advance_property_setter()
    
def employee_advance_custom_fields():
    custom_field = {
        'Employee Advance':[
            dict(fieldname='remaining_amount', label='Remaining Amount', fieldtype='Currency', insert_after='return_amount', 
                 read_only=1, allow_on_submit=1)
        ]
    }
    create_custom_fields(custom_field)

def employee_advance_property_setter():
    pass