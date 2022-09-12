import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def payroll_entry_customization():
    payroll_custom_fields()
    payroll_property_setter()

def payroll_custom_fields():
    custom_fields = {
        'Payroll Employee Detail':[
             dict(
               fieldname= "total_balance_amount",
                fieldtype= "Currency",
                insert_after= "designation",
                label= "Total Employee Advance Amount",
                read_only = 1
            ),
            dict(
               fieldname= "amount_taken",
                fieldtype= "Currency",
                insert_after= "total_balance_amount",
                label= "Amount Taken",
                depends_on = 'eval:doc.total_balance_amount>0'
            ),
        ]
    }
    create_custom_fields(custom_fields)
def payroll_property_setter():
    make_property_setter('Payroll Entry', 'salary_slip_based_on_timesheet', 'hidden', '1', 'Check')
    make_property_setter('Payroll Entry', 'project', 'hidden', '1', 'Check')