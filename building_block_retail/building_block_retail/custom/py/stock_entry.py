from dataclasses import fields
from operator import index
import frappe 
from frappe.utils.data import get_link_to_form
def before_validate(doc,action):
    if doc.from_bom == 1 and doc.stock_entry_type == "Manufacture":
        doc.code = ""
        emp_qty={}
        emp_list=[]
        wo=frappe.get_doc("Work Order",doc.work_order)
        expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
        job_card= frappe.get_doc("Job Card",doc.ts_job_card)
        old_stock_entry = frappe.get_all("Stock Entry", fields=["name","code"], filters={"ts_job_card":doc.ts_job_card,"docstatus": 1,})
        completed_qty = {}
        if len(old_stock_entry) > 0:
            for i in old_stock_entry:
                if i.code != None:
                    code =  eval(i.code)
                    for j in code:
                        if j in completed_qty.keys():
                            completed_qty[j] += code[j]
                        else:
                            completed_qty.update({j: code[j]}) 
        for i in job_card.time_logs:
            emp_list.append(str(i.employee)) 
        index = 0
        for d in emp_list:
            if d in emp_qty.keys():
                emp_qty[d] += job_card.time_logs[index].completed_qty
                index += 1
            else:
                emp_qty.update({d: job_card.time_logs[index].completed_qty}) 
                index += 1
        
        final_qty={i:((emp_qty.get(i) or 0) - (completed_qty.get(i) or 0)) for i in emp_qty}
        if completed_qty:
            doc.code = str(final_qty)
        else:
            doc.code = str(emp_qty)
        amt = 0
        for i in final_qty:
            emp_per = frappe.get_value("Employee",i,"employee_percentage") or 0
            hike = wo.total_expanse * emp_per / 100
            amt +=  (hike * final_qty[i]) + (wo.total_expanse * final_qty[i])
        wo=frappe.get_doc("Work Order",doc.work_order)
        expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
        amount = amt
        if doc.amended_from:
            if wo.total_expanse:
                creating_journal_entry(doc,wo.total_expanse)
        else:
            doc.append('additional_costs', dict(
                expense_account = expenses_included_in_valuation, amount = float(amount),base_amount = float(amount),description = "Employee Cost",
            ))
            creating_journal_entry(doc,wo.total_expanse)
        doc.distribute_additional_costs()
        doc.update_valuation_rate()
def after_submit(doc,action):
    if(doc.stock_entry_type == 'Manufacture'):
        job_card= frappe.get_doc("Job Card",doc.ts_job_card)
        get_job_card = frappe.get_all("Stock Entry", pluck = 'fg_completed_qty', filters={"ts_job_card": job_card.name,"docstatus": 1})  
        if job_card.for_quantity == float(sum(get_job_card)):
            job_card.submit()
def creating_journal_entry(doc,income):
    code = eval(doc.code)
    for i in code:
        if code[i] != 0:
            income_account = frappe.get_value("Employee",i,"contracter_expense_account")
            per_emp = frappe.get_value("Employee",i,"employee_percentage") or 0
            hike = income * per_emp / 100
            amt =  (hike * code[i]) + (income * code[i])
            if income_account:
                default_employee_expenses_account = frappe.get_cached_value("Company", doc.company, "default_employee_expenses_account")
                def_cost_center = frappe.get_cached_value("Company", doc.company, "cost_center")
                
                if default_employee_expenses_account:
                    new_journal=frappe.get_doc({
                        "doctype":"Journal Entry",
                        "company":doc.company,
                        "posting_date":doc.posting_date,
                        "stock_entry_linked":doc.name,
                        "cost_center": def_cost_center,
                        "accounts":[
                            {
                                "account":default_employee_expenses_account,
                                "credit_in_account_currency":amt,
                                "cost_center": def_cost_center
                            },
                            {
                                "account":income_account,
                                "debit_in_account_currency":amt,
                                "cost_center": def_cost_center,
                            },
                        ],
                    })
                    # new_journal.insert()
                    new_journal.submit()
                else:
                    linkto = get_link_to_form("Company", doc.company)
                    frappe.throw(
                        ("Enter Default Employee Expenses Account in company => {}.").format(
                            frappe.bold(linkto)
                        )
                    )
            else:
                linkto = get_link_to_form("Employee", i)
                frappe.throw(
                    ("Enter Salary Account for Contractor in {}.").format(
                        frappe.bold(linkto)
                    )
                )