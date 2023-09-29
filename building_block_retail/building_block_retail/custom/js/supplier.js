frappe.ui.form.on("Supplier",{
    refresh:function(frm){
        console.log("SSSS")
        frappe.call({
            method: "building_block_retail.building_block_retail.custom.py.supplier.balance_purchase_receipt",
            args: {
                supplier:frm.doc.name
            },
            callback: function(r) { 
                if(r.message[0]["balance"]){
                    var bal=Math.round(r.message[0]["balance"])
                    let balance = `<p style="font-size:15px;font-weight:bold;">Balance Purchase Receipt Amount - ${fmt_money(bal)}</p>`;
                    frm.set_df_property('balance_purchase_receipt', 'options', balance); 

                }
               
            }
        });

    }

})