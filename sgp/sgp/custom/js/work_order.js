frappe.ui.form.on("Work Order",{
    on_submit: function(frm){
        frappe.call({
            method: "sgp.sgp.custom.py.job_card.get_link_to_jobcard",
            args: {
                work_order: frm.doc.name
            },
            callback(r){
                window.location.assign(r.message)
            }
        })
    },
    refresh(frm){
        frm.remove_custom_button('Create Job Card')
        cur_frm.set_value("skip_transfer",1)
        cur_frm.refresh()
    }
})