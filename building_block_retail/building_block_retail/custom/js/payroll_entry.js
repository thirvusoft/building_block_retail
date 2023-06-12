frappe.ui.form.on("Payroll Employee Detail",{
    amount_taken: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        if(row.amount_taken > row.total_balance_amount){
            frappe.model.set_value(cdt, cdn, 'amount_taken', 0)
            frappe.throw("Row #"+(row.idx)+": Total Balance Amount cannot be greater than Amount Taken.")
        }
    }
})