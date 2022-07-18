from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def sales_order_customization():
    custom_fields = {
        "Sales Order": [
            dict(fieldname='available_qty', label='Stock Available Qty',
                fieldtype='Table',options="TS Availbale Qty",insert_after='naming_series', allow_on_submit =1),
            
            dict(fieldname='section', fieldtype='Section Break',insert_after='available_qty'),
            
            dict(fieldname='is_multi_customer', label='is_multi_customer',
                fieldtype='Check',insert_after='section'),
            
            dict(fieldname='customers_name', label='Customers Name',
                fieldtype='Table',insert_after='customer', options='TS Customer', depends_on='eval:doc.is_multi_customer', mandatory_depends_on='eval:doc.is_multi_customer'),
            dict(fieldname='temporary_customer', label='temporary_customer', allow_on_submit=1, hidden=1,
                fieldtype='Data',insert_after='customers_name'),
            dict(fieldname='type', label='Type', reqd=1,
                fieldtype='Select',insert_after='temporary_customer', options='\nPavers\nCompound Wall'),
            dict(fieldname='work', label='Work', 
                fieldtype='Select',insert_after='type', options='\nSupply Only\nLaying Only\nSupply and Laying'),
            dict(fieldname='site_work', label='Site Name', 
                fieldtype='Link',insert_after='work', options='Project', allow_on_submit=1, mandatory_depends_on="eval:doc.work!='Supply Only'", depends_on="eval:doc.work!='Supply Only'"),
            dict(fieldname='supervisor', label='Supervisor',
                fieldtype='Link',insert_after='site_work', options='Employee'),
            dict(fieldname='supervisor_name', label='Supervisor Name', 
                fieldtype='Data',insert_after='supervisor', fetch_from='supervisor.first_name', read_only=1),
            dict(fieldname='delivery_details', label='Delivery Details', 
                fieldtype='Section Break',insert_after='tax_id'),
            dict(fieldname='distance', label='Distance (km)', precision=2, allow_on_submit=1,
                fieldtype='Float',insert_after='delivery_details'),
            dict(fieldname='pavers', label='Pavers',
                fieldtype='Table',insert_after='items', options='Item Detail Pavers', depends_on="eval:doc.type=='Pavers'"),
            dict(fieldname='compoun_walls', label='Compound Walls', 
                fieldtype='Table',insert_after='pavers', options='Item Detail Compound Wall', depends_on="eval:doc.type=='Compound Wall'"),
            dict(fieldname='raw_materials_', label='Raw Materials ',
                fieldtype='Section Break',insert_after='compoun_walls'),
            dict(fieldname='raw_materials', label='Raw Materials', 
                    fieldtype='Table',insert_after='raw_materials_', options='TS Raw Materials'),
            dict(fieldname='branch', label='Branch', 
                    fieldtype='Link',insert_after='update_auto_repeat_reference', options='Branch')
        ]
    }
    create_custom_fields(custom_fields)
    properties=[
        ['hidden', 'Check', 'accounting_dimensions_section', 1],
        
        ['hidden', 'Check', 'contact_info', 1],
        
        ['hidden', 'Check', 'currency_and_price_list', 1],
        
        ['hidden', 'Check', 'set_warehouse', 1],
        
        ['hidden', 'Check', 'scan_barcode', 1],
        
        ['hidden', 'Check', 'packing_list', 1],
        
        ['hidden', 'Check', 'base_total', 1],
        
        ['hidden', 'Check', 'base_net_total', 1],
        
        ['hidden', 'Check', 'total_net_weight', 1],
        
        ['hidden', 'Check', 'net_total', 1],
        
        ['hidden', 'Check', 'loyalty_points_redemption', 1],
        
        ['hidden', 'Check', 'base_total_taxes_and_charges', 1],
        
        ['hidden', 'Check', 'shipping_rule', 1],
        
        ['hidden', 'Check', 'section_break_48', 1],
        
        ['hidden', 'Check', 'payment_schedule_section', 1],
                
        ['hidden', 'Check', 'more_info', 1],
        
        ['hidden', 'Check', 'printing_details', 1],
        
        ['hidden', 'Check', 'sales_team_section_break', 1],
        
        ['hidden', 'Check', 'section_break1', 1],
        
        ['hidden', 'Check', 'subscription_section', 1]
    ]
    for prop in properties:
        so=frappe.get_doc({
            'doctype':'Property Setter',
            'doctype_or_field': "DocField",
            'doc_type': "Sales Order",
            'property':prop[0],
            'property_type':prop[1],
            'field_name':prop[2],
            "value":prop[3]
        })
        so.save()