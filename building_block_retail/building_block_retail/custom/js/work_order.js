frappe.ui.form.on("Work Order",{
    refresh(frm){
        cur_frm.set_value("skip_transfer",1)
    }
})