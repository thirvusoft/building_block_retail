from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_month_details
import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe import _
from frappe.utils import (
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
    stock_entry = frappe.get_all("Stock Entry", filters={'company':doc.company,'stock_entry_type': 'Manufacture', 'docstatus':1, 'posting_date': ['between',(doc.start_date, doc.end_date)]}, pluck = 'Name')
    journal_entry = frappe.get_all("Journal Entry", filters={'stock_entry_linked': ['in', stock_entry]}, pluck='name')
    emp_account = frappe.get_value("Employee", doc.employee, 'contracter_expense_account')
    je = frappe.get_all("Journal Entry Account", fields=['account', 'debit_in_account_currency'], filters={'debit_in_account_currency':['>',0], 'parent': ['in',journal_entry]})
    emp_amount = sum([i['debit_in_account_currency'] for i in  je if(i['account'] == emp_account)]) or 0
    doc.gross_pay = emp_amount
    doc.total_expense = emp_amount
    doc.net_pay = emp_amount - doc.total_deduction
    doc.rounded_total = round(doc.net_pay)
    doc.compute_year_to_date()
        
    #Calculation of Month to date
    doc.compute_month_to_date()
    doc.compute_component_wise_year_to_date()
    doc.set_net_total_in_words()
    
    #### Get Employee Expense Report Table
    table = get_employe_expense_report(doc)
    doc.set('ts_hr_employee_salary_report', table)

def get_employe_expense_report(doc):
    work_order = frappe.get_all("Stock Entry", filters={'company':doc.company, 'stock_entry_type': 'Manufacture', 'docstatus':1, 'posting_date': ['between',(doc.start_date, doc.end_date)]}, pluck = 'work_order')
    job_card = frappe.get_all("Job Card", filters={'work_order': ['in', work_order], 'docstatus':1, 'company':doc.company}, fields=['name', 'workstation', 'production_item', 'posting_date'])
    jc_name = [i['name'] for i in job_card]
    jc_details = {i['name']:[i['posting_date'], i['workstation'], i['production_item']] for i in job_card}
    jc_data = {}
    for i in frappe.get_all('Job Card Time Log', filters={'parent': ['in', jc_name], 'employee':doc.employee}, fields=['completed_qty', 'parent']):
        if(i['parent'] in list(jc_data.keys())):jc_data[i['parent']] += (i['completed_qty'] or 0)
        else:jc_data[i['parent']]= i['completed_qty']
    final_data=[]
    for i in jc_data:
        row = {}
        row['qty_produced'] = jc_data[i]
        row['date'] = jc_details[i][0]
        row['workstation'] = jc_details[i][1]
        row['production_item'] = jc_details[i][2]
        row['expense'] = get_expense_from_stock_entry(i, doc.employee)
        final_data.append(row)
    return final_data

def get_expense_from_stock_entry(job_card, employee):
    se = frappe.get_all("Stock Entry", filters={'ts_job_card': job_card}, fields=['code', 'work_order', 'name'])
    wo_name = {i['name']:i['work_order'] for i in se}
    emp_expense={}
    for i in wo_name:
        expense = frappe.get_value("Work Order", wo_name[i], 'total_expanse')
        emp_expense[wo_name[i]] = expense
    expense = 0
    for i in se:
        exp_dict = eval(i['code'])
        expense += ((exp_dict.get(employee) or 0) * float(emp_expense[i['work_order']]))
    return expense