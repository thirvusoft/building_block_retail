import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def create_salary_custom_field():
    custom_field = {
        'Salary Slip': [
            dict(
                fieldname = 'ts_hr_employee_salary_report',
                fieldtype = 'Table',
                options = 'TS HR Employee Report',
                insert_after = 'totals',
                label = 'Employee Expense Report',
                depends_on = "eval:doc.designation == 'Contractor'"
            ),
            dict(
              fieldname = 'total_expense',
              fieldtype = 'Currency',
              insert_after = 'ts_hr_employee_salary_report'  ,
              label = 'Total Expense',
              depends_on = "eval:doc.designation == 'Contractor'"
            ),
            dict(
              fieldname = 'sec_brk',
              fieldtype = 'Section Break',
              insert_after = 'total_expense'
            ),
            dict(
              fieldname = 'salary_balance',
              fieldtype = 'Currency',
              label = 'Salary Balance',
              read_only = 1,
              insert_after = 'payroll_frequency',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
            dict(
              fieldname = 'pay_the_balance',
              fieldtype = 'Check',
              label = 'Pay the Balance',
              insert_after = 'salary_balance',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
            dict(
              fieldname = 'section_break_41',
              fieldtype = 'Section Break',
              insert_after = 'total_unpaid_amount',
            ),
            dict(
              fieldname = 'total_unpaid_amount',
              fieldtype = 'Currency',
              label = 'Total Unpaid Amount',
              insert_after = 'total_paid_amount',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
            dict(
              fieldname = 'total_paid_amount',
              fieldtype = 'Currency',
              label = 'Total Paid Amount',
              insert_after = 'total_amount',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
            dict(
              fieldname = 'total_amount',
              fieldtype = 'Currency',
              label = 'Total Amount',
              insert_after = 'column_break_37',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
             dict(
              fieldname = 'site_work_details',
              fieldtype = 'Table',
              label = 'Site work Details',
              insert_after = 'section_break_26',
              options = 'Site work Details',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
             dict(
              fieldname = 'total_advance_amount',
              fieldtype = 'Currency',
              label = 'Emplyee Advance Amount',
              insert_after = 'site_work_details',
              read_only = 1,
              description = "Employee Advance Created from <a href = /app/employee-advance-tool>Employee Advance Tool<a>"
              ),
              dict(
              fieldname = 'column_break_37',
              fieldtype = 'Column Break',
              insert_after = 'total_advance_amount',
            ),
              dict(
              fieldname = 'payment_account',
              fieldtype = 'Link',
              label = 'Payment Account',
              insert_after = 'designation',
              options = 'Account',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'",
              mandatory_depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader'"
            ),
        ]
    }
    create_custom_fields(custom_field)
    create_property_setter()
    
def create_property_setter():
  make_property_setter('Payroll Entry', 'payroll_frequency', 'options', 'Monthly\nFortnightly\nBimonthly\nWeekly\nDaily\nCustom', 'Text Editor')
  
  
