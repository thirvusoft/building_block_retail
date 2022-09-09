import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def address_customization():
    address_custom_fields()
    address_property_setter()

def address_custom_fields():
    pass

def address_property_setter():
    make_property_setter('Address', 'county', 'hidden', '1', 'Check')