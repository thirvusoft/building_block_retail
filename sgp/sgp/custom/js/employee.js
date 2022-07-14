frappe.ui.form.on("Employee", {
    setup: function(frm) {
        
		frm.set_query('contracter_expense_account', function(doc) {
            if(!doc.company){
                frappe.throw("Select the company")
            }
			return {
				filters: {
					"is_group": 0,
					"company": doc.company
				}
			};
		});
	},
});