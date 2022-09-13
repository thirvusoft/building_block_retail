frappe.ui.form.on("Purchase Receipt" ,{
    onload:function(frm){
        frm.set_query('transporter', function(frm){
                    return {
                        filters:{
                            'supplier_name': 'Own Transporter'
                        }
                    }
                });
        // To ignore price list while changing conversion factor
        frappe.flags.dont_fetch_price_list_rate = true
        },

        // Thirvu_dual_Accounting
        company:function(frm){
    
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
            })}
})