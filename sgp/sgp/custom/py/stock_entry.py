import frappe
from frappe.utils import lazy_loader
from frappe.utils.data import get_link_to_form
def before_validate(doc,action):
    if doc.from_bom == 1:
        wo=frappe.get_doc("Work Order",doc.work_order)
        expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
        if doc.amended_from:
            if wo.total_expanse:
                creating_journal_entry(doc,wo.total_expanse)
        else:
            for i in doc.additional_costs:
                if expenses_included_in_valuation == i.expense_account:
                    i.amount += wo.total_expanse
                    creating_journal_entry(doc,wo.total_expanse)
                    break
def creating_journal_entry(doc,income):
    job_card = frappe.get_all(
				"Job Card",
				filters={
					"work_order": doc.work_order,
                    "status": "Completed" 
				},
				order_by="modified desc" ,
				fields=["name"],
				limit =1
			)
    debit = frappe.get_all(
				"Job Card Time Log" ,
				filters={
					"parent": job_card[0].name,
                    "docstatus": 1 
				},
				order_by="creation desc",
				fields=["employee",'parent'],
				limit =1
			)
    if len(debit)>0:
        income_account = frappe.get_value("Employee",debit[0].employee,"contracter_expense_account")
        if debit[0].employee:
            if income_account:
                default_cash_account = frappe.get_cached_value("Company", doc.company, "default_cash_account")
                new_journal=frappe.get_doc({
                    "doctype":"Journal Entry",
                    "company":doc.company,
                    "posting_date":doc.posting_date,
                    "accounts":[
                        {
                            "account":default_cash_account,
                            "credit_in_account_currency":income
                        },
                        {
                            "account":income_account,
                            "debit_in_account_currency":income,
                        },
                    ],
                })
                new_journal.insert()
                new_journal.submit()
            else:
                linkto = get_link_to_form("Employee", debit[0].employee)
                frappe.throw(
                    ("Enter Salary Account for Contracter for {}.").format(
                        frappe.bold(linkto)
                    )
                )
        else:
            linkto = get_link_to_form("Job Card", debit[0].parent)
            frappe.throw(
                ("Select the Employee in Job Card Time Log {}.").format(
                    frappe.bold(linkto)
                )
            )
    else:
        linkto = get_link_to_form("Work Order", doc.work_order)
        frappe.throw(
            ("Create Job Card for {}.").format(
                frappe.bold(linkto)
            )
        )