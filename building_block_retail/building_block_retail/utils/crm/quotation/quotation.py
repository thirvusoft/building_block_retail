import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def quotation_customization():
    quotation_custom_field()
    quotation_property_setter()

def quotation_custom_field():
    custom_fields={
        "Quotation":[
            dict(
                fieldname= "supervisor",
                fieldtype= "Link",
                insert_after= "customer_name",
                label= "Supervisor",
                options= "Employee"
            ),
            dict(
                fieldname= "supervisor_name",
                fieldtype= "Data",
                insert_after= "supervisor",
                label= "Supervisor Name",
                fetch_from = "supervisor.first_name"
            ),
            dict(
                fieldname= "supervisor_number",
                fieldtype= "Data",
                insert_after= "supervisor_name",
                label= "Supervisor Number",
                fetch_from = "supervisor.cell_number"
            ),
            dict(
                fieldname= "site_work",
                fieldtype= "Link",
                insert_after= "work",
                label= "Site Name",
                options= "Project",
                depends_on="eval:doc.work!='Supply Only'"
            ),
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "order_type",
                label= "Work",
                options= "Supply Only\nSupply and Laying"
            ),
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "site_work",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                length=1000,
            ),
        ],
        'Quotation Item':[
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "item_code",
                label= "Work",
                options= "Supply Only\nSupply and Laying"
            ),
        ]
    }
    create_custom_fields(custom_fields)

def quotation_property_setter():
    make_property_setter('Quotation', 'items', 'reqd', '0', 'Check')
    make_property_setter('Quotation', 'rounding_adjustment', 'read_only', '0', 'Check')
    make_property_setter('Quotation Item', 'conversion_factor', 'precision', '5', 'Select')