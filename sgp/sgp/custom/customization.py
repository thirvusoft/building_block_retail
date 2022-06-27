from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe



def execute():
    custom_fields = {
        "Request for Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='naming_series', read_only=0,reqd=1),
            
        ],
        "Supplier Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
            
        ],
         "Purchase Order": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
            
        ],
         "Purchase Invoice": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
            
        ],
        "Purchase Invoice": [
            dict(fieldname='branch', label='Branch',
                fieldtype='Link', options='Branch',insert_after='company_name', read_only=0),
            
        ],
       
        
       
      
      
    }
    Purchase_Order=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Order",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_dimensions_section",
        "value":1
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

    # Purchase Receipt
  
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"more_info",
        "value":1
    })
    Purchase_Receipt.save()
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_dimensions_section",
        "value":1
    })
    Purchase_Receipt.save()
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sec_warehouse",
        "value":1
    })
    Purchase_Receipt.save()
  
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"raw_material_details",
        "value":1
    })
    Purchase_Receipt.save()
  
   
   

    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"printing_settings",
        "value":1
    })
    Purchase_Receipt.save()
  
    
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"shipping_rule",
        "value":1
    })
    Purchase_Receipt.save()
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"raw_material_details",
        "value":0
    })
    Purchase_Receipt.save()
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"column_break5",
        "value":1
    })
    Purchase_Receipt.save()
    Purchase_Receipt=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Receipt",
        'property':"label",
        'field_name':"lr_date",
        "value":"Driver Name"
    })
    Purchase_Receipt.save()

    # Purchase Invoice
  
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"due_date",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"section_addresses",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"currency_and_price_list",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"taxes_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"shipping_rule",
        "value":1
    })
    Purchase_Invoice.save()
   
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"payment_schedule_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"gst_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"more_info",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"subscription_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"printing_settings",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_details_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"terms_section_break",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"accounting_dimensions_section",
        "value":1
    })
    Purchase_Invoice.save()
    Purchase_Invoice=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Purchase Invoice",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"",
        "value":1
    })
    Purchase_Invoice.save()
    create_custom_fields(custom_fields)