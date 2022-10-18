import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_contracter_expense_account():
    custom_fields = {
        "Employee":[
            dict(fieldname='contracter_expense_account',
                 label="Salary Account",
                 fieldtype='Link', 
                 insert_after='column_break_52', 
                 options="Account", 
                 description="Manufacturing cost for Contractor or Earth Rammer Cost of Site Work will add in this account.",
                 mandatory_depends_on='eval:in_list(["Contractor","Earth Rammer Contractor"],doc.designation)'
              ),
            dict(
                fieldname = 'salary_balance',
                label = 'Salary Balance',
                fieldtype = 'Currency',
                insert_after = 'date_of_joining',
                read_only = 1,
                description = "Pending Salary For Job Worker From Salary Slip."
            ),
            dict(
                fieldname = 'employee_percentage',
                label = 'Employee Percentage',
                fieldtype = 'Currency',
                insert_after = 'salary_balance',
                description = "percentage of hike"
            ),
            dict(
                fieldname = 'earth_rammer_cost',
                label = 'Earth Rammer Cost',
                fieldtype = 'Currency',
                insert_after = 'employment_type',
                description = "Per Sqft",
                mandatory_depends_on = 'eval:doc.designation == "Earth Rammer Contractor"',
                depends_on = 'eval:doc.designation == "Earth Rammer Contractor"'
            )
        ]
    }
    
    create_custom_fields(custom_fields)
    