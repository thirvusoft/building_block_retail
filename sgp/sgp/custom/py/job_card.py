import frappe
from frappe.desk.form import assign_to

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
    frappe.db.set_value("Work Order Operation",{'operation':opr,'workstation':workstation,'parent':work_order},'completed_qty', qty)
    frappe.db.commit()
    return wo