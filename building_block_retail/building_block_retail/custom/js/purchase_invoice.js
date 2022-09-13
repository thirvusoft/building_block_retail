frappe.ui.form.on("Purchase Invoice",{
    //  Thirvu_dual_Accounting
    company:function(frm){
  
        frappe.call({
            method:"thirvu_dual_accounting.thirvu_dual_accounting.custom.py.sales_order.branch_list",
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