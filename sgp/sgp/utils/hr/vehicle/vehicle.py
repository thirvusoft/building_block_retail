import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def vehicle_customization():
    vehicle_custom_field()
    vehicle_property_setter()

def vehicle_custom_field():
    custom_fields={
        "Vehicle":[
            dict(
                fieldname= "section_break_maintenance_details",
                fieldtype= "Section Break",
                insert_after= "amended_from",
                label= "Maintanence Details"
            ),
            dict(
                fieldname= "maintenance_details",
                fieldtype= "Table",
                insert_after= "section_break_maintenance_details",
                label= "maintenance_details",
                options= "Maintenance Details"
            )
        ]
    }
    create_custom_fields(custom_fields)

def vehicle_property_setter():
    pass