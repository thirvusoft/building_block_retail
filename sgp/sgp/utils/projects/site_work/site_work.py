from email.policy import default
from ipaddress import collapse_addresses
from optparse import Option
from os import link
from ssl import Options
from requests import options
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def customize_field():
    custom_fields = {
        "Project": [
            dict(fieldname='work', label='Work',
                 fieldtype='Data', insert_after='status',
                 ),
            dict(fieldname='total_expense_amount', label='Total Costing',
                 fieldtype='Currency', insert_after='work',
                 ),
            dict(fieldname='supervisor_name', label='Supervisor',
                 fieldtype='Data', insert_after='priority',
                 ),
            dict(fieldname='total_required_area', label='Total Required Area',
                 fieldtype='Data', insert_after='supervisor_name', default=0
                 ),
            dict(fieldname='total_completed_area', label='Total Completed Area',
                 fieldtype='Data', insert_after='total_required_area', default=0
                 ),
            dict(fieldname='total_required_bundle', label='Total Required Bundle',
                 fieldtype='Data', insert_after='total_completed_area', default=0
                 ),
            dict(fieldname='total_completed_bundle', label='Total Completed Bundle',
                 fieldtype='Data', insert_after='total_required_bundle', default=0
                 ),
            dict(fieldname='is_multi_customer', label='is_multi_customer',
                 fieldtype='Check', insert_after='customer_details',
                 ),
            dict(fieldname='customer_name', label='Customer Name',
                 fieldtype='Table', insert_after='is_multi_customer',
                 depends_on="eval:doc.is_multi_customer==1", options="TS Customer"
                 ),
            dict(fieldname='section_job', label='Job Worker Details',
                 fieldtype='Section Break', insert_after='copied_from', collapsible=1
                 ),
            dict(fieldname='job_worker', label='Job Worker',
                 fieldtype='Table', insert_after='section_job',
                 options="TS Job Worker"
                 ),
            dict(fieldname='additional_costs', label='Additional Costs',
                 fieldtype='Section Break', insert_after='notes', collapsible=1
                 ),
            dict(fieldname='additional_costs_1', label='Additional Cost',
                 fieldtype='Table', insert_after='additional_costs', options="TS Additional Costs"
                 ),

        ]
    }

    create_custom_fields(custom_fields)


def site_doc_name():

    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "label",
        'field_name': "project_name",
        "value": "Site Name"
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "project_template",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "expected_start_date",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "expected_end_date",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "department",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "project_type",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "is_active",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "percent_complete_method",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "sales_order",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "users_section",
        "property_type": "Check",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "project_details",
        "property_type": "Check",
        "value": 1
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Project",
        'property': "hidden",
        'field_name': "monitor_progress",
        "property_type": "Check",
        "value": 1
    })
    Project.save(ignore_permissions=True)
