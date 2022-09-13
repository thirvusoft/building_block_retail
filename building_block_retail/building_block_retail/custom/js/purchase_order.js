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