import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def lead_customisation():
    lead_custom_fields()
    lead_property_setter()

def lead_custom_fields():
    custom_fields = {
        'Lead':[
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "email_id",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                length=1000,
            ),
        ],
        'Opportunity':[
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "source",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                length=1000,
            ),
        ]
    }
    create_custom_fields(custom_fields)

def lead_property_setter():
    make_property_setter('Opportunity', 'language', 'hidden', 1, 'Check')
    
    make_property_setter('Lead', 'lead_owner', 'read_only', 1, 'Check')
    make_property_setter('Lead', 'lead_owner', 'hidden', 1, 'Check')
    make_property_setter('Lead', 'campaign_name', 'depends_on', 'eval:doc.source == "Campaign"', 'Text Editor')
    make_property_setter('Lead', 'fax', 'hidden', 1, 'Check')
    make_property_setter('Lead', 'language', 'hidden', 1, 'Check')
    make_property_setter('Lead', 'blog_subscriber', 'hidden', 1, 'Check')
    make_property_setter('Lead', 'unsubscribed', 'hidden', 1, 'Check')
    make_property_setter('Lead', 'county', 'hidden', 1, 'Check')