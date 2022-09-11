import json
from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_month_details
from frappe.utils.data import get_link_to_form
import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils.data import get_link_to_form
from frappe import _
from frappe.utils import (
	add_days,
	getdate
)
from frappe.utils.data import flt, today
from numpy import average
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
    
#validate   
def salary_slip_add_gross_pay(doc, event):
    if(doc.designation != 'Contractor'):
        set_net_pay(doc)
        return
    stock_entry = frappe.get_all("Stock Entry", filters={'company':doc.company,'stock_entry_type': 'Manufacture', 'docstatus':1, 'posting_date': ['between',(doc.start_date, doc.end_date)]}, pluck = 'Name')
    journal_entry = frappe.get_all("Journal Entry", filters={'stock_entry_linked': ['in', stock_entry]}, pluck='name')
    emp_account = frappe.get_value("Employee", doc.employee, 'contracter_expense_account')
    je = frappe.get_all("Journal Entry Account", fields=['account', 'debit_in_account_currency'], filters={'debit_in_account_currency':['>',0], 'parent': ['in',journal_entry]})
    emp_amount = sum([i['debit_in_account_currency'] for i in  je if(i['account'] == emp_account)]) or 0
    doc.total_expense = emp_amount
    if(not doc.contractor_to_pay):
        doc.contractor_to_pay = emp_amount
    com = [i.salary_component for i in doc.earnings]
    if "Basic" not in com:
        doc.append('earnings',{'salary_component':'Basic', 'amount':doc.total_expense})
    doc.gross_pay =sum([(i.amount or 0) for i in doc.earnings]) or 0
    adv_acc = frappe.db.get_value('Company', doc.company, 'default_employee_advance_account')
    if(not adv_acc):
        url = get_link_to_form('Company', doc.company)
        frappe.throw(f'Please fill the <b>Employee Advance Account</b> in {url}')
    com = [i.salary_component for i in doc.deductions]

    doc.net_pay = doc.gross_pay - doc.total_deduction
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
    job_card = frappe.get_all("Job Card", filters={'work_order': ['in', work_order],  'company':doc.company}, fields=['name', 'workstation', 'production_item', 'posting_date'])
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
        row['expense'], row['rate_per_piece'] = get_expense_from_stock_entry(i, doc.employee, jc_details[i][2])
        # row['rate_per_piece'] = 10
        final_data.append(row)
    return final_data

def get_expense_from_stock_entry(job_card, employee, item):
    se = frappe.get_all("Stock Entry", filters={'ts_job_card': job_card}, fields=['code', 'work_order', 'name'])
    wo_name = {i['name']:i['work_order'] for i in se}
    emp_expense={}
    for i in wo_name:
        expense = frappe.get_value("Work Order", wo_name[i], 'total_expanse')
        emp_expense[wo_name[i]] = expense
    expense = 0
    rate = []
    amount = []
    for i in list(wo_name.keys()):
        rate.append(frappe.db.get_value('Work Order', wo_name[i], 'total_expanse') or 0)
        amount.append(average(frappe.get_all("Stock Entry Detail", filters={'parent':i, 'item_code':item}, pluck='amount')))
    if(len(rate) == 0):rate=0
    if(len(amount) == 0):amount=[0]
    for i in se:
        exp_dict = eval(i['code'])
        expense += ((exp_dict.get(employee) or 0) * float(emp_expense[i['work_order']]))
    return expense, average(rate) or 0



@frappe.whitelist(allow_guest=True)
def site_work_details(employee,start_date,end_date,designation):
    if(designation == 'Job Worker'):
        job_worker = frappe.db.get_all(
                'TS Job Worker Details',
                fields=['parent as site_work_name','amount','start_date','end_date', 'rate', 'sqft_allocated'],
                filters={'start_date':['>=', start_date], 'end_date':['<=', end_date], 'name1':employee})
        return job_worker

    elif(designation == 'Loader'):
        delivery_note = frappe.db.get_all("Delivery Note", filters={'posting_date':['between',(start_date, end_date)], 'docstatus':1}, fields=['name', 'site_work', 'ts_loadman_work'])
        dn_names = [i['name'] for i in delivery_note]
        loadman_cost = frappe.db.get_all('TS Loadman Cost', filters={'parent':['in', dn_names], 'employee':employee},  fields=['amount', 'rate', 'parent'])
        for i in range(len(loadman_cost)):
            for j in delivery_note:
                if(loadman_cost[i].parent == j.name):
                    loadman_cost[i]['site_work_name'] = j.site_work
                    loadman_cost[i]['loadman_work'] = j.ts_loadman_work
                    del loadman_cost[i]['parent']
        return loadman_cost

