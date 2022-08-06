from requests import options
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
                fieldname= "maintanence_details_",
                fieldtype= "Table",
                insert_after= "section_break_maintenance_details",
                label= "Maintanance Details",
                options= "Maintenance Details"
            ),
            dict(
                fieldname= "is_add_on",
                fieldtype= "Check",
                insert_after= "model",
                label= "Is Add-On",
            ),
            dict(
                fieldname= "add_on",
                fieldtype= "Link",
                insert_after= "make",
                label= "Add-On",
                options= "Vehicle",
                depends_on= "eval:doc.is_add_on == 1"
            ),
            dict(
                fieldname= "driver",
                fieldtype= "Link",
                insert_after= "vehicle_value",
                label= "Driver",
                options= "Driver",
            ),
            dict(
                fieldname= "employee_name",
                fieldtype= "Data",
                insert_after= "driver",
                label= "Employee",
                fetch_from= "driver.employee",
                read_only="1"
            ),
            dict(
                fieldname= "costing_details",
                fieldtype= "Section Break",
                insert_after= "employee_name",
                label= "Costing Details",
            ),
            dict(
                fieldname= "operator",
                fieldtype= "Link",
                insert_after= "acquisition_date",
                label= "Operator",
                options="Driver"
            ),
            dict(
                fieldname= "maintenance_cost",
                fieldtype= "Float",
                insert_after= "costing_details",
                label= "Maintenance Cost Per Km",
                precision=2
            ),
            dict(
                fieldname= "driver_cost",
                fieldtype= "Float",
                insert_after= "maintenance_cost",
                label= "Driver Cost",
                precision=2
            ),
            dict(
                insert_after= "driver_cost",
                fieldtype= "Column Break",
                fieldname= "column_break_18",
            ),
            dict(
                fieldname= "mileage",
                fieldtype= "Float",
                insert_after= "column_break_18",
                label= "Mileage",
                precision=2
            ),
            dict(
                fieldname= "service_details",
                fieldtype= "Section Break",
                insert_after= "maintanence_details_",
                label= "Service Details",
            ),
            dict(
                fieldname= "service_details_table",
                fieldtype= "Table",
                insert_after= "service_details",
                label= "Service Details",
                options= "TS Vehicle Service"
            )
        ]
    }
    create_custom_fields(custom_fields)

def vehicle_property_setter():
    doctype = "Vehicle"
    make_property_setter(doctype, 'location', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'employee', 'hidden', '1', 'Check')