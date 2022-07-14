import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def create_job_card_custom_fields():
    custom_fields={
        "Job Card" :[
            dict(
                 fieldname  = "se_created",
                 fieldtype  = "Check",
                 insert_after  = "naming_series",
                 label = "Stock Entry Created",
                 in_standard_filter = 1,
                 in_list_view = 1
            ),
        ]
    }
    create_custom_fields(custom_fields)
    create_property_setter()
    
def create_property_setter():
    make_property_setter("Job Card", 'wip_warehouse', 'reqd', '0', 'Check')
    
def before_submit(self, event):
    if(not self.se_created):frappe.throw("Please click <b>Finish</b> button to create stock entry and then submit this.")