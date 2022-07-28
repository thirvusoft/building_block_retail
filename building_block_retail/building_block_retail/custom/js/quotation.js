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
            frm.this.grid_buttons.find('.btn-custom').addClass('hidden');;
        }
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
    }
})