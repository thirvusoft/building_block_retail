import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def customer_customizations():
    create_customer_custom_fields()
    create_customer_property_setter()
    
def create_customer_custom_fields():
    pass

def create_customer_property_setter():
    make_property_setter('Customer', 'account_manager', 'hidden', 1, 'Check')
    make_property_setter('Customer', 'gst_category', 'options', 'Registered Regular\nUnregistered', 'Text Editor')
