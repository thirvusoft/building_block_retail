from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe


def purchase_invoice():
    custom_fields = {

        "Purchase Invoice": [
            dict(fieldname='branch', label='Branch',
                 fieldtype='Link', options='Branch', insert_after='company', read_only=0),
            dict(fieldname='vehicle_log', label='Vehicle Log',
                    fieldtype='Link', options='Vehicle Log', insert_after='tax_id', read_only=1),
        ],
        "Purchase Invoice Item": [
            dict(fieldname='vehicle', label='Vehicle', fieldtype='Link', options='Vehicle', 
                 mandatory_depends_on='eval:doc.item_group == "Fuel"', depends_on='eval:doc.item_group == "Fuel"',
                 insert_after = 'item_code'),
            dict(fieldname='current_odometer_value', label='Current Oddometer', fieldtype='Float', 
                fetch_from='vehicle.last_odometer', insert_after = 'vehicle')
        ]

    }
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "due_date",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "accounting_dimensions_section",
        "value":0
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "section_addresses",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "apply_discount_on",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "base_discount_amount",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "is_subcontracted",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "currency_and_price_list",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "set_warehouse",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "rejected_warehouse",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "taxes_section",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "shipping_rule",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "payment_schedule_section",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "gst_section",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "more_info",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "subscription_section",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "terms_section_break",
        "value": 1
    })
    Purchase_Invoice.save()
    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "printing_settings",
        "value": 1
    })
    Purchase_Invoice.save()

    Purchase_Invoice = frappe.get_doc({
        'doctype': 'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property': "hidden",
        'property_type': "Check",
        'field_name': "accounting_details_section",
        "value": 1
    })
    Purchase_Invoice.save()
    make_property_setter('Purchase Invoice Item', 'conversion_factor', 'precision', '5', 'Select')
    create_custom_fields(custom_fields)
