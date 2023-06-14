import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def manufacturing_setting_custom_fields():
    custom_fields={
        "Manufacturing Settings" :[
            dict(
                 fieldname  = "workstation_capacity_planning_section",
                 fieldtype  = "Section Break",
                 insert_after  = "column_break_5quxt",
                 label = "Workstation Capacity Planning",
            ),
            dict(
                 fieldname  = "get_items",
                 fieldtype  = "Select",
                 insert_after  = "workstation_capacity_planning_section",
                 label = "Get Items",
                options="Template\nVariants"
            ),
             dict(
                 fieldname  = "column_break_pmmw1",
                 fieldtype  = "Column Break",
                 insert_after  = "get_items",
               
            ),
             dict(
                 fieldname  = "item_groups",
                 fieldtype  = "Table MultiSelect",
                 insert_after  = "column_break_pmmw1",
                 label = "Item Groups",
                options="Settings Item Group"
            ),
             dict(
                 fieldname  = "column_break_3",
                 fieldtype  = "Column Break",
                 insert_after  = "item_groups",
               
            ),
         
        ],
    }
    create_custom_fields(custom_fields)