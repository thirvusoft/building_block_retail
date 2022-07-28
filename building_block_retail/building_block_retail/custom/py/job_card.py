import frappe
from frappe.desk.form import assign_to
import json
def create_timesheet(doc,action):
    time_logs = doc.time_logs
    employees = list(set([i.employee for i in time_logs]))
    for i in employees:
        timesheet = frappe.new_doc("Timesheet")
        if(not frappe.db.exists("Activity Type", "Production")):
            activity = frappe.new_doc("Activity Type")
            activity.activity_type = "Production"
            activity.save()
        employees_time_log = [j for j in time_logs if(j.employee == i)] 
        timelogs_timesheet = []
        for k in employees_time_log:
            timelogs_timesheet.append({
                'activity_type': "Production",
                'from_time' : k.from_time,
                'to_time' : k.to_time,
                'hours' :  k.time_in_mins/60,
                'total_production_pavers' : k.completed_qty
            })
        timesheet.update({
            'company': doc.company,
            'workstation' : doc.workstation,
            'time_logs' : timelogs_timesheet,
            'employee' : i
        })
        timesheet.insert(ignore_permissions = True)
        timesheet.submit()
        user_id = frappe.get_value("Employee", i, 'user_id')
        if(user_id):
            assign_to.add(
                    dict(
                        assign_to=[user_id],
                        doctype="Timesheet",
                        name=timesheet.name,
                        notify=True,
                    )
                )
        else:
            frappe.msgprint(f"User id not set for Employee: {i}")
    
@frappe.whitelist()
def get_workorder_doc(work_order, opr, workstation, qty=0):
    wo=frappe.get_doc("Work Order", work_order)
    over_prdn_prcnt = frappe.db.get_singles_value("Manufacturing Settings", 'overproduction_percentage_for_work_order')
    wo.update({
        'over_prdn_prcnt' : over_prdn_prcnt
    })
    return wo

@frappe.whitelist()
def get_link_to_jobcard(work_order):
    job_card = frappe.get_all("Job Card", filters={'work_order':work_order},pluck = 'name')
    if(not len(job_card)):frappe.throw("Job Card doesn't Created. This may cause if the <b>Linked BOM doesn't have any Operation.</b>")
    return "/app/job-card/"+job_card[-1]
    
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