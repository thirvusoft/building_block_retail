import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sales_taxes_and_charges_custom_fields():
    custom_fields={
        "Sales Taxes and charges":[
          dict(
          fieldname = "branch",
          fieldtype = "Link",
          insert_after = "accounting_dimensions_section",
          label = "Branch",
          options = "Branch"
          ),
        ],
    }
    create_custom_fields(custom_fields)


def sales_taxes_and_charges_property_setter():
    pass