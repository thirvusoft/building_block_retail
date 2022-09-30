// frappe.ui.form.on('Payroll Entry', {
//     refresh: function(frm) {
//         if (cur_frm.doc.__islocal == undefined){
//         frm.add_custom_button(__('Get amount from employee account'), function(){
//             frappe.call({
//                 method: "building_block_retail.building_block_retail.utils.hr.journel_entry.journel_entry.create_journal_entry",
//                 args: {
//                     'self': frm.doc
                    
//                 },
                
//             })
//         }
//         );}
 

//     }});

frappe.ui.form.on("Payroll Employee Detail",{
    amount_taken: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        if(row.amount_taken > row.total_balance_amount){
            frappe.model.set_value(cdt, cdn, 'amount_taken', 0)
            frappe.throw("Row #"+(row.idx)+": Total Balance Amount cannot be greater than Amount Taken.")
        }
    }
})