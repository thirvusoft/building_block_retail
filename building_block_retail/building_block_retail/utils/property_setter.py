import frappe 
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def create_property_setter():
    make_property_setter('BOM Operation', 'time_in_mins', 'reqd', 0, 'Check')
    make_property_setter('Payment Entry','mode_of_payment', 'reqd', 1, 'Check')
    make_property_setter('Payment Entry', 'mode_of_payment', 'default', 'Cash', 'Text Editor')
    make_property_setter('Payment Entry', 'section_break_14', 'depends_on', 'eval:(doc.party && doc.paid_from && doc.paid_to)', 'Text Editor')
    make_property_setter('Sales Invoice', 'outstanding_amount', 'in_list_view', 1, 'Check')
    make_property_setter('Purchase Receipt','apply_putaway_rule','hidden',1,'Check')
    make_property_setter('Stock Entry','apply_putaway_rule','hidden',1,'Check')
    make_property_setter('BOM','routing','hidden',1,'Check')
    make_property_setter('Quotation','coupon_code','hidden',1,'Check')
    make_property_setter('Quotation','referral_sales_partner','hidden',1,'Check')
    make_property_setter('Quotation','select_print_heading','hidden',1,'Check')
    make_property_setter('Quotation','language','hidden',1,'Check')
    make_property_setter('Quotation','supplier_quotation','hidden',1,'Check')
    make_property_setter('Quotation','shipping_rule','hidden',1,'Check')
    make_property_setter('BOM','website_section','hidden',1,'Check')
    make_property_setter('BOM','scrap_section','hidden',1,'Check')
    make_property_setter('BOM','transfer_material_against','hidden',1,'Check')
    make_property_setter('BOM','transfer_material_against','default','Work Order','Text Editor')
    make_property_setter('Workstation','working_hours_section','hidden',1,'Check')
    make_property_setter('Work Order','serial_no_and_batch_for_finished_good_section','hidden',1,'Check')
    make_property_setter('BOM','with_operations','default',1,'Check')
    make_property_setter('Sales Invoice Item','ts_qty','depends_on','eval:!doc.cannot_be_bundle','Text Editor')
    make_property_setter('Sales Invoice Item','area_per_bundle','depends_on','eval:!doc.cannot_be_bundle','Text Editor')
    make_property_setter('Item Detail Pavers','area_per_bundle','depends_on','eval:!doc.cannot_be_bundle','Text Editor')
    
