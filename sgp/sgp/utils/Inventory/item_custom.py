from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_Customization():
    item_customization()

def item_customization():
    custom_fields={
        "Item":[
            dict(
                 fieldname  = "employee_rate",
                 fieldtype  = "Currency",
                 insert_after  = "standard_rate",
                 label = "Employee Rate(For Manufacture)",
                 description = "Per Qty",
                 depends_on = 'eval:doc.item_group != "Raw Material"'
            ),
            dict(
                 fieldname  = "laying_cost",
                 fieldtype  = "Currency",
                 insert_after  = "employee_rate",
                 label = "Employee Rate(For Laying)",
                 description = "Per Qty",
                 depends_on = 'eval:doc.item_group != "Raw Material"'
            ),
        ],
    }
    create_custom_fields(custom_fields)