def employee_update(doc,action):
    update_employee_advance(doc)
    employee_doc = frappe.get_doc('Employee',doc.employee)
    if(doc.designation in ['Loader', 'Job Worker']):
        if(doc.get('pay_the_balance')):
            employee_doc.salary_balance=doc.total_unpaid_amount
        else:
            employee_doc.salary_balance+=doc.total_unpaid_amount
    elif(doc.designation in ['Contractor']):
        employee_doc.salary_balance += (doc.total_expense-doc.contractor_to_pay)
    employee_doc.save()

def set_net_pay(self):
    earnings=self.earnings
    if self.designation in ['Job Worker', 'Loader']:
        for row in range(len(earnings)):
            if(earnings[row].salary_component=='Basic'):
                earnings[row].amount=self.total_paid_amount
        self.update({
            'earnings':earnings,
            'gross_pay':self.total_paid_amount,
        })

    # Calculation of net Pay by round off
    if self.gross_pay:
        self.net_pay = self.gross_pay - self.total_deduction

        #Calculation of year to date
        self.compute_year_to_date()
        
        #Calculation of Month to date
        self.compute_month_to_date()
        self.compute_component_wise_year_to_date()
        self.set_net_total_in_words()
        
def create_journal_entry(doc,action):
    earn_component_list=[]
    earn_amount=[]
    ded_component_list=[]
    ded_amount=[]
    if doc.earnings:
        for data in doc.earnings:
            account = frappe.get_doc('Salary Component',data.salary_component)
            url = get_link_to_form('Salary Component',data.salary_component)
            if(not len(account.accounts)):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
            for row in account.accounts:
                if(row.company == doc.company):
                    if(not row.account):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
                    earn_component_list.append(row.account)
            earn_amount.append(data.amount)

    if doc.deductions:
        for data in doc.deductions:
            account = frappe.get_doc('Salary Component',data.salary_component)
            url = get_link_to_form('Salary Component',data.salary_component)
            if(not len(account.accounts)):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
            for row in account.accounts:
                if(row.company == doc.company):
                    if(not row.account):frappe.throw(f"Please Fill the Account for Salary Component <b>{url}<b>.")
                    ded_component_list.append(row.account)
            ded_amount.append(data.amount)

    new_jv_doc=frappe.new_doc('Journal Entry')
    new_jv_doc.voucher_type='Journal Entry'
    new_jv_doc.posting_date=doc.posting_date
    new_jv_doc.company = doc.company
    new_jv_doc.user_remark = _("Accrual Journal Entry for salaries from {0} to {1}").format(
				doc.start_date, doc.end_date
			)
    for data in range(0,len(earn_component_list),1):
        new_jv_doc.append('accounts',{'account':earn_component_list[data],'debit_in_account_currency':earn_amount[data]})
    for data in range(0,len(ded_component_list),1):
        new_jv_doc.append('accounts',{'account':ded_component_list[data],'credit_in_account_currency':ded_amount[data]})
    if(frappe.db.get_value("Company",doc.company, "default_payroll_payable_account")):
        new_jv_doc.append('accounts',{'account':frappe.db.get_value("Company",doc.company, "default_payroll_payable_account"),'credit_in_account_currency':doc.net_pay})
    else:
        frappe.msgprint(_("Set Default Payable Account in {0}").format(doc.company), alert=True)
    new_jv_doc.ts_salary_slip = doc.name
    new_jv_doc.insert()
    new_jv_doc.submit()
    if(doc.designation == "Contractor"):
        journal_entry(doc)
    elif(doc.designation in ['Job Worker', 'Loader']):
        make_bank_entry(doc)

