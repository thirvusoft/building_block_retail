from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe


def purchase_receipt():
    custom_fields = {
        "Purchase Receipt": [
            dict(fieldname='company_name', label='Company',
                 fieldtype='Link', options='Company', insert_after='column_break1', read_only=0, reqd=1),

            dict(fieldname='transporter', label='Transporter',
                 fieldtype='Link', options='Supplier', insert_after='transporter_name'),

            dict(fieldname='vehicle', label='Vehicle Number',
                 fieldtype='Link', options='Vehicle', insert_after='transporter', depends_on='eval:doc.transporter=="Own Transporter"'),

            dict(fieldname='driver_name', label='Driver Name',
                 fieldtype='Data',  insert_after='vehicle', depends_on='eval:doc.transporter=="Own Transporter"'),

            dict(fieldname='operator', label='Operator',
                 fieldtype='Data',  insert_after='driver_name', depends_on='eval:doc.transporter=="Own Transporter"'),

            dict(fieldname='vehicle_number', label='Vehicle Number',
                 fieldtype='Data', insert_after='operator'),

            dict(fieldname='driver', label='Driver Name',
                 fieldtype='Data', insert_after='vehicle_number'),
                          	dict(fieldname='accounting', label='Accounting',
				fieldtype='Check', insert_after='branch',fetch_from="branch.is_accounting",hidden=1),
        dict(fieldname='abbr_purchase_receipt', label='Abbrevation',
				fieldtype='Data', insert_after='accounting',fetch_from="branch.abbr",hidden=1)


        ],
    }
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "more_info",
        "value": 1
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "accounting_dimensions_section",
        "value": 0
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "sec_warehouse",
        "value": 1
    })
    Purchase_Receipt.save()

    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "raw_material_details",
        "value": 1
    })
    Purchase_Receipt.save()

    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "printing_settings",
        "value": 1
    })
    Purchase_Receipt.save()

    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "shipping_rule",
        "value": 1
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "raw_material_details",
        "value": 1
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "taxes_and_charges",
        "value": 1
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "column_break5",
        "value": 1
    })
    Purchase_Receipt.save()
    Purchase_Receipt = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property': "label",
        'field_name': "lr_date",
        "value": "Driver Name"
    })
    Purchase_Receipt.save()
    make_property_setter('Purchase Receipt Item', 'conversion_factor', 'precision', '5', 'Select')

    create_custom_fields(custom_fields)
