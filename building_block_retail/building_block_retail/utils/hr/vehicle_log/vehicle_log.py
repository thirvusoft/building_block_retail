from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def vehicle_log_customization():
    vehicle_log_custom_fields()
    vehicle_log_property_setter()
def vehicle_log_custom_fields():
    custom_fields = {
        "Vehicle Log": [
            dict(
                fieldname="select_purpose",
                fieldtype="Select",
                label="Purpose",
                insert_after="today_odometer_value",
                options="\nFuel\nRaw Material\nService\nGoods Supply"
            ),
            dict(
                fieldname="sales_invoice",
                fieldtype="Link",
                label="Sales Invoice",
                insert_after="odometer",
                options="Sales Invoice",
                depends_on="eval:doc.select_purpose == 'Goods Supply' "
            ),
            dict(
                fieldname="purchase_invoice",
                fieldtype="Link",
                label="Purchase Invoice",
                insert_after="odometer",
                options="Purchase Invoice",
                depends_on="eval:doc.select_purpose == 'Raw Material' "
            ),
            dict(
                fieldname="purchase_receipt",
                fieldtype="Link",
                label="Purchase Receipt",
                insert_after="select_purpose",
                options="Purchase Receipt",
                depends_on="eval:doc.select_purpose == 'Raw Material' "
            ),
            dict(
                fieldname="service_item_table",
                fieldtype="Table",
                label="Service Item",
                insert_after="service_detail",
                options="Vehicle Log Service"
            ),
            dict(
                fieldname="today_odometer_value",
                fieldtype="Float",
                label="Distance Travelled",
                insert_after="last_odometer",
            ),
            dict(
                fieldname="select_purpose",
                fieldtype="Select",
                label="Purpose",
                insert_after="today_odometer_value",
                options="\nFuel\nRaw Material\nService\nGoods Supply",
                reqd="1",
            ),
            dict(
                fieldname="delivery_note",
                fieldtype="Link",
                label="Delivery Note",
                insert_after="purchase_receipt",
                options="Delivery Note",
                depends_on="eval:doc.select_purpose == 'Goods Supply'"
            ),
            dict(
                label="Costing Details",
                fieldtype="Section Break",
                fieldname="costing_details",
                insert_after="delivery_note",
            ),
            dict(
                fieldname="driver_cost",
                fieldtype="Float",
                label="Driver Cost",
                insert_after="costing_details",
            ),
            dict(
                fieldname="column_break_21",
                fieldtype="Column Break",
                insert_after="driver_cost",
            ),
            dict(
                fieldname="ts_total_cost",
                fieldtype="Float",
                label="Total Cost",
                insert_after="column_break_21",
            ),
            dict(
                fieldname="section_break_21",
                fieldtype="Section Break",
                label="Maintanence Details",
                insert_after="service_item_table",
                collapsible=1 
            ),
            dict(
                fieldname="maintanence_details",
                fieldtype="Table",
                label="Maintanence Details",
                insert_after="section_break_21",
                options="Maintenance Details"
            ),
            ]
    }
    create_custom_fields(custom_fields)

def vehicle_log_property_setter():         
    make_property_setter("Vehicle Log", "add_on_service_details", "hidden", "1", "Check")
    make_property_setter("Vehicle Log", "employee", "fetch_from", "license_plate.employee_name", "Text Editor")
    make_property_setter("Vehicle Log", "purpose", "hidden", "1", "Check")
    make_property_setter("Vehicle Service", "frequency", "reqd", "0", "Check")
    make_property_setter("Vehicle Service", "frequency", "hidden", "1", "Check")
    make_property_setter("Vehicle Log", "service_detail", "hidden", "1", "Check")
    make_property_setter("Vehicle Log", "today_odometer_value", "label", "Distance Travelled", "Data")
    make_property_setter("Vehicle Log", "today_odometer_value", "read_only", "1", "Check")
    make_property_setter("Vehicle Log", "select_purpose", "reqd", "1", "Check")