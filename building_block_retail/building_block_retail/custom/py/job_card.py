import frappe
from frappe.desk.form import assign_to

@frappe.whitelist()
def get_workorder_doc(work_order, opr, workstation, qty=0):
    wo=frappe.get_doc("Work Order", work_order)
    over_prdn_prcnt = frappe.db.get_singles_value("Manufacturing Settings", 'overproduction_percentage_for_work_order')
    wo.update({
        'over_prdn_prcnt' : over_prdn_prcnt
    })
    return wo
    
@frappe.whitelist()
def calculate_max_qty(job_card):
    cur_job_card = frappe.get_doc("Job Card",job_card)
    get_job_card = frappe.get_all("Stock Entry", pluck = 'fg_completed_qty', filters={"ts_job_card": job_card,"docstatus": 1})  
    max = float(cur_job_card.total_completed_qty) - float(sum(get_job_card))
    return max
@frappe.whitelist()
def update_operation_completed_qty(work_order, opr, workstation, qty=0):
    completed_qty = frappe.get_value("Work Order Operation",{'operation':opr,'parent':work_order},'completed_qty') or 0
    frappe.db.set_value("Work Order Operation",{'operation':opr,'parent':work_order},'completed_qty', float(qty)+float(completed_qty))
    frappe.db.commit()