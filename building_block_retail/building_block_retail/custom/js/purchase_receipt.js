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

        // Thirvu_dual_Accounting
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