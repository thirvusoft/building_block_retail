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
                insert_after= "site_work",
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
                insert_after= "type",
                label= "Work",
                options= "Supply Only\nSupply and Laying\nLaying Only"
            ),
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "order_type",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                length=1000,
            ),
            dict(fieldname='site_work', 
                label='Site Name', 
                fieldtype='Link',
                insert_after='work', 
                options='Project', 
                allow_on_submit=0, 
                mandatory_depends_on="eval:doc.work!='Supply Only'", 
                depends_on="eval:doc.work!='Supply Only'"
            ),
            dict(fieldname='type', 
                label='Type', 
                reqd=1,
                fieldtype='Select',
                insert_after='customer_name', 
                options='\nPavers\nCompound Wall',
                default = 'Pavers',
            ),
            dict(fieldname='possible_delivery_dates', 
            label='Possible Delivery Dates',
            fieldtype='Table',
            insert_after='items', 
            options='Item wise Delivery Date', 
            read_only = 1,
            allow_on_submit = 1,
            ),
            dict(fieldname='pavers', 
                label='Pavers',
                fieldtype='Table',
                insert_after='possible_delivery_dates', 
                options='Item Detail Pavers', 
                depends_on="eval:doc.type=='Pavers'"
                ),
            dict(fieldname='compoun_walls', 
                label='Compound Walls', 
                fieldtype='Table',
                insert_after='pavers', 
                options='Item Detail Compound Wall', 
                depends_on="eval:doc.type=='Compound Wall'"
                ),
            dict(fieldname='raw_material_sec', 
                label='Raw Materials', 
                fieldtype='Section Break',
                insert_after='compoun_walls', 
                collapsible=1
                ),
            dict(fieldname='raw_materials', 
                label='Raw Materials', 
                fieldtype='Table',
                insert_after='raw_material_sec', 
                options='TS Raw Materials',
                ),
        ],
        'Quotation Item':[
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "item_code",
                label= "Work",
                options= "Supply Only\nSupply and Laying\nLaying Only"
            ),
        ]
    }
    create_custom_fields(custom_fields)

def quotation_property_setter():
    make_property_setter('Quotation', 'items', 'reqd', '0', 'Check')
    make_property_setter('Quotation', 'rounding_adjustment', 'read_only', '0', 'Check')
    make_property_setter('Quotation Item', 'conversion_factor', 'precision', '5', 'Select')