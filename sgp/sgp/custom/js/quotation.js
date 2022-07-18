frappe.ui.form.on('Quotation', {
    setup:function(frm){
        frm.set_query("supervisor", function() {
            return {
                filters: {"Designation":"Supervisor"}
            }
        })
    },
    refresh:function(frm){
        if(frm.doc.workflow_state == "Rejected" ){
            frm.clear_custom_buttons();
        }
    }
})

