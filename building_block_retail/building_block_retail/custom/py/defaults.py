import frappe

@frappe.whitelist()
def create_defaults():
    if(not frappe.db.exists('Designation', 'Job Worker')):
        doc=frappe.new_doc('Designation')
        doc.update({
            'doctype': 'Designation',
            'designation_name': 'Job Worker'
        })
        doc.save()
    
    if(not frappe.db.exists('Designation', 'Operator')):
        doc=frappe.new_doc('Designation')
        doc.update({
            'doctype': 'Designation',
            'designation_name': 'Operator'
        })
        doc.save()
    
    if(not frappe.db.exists('Designation', 'Supervisor')):
        doc=frappe.new_doc('Designation')
        doc.update({
            'doctype': 'Designation',
            'designation_name': 'Supervisor'
        })
        doc.save()
        
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Project",
        "field_name":"status",
        "property":"options",
        "value":"\nOpen\nLand Work Completed\nOn Process\nHold\nStock Pending at Site\nPending Qty Returned\nPart Measurement\nSite Measured\nCompleted\nCancelled"
    })
    doc.save()

    if(not frappe.db.exists("Designation", "Contractor")):
        doc = frappe.new_doc("Designation")
        doc.designation_name = "Contractor"
        doc.save(ignore_permissions=True)
    if(not frappe.db.exists("Designation", "Loader")):
        doc = frappe.new_doc("Designation")
        doc.designation_name = "Loader"
        doc.save(ignore_permissions=True)
    if(not frappe.db.exists("Designation", "Driver")):
        doc = frappe.new_doc("Designation")
        doc.designation_name = "Driver"
        doc.save(ignore_permissions=True)
    if(not frappe.db.exists("Designation", "Earth Rammer Contractor")):
        doc = frappe.new_doc("Designation")
        doc.designation_name = "Earth Rammer Contractor"
        doc.save(ignore_permissions=True)
        
    if(not frappe.db.exists("Salary Component", "Advance")):
        doc = frappe.new_doc("Salary Component")
        doc.salary_component = "Advance"
        doc.salary_component_abbr = 'ADV'
        doc.type = 'Deduction'
        doc.save(ignore_permissions=True)
    frappe.db.commit()