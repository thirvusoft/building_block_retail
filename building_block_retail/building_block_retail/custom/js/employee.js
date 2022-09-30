frappe.ui.form.on("Employee", {
    refresh: function(frm) {
        
		frm.set_query('contracter_expense_account', function(doc) {
            if(!doc.company){
                frappe.throw("Select the company")
            }
			if(frm.doc.__islocal){frappe.throw("Please save this employee and fill this Account.")}
			return {
				filters: {
					"is_group": 0,
					"company": doc.company,
				}
			};
		});
	},
});