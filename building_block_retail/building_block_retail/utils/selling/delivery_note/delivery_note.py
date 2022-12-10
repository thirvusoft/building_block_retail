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
                options= "Project"
            ),
            dict(
                fieldname= "type",
                fieldtype= "Select",
                insert_after= "site_work",
                label= "Sales Type",
                options= "\nPavers\nCompound Wall"
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
				insert_after= "lr_date",
				label= "Current Odometer Value",
                fetch_from= "own_vehicle_no.last_odometer",
                read_only=1,
                depends_on= "eval:doc.transporter=='Own Transporter'"
            ),
            dict(
                fieldname= "return_odometer_value",
				fieldtype= "Int",
				insert_after= "current_odometer_value",
				label= "Return Odometer Value",
                allow_on_submit=1,
                depends_on= "eval:doc.transporter=='Own Transporter'"
            ),
            dict(
                fieldname= "total_distance",
				fieldtype= "Int",
				insert_after= "return_odometer_value",
				label= "Total Distance",
                read_only=1,
                allow_on_submit=1,
                depends_on= "eval:doc.transporter=='Own Transporter'"
            ),
            dict(
                fieldname= "own_vehicle_no",
				fieldtype= "Link",
				insert_after= "transporter",
				label= "Vehicle No",
                options= "Vehicle",
                depends_on= "eval:doc.transporter=='Own Transporter'"
            ),
            dict(
                fieldname= "driver_name2",
				fieldtype= "Link",
				insert_after= "own_vehicle_no",
				label= "Driver Name",
                depends_on= "eval:doc.transporter=='Own Transporter'",
                fetch_from= "own_vehicle_no.driver",
                options="Driver"
            ),
            dict(
                fieldname= "employee",
				fieldtype= "Data",
				insert_after= "driver_name2",
				label= "Driver Name",
                fetch_from ="driver_name2.employee"
            ),
            dict(
                fieldname= "operator_",
				fieldtype= "Data",
				insert_after= "employee",
				label= "Operator",
                depends_on= "eval:doc.transporter=='Own Transporter'",
                fetch_from= "own_vehicle_no.operator"
            ),
            dict(
                fieldname= "driver_name_1",
				fieldtype= "Data",
				insert_after= "vehicle_no",
				label= "Driver Name ",
                depends_on= "eval:doc.transporter!='Own Transporter'"
            ),
            dict(
                fieldname= "branch",
				fieldtype= "Link",
				insert_after= "cost_center",
				label= "Branch",
                options= "Branch"
            ),
            dict(
                fieldname= "has_work_order",
				fieldtype= "Check",
				insert_after= "value_bundle",
				label= "Has Work Order",
                hidden = 1,
                no_copy = 1
            ),
            dict(
                fieldname= "remarks",
				fieldtype= "Small Text",
				insert_after= "items",
				label= "Remarks",
                no_copy = 1
            ),
            dict(
                fieldname= "total_cost",
				fieldtype= "Data",
				insert_after= "gst_vehicle_type",
				label= "Total Cost",
                read_only = 1
            ),
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "site_work",
                label= "Work",
                options= "Supply Only\nSupply and Laying\nLaying Only",
                reqd = 1
            ),
            dict(
                fieldname= "loadman_info_section",
                fieldtype= "Section Break",
                insert_after= "total_distance",
                label= "Loadman Info",
                collapsible = 1
            ),
            dict(
                fieldname= "ts_loadman_info",
                fieldtype= "Table",
                insert_after= "loadman_info_section",
                label= "Loadman Info",
                options= "TS Loadman Cost",
            ),
            dict(
                fieldname= "ts_loadman_total_amount",
                fieldtype= "Currency",
                insert_after= "ts_loadman_info",
                label= "Total Cost For Loading/Unloading",
            ),
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "return_against",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                allow_on_submit = 1,
                fetch_from = "site_work.ts_map_link",
                length=1000,
            ),
            dict(
                fieldname= "ts_open_link",
                fieldtype= "Button",
                insert_after= "ts_map_link",
                label= "Open Delivery Location",
            ),
               	dict(fieldname='accounting', label='Accounting',
				fieldtype='Check', insert_after='branch',fetch_from="branch.is_accounting",hidden=1),
        dict(fieldname='abbr_delivery_note', label='Abbrevation',
				fieldtype='Data', insert_after='accounting',fetch_from="branch.abbr",hidden=1)
        ],

        "Delivery Note Item":[
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "item_code",
                label= "Work",
                options= "Supply Only\nSupply and Laying\nLaying Only"
            ),
            dict(
                fieldname= "ts_qty",
				fieldtype= "Float",
				insert_after= "qty",
				label= "Bundle"
            ),
            dict(
                fieldname= "pieces",
				fieldtype= "Int",
				insert_after= "ts_qty",
				label= "Pieces"
            ),
            dict(
                fieldname= "branch",
				fieldtype= "Link",
				insert_after= "accounting_dimensions_section",
				label= "Branch",
                options= "Branch"
            ),
            dict(
                fieldname= "branch_",
				fieldtype= "Link",
				insert_after= "branch",
				label= "Branch",
                options= "Branch"
            ),
            dict(
                fieldname= "delivery_detail",
				fieldtype= "Section Break",
				insert_after= "project",
				label= "Delivery Detail"
            ),
            dict(
                fieldname= "pending_qty",
				fieldtype= "Float",
				insert_after= "delivery_detail",
				label= "Pending qty"
            ),
            dict(
                fieldname= "column_break_92",
				fieldtype= "Section Break",
				insert_after= "pending_qty",
            ),
            dict(
                fieldname= "column_break_93",
				fieldtype= "Section Break",
				insert_after= "column_break_92",
            ),
            dict(
                fieldname= "delivery_qty_till_date",
				fieldtype= "Float",
				insert_after= "column_break_92",
				label= "Delivery qty till date"
            ),
            dict(
                 fieldname  = "cannot_be_bundle",
                 fieldtype  = "Check",
                 insert_after  = "item_code",
                 label = "Cannot Be Bundle",
                 fetch_from = 'item_code.cannot_be_bundle',
                 hidden=1
            ),
            dict(
                 fieldname  = "dont_include_in_loadman_cost",
                 fieldtype  = "Check",
                 insert_after  = "item_name",
                 label = "Don't Include in Loadman Cost",
                 description = 'If this is checked this item\'s loading cost will not be added in Total Loading/Unloading cost'
            )

        ]
    }
    create_custom_fields(custom_fields)

