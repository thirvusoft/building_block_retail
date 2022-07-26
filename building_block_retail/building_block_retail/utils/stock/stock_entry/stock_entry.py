from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def stock_entry_custom():
    stock_entry_custom_fields()
    stock_entry_property_setter()
def stock_entry_custom_fields():
    custom_fields = {
        "Stock Entry": [
            dict(
                fieldname= "ts_job_card",
                fieldtype= "Link",
                insert_after= "job_card",
                label= "Job Card",
                options= "Job Card"
            ),
            dict(
                fieldname= "code",
                fieldtype= "Code",
                insert_after= "ts_job_card",
                label= "Current Completed Qty",
            ),
        ]
    }
    create_custom_fields(custom_fields)
def stock_entry_property_setter():
    doctype="Stock Entry"
    make_property_setter(doctype, 'inspection_required', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'more_info', 'hidden', '1', 'Check')
    make_property_setter(doctype, 'printing_settings', 'hidden', '1', 'Check')
