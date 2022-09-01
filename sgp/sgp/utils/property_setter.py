import frappe 
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def create_property_setter():
    make_property_setter('BOM Operation', 'time_in_mins', 'reqd', 0, 'Check')
    make_property_setter('Payment Entry','mode_of_payment', 'reqd', 1, 'Check')
    make_property_setter('Payment Entry', 'mode_of_payment', 'default', 'Cash', 'Text Editor')
    make_property_setter('Payment Entry', 'section_break_14', 'depends_on', 'eval:(doc.party && doc.paid_from && doc.paid_to)', 'Text Editor')
    make_property_setter('Sales Invoice', 'outstanding_amount', 'in_list_view', 1, 'Check')