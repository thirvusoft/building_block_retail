import frappe
from building_block_retail.building_block_retail.utils.hr.role.roles import create_role

def workflow_document_creation():
    create_state()
    create_action()
    create_quotation_flow()
    create_designation()

def create_quotation_flow():
    if frappe.db.exists('Workflow', 'Quotation Flow'):
        return
        # frappe.delete_doc('Workflow', 'Quotation Flow')
    create_role()
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Quotation Flow'
    workflow.document_type = 'Quotation'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Open', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Waiting for Approval', allow_edit = 'Admin',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Approved', allow_edit = 'Admin',doc_status = 1,
    ))
    workflow.append('states', dict(
        state = 'Rejected', allow_edit = 'Admin',doc_status = 1,
    ))
    
    
    workflow.append('transitions', dict(
        state = 'Open', action='Send to Approval', next_state = 'Waiting for Approval',
        allowed='Admin', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Waiting for Approval', action='Approve', next_state = 'Approved',
        allowed='Admin', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Waiting for Approval', action='Reject', next_state = 'Rejected',
        allowed='Admin', allow_self_approval= 1,
    ))
    workflow.insert(ignore_permissions=True)
    return workflow
def create_state():
    list={"Open":"Warning", "Waiting for Approval":"Primary", "Approved":"Success", "Rejected":"Danger"}
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            new_doc.style=list[row]
            new_doc.save()
    list=['Send to Approval', 'Approve', 'Reject']
    for i in list:
        if not frappe.db.exists('Workflow Action Master', i):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = i
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
