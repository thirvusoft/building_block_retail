frappe.ui.form.on('Payroll Entry', {
    refresh: function(frm) {
        frm.add_custom_button(__('Payment'), function(){
            frappe.call({
                method: "sgp.sgp.utils.hr.journel_entry.journel_entry.create_journal_entry",
                args: {
                    'self': frm.doc
                },
                
            })
        },);
 

    }});