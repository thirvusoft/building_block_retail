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
                label = 'Employee Expense Report'
            ),
            dict(
              fieldname = 'total_expense',
              fieldtype = 'Currency',
              insert_after = 'ts_hr_employee_salary_report'  ,
              label = 'Total Expense'
            ),
            dict(
              fieldname = 'sec_brk',
              fieldtype = 'Section Break',
              insert_after = 'total_expense'
            )
        ]
    }
    create_custom_fields(custom_field)
    create_property_setter()
    
def create_property_setter():
  make_property_setter('Payroll Entry', 'payroll_frequency', 'options', 'Monthly\nFortnightly\nBimonthly\nWeekly\nDaily\nCustom', 'Text Editor')
  
  
