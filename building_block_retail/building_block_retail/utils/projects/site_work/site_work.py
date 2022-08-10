import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def customize_field():
   custom_fields = {
       "Project": [
         dict(fieldname='work', label='Work',
              fieldtype='Data', insert_after='status', read_only=1
              ),
         dict(fieldname='completed', label='% Completed',
              fieldtype='Percent', insert_after='work', read_only=1
              ),
         dict(fieldname='total_expense_amount', label='Total Costing as Per Bill',
              fieldtype='Currency', insert_after='completed', read_only=1, description='It includes Items sales rate, Raw Materials Sales Rate and Additional Cost except Site Advance.'
              ),
          dict(fieldname='actual_site_cost_calculation', label='Actual Costing of this Site',
              fieldtype='Currency', insert_after='total_expense_amount', read_only=1, description= 'It includes Items Valuation rate, Raw Materials Buying Rate, Job Workers cost and Additional Cost except Site Advance.'
              ),
          dict(fieldname='site_profit', label='Site Profit',
              fieldtype='Currency', insert_after='actual_site_cost_calculation', read_only=1
              ),
         dict(fieldname='job__work', label='Job worker',
              fieldtype='Link', insert_after='completed', options="Employee", hidden=1
              ),
         dict(fieldname='supervisor_name', label='Supervisor Name',
              fieldtype='Data', insert_after='supervisor', read_only=1, fetch_from= "supervisor.employee_name"
              ),
         dict(fieldname='supervisor', label='Supervisor',
              fieldtype='Link', insert_after='priority', options="Employee"
              ),
         dict(
                fieldname= "supervisor_number",
                fieldtype= "Data",
                insert_after= "supervisor_name",
                label= "Supervisor Number",
                fetch_from = "supervisor.cell_number"
            ),
         dict(fieldname='total_required_area', label='Total Required Area',
              fieldtype='Data', insert_after='supervisor_number', default=0,read_only=1
              ),
         dict(fieldname='total_completed_area', label='Total Completed Area',
              fieldtype='Data', insert_after='total_required_area', default=0,read_only=1
              ),
         dict(fieldname='total_required_bundle', label='Total Required Bundle',
              fieldtype='Data', insert_after='total_completed_area', default=0,read_only=1
              ),
         dict(fieldname='total_completed_bundle', label='Total Completed Bundle',
              fieldtype='Data', insert_after='total_required_bundle', default=0,read_only=1
              ),
         dict(fieldname='is_multi_customer', label='is_multi_customer',
              fieldtype='Check', insert_after='customer_details', allow_in_quick_entry=1
              ),
         dict(fieldname='customer_name', label='Customer Name',
              fieldtype='Table', insert_after='customer',
              depends_on="eval:doc.is_multi_customer==1", options="TS Customer"
              ),
         dict(fieldname='section_job', label='Job Worker Details',
              fieldtype='Section Break', insert_after='delivery_detail', collapsible=0
              ),
         dict(fieldname='job_worker', label='Job Worker',
              fieldtype='Table', insert_after='section_job',
              options="TS Job Worker Details"
              ),
         dict(fieldname='additional_costs_1', label='Additional Costs',
              fieldtype='Section Break', insert_after='notes', collapsible=1
              ),
         dict(fieldname='additional_cost', label='Additional Cost',
              fieldtype='Table', insert_after='additional_costs', options="Additional Costs"
              ),
         dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "sales_order",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                allow_on_submit = 1,
                length=1000,
            ),
            dict(
                fieldname= "ts_open_link",
                fieldtype= "Button",
                insert_after= "ts_map_link",
                label= "Open Delivery Location",
            ),
         dict(fieldname='section_break_19', label="Item Details",
              fieldtype='Section Break', insert_after='ts_open_link'
              ),
         dict(fieldname='item_details', options= "Pavers", label="Item Details Pavers",
              fieldtype='Table', insert_after='section_break_19', read_only=1
              ),
         dict(fieldname='item_details_compound_wall', options= "Compound Wall", label="Item Details Compound Wall",
              fieldtype='Table', insert_after='item_details', read_only=1
              ),
         dict(fieldname='total_amount', label="Total Amount",
              fieldtype='Currency', insert_after='item_details_compound_wall', read_only=1
              ),
         dict(fieldname='raw_materials', label="Raw Materials",
              fieldtype='Section Break', insert_after='total_amount'
              ),
         dict(fieldname='raw_material', options= "Raw Materials", label="Raw Material",
              fieldtype='Table', insert_after='raw_materials', read_only=1
              ),
         dict(fieldname='total_amount_of_raw_material', label="Total Amount",
              fieldtype='Currency', insert_after='raw_material', read_only=1
              ),
         dict(fieldname='delivery_details', label="Delivery Details",
              fieldtype='Section Break', insert_after='total_amount_of_raw_material'
              ),
         dict(fieldname='distance', label="Distance (km)", precision=2,
              fieldtype='Float', insert_after='delivery_details', read_only=1
              ),
         dict(fieldname='delivery_detail', options= "Delivery Status", label="Delivery Detail",
              fieldtype='Table', insert_after='distance', read_only=1
              ),
         dict(fieldname='total_job_worker_cost', label="Total Amount",
              fieldtype='Currency', insert_after='job_worker', read_only=1
              ),
         dict(fieldname='section_break_30',
              fieldtype='Section Break', insert_after='total_job_worker_cost',
              ),
         dict(fieldname='additional_costs', label="Additional Costs",
              fieldtype='Section Break', insert_after='message'
              ),
         dict(fieldname='total', label=" Total Amount",
              fieldtype='Currency', insert_after='total_advance_amount', read_only=1
              ),
         dict(fieldname='material_supply', label="Material Supply",
              fieldtype='Check', insert_after='total',
              ),
         dict(fieldname='work_completed', label="Work Completed",
              fieldtype='Check', insert_after='material_supply'
              ),
         dict(fieldname='dust_swing', label="Dust Swing",
              fieldtype='Check', insert_after='work_completed'
              ),
         dict(fieldname='cutting_piece', label="Cutting Piece",
              fieldtype='Check', insert_after='dust_swing'
              ),
         dict(fieldname='dust_finishing_with_rammer', label="Dust Finishing With Rammer",
              fieldtype='Check', insert_after='cutting_piece'
              ),
         dict(fieldname='dust_sweeping', label="Dust Sweeping",
              fieldtype='Check', insert_after='dust_finishing_with_rammer'
              ),
         dict(fieldname='total_advance_amount', label=" Total Advance Amount",
                 fieldtype='Float', insert_after='additional_cost', read_only=1
                )
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
         'property': "allow_in_quick_entry",
         'field_name': "customer",
         "value": "1"
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "mandatory_depends_on",
         'field_name': "customer",
         "value": "eval:!doc.is_multi_customer"
    })
    Project.save(ignore_permissions=True),
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "depends_on",
         'field_name': "customer",
         "value": "eval:!doc.is_multi_customer"
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
         'field_name': "percent_complete",
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
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "hidden",
         'field_name': "section_break_18",
         "property_type": "Check",
         "value": 1
    })
    Project.save(ignore_permissions=True)
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "hidden",
         'field_name': "margin",
         "property_type": "Check",
         "value": 1
    })
    Project.save(ignore_permissions=True)
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "hidden",
         'field_name': "section_break_18",
         "property_type": "Check",
         "value": 1
    })
    Project.save(ignore_permissions=True)
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocField",
         'doc_type': "Project",
         'property': "hidden",
         'field_name': "section_break0",
         "property_type": "Check",
         "value": 1
    })
    Project.save(ignore_permissions=True)
    Project = frappe.get_doc({
         'doctype': 'Property Setter',
         'doctype_or_field': "DocType",
         'doc_type': "Project",
         'property': "track_changes",
         "property_type": "Check",
         "value": 1
    })
    Project.save(ignore_permissions=True)
    if(not frappe.get_all('Translation', {"source_text": "Project", "translated_text": "Site Work", "language": "en-US"})):
        frappe.get_doc(
            {
                "doctype": "Translation",
                "source_text": "Project",
                "translated_text": "Site Work",
                "language": "en-US",
            }
        ).insert()

    if(not frappe.get_all('Translation', {"source_text": "Projects", "translated_text": "Site Work", "language": "en-US"})):
        frappe.get_doc(
            {
                "doctype": "Translation",
                "source_text": "Projects",
                "translated_text": "Site Work",
                "language": "en-US",
            }
        ).insert()
