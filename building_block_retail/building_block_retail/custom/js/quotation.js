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
            frm.grid_buttons.find('.btn-custom').addClass('hidden');
        }
        frappe.call({
            method: "building_block_retail.building_block_retail.custom.py.quotation.get_permission_for_attachment",
            args:{user: frappe.session.user},
            callback(r){
                if(r.message){
                    // window.navigator.mediaDevices = true
                }
                else{
                    // window.navigator.mediaDevices = false
                }
            }
        })
    }
})

frappe.ui.form.on("Quotation", {
    refresh: function(frm){
        setTimeout(() => {
			frm.remove_custom_button('Subscription', "Create");
		}, 500);  
    },
    work: function(frm){
        if(frm.doc.work=="Supply Only"){
            frm.set_value('site_work','')
        }
        for(let row=0; row<(frm.doc.items?frm.doc.items.length:0);row++){
            frappe.model.set_value(frm.doc.items[row].doctype, frm.doc.items[row].name, 'work', frm.doc.work)
        }
    },
    rounding_adjustment: function(frm){
            cur_frm.set_value('rounded_total', (frm.doc.rounding_adjustment + frm.doc.grand_total))
            cur_frm.refresh()
    }
})