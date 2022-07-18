frappe.ui.form.on("Journal Receipt", {
    setup: function(frm) {
        
		frm.set_query('account', function(doc) {
            if(!doc.company_name){
                frappe.throw("Kindly Select The Company")
            }
			return {
				filters: {
					"is_group": 0,
					"company": doc.company_name,
					"parent_account": ["in",[`Cash In Hand - ${frm.doc.abbr}`,`Bank Accounts - ${frm.doc.abbr}`]]
				}
			};
		});
	},

});

// frappe.ui.form.on('Journal Receipt', {
//     company_name: function(frm) {
//         if(company_name)
//         frappe.call({
// 			method: "sgp.sgp.doctype.journal_receipt.journal_receipt.abbrivation",
// 			args: {
// 				'self': frm.doc
// 			},
			
// 		})}
        
 

//     });