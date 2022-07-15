import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def create_job_card_custom_fields():
    custom_fields={
        "Job Card" :[
            dict(
                 fieldname  = "doc_onload",
                 fieldtype  = "Check",
                 insert_after  = "se_created",
                 label = "doc_onload",
                 hidden = 1,
                 no_copy = 1
            ),
        ]
    }
    create_custom_fields(custom_fields)
    create_property_setter()
    
def create_property_setter():
    doctype="Job Card"
    make_property_setter(doctype, 'wip_warehouse', 'reqd', '0', 'Check')
    make_property_setter(doctype, 'naming_series', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'se_created', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'serial_no', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'quality_inspection_template', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'batch_no', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'more_information', 'hidden', '1', 'Check')
def before_submit(self, event):
    se_qty = sum(frappe.db.get_all("Stock Entry", filters={'work_order':self.work_order,'docstatus':1},pluck="fg_completed_qty"))
    if(se_qty != self.total_completed_qty):frappe.throw("Please click <b>Finish</b> button to create stock entry and then submit this.")