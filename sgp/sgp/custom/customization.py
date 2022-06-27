from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
def execute():
    custom_fields = {
        "Request for Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='naming_series', read_only=0,reqd=1),
            
        ],
        "Supplier Quotation": [
            dict(fieldname='company_name', label='Company',
                fieldtype='Link', options='Company',insert_after='column_break1', read_only=0,reqd=1),
            
        ],
      
      
    }
    create_custom_fields(custom_fields)
    print('finished')



