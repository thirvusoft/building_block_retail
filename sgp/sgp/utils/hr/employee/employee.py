import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_contracter_expense_account():
    custom_fields = {
        "Employee":[
            dict(fieldname='contracter_expense_account', label="Salary Account for Contracter",
              fieldtype='Link', insert_after='column_break_52', options="Account", description="Manufacturing cost for Contracter will add in this account."
              )
        ]
    }
    
    create_custom_fields(custom_fields)
    