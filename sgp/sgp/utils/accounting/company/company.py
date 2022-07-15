from decimal import DefaultContext
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def company_customization():
    company_custom_field()
    company_property_setter()

def company_custom_field():
    custom_fields={
        "Company":[
            dict(
                fieldname= "default_employee_expenses_account",
                fieldtype= "Link",
                insert_after= "unrealized_profit_loss_account",
                label= "Default Employee Expenses Account",
                options = "Account",
            ),
        ]
    }
    create_custom_fields(custom_fields)

def company_property_setter():
    pass