frappe.ui.form.on('Quotation', {
    setup:function(frm){
        frm.set_query("supervisor", function() {
            return {
                filters: {"Designation":"Supervisor"}
            }
        })
    }
})

