from warnings import filters
from building_block_retail.building_block_retail.custom.py.vehicle_log import notification
import frappe


@frappe.whitelist()
def get_permission_for_attachment(user):
    user = frappe.get_all("Has Role", filters={'parent':user, 'role':'Supervisor'}, pluck='role')
    if(len(user)):return False
    return True

def workflow_quotation(doc,action):
    if doc.workflow_state == "Waiting for Approval":
        user_list = frappe.get_all("Has Role",pluck="parent",filters={"role":"Admin","parent":['!=', 'Administrator']})
        for i in user_list:
            notification = frappe.new_doc("Notification Log")
            notification.update({
                "subject" : f"{doc.name} Quotation has been waiting for your approval",
                "email_content" : f"{doc.name} Quotation has been waiting for your approval",
                "document_type" : "Quotation",
                "document_name" : doc.name,
                "for_user" : i,
                "from_user" : doc.owner,
                "type" : "Energy Point"
            })
            notification.insert(ignore_permissions=True)

def quotation_whatsapp(doc, action):

    import http.client
    import json
    from frappe.utils.password import get_decrypted_password

    conn = http.client.HTTPSConnection(frappe.db.get_single_value('Whatsapp Setting', 'ts_api_endpoint'))

    payload = json.dumps({
    "countryCode": "+91",
    "phoneNumber": doc.supervisor_number,
    "callbackData": "some text here",
    "type": "Template",
    "template": {
        "name": "velavabricks_quotation_", 
        "languageCode": "en",
        "bodyValues": [
        doc.customer_name,
        doc.name
        ],
        "buttonValues": {
        "0": [
            (frappe.utils.get_url()+"/app/quotation/"+doc.name).split("https://velavaabricks.thirvusoft.com/")[-1]
        ]
        }
    }
    })
    try:
        headers = {
        'Authorization': get_decrypted_password('Whatsapp Setting', 'Whatsapp Setting', 'ts_authentication',False),
        'Content-Type': 'application/json',
        'Cookie': 'ApplicationGatewayAffinity=a8f6ae06c0b3046487ae2c0ab287e175; ApplicationGatewayAffinityCORS=a8f6ae06c0b3046487ae2c0ab287e175'
        }
        conn.request("POST", "/v1/public/message/", payload, headers)
        res = conn.getresponse()
        data = res.read()
    except Exception as e:
        error = f"Doctype: {doc.doctype} " + str(e)
        api_endpoint = frappe.db.get_single_value('Whatsapp Setting', 'ts_api_endpoint')
        api_authentication = frappe.db.get_single_value('Whatsapp Setting', 'ts_authentication')
        if(not api_endpoint):
            error += "\n API End Point Not found."
        if(not api_authentication):
            error += "\n API Authentication Not found."
        frappe.log_error(error,"Whatsapp error")