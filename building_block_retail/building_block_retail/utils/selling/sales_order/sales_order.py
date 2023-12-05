from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
import frappe
import building_block_retail


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
                fieldtype='Select',insert_after='temporary_customer', options='\nPavers\nCompound Wall', default = 'Pavers',),
            dict(fieldname='work', label='Work', 
                fieldtype='Select',insert_after='type', options='\nSupply Only\nSupply and Laying\nLaying Only', reqd=1),
            dict(fieldname='site_work', label='Site Name', 
                fieldtype='Link',insert_after='work', options='Project', allow_on_submit=0, mandatory_depends_on="eval:doc.work!='Supply Only'", depends_on="eval:doc.work!='Supply Only'"),
            dict(fieldname='supervisor', label='Supervisor',
                fieldtype='Link',insert_after='site_work', options='Employee'),
            dict(fieldname='supervisor_name', label='Supervisor Name', 
                fieldtype='Data',insert_after='supervisor', fetch_from='supervisor.first_name', read_only=1),
             dict(
                fieldname= "supervisor_number",
                fieldtype= "Data",
                insert_after= "supervisor_name",
                label= "Supervisor Number",
                fetch_from = "supervisor.cell_number"
            ),
            dict(fieldname='delivery_details', label='Delivery Details', 
                fieldtype='Section Break',insert_after='tax_id'),
            dict(fieldname='distance', label='Distance (km)', precision=2, allow_on_submit=1,
                fieldtype='Float',insert_after='delivery_details'),
            dict(fieldname='possible_delivery_dates', 
            label='Possible Delivery Dates',
            fieldtype='Table',
            insert_after='items', 
            options='Item wise Delivery Date', 
            read_only = 1,
            allow_on_submit = 1,
            ),
            dict(fieldname='pavers', label='Pavers',
                fieldtype='Table',insert_after='possible_delivery_dates', options='Item Detail Pavers', depends_on="eval:doc.type=='Pavers'", hidden=1),
            dict(fieldname='compoun_walls', label='Compound Walls', 
                fieldtype='Table',insert_after='pavers', options='Item Detail Compound Wall', depends_on="eval:doc.type=='Compound Wall'", hidden=1),
            dict(fieldname='raw_materials_', label='Raw Materials ',
                fieldtype='Section Break',insert_after='compoun_walls'),
            dict(fieldname='raw_materials', label='Raw Materials', 
                    fieldtype='Table',insert_after='raw_materials_', options='TS Raw Materials', hidden=1),
            dict(fieldname='branch', label='Branch', 
                    fieldtype='Link',insert_after='cost_center', options='Branch'),
            dict(
                fieldname= "ts_map_link",
                fieldtype= "Data",
                insert_after= "po_no",
                label= "Enter Delivery Location Map Link",
                description = 'Open Google Map in Browser and Point a Exact Delivery Location and Copy the Browser Url and Paste Here. Eg: <a href = https://maps.google.com>https://maps.google.com</a>',
                length=1000,
            ),
            	dict(fieldname='accounting', label='Accounting',
				fieldtype='Check', insert_after='branch',fetch_from="branch.is_accounting",hidden=1),
        dict(fieldname='abbr_sales_order', label='Abbrevation',
				fieldtype='Data', insert_after='accounting',fetch_from="branch.abbr",hidden=1)
        
        ]
    }
    create_custom_fields(custom_fields)
    properties=[
        ['hidden', 'Check', 'accounting_dimensions_section', 0],
        
        ['hidden', 'Check', 'contact_info', 1],
        
        ['hidden', 'Check', 'currency_and_price_list', 1],
        
        ['hidden', 'Check', 'set_warehouse', 0],
        
        ['reqd', 'Check', 'set_warehouse', 0],

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
    make_property_setter('Sales Order Item', 'conversion_factor', 'precision', '5', 'Select')
        
def item_details_pavers_customization():
    item_details_custom_fields = {
        "Item Detail Pavers": [
              dict(
                 fieldname  = "cannot_be_bundle",
                 fieldtype  = "Check",
                 insert_after  = "item",
                 label = "Cannot Be Bundle",
                 fetch_from = 'item.cannot_be_bundle',
                 hidden=1
            )
           
        ]
    }
    create_custom_fields(item_details_custom_fields)






import math

def update_old_sales_orders():
    """
    Patch to update new fields in sales order item table
    """
    so=frappe.get_all("Sales Order", filters={"docstatus":1}, pluck="name")
    for i in so:
        doc=frappe.get_doc("Sales Order", i)
        print(doc.name)
        for item in doc.items:
            if frappe.get_value("Item", item.item_code, "sales_uom") == "Square Foot":
                pcs_per_sqft = frappe.db.get_value("UOM Conversion Detail", {'parent': item.item_code, 'parenttype': 'Item', 'uom': "Square Foot"}, 'conversion_factor') or 0
                pcs_per_bundle = frappe.db.get_value("UOM Conversion Detail", {'parent': item.item_code, 'parenttype': 'Item', 'uom': "bundle"}, 'conversion_factor') or 0
                qty_str = str(item.qty)
                pcs_qty=0
                if len(qty_str.split(".")) > 1:
                    dec_val = qty_str.split(".")[1]
                    pcs_qty =  building_block_retail.uom_conversion(item=item.item_code, from_uom = item.uom, from_qty=float(f"0.{dec_val}"), to_uom="Nos")
                    item.qty = float(qty_str.split(".")[0])
                # sqft_qty = building_block_retail.uom_conversion(item=item.code, from_uom = item.uom, from_qty=item.qty, to_uom="Nos")
                frappe.db.set_value("Sales Order Item", {"name":item.name}, "pieces_per_sqft", pcs_per_sqft, update_modified=False)
                frappe.db.set_value("Sales Order Item", {"name":item.name}, "pieces_per_bundle", pcs_per_bundle, update_modified=False)
                frappe.db.set_value("Sales Order Item", {"name":item.name}, "pieces", math.ceil(pcs_qty), update_modified=False)
                frappe.db.set_value("Sales Order Item", {"name":item.name}, "required_sqft", item.qty, update_modified=False)