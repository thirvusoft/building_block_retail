import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_note_customization():
    delivery_note_custom_field()
    delivery_note_property_setter()

def delivery_note_custom_field():
    custom_fields={
        "Delivery Note":[
            dict(
                fieldname= "supervisor",
                fieldtype= "Link",
                insert_after= "customer",
                label= "Supervisor",
                options= "Employee"
            ),
            dict(
                fieldname= "supervisor_name",
                fieldtype= "Data",
                insert_after= "supervisor",
                label= "Supervisor Name",
                fetch_from= "supervisor.employee_name"
            ),
            dict(
                fieldname= "supervisor_phone_no",
                fieldtype= "Data",
                insert_after= "supervisor_name",
                label= "Supervisor Phone No",
                fetch_from= "supervisor.cell_number"
            ),
            dict(
                fieldname= "site_work",
                fieldtype= "Link",
                insert_after= "supervisor_phone_no",
                label= "Site Name",
                options= "Employee"
            ),
            dict(
                fieldname= "type",
                fieldtype= "Select",
                insert_after= "site_work",
                label= "Sales Type",
                options= "\nPavers \nCompound Wall"
            ),
            dict(
                fieldname= "value_pieces",
                fieldtype= "Check",
                insert_after= "items",
                label= "Value in Pieces"
            ),
            dict(
                fieldname= "value_bundle",
                fieldtype= "Check",
                insert_after= "value_pieces",
                label= "Value in Bundle"
            ),
            dict(
                fieldname= "pending_quantity",
				fieldtype= "Int",
				insert_after= "total_qty",
				label= "Pending Quantity"
            ),
            dict(
                fieldname= "total_delivery_till_date",
				fieldtype= "Int",
				insert_after= "pending_quantity",
				label= "Total Delivery till date"
            ),
            dict(
				fieldname= "remarks",
				fieldtype= "Data",
				insert_after= "lr_date",
				label= "Remarks"
            ),
            dict(
                fieldname= "current_odometer_value",
				fieldtype= "Int",
				insert_after= "distance",
				label= "Current Odometer Value"
            ),
            dict(
                fieldname= "return_odometer_value",
				fieldtype= "Int",
				insert_after= "current_odometer_value",
				label= "Return Odometer Value"
            ),
            dict(
                fieldname= "total_distance",
				fieldtype= "Int",
				insert_after= "return_odometer_value",
				label= "Total Distance"
            )

        ],
    }
    create_custom_fields(custom_fields)

def delivery_note_property_setter():
    make_property_setter("Delivery Note", "company", "hidden", "0", "Check")
    make_property_setter("Delivery Note", "transporter_name", "hidden", "0", "Check")
    make_property_setter("Delivery Note", "accounting_dimensions_section", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "customer_po_details", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "currency_and_price_list", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "sec_warehouse", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "terms_section_break", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "mode_of_transport", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "gst_transporter_id", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "driver", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "lr_no", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "gst_vehicle_type", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "gst_category", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "distance", "hidden", "0", "Check")
    make_property_setter("Delivery Note", "more_info", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "printing_details", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "sales_team_section_break", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "section_break1", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "shipping_rule", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "driver_name", "insert_after", "vehicle_no", "Data")