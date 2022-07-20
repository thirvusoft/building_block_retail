from dataclasses import fields
from operator import index
import frappe 
from frappe.utils.data import get_link_to_form
def before_validate(doc,action):
    #-----------------------------------usecase is changed it will remove after conform-----------------------------------------
    # if doc.from_bom == 1:
    #     wo=frappe.get_doc("Work Order",doc.work_order)
    #     expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
    #     amount = wo.total_expanse * doc.fg_completed_qty
    #     if doc.amended_from:
    #         if wo.total_expanse:
    #             creating_journal_entry(doc,amount)
    #     else:
    #         for i in doc.additional_costs:
    #             if expenses_included_in_valuation == i.expense_account:
    #                 i.amount += amount
    #                 i.base_amount += amount
    #                 doc.total_additional_costs += amount
    #                 creating_journal_entry(doc,amount)
    #                 break
    # doc.distribute_additional_costs()
    # doc.update_valuation_rate()
    #---------------------------------------------------------------------------------------------------------------------------
    if doc.from_bom == 1:
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
                            x=[] 
                            x.append(completed_qty[j])
                            completed_qty.update({j: x[0]+ code[j]})
                        else:
                            completed_qty.update({j: code[j]}) 
        for i in job_card.time_logs:
            emp_list.append(str(i.employee)) 
        index = 0
        for d in emp_list:
            if d in emp_qty.keys():
                x=[] 
                x.append(emp_qty[d])
                emp_qty.update({d: x[0]+ job_card.time_logs[index].completed_qty})
                index += 1
            else:
                emp_qty.update({d: job_card.time_logs[index].completed_qty}) 
                index += 1
        
        final_qty={i:((emp_qty.get(i) or 0) - (completed_qty.get(i) or 0)) for i in emp_qty}
        if completed_qty:
            doc.code = str(final_qty)
        else:
            doc.code = str(emp_qty)
        wo=frappe.get_doc("Work Order",doc.work_order)
        expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
        amount = wo.total_expanse * doc.fg_completed_qty
        if doc.amended_from:
            if wo.total_expanse:
                creating_journal_entry(doc)
        else:
            for i in doc.additional_costs:
                if expenses_included_in_valuation == i.expense_account:
                    i.amount += amount
                    i.base_amount += amount
                    doc.total_additional_costs += amount
                    creating_journal_entry(doc)
                    break
        doc.distribute_additional_costs()
        doc.update_valuation_rate()
def creating_journal_entry(doc):
    code = eval(doc.code)
    for i in code:
        if code[i] != 0:
            income_account = frappe.get_value("Employee",i,"contracter_expense_account")
            if income_account:
                default_employee_expenses_account = frappe.get_cached_value("Company", doc.company, "default_employee_expenses_account")
                if default_employee_expenses_account:
                    new_journal=frappe.get_doc({
                        "doctype":"Journal Entry",
                        "company":doc.company,
                        "posting_date":doc.posting_date,
                        "stock_entry_linked":doc.name,
                        "accounts":[
                            {
                                "account":default_employee_expenses_account,
                                "credit_in_account_currency":code[i]
                            },
                            {
                                "account":income_account,
                                "debit_in_account_currency":code[i],
                            },
                        ],
                    })
                    new_journal.insert()
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
                    ("Enter Salary Account for Contracter in {}.").format(
                        frappe.bold(linkto)
                    )
                )