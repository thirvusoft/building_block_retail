import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sales_invoice_item_custom_fields():
    custom_fields={
        "Sales Invoice Item" :[
            dict(
                fieldname= "area_per_bundle",
                fieldtype= "Float",
                insert_after= "qty",
                label= "Area Per Bundle",
   
            ),
            dict(
                 fieldname  = "ts_qty",
                 fieldtype  = "Float",
                 insert_after  = "area_per_bundle",
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
           
        ],
    }
    create_custom_fields(custom_fields)


def sales_invoice_item_property_setter():
    pass