from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe


def item_customization():
    custom_fields = {
        "Item": [
            dict(fieldname='brand_field', label='Brand',
                fieldtype='Link', options='Brand',insert_after='stock_uom', read_only=0),
          
            
        ],
     
    }
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"is_nil_exempt",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"is_item_from_hub",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"is_non_gst",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"allow_alternative_item",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"section_break_11",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"inventory_section",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"batch_number_series",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"has_expiry_date",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"retain_sample",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"has_serial_no",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deferred_revenue",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deferred_revenue",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"deferred_expense_section",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"inspection_criteria",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"manufacturing",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"hub_publishing_sb",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"hub_publishing_sb",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"defaults",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"min_order_qty",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"safety_stock",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"is_customer_provided_item",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"delivered_by_supplier",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"foreign_trade_details",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"max_discount",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"max_discount",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"customer_details",
        "value":1
    })
    item.save()
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"grant_commission",
        "value":1
    })
    item.save()
    create_custom_fields(custom_fields)