import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def delivery_note_customization():
    delivery_note_item_property_setter()
    delivery_note_item_custom_fields()
    delivery_note_custom_field()
    delivery_note_property_setter()
    packed_item_customization()
def delivery_note_custom_field():
    pass
def delivery_note_property_setter():
    pass