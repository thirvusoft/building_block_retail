frappe.ui.form.on('BOM Operation', {
    workstation:function(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        if(row.workstation && row.workstation != ""){
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.bom.get_workstation_capacity",
                args:{
                    item:frm.doc.item,
                    workstation:row.workstation
                },
                callback(r){
                    frappe.model.set_value(cdt, cdn, 'workstation_capacity', r.message)
                }
            })
        }
        else{
            frappe.model.set_value(cdt, cdn, 'workstation_capacity', 0)
        }
    }
})