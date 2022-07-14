frappe.ui.form.on('Delivery Note Item', {
    ts_qty: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    conversion_factor: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    pieces: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    }
})


async function bundle_calc(frm, cdt, cdn){
    let row = locals[cdt][cdn]
    let uom=row.uom
    let conv1
    let conv2
    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
        let bundle_conv=doc.bundle_per_sqr_ft?doc.bundle_per_sqr_ft:1;
        let other_conv=1;
        let nos_conv=doc.pavers_per_sqft?1/doc.pavers_per_sqft:1;
        for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
            if(doc.uoms[doc_row].uom==uom){
                other_conv=doc.uoms[doc_row].conversion_factor
            }
        }
        conv1=bundle_conv/other_conv
        conv2=nos_conv/other_conv
    })

    if(row.item_group=='Pavers'){
        frappe.model.set_value(cdt, cdn, 'qty', row.ts_qty*conv1 + row.pieces*conv2)
        let rate=row.rate
        frappe.model.set_value(cdt, cdn, 'rate', 0)
        frappe.model.set_value(cdt, cdn, 'rate', rate)
    }
    
}



frappe.ui.form.on('Delivery Note', {
    onload:async function(frm){
        if(cur_frm.is_new() ){
            for(let ind=0;ind<cur_frm.doc.items.length;ind++){
                let cdt=cur_frm.doc.items[ind].doctype
                let cdn=cur_frm.doc.items[ind].name
                let row=locals[cdt][cdn]
                let uom=row.uom
                let conv1
                let conv2
                if(row.item_code)
                {
                    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
                        let bundle_conv=doc.bundle_per_sqr_ft?doc.bundle_per_sqr_ft:1;
                        let other_conv=1;
                        let nos_conv=doc.pavers_per_sqft?1/doc.pavers_per_sqft:1;
                        for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
                            if(doc.uoms[doc_row].uom==uom){
                                other_conv=doc.uoms[doc_row].conversion_factor
                            }
                        }
                        conv1=bundle_conv/other_conv
                        conv2=nos_conv/other_conv
                    })
            
                
               
                if(row.item_group=='Pavers'){
                    let total_qty=row.qty
                    await frappe.model.set_value(cdt, cdn, 'ts_qty', parseInt(row.qty/conv1))
                    await frappe.model.set_value(cdt, cdn, 'pieces', 0)
                    let bundle_qty=row.qty
                    let pieces_qty=total_qty-bundle_qty
                    await frappe.model.set_value(cdt, cdn, 'pieces', pieces_qty/conv2)
                    let rate=row.rate
                    frappe.model.set_value(cdt, cdn, 'rate', 0)
                    frappe.model.set_value(cdt, cdn, 'rate', rate)
                }    
                }
            }
            let items = cur_frm.doc.items || [];
            let len = items.length;
            while (len--)
            {
                if(items[len].qty == 0)
                {
                    await cur_frm.get_field("items").grid.grid_rows[len].remove();
                }
            }
            cur_frm.refresh();
            
            
            }
            
    },
	refresh: function(frm) {
        frm.add_custom_button(__('Work Order'), function(){
            frappe.call({
				method: 'sgp.sgp.custom.py.delivery_note.get_work_order_items',
				args:{
					self:frm.doc,
				},
				callback: function(r) {
					if(!r.message) {
						frappe.msgprint({
							title: __('Work Order not created'),
							message: __('No Items with Bill of Materials to Manufacture'),
							indicator: 'orange'
						});
						return;
					}
					else if(!r.message) {
						frappe.msgprint({
							title: __('Work Order not created'),
							message: __('Work Order already created for all items with BOM'),
							indicator: 'orange'
						});
						return;
					} else {
						const fields = [{
							label: 'Items',
							fieldtype: 'Table',
							fieldname: 'items',
							description: __('Select BOM and Qty for Production \nSelect the item check box and then Create '),
							fields: [{
								fieldtype: 'Read Only',
								fieldname: 'item_code',
								label: __('Item Code'),
								in_list_view: 1
							}, {
								fieldtype: 'Link',
								fieldname: 'bom',
								options: 'BOM',
								reqd: 1,
								label: __('Select BOM'),
								in_list_view: 1,
								get_query: function (doc) {
									return { filters: { item: doc.item_code } };
								}
							}, {
								fieldtype: 'Float',
								fieldname: 'pending_qty',
								reqd: 1,
								label: __('Qty'),
								in_list_view: 1
							}, {
								fieldtype: 'Data',
								fieldname: 'sales_order_item',
								reqd: 1,
								label: __('Sales Order Item'),
								hidden: 1
							}],
							data: r.message,
							get_data: () => {
								return r.message
							}
						}]
						var d = new frappe.ui.Dialog({
							title: __('Select Items to Manufacture'),
							fields: fields,
							primary_action: function() {
								var data = {items: d.fields_dict.items.grid.get_selected_children()};
								frappe.call({
									method: 'sgp.sgp.custom.py.delivery_note.make_work_orders',
									args: {
										items: data,
										company: frm.doc.company,
										delivery_note: frm.docname,
										project: frm.project
									},
									freeze: true,
									callback: function(r) {
										if(r.message) {
											frappe.msgprint({
												message: __('Work Orders Created: {0}', [r.message.map(function(d) {
														return repl('<a href="/app/work-order/%(name)s">%(name)s</a>', {name:d})
													}).join(', ')]),
												indicator: 'green'
											})
										}
										d.hide();
									}
								});
							},
							primary_action_label: __('Create')
						});
						d.show();
					}
				}
			});
        },"Create");
	}
})