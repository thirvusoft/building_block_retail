import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sales_invoice_item_custom_fields():
    custom_fields={
        "Sales Invoice Item" :[
            dict(
                 fieldname  = "ts_qty",
                 fieldtype  = "Float",
                 insert_after  = "qty",
                label = "No of Bundle",
   
            ),
            dict(  
                fieldname = "pieces",
                fieldtype = "Int",
                insert_after = "ts_qty",
                label = "Pieces",
            ),
            dict(
                fieldname= "Branch",
                fieldtype = "Link",
                insert_after= "accounting_dimensions_section",
                label= "Branch",
                options= "Branch",
            ),
            dict(
                 fieldname  = "cannot_be_bundle",
                 fieldtype  = "Check",
                 insert_after  = "item_code",
                 label = "Cannot Be Bundle",
                 fetch_from = 'item_code.cannot_be_bundle',
                 hidden=1
            )
           
        ],
    }
    create_custom_fields(custom_fields)


def sales_invoice_item_property_setter():
    make_property_setter('Sales Invoice Item', 'conversion_factor', 'precision', '5', 'Select')