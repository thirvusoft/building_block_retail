import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def work_order_custom():
    work_order_custom_fields()
    work_order_property_setter()
def work_order_custom_fields():
    custom_fields={
        "Work Order" :[
            dict(
                 fieldname  = "priority",
                 fieldtype  = "Select",
                 insert_after  = "bom_no",
                 label = "Priority",
                 options = "Urgent Priority\nHigh Priority\nLow Priority",
                 in_standard_filter = 1,
                 in_list_view = 1
            ),
            dict(
                 fieldname  = "total_expanse",
                 fieldtype  = "Currency",
                 insert_after  = "corrective_operation_cost",
                 label = "Total Expanse",
                 hidden = 1
            ),
         
        ],
    }
    create_custom_fields(custom_fields)


def work_order_property_setter():
    doctype="Work Order"
    make_property_setter(doctype, 'more_info', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'settings_section', 'hidden', '1', 'Check') 
    make_property_setter(doctype, 'skip_transfer', 'default', '1', 'Text Editor')
