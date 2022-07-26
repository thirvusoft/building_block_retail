from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def item_Customization():
    item_customization()
    create_property_setter()

def item_customization():
    custom_fields={
        "Item":[
            dict(fieldname='parent_item_group',
                label='Parent Item Group',
                fieldtype='Data',
                insert_after='compound_wall_type',
                fetch_from = 'item_group.parent_item_group',
                hidden = 1
            ),
            dict(
                 fieldname  = "sec_brk_cost",
                 fieldtype  = "Section Break",
                 insert_after  = "bundle_per_sqr_ft",
                 label = "Cost",
                 depends_on = 'eval:doc.parent_item_group == "Products"'
            ),
            dict(
                 fieldname  = "employee_rate",
                 fieldtype  = "Currency",
                 insert_after  = "sec_brk_cost",
                 label = "Piece Rate(For Manufacture)",
                 description = "Per Qty",
            ),
            dict(
              fieldname = "col_brk_cost",
              fieldtype = "Column Break",
              insert_after = "employee_rate"  
            ),
            dict(
                 fieldname  = "laying_cost",
                 fieldtype  = "Currency",
                 insert_after  = "col_brk_cost",
                 label = "Square Foot Rate(For Laying)",
                 description = "Per Qty",
            ),
        ],
    }
    create_custom_fields(custom_fields)
    
    
def create_property_setter():
    make_property_setter('Item', 'serial_nos_and_batches', 'hidden', 1, 'Check')
    make_property_setter('Item', 'reorder_section', 'depends_on', 'eval:doc.parent_item_group != "Products"', 'Text Editor')
    make_property_setter('Item', 'sales_uom', 'depends_on', 'eval:doc.is_sales_item == 1', 'Text Editor')
    make_property_setter('Item', 'purchase_uom', 'depends_on', 'eval:doc.is_purchase_item == 1', 'Text Editor')
    make_property_setter('Item', 'sales_uom', 'mandatory_depends_on', 'eval:doc.is_sales_item == 1', 'Text Editor')
    make_property_setter('Item', 'purchase_uom', 'mandatory_depends_on', 'eval:doc.is_purchase_item == 1', 'Text Editor')
    make_property_setter('Item', 'valuation_rate', 'depends_on', 'eval:doc.parent_item_group != "Products"', 'Text Editor')
    make_property_setter('Item', 'standard_rate', 'depends_on', 'eval:doc.parent_item_group != "Products"', 'Text Editor')
    make_property_setter('Item', 'is_fixed_asset', 'depends_on', 'eval:doc.parent_item_group != "Products"', 'Text Editor')