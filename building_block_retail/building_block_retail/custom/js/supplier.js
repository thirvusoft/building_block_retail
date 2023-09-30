frappe.ui.form.on("Supplier",{
    refresh:function(frm){
        console.log("SSSS")
        frappe.call({
            method: "building_block_retail.building_block_retail.custom.py.supplier.balance_purchase_receipt",
            args: {
                supplier:frm.doc.name
            },
            callback: function(r) { 
                    var bal=r.message && r.message[0]?Math.round(r.message[0]["balance"] || 0):0
                    let balance = `<p style="font-size:15px;font-weight:bold;">Balance Purchase Receipt Amount - ${fmt_money(bal)}</p>`;
                    frm.dashboard.add_indicator(__('Purchase Receipt Bal: {0}',
					    [format_currency(bal)]),
				        bal ? 'orange' : 'green');                
            }
        });

    }

})