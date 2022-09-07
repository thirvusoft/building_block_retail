import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def customer_customization():
    customer_custom_fields()
    customer_property_setter()

def customer_custom_fields():
    pass

def customer_property_setter():pass
    # make_property_setter('Customer', 'naming_series', 'options', 'CUST-.YYYY.-\n.{customer_name}.-.{mobile_no}', 'Text Editor')
    # make_property_setter('Customer', 'naming_series', 'default', '.{customer_name}.-.{mobile_no}', 'Text Editor')