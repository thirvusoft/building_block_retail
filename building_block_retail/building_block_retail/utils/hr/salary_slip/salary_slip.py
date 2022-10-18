from asyncore import read
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
              fieldname = '',
              fieldtype = 'Currency',
              insert_after = 'total_expense'  ,
              label = 'Amount to Pay',
              depends_on = "eval:doc.designation == 'Contractor'"
            ),
            dict(
              fieldname = 'sec_brk',
              fieldtype = 'Section Break',
              insert_after = 'contractor_to_pay'
            ),
            dict(
              fieldname = 'salary_balance',
              fieldtype = 'Currency',
              label = 'Salary Balance',
              read_only = 1,
              insert_after = 'payroll_frequency',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor' || doc.designation == 'Contractor'"
            ),
            dict(
              fieldname = 'pay_the_balance',
              fieldtype = 'Check',
              label = 'Pay the Balance',
              insert_after = 'salary_balance',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor' || doc.designation == 'Contractor'"
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
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'"
            ),
            dict(
              fieldname = 'total_paid_amount',
              fieldtype = 'Currency',
              label = 'Total Paid Amount',
              insert_after = 'total_amount',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'"
            ),
            dict(
              fieldname = 'total_amount',
              fieldtype = 'Currency',
              label = 'Total Amount',
              insert_after = 'column_break_37',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'"
            ),
             dict(
              fieldname = 'site_work_details',
              fieldtype = 'Table',
              label = 'Work Details',
              insert_after = 'section_break_26',
              options = 'Site work Details',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'"
            ),
              dict(
              fieldname = 'column_break_37',
              fieldtype = 'Column Break',
              insert_after = 'site_work_details',
            ),
              dict(
              fieldname = 'payment_account',
              fieldtype = 'Link',
              label = 'Payment Account',
              insert_after = 'designation',
              options = 'Account',
              depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'",
              mandatory_depends_on = "eval:doc.designation == 'Job Worker' || doc.designation == 'Loader' || doc.designation == 'Earth Rammer Contractor'"
            ),
            dict(
              label = 'Get Employee Advance',
              fieldname = 'get_emp_advance',
              fieldtype = 'Button',
              insert_after = 'earnings',
            ),
        ],
      "Salary Detail":[
        dict(
          fieldname = 'employee_advance',
          label = 'Employee Advance', 
          fieldtype = 'Link', 
          insert_after = 'amount', 
          options = 'Employee Advance', 
          read_only=1
          ),
        dict(
          fieldname = "amount_to_pay",
          fieldtype = "Currency",
          insert_after = "amount",
          label = "Amount to Pay"
          ),
      ]
    }
    create_custom_fields(custom_field)
    create_property_setter()
    
def create_property_setter():
  make_property_setter('Payroll Entry', 'payroll_frequency', 'options', 'Monthly\nFortnightly\nBimonthly\nWeekly\nDaily\nCustom', 'Text Editor')
  make_property_setter('Salary Detail', 'amount', 'read_only_depends_on', 'eval: doc.employee_advance', 'Text Editor')