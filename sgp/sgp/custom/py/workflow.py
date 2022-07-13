import frappe
from sgp.sgp.utils.hr.role.roles import create_role

def workflow_document_creation():
    create_state()
    create_action()
    create_quotation_flow()
    create_designation()

def create_quotation_flow():
    if frappe.db.exists('Workflow', 'Quotation Flow'):
        frappe.delete_doc('Workflow', 'Quotation Flow')
    create_role()
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Quotation Flow'
    workflow.document_type = 'Quotation'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Draft', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Approved', allow_edit = 'Admin',doc_status = 1,
    ))
    workflow.append('transitions', dict(
        state = 'Draft', action='Approve', next_state = 'Approved',
        allowed='Admin', allow_self_approval= 1,
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list=["Draft"]
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            if(row=="Draft"):
                new_doc.style="Danger"
            new_doc.save()
def create_action():
    pass
def create_designation():
    list=["Supervisor"]
    for row in list:
        if not frappe.db.exists('Designation', row):
            new_doc = frappe.new_doc('Designation')
            new_doc.designation_name = row
            new_doc.save()