from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def journal_entry_customization():
    journal_entry_custom_field()
    journal_entry_property_setter()

def journal_entry_custom_field():
    custom_fields={
        "Journal Entry":[
            dict(
                fieldname= "stock_entry_linked",
                fieldtype= "Link",
                insert_after= "stock_entry",
                label= "Stock Entry",
                options = "Stock Entry",
                hidden = 1
            ),
            dict(
                fieldname= "ts_salary_slip",
                fieldtype= "Link",
                insert_after= "naming_series",
                label= "Salary Slip",
                options = "Salary Slip",
                hidden = 1
            )
        ]
    }
    create_custom_fields(custom_fields)

def journal_entry_property_setter():
    pass