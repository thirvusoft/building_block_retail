import frappe
import json 

def a():
        try:
            last_update='2022-12-19 13:27:32.385625'
            f= open("/home/ponnusamy/v13bench/apps/building_block_retail/event_res.txt","w+")
            f.write(f"""last_update: {last_update}""")
            f.close()

            res = frappe.call("frappe.event_streaming.doctype.event_update_log.event_update_log.get_update_logs_for_consumer", 
                event_consumer="https://vbprime.thirvusoft.com",
                doctypes='[\n "Company",\n "Branch",\n "Customer",\n "Supplier",\n "Item",\n "Item Tax Template",\n "Accounting Dimension",\n "Sales Invoice",\n "Purchase Invoice",\n "Payment Entry",\n "Address",\n "Contact",\n "Terms and Conditions",\n "Sales Order",\n "Delivery Note",\n "Purchase Order",\n "Purchase Receipt",\n "File",\n "Employee",\n "Cost Center",\n "Warehouse",\n "Item Attribute",\n "Item Group",\n "Item Price",\n "Price List",\n "Item Tax Template",\n "TS Item Tax",\n "UOM Conversion Factor",\n "UOM"\n]',
                last_update=last_update
            )

            f= open("/home/ponnusamy/v13bench/apps/building_block_retail/event_res.txt","w+")
            f.write(json.dumps(res, default=str, indent=4))
            f.close()
            frappe.log_error(title="EVENT SYNC RES", message=frappe.utils.now())
        except:
            frappe.log_error(title='event sync res', message=frappe.get_traceback())

def event_sync():   
    frappe.enqueue(method=a, queue='long')

# from event_sync import event_sync