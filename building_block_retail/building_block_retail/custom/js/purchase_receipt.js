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
        }
})