def journal_entry(doc):
    new_journel = frappe.new_doc("Journal Entry")
    new_journel.company = doc.get("company")
    new_journel.posting_date = doc.get("posting_date")
    new_journel.accounts =  [] 

    empaccount = frappe.get_value("Employee",doc.employee,"contracter_expense_account")
   
    new_journel.append("accounts",{"account":empaccount,"credit_in_account_currency":doc.net_pay})
    new_journel.append("accounts",{"account":frappe.db.get_value("Company",doc.company, "default_payroll_payable_account"),"debit_in_account_currency":doc.net_pay})
    new_journel.insert()
    new_journel.submit()
    frappe.msgprint("Journel Entry Submitted")

def make_bank_entry(doc):
    new_journel = frappe.new_doc("Journal Entry")
    new_journel.company = doc.get("company")
    new_journel.posting_date = doc.get("posting_date")
    new_journel.accounts =  [] 
    account = doc.payment_account
    new_journel.append("accounts",{"account":account,"credit_in_account_currency":doc.gross_pay})
    new_journel.ts_salary_slip = doc.name
    if(not frappe.db.get_value("Company",doc.company, "default_payroll_payable_account")):
        frappe.throw("Set Default Payroll Payable Account in {0}").format(doc.company)
    new_journel.append("accounts",{"account":frappe.db.get_value("Company",doc.company, "default_payroll_payable_account"),"debit_in_account_currency":doc.gross_pay})
    new_journel.insert()
    new_journel.submit()
    frappe.msgprint("Journel Entry Submitted")

@frappe.whitelist()
def get_advance_amounts(employee):
    adv = frappe.get_all(
            "Employee Advance",
            filters=
                {'employee':employee, 'purpose':'Deduct from Salary', 'remaining_amount': ['>', 0]}, 
            fields=['name', 'remaining_amount'])
    fields = []
    for i in range(len(adv)):
        fields.append({'label':'Name','fieldname':f'name{i}', 'fieldtype':'Link', 'options':'Employee Advance', 'default':adv[i]['name'], 'read_only':1})
        fields.append({'fieldname':f'col_brk1{i}', 'fieldtype':'Column Break'})
        fields.append({'fieldname':f'adv_amt{i}', 'label':'Advance Amount', 'fieldtype':'Currency', 'default':adv[i]['remaining_amount'], 'read_only':1})
        fields.append({'fieldname':f'col_brk2{i}', 'fieldtype':'Column Break'})
        fields.append({'fieldname':f'amt_take{i}', 'label':'Amount Taken', 'fieldtype':'Currency'})
        fields.append({'fieldname':f'sec_brk1{i}', 'fieldtype':'Section Break'})
    
    fields.append({'fieldname':'dataaa', 'fieldtype':'Data', 'hidden':1})   
    fields.append({'fieldname':'col_brk', 'fieldtype':'Column Break'})
    fields.append({'fieldname':'total_amount', 'label':'Total Amount', 'fieldtype':'Currency', 'read_only':1})
    return fields, len(adv)

@frappe.whitelist()
def change_remaining_amount(data, length):
    from building_block_retail.building_block_retail.custom.py.defaults import create_defaults
    create_defaults()
    data = json.loads(data)
    amount = 0 
    deductions = []
    for i in range(int(length)):
        amount += data[f'amt_take{i}']
        if(data[f'amt_take{i}'] > 0):
            deductions.append({'salary_component':'Advance','amount':  data[f'amt_take{i}'], 'employee_advance': data[f'name{i}']})
        # frappe.db.set_value('Employee Advance', data[f'name{i}'], 'remaining_amount', data[f'adv_amt{i}'] - data[f'amt_take{i}'])
    return deductions

def update_employee_advance(doc):
    for i in doc.deductions:
        if(i.employee_advance):
            amt = frappe.db.get_value('Employee Advance', i.employee_advance, 'remaining_amount')
            frappe.db.set_value('Employee Advance', i.employee_advance, 'remaining_amount', amt-i.amount)
def on_cancel(doc, action):
    balance = frappe.db.get_value('Employee', doc.employee, 'salary_balance') or 0
    frappe.db.set_value('Employee', doc.employee, 'salary_balance', balance - (doc.total_unpaid_amount or 0))
    for i in doc.deductions:
        if(i.employee_advance):
            amt = frappe.db.get_value('Employee Advance', i.employee_advance, 'remaining_amount')
            frappe.db.set_value('Employee Advance', i.employee_advance, 'remaining_amount', amt+i.amount)
