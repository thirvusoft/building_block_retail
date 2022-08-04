from requests import options
import frappe
from building_block_retail.building_block_retail.utils.selling.sales_invoice.sales_taxes_and_charges.sales_taxes_and_charges_custom_fields import sales_taxes_and_charges_custom_fields,sales_taxes_and_charges_property_setter
from building_block_retail.building_block_retail.utils.selling.sales_invoice.sales_invoice_item.sales_invoice_item_custom_fields import sales_invoice_item_custom_fields,sales_invoice_item_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def sales_invoice_customization():
    sales_invoice_custom_field()
    sales_invoice_property_setter()
    sales_taxes_and_charges_custom_fields()
    sales_taxes_and_charges_property_setter()
    sales_invoice_item_custom_fields()
    sales_invoice_item_property_setter()

def sales_invoice_custom_field():
    custom_fields={
        "Sales Invoice":[
            dict(
                fieldname= "branch",
                fieldtype= "Link",
                insert_after= "company",
                label= "Branch",
                options= "Branch"
            ),
            dict(
                fieldname= "site_work",
                fieldtype= "Link",
                insert_after= "customer",
                label= "Site Work",
                options= "Project",
            ),
            dict(
                fieldname= "type",
                fieldtype= "Select",
                insert_after= "ref_practitioner",
                label= "Sales Type",
                options= "\nPavers\nCompound Wall",
            ),
            dict(
                fieldname= "work",
                fieldtype= "Select",
                insert_after= "eway_bill_cancelled",
                label= "Work",
                options= '\nSupply Only\nSupply and Laying',
                reqd = 1 
            ),
            dict(
                fetch_from= "project.project_name",
                fieldname= "ts_site_name",
                fieldtype= "Data",
                hidden= 1,
                insert_after= "cost_center",
                label= "Site Name",
            ),
            dict(
                fetch_from= "shipping_address_name.gstin",
                fieldname= "customer_gstin",
                fieldtype= "Data",
                hidden= 1,
                insert_after= "shipping_address_name",
                label= "Customer GSTIN",
            ),
            dict(
                fieldname= "place_of_supply",
                fieldtype= "Data",
                insert_after= "customer_gstin",
                label= "Place of Supply",
                read_only= 1,
            ),
            dict(
                fieldname= "transporter_info",
                fieldtype= "Section Break",
                insert_after= "set_target_warehouse",
                label= "Transporter Info",
                print_hide= 1,
                translatable= 1,
            ),
            dict(
                fieldname= "transporter",
                fieldtype= "Link",
                insert_after= "transporter_info",
                label= "Transporter",
                options= "Supplier",
            ),
            dict(
                fieldname= "mode_of_transport",
                fieldtype= "Select",
                insert_after= "transporter",
                label= "Mode of Transport",
                options= "\nRoad\nAir\nRail\nShip",
                print_hide= 1,
            ),
            dict(
                fieldname= "column_break_80",
                fieldtype= "Column Break",
                insert_after= "mode_of_transporter",
            ),
            dict(
                fieldname= "vehicle_no",
                fieldtype= "Data",
                insert_after= "column_break_80",
                label= "Vehicle No",
                print_hide= 1,
            ),
            dict(
                fieldname= "sales_invoice_print_items",
                fieldtype= "Section Break",
                hidden= 1,
                insert_after= "items",
                label= "Sales Invoice Print Items",
            ),
            dict(
                fieldname= "sales_invoice_print_items_table",
                fieldtype= "Table",
                insert_after= "sales_invoice_print_items",
                label= "Sales Invoice Print Items Table",
                options= "Sales Invoice Print Items",
            ),
            dict(
                fieldname= "print_item_tax",
                fieldtype= "Section Break",
                hidden= 1,
                insert_after= "taxes",
                label= "Print Item Tax",
            ),
            dict(
                fieldname= "print_item_tax_table",
                fieldtype= "Table",
                insert_after= "print_item_tax",
                label= "Print Item tax table",
                options= "Print Items Tax",
            ),
            dict(
                fieldname= "si_remarks",
				fieldtype= "Small Text",
				insert_after= "items",
				label= "Remarks",
                no_copy = 1
            ),
            dict(
                fieldname= "jobworker_salary",
				fieldtype= "Section Break",
				insert_after= "accounting_dimensions_section",
				label= "Job Worker Salary",
                collapsible = 1
            ),
             dict(
                fieldname= "jobworker_name",
				fieldtype= "Link",
				insert_after= "jobworker_salary",
				label= "Job Worker Name",
                options = 'Employee'
            ),
            dict(
                fieldname= "job_worker_table",
				fieldtype= "Table",
				insert_after= "jobworker_name",
				label= "Job Worker Salary",
                options = 'TS Job Worker Salary'
            ),
            dict(
                fieldname= "total_amount_job_worker",
				fieldtype= "Float",
				insert_after= "job_worker_table",
				label= "Total Amount",
            ),
            dict(
                fieldname= "section_break1",
				fieldtype= "Section Break",
				insert_after= "total_amount_job_worker",

            ),
            
        
        ],
    }
    create_custom_fields(custom_fields)

def sales_invoice_property_setter():
    make_property_setter("Sales Invoice", "driver_name", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "lr_date", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "gst_vehicle_type", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "gst_transporter_id", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "driver", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "lr_no", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "customer_po_details", " collapsible ", "0", "Check")
    make_property_setter("Sales Invoice", "address_and_contact", " collapsible ", "0", "Check")
    make_property_setter("Sales Invoice", "accounting_dimensions_section", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "contact_mobile", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "contact_email", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "customer_gstin", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "company_gstin", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "company_address_display", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "currency_and_price_list", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "sec_warehouse", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "scan_barcode", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "sales_invoice_print_items", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "pricing_rule_details", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "time_sheet_list", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "shipping_rule", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "print_item_tax", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "loyalty_points_redemption", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "additional_discount_account", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "column_break4", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "payment_schedule_section", "hidden", "0", "Check")
    make_property_setter("Sales Invoice", "cash_bank_account", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "terms_section_break", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "edit_printing_settings", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "gst_section", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "more_information", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "inter_company_invoice_reference", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "represents_company", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "is_discounted", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "campaign", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "is_internal_customer", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "source", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "more_info", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "c_form_applicable", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "c_form_no", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "sales_team_section_break", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "section_break2", "hidden", "1", "Check")
    make_property_setter("Sales Invoice", "subscription_section", "hidden", "1", "Check")