// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Order', {
	refresh: function(frm) {
        frm.set_query("item_template", function () {
            return {
                filters: {
                    has_variants:1
                }
            }
        })
	}
});