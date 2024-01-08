// Copyright (c) 2024, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Curing Chamber', {
	refresh: function (frm) {
		frm.set_query("finished_warehouse", "items", function() {
			return {
				filters: {
					is_group: 0
				}
			};
		});
		frm.set_query("scrap_warehouse", "items", function() {
			return {
				filters: {
					is_group: 0
				}
			};
		});
		frm.set_query("employee", "items", function() {
			return {
				filters: {
					status: "Active"
				}
			};
		});

		frm.fields_dict.items.grid.add_custom_button("Update Finished Warehouse", async function onclick() {
			let selected = frm.fields_dict.items.grid.get_selected_children();
			if (!selected || !selected.length) {
				frappe.show_alert({ "message": "Please select the rows", indicator: "red" })
				return
			}
			let dialog = new frappe.ui.Dialog({
				title: "Update Finished Warehouse",
				fields: [{
					fieldname: "warehouse",
					label: __("Warehouse"),
					fieldtype: "Link",
					options: "Warehouse",
					reqd: 1,
					get_query: function() {
						return {
							filters: {
								is_group: 0
							}
						};
					}
				}],
				primary_action_label: __('Update'),
				primary_action: (data) => {
					selected.forEach(r => {
						frappe.model.set_value(r.doctype, r.name, 'finished_warehouse', data.warehouse)
					});
					frappe.show_alert({message: 'Updated', indicator: 'green'});
					dialog.hide()
				}
			});
			dialog.show();
		}).removeClass('btn-default btn-custom').addClass('btn-secondary');

		frm.fields_dict.items.grid.add_custom_button("Update Scrap Warehouse", async function onclick() {
			let selected = frm.fields_dict.items.grid.get_selected_children();
			if (!selected || !selected.length) {
				frappe.show_alert({ "message": "Please select the rows", indicator: "red" })
				return
			}
			let dialog = new frappe.ui.Dialog({
				title: "Update Scrap Warehouse",
				fields: [{
					fieldname: "warehouse",
					label: __("Warehouse"),
					fieldtype: "Link",
					options: "Warehouse",
					reqd: 1,
					get_query: function() {
						return {
							filters: {
								is_group: 0
							}
						};
					}
				}],
				primary_action_label: __('Update'),
				primary_action: (data) => {
					selected.forEach(r => {
						frappe.model.set_value(r.doctype, r.name, 'scrap_warehouse', data.warehouse)
					});
					frappe.show_alert({message: 'Updated', indicator: 'green'});
					dialog.hide()
				}
			});
			dialog.show();
		}).removeClass('btn-default btn-custom').addClass('btn-secondary');
	},
	fetch_items: function (frm) {
		if ((frm.doc.items || []).length > 0) {
			frm.scroll_to_field("items");
			frappe.confirm(
				"The existing data in the items table will gets erased. Are you sure?",
				() => {
					frm.trigger("__fetch_items");
				}
			);
		} else {
			frm.trigger("__fetch_items");
		}
	},
	__fetch_items: async function (frm) {
		if (frm.is_new()) {
			await frm.save()
		}
		await frappe.call({
			method: "run_doc_method",
			args: { 'docs': frm.doc, 'method': "fetch_items" },
			freeze: true,
			freeze_message: 'Fetching...',
			callback: function (r) {
				if (!r.exc) {
					frm.refresh_fields();
					frm.refresh()
				}
			}
		});
	},
	complete_curing: async function (frm) {
		frappe.confirm(
			"Complete the curing process.",
			async () => {
				if (frm.is_new()) {
					await frm.save()
				}
				await frappe.call({
					method: "run_doc_method",
					args: { 'docs': frm.doc, 'method': "complete_curing" },
					freeze: true,
					freeze_message: 'Please Wait...',
					callback: function (r) {
						if (!r.exc) {
							frm.refresh_fields();
							frm.refresh()

							if (r["stock-entry"]) {
								frappe.set_route("Form", "Stock Entry", r["stock-entry"])
							}
						}
					}
				});
			}
		);
	}
});

frappe.ui.form.on("Curing Chamber Items", {
	to_bundle_qty: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		if ((data.to_bundle_qty || 0) > ((data.before_remaining_qty || 0) + (data.production_qty || 0) - (data.today_remaining_qty || 0))) {
			frappe.show_alert({
				message: "Incorrect value for <b>To bundle qty</b>.",
				indicator: "red"
			});
		}
		frm.trigger("__calc_damaged_qty", cdt, cdn);
	},
	today_remaining_qty: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		if ((data.today_remaining_qty || 0) > ((data.before_remaining_qty || 0) + (data.production_qty || 0) - (data.to_bundle_qty || 0))) {
			frappe.show_alert({
				message: "Incorrect value for <b>Today Remaining qty</b>",
				indicator: "red"
			});
		}
		frm.trigger("__calc_damaged_qty", cdt, cdn);
	},
	__calc_damaged_qty: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		let damage_qty = (data.before_remaining_qty || 0) + (data.production_qty || 0) - (data.to_bundle_qty || 0) - (data.today_remaining_qty || 0)
		frappe.model.set_value(cdt, cdn, 'damaged_qty', damage_qty);
	},
	split_item: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		let dialog = new frappe.ui.Dialog({
			title: "Split Qty",
			fields: [
				{
					fieldname: "item",
					label: "Item",
					fieldtype: "Link",
					options: "Item",
					read_only: 1,
					default: data.item
				},
				{
					label: "Qty",
					fieldtype: 'Section Break'
				},
				{
					fieldname: "before_remaining_qty",
					label: "Before Date Remaining Qty",
					fieldtype: "Float",
					read_only: 1,
					default: data.before_remaining_qty
				},
				{
					fieldname: "production_qty",
					label: "Production Qty",
					fieldtype: "Float",
					read_only: 1,
					default: data.production_qty
				},
				{
					label: "Qty to Split",
					fieldtype: "Column Break"
				},
				{
					fieldname: "split_before_remaining_qty",
					label: "Before Date Remaining Qty (To Split)",
					fieldtype: "Float",
				},
				{
					fieldname: "split_production_qty",
					label: "Production Qty (To Split)",
					fieldtype: "Float",
				},
			],
			primary_action_label: 'Split',
			primary_action: function (res) {
				if ((res.split_before_remaining_qty > data.before_remaining_qty) || (res.split_production_qty > res.production_qty)) {
					frappe.msgprint("Split qty must be less than actual qty");
					return;
				}
				let row = frm.fields_dict.items.grid.add_new_row(data.idx + 1);
				row.item = data.item
				row.employee = data.employee
				row.before_remaining_qty = res.split_before_remaining_qty
				row.production_qty = res.split_production_qty
				row.finished_warehouse = data.finished_warehouse
				row.scrap_warehouse = data.scrap_warehouse
				
				frappe.model.set_value(data.doctype, data.name, 'before_remaining_qty', (data.before_remaining_qty || 0) - (res.split_before_remaining_qty || 0))
				frappe.model.set_value(data.doctype, data.name, 'production_qty', (data.production_qty || 0) - (res.split_production_qty || 0))
				if (data.to_bundle_qty > ((data.before_remaining_qty || 0) + (data.production_qty || 0))) {
					frappe.model.set_value(data.doctype, data.name, 'to_bundle_qty', 0)
				}
				frm.fields_dict.items.grid.refresh();
				dialog.hide();
			}
		});
		dialog.show();
	}
});
