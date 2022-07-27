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
        frm.set_query("default_company_bank_account",function(){
            return {
                "filters": {
                    "is_company_account":1,
                    "company":frm.doc.company_name
                }
            }
        })
    }
})