import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def supplier_customizations():
    supplier_custom_field()
    create_property_setter()
    
    
def supplier_custom_field():
    custom_field = {
        'Supplier':[
            dict(
                fieldname = 'sec_brk_sup',
                label = 'Default Item For Supplier',
                fieldtype = 'Section Break',
                insert_after = 'companies'
            ),
            dict(
                fieldname = 'default_items',
                label = 'Default Items',
                fieldtype = 'Table',
                options = 'TS Supplier Default Items',
                insert_after = 'sec_brk_sup',
                description = "This will add the supplier name in each Item's 'Supplier Item' table under 'Supplier Detail' Section"
            ),
            dict(
                fieldname = 'col_brk_123',
                fieldtype = 'Column Break',
                insert_after = 'default_items'
            ),
            dict(
                fieldname = 'remove_items',
                fieldtype = 'Button',
                insert_after = 'col_brk_123',
                label = 'Remove all Default Item for Suppliers',
                description = 'Click Here to Remove all Default Item From Supplier'
            ),
        ]
    }
    create_custom_fields(custom_field)
    
    
def create_property_setter():
    pass