frappe.ui.form.on("Work Order",{
    on_submit: function(frm){
        frappe.call({
            method: "building_block_retail.building_block_retail.custom.py.job_card.get_link_to_jobcard",
            args: {
                work_order: frm.doc.name
            },
            callback(r){
                window.location.assign(r.message)
            }
        })
    },
    refresh(frm){
        cur_frm.set_value("skip_transfer",1)
    }
})