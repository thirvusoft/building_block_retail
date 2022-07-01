from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe


def item_customization():
    custom_fields = {
        "Item": [
            dict(fieldname='brand_field',
                label='Brand',
                fieldtype='Link',
                options='Brand',
                insert_after='stock_uom',
                depends_on='eval:!in_list(["Pavers","Compound Wall"], doc.item_group)',
                read_only=0),

            dict(fieldname='section_break_inventory',
                label='Inventory',
                fieldtype='Section Break',
                insert_after='is_fixed_asset',
                depends_on='eval:in_list(["Pavers","Compound Walls"],doc.item_group)'),

            dict(fieldname='plates_per_rack',
                label='Plates Per Rack',
                fieldtype='Int',
                insert_after='section_break_inventory',
                depends_on='eval:doc.item_group == "Pavers"'
                ),

            dict(fieldname='pavers_per_plate',
                label="Pavers Per Plate",
                fieldtype="Int",
                insert_after="plates_per_rack",
                depends_on='eval:doc.item_group == "Pavers"'),

            dict(fieldname='length',
                label='Length',
                fieldtype='Float',
                insert_after='pavers_per_plate',
                depends_on='eval:doc.item_group == "Compound Walls"'),

            dict(fieldname="pieces_per_bundle",
                label='Pieces Per Bundle',
                fieldtype='Int',
                insert_after='length'),
            
            dict(fieldname="weight_per_piece",
                label='Weight Per Piece',
                fieldtype='Float',
                insert_after='pieces_per_bundle',
                depends_on='eval:doc.item_group == "Compound Walls"'),
            
            dict(fieldname='per_sqr_ft',
                label='Per Sqr ft',
                fieldtype='Data',
                insert_after='weight_per_piece',
                hidden=1),

            dict(fieldname='pavers_per_sqft',
                label='Pavers Per Sqft',
                fieldtype='Float',
                insert_after='per_sqr_ft',
                depends_on='eval:doc.item_group == "Pavers"'),
            
            dict(fieldname='weight_per_paver',
                label='Weight Per Paver',
                fieldtype="Float",
                insert_after='pavers_per_sqft',
                depends_on='eval:doc.item_group == "Pavers"'),
            
            dict(fieldname='sqft_per_slab',
                label='Sqft Per Slab',
                insert_after='weight_per_paver',
                depends_on='eval:doc.item_group == "Compound Walls"',
                hidden=1),
            
            
            dict(fieldname='colum_break_item',
                label='',
                fieldtype='Column Break',
                insert_after='weight_per_paver'),
            
            dict(fieldname='no_of_layers_per_bundle',
                label='No of Layers Per Bundle',
                fieldtype='Int',
                insert_after='colum_break_item',
                depends_on='eval:doc.item_group == "Pavers"'),
            
            dict(fieldname='pavers_per_layer',
                label='Pavers Per Layer',
                fieldtype='Float',
                insert_after='no_of_layers_per_bundle',
                depends_on='eval:doc.item_group == "Pavers"'),
            
            dict(fieldname='weight_per_slab',
                label='Weight Per Slab',
                insert_after='pavers_per_layer',
                depends_on='eval:doc.item_group == "Compound Walls"',
                hidden=1),

            dict(fieldname='pavers_per_bundle',
                label='Pavers Per Bundle',
                fieldtype='Int',
                insert_after='weight_per_slab',
                depends_on='eval:doc.item_group == "Pavers"'),
            
            dict(fieldname="weight_per_bundle",
                label='Weight Per Bundle',
                fieldtype='Float',
                insert_after='pavers_per_bundle',
                read_only=1),

            
            dict(fieldname='sqft_per_bundle',
                label='Sqft Per Bundle',
                fieldtype='Data',
                insert_after='weight_per_bundle',
                depends_on='eval:doc.item_group == "Pavers"'),

            dict(fieldname='compound_wall_type',
                label='Compound Wall Type',
                fieldtype='Select',
                insert_after='item_group',
                depends_on='eval:doc.item_group == "Compound Walls"',
                options='Slab\nPost'
                ),
            dict(fieldname='colour',
                label='Colour',
                fieldtype='Data',
                insert_after='include_item_in_manufacturing',
                hidden=1),
            dict(fieldname='column_break_46',
                label='',
                fieldtype='Column Break',
                insert_after='warranty_period',
                hidden=1),
            dict(fieldname='short_blast',
                label='Short Blast',
                fieldtype='Check',
                insert_after='is_non_gst',
                hidden=1
                ),
            dict(fieldname='item_size',
                label='Item Size',
                fieldtype='Data',
                insert_after='short_blast',
                hidden=1),

            dict(fieldname='column_break_41',
                label="",
                fieldtype='Column Break',
                insert_after='item_size'),

            dict(fieldname='block_weight',
                label='Block Weight',
                fieldtype='Float',
                insert_after='column_break_41',
                hidden=1),
                
            dict(fieldname="bundle_weight",
                label='Bundle Weight',
                fieldtype='Int',
                insert_after='block_weight',
                hidden=1)
        ],
     
    }
    item=frappe.get_doc({
        'doctype':'Property Setter',
        'doctype_or_field': "DocField",
        'doc_type': "Item",
        'property':"hidden",
        'property_type':"Check",
        'field_name':"sb_barcodes",
        "value":1   
         })
    item.save()
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