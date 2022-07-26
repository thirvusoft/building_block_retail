import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_contracter_expense_account():
    custom_fields = {
        "Employee":[
            dict(fieldname='contracter_expense_account',
                 label="Salary Account for Contracter",
                 fieldtype='Link', 
                 insert_after='column_break_52', 
                 options="Account", 
                 description="Manufacturing cost for Contracter will add in this account."
              ),
            dict(
                fieldname = 'salary_balance',
                label = 'Salary Balance',
                fieldtype = 'Currency',
                insert_after = 'date_of_joining',
                read_only = 1,
                depends_on = "eval:doc.designation == 'Job Worker'",
                description = "Pending Salary For Job Worker From Salary Slip."
            )
        ]
    }
    
    create_custom_fields(custom_fields)
    