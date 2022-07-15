from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def workstation_custom():
    workstation_custom_fields()
    workstation_property_setter()
def workstation_custom_fields():
    custom_fields={
        "Workstation" :[
            dict(
                 fieldname  = "expanse_per_piece",
                 fieldtype  = "Currency",
                 insert_after  = "hour_rate_consumable",
                 label = "Expense Per Piece",
                 description = "per qty"
            ),
        ],
    }
    create_custom_fields(custom_fields)


def workstation_property_setter():
    doctype="Workstation"
    make_property_setter(doctype, 'hour_rate_labour', 'description', 'wages per hour', 'Text Editor')