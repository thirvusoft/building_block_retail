frappe.ui.form.on('Payroll Entry', {
    refresh: function(frm) {
        if (cur_frm.doc.__islocal == undefined){
        frm.add_custom_button(__('Get amount from employee account'), function(){
            frappe.call({
                method: "building_block_retail.building_block_retail.utils.hr.journel_entry.journel_entry.create_journal_entry",
                args: {
                    'self': frm.doc
                    
                },
                
            })
        }
        );}
 

    }});