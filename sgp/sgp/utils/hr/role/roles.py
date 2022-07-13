import frappe

def create_role():
    ## Creating Work Flow for Quotation Workflow
    if(not frappe.db.exists("Role", "Admin")):
        role = frappe.new_doc("Role")
        role.update({
                "role_name":"Admin",
                "disabled":0,
                "is_custom":0,
                "desk_access":1,
                "two_factor_auth":0,
                "search_bar":1,
                "notifications":1,
                "list_sidebar":1,
                "bulk_actions":1,
                "view_switcher":1,
                "form_sidebar":1,
                "timeline":1,
                "dashboard":1,
        })
        role.insert(ignore_permissions=True)