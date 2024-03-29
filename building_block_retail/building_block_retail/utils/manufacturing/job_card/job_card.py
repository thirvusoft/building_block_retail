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
            dict(
                fieldname = 'col123',
                fieldtype = "Column Break",
                insert_after = 'total_completed_qty'  
            ),
            dict(
                 fieldname  = "max_qty",
                 fieldtype  = "Float",
                 insert_after  = "col123",
                 label = "Maximum Qty to Produce",
                 fetch_from = 'for_quantity',
                 read_only = 1
            ),
            dict(
                 fieldname  = "reason",
                 fieldtype  = "Small Text",
                 insert_after  = "project",
                 label = "Reason",
                 allow_on_submit =1,
                 read_only = 1
            ),
            dict(
                 fieldname  = "priority",
                 fieldtype  = "Select",
                 insert_after  = "posting_date",
                 label = "Priority",
                 no_copy = 1,
                 fetch_from = 'work_order.priority',
                 options = "\nUrgent Priority\nHigh Priority\nLow Priority",
                 in_standard_filter = 1,
                 in_list_view = 1
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
    make_property_setter(doctype, 'wip_warehouse', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'quality_inspection', 'hidden', '1', 'Check')
    