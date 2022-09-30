frappe.ui.form.on("Purchase Order", {
    onload: function(frm){
        setTimeout(() => {
			frm.remove_custom_button('Product Bundle', "Get Items From");
		}, 500);  
    },
    schedule_date: function(frm){
        frm.doc.items.forEach( (row)=>{
            row.schedule_date = frm.doc.schedule_date
        })
        frm.refresh()
    },
    taxes_and_charges: function(frm) {
        if(frm.doc.branch) {
            frappe.db.get_value("Branch", frm.doc.branch, "is_accounting").then( value => {
                if (!value.message.is_accounting) {
                    if(frm.doc.taxes_and_charges)
                        frm.set_value("taxes_and_charges", "")
                    if(frm.doc.tax_category)
                        frm.set_value("tax_category", "")
                    if(frm.doc.taxes)
                        frm.clear_table("taxes")
                        refresh_field("taxes")
                }
            })
        }
    },
    tax_category: function(frm) {
        frm.trigger("taxes_and_charges")
    },
    branch: function (frm) {
        frm.trigger("taxes_and_charges")
    },
    validate: function(frm) {
        frm.trigger("taxes_and_charges")
    },


    // thirvu_dual_accounting
    company:function(frm){
        if(frm.doc.company){
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.sales_order.branch_list",
            args:{
                company:frm.doc.company
            },
            callback: function(r){
               
            frm.set_query('branch',function(frm){
                return{
                    filters:{
                        'name':['in',r.message]
                    }
                }
            
            })
            }
        })}}
})