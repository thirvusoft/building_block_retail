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
        ],
    }
    create_custom_fields(custom_fields)


def work_order_property_setter():pass
    # make_property_setter("Work Order", "status", "options", "Urgent Priority\nHigh Priority\nLow Priority", "Data")