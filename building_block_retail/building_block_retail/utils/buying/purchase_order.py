from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe



def purchase_order():
    custom_fields = {
        "Purchase Order": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
                     	dict(fieldname='accounting', label='Accounting',
				fieldtype='Check', insert_after='branch',fetch_from="branch.is_accounting",hidden=1),
        dict(fieldname='abbr_purchase_order', label='Abbrevation',
				fieldtype='Data', insert_after='accounting',fetch_from="branch.abbr",hidden=1)
            
        ]
        }
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_dimensions_section",
        "value":0
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"tax_category",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"shipping_rule",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"set_warehouse",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sec_warehouse",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"payment_schedule_section",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"more_info",
        "value":1
    })

    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"tracking_section",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"terms_section_break",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"column_break5",
        "value":1
    })
    Purchase_Order.save()
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"subscription_section",
        "value":1
    })
    Purchase_Order.save()
    make_property_setter('Purchase Order Item', 'conversion_factor', 'precision', '5', 'Select')
    create_custom_fields(custom_fields)