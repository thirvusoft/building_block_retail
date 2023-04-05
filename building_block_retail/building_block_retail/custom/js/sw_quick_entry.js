frappe.ui.form.ProjectQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
    render_dialog: async function() {
        this._super();
        this.doc.additional_cost=[{'description': 'Any Food Exp in Site'}, 
                            {'description': 'Other Labour Work'}, 
                            {'description': 'Site Advance'}]
    }
});

frappe.listview_settings['Project'] = {
    
	add_fields: ["status", "priority", "is_active", "percent_complete", "expected_end_date", "project_name"],
	filters:[["status","=", "Open"],['status','!=','In Quotation']],
	
	get_indicator: function(doc) {
		if(doc.status=="Open" && doc.percent_complete) {
			return [__("{0}%", [cint(doc.percent_complete)]), "orange", "percent_complete,>,0|status,=,Open"];
		} else {
			return [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
		}
	}
};