def delivery_note_property_setter():
    make_property_setter("Delivery Note", "company", "hidden", "0", "Check")
    make_property_setter("Delivery Note", "transporter_name", "hidden", "0", "Check")
    make_property_setter("Delivery Note", "accounting_dimensions_section", "hidden", "0", "Check")
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
    make_property_setter("Delivery Note", "distance", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "more_info", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "printing_details", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "sales_team_section_break", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "section_break1", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "shipping_rule", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "driver_name", "insert_after", "vehicle_no", "Data")
    make_property_setter("Delivery Note", "in_words", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "per_installed", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "per_returned", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "brand_field", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "opening_stock", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "valuation_rate", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "standard_rate", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "is_fixed_asset", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "purchase_details", "hidden", "1", "Check")
    make_property_setter("Delivery Note Item", "supplier_details", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "driver", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "driver_name", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "vehicle_no", "depends_on", "eval:doc.transporter!='Own Transporter'", "Data")
    make_property_setter("Delivery Note", "value_pieces", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "value_bundle", "hidden", "1", "Check")
    make_property_setter("Delivery Note", "employee", "label", "Employee", "Data")
    make_property_setter("Delivery Note", "driver_name_2", "hidden", "1", "Check")
    make_property_setter('Delivery Note Item', 'conversion_factor', 'precision', '5', 'Select')