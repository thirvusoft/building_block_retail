from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_month_details
import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	getdate
)
from frappe.utils.data import today
@frappe.whitelist()
def get_start_end_dates(payroll_frequency, start_date=None, company=None):
    if payroll_frequency == "Monthly" or payroll_frequency == "Bimonthly" or payroll_frequency == "":
        fiscal_year = get_fiscal_year(start_date, company=company)[0]
        month = "%02d" % getdate(start_date).month
        m = get_month_details(fiscal_year, month)
        if payroll_frequency == "Bimonthly":
            if getdate(start_date).day <= 15:
                start_date = m["month_start_date"]
                end_date = m["month_mid_end_date"]
            else:
                start_date = m["month_mid_start_date"]
                end_date = m["month_end_date"]
        else:
            start_date = m["month_start_date"]
            end_date = m["month_end_date"]
            
    if payroll_frequency == "Weekly":
        end_date = add_days(start_date, 6)
        
    if payroll_frequency == "Fortnightly":
        end_date = add_days(start_date, 13)
    
    if payroll_frequency == "Daily":
        end_date = start_date
        
    if payroll_frequency == "Custom":
        end_date = add_days(today(), 6)
        start_date = today()
        
    return frappe._dict({"start_date": start_date, "end_date": end_date})

@frappe.whitelist()
def submit_salary_slips_for_employees(payroll_entry, salary_slips, publish_progress=True):
    submitted_ss = []
    not_submitted_ss = []
    frappe.flags.via_payroll_entry = True

    count = 0
    for ss in salary_slips:
        ss_obj = frappe.get_doc("Salary Slip", ss[0])
        if ss_obj.net_pay < 0:
            not_submitted_ss.append(ss[0])
        else:
            try:
                ss_obj.submit()
                submitted_ss.append(ss_obj)
            except frappe.ValidationError:
                not_submitted_ss.append(ss[0])

        count += 1
        if publish_progress:
            frappe.publish_progress(count * 100 / len(salary_slips), title=_("Submitting Salary Slips..."))
    if submitted_ss:
        payroll_entry.make_accrual_jv_entry()
        frappe.msgprint(
            _("Salary Slip submitted for period from {0} to {1}").format(ss_obj.start_date, ss_obj.end_date)
        )

        payroll_entry.email_salary_slip(submitted_ss)

        payroll_entry.db_set("salary_slips_submitted", 1)
        payroll_entry.notify_update()

    if not submitted_ss and not not_submitted_ss:
        frappe.msgprint(
            _(
                "No salary slip found to submit for the above selected criteria OR salary slip already submitted"
            )
        )

    if not_submitted_ss:
        frappe.msgprint(_("Could not submit some Salary Slips"))

    frappe.flags.via_payroll_entry = False
    
    
def salary_slip_add_gross_pay(doc, event):
    stock_entry = frappe.get_all("Stock Entry", filters={'work_order': ['!=',None]}, pluck = 'Name')
    journal_entry = frappe.get_all("Journal Entry", filters={'stock_entry_linked': ['in', stock_entry]}, pluck='name')
    # emp_name_account = frappe.db.sql('''
    #                                  SELECT name as employee, contracter_expense_account as account
    #                                  FROM `tabEmployee`
    #                                  WHERE status = 'Active'
    #                                  ''')
    # emp_name_wise_acc = {i[1]:i[0] for i in emp_name_account}
    journal_emp_acc = {i['account']:i['debit_in_account_currency'] for i in frappe.get_all("Journal Entry Account", filters={'credit_in_account_currency':0, 'parent': ['in',journal_entry]},fields=['account', 'debit_in_account_currency'])}
    emp_amount = 0
    emp_account = frappe.get_value("Employee", doc.employee, 'contracter_expense_account')
    for i in journal_emp_acc:
        if(i == emp_account):
            emp_amount += journal_emp_acc[i]
    doc.gross_pay = emp_amount