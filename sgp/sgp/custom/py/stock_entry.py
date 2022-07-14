import frappe
def before_validate(doc,action):
    if doc.from_bom == 1:
        wo=frappe.get_doc("Work Order",doc.work_order)
        expenses_included_in_valuation = frappe.get_cached_value("Company", wo.company, "expenses_included_in_valuation")
        for i in doc.additional_costs:
            if expenses_included_in_valuation == i.expense_account:
                i.amount += wo.total_expanse
                break