frappe.ui.form.on("Company",{
    setup: function(frm){
        frm.set_query("default_employee_expenses_account",function(){
            return {
                "filters": {
                    "is_group":0,
                    "company":frm.doc.name
                }
            }
        })
    }
})