frappe.ui.form.on('Delivery Note Item', {
    ts_qty: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    conversion_factor: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    pieces: function(frm,cdt,cdn){
        bundle_calc(frm, cdt, cdn)
    },
    dont_include_in_loadman_cost: function(frm){
        if(frm.doc.work != "Supply and Laying")return
        calculate_loading_cost(frm)
    },
    qty: function(frm){
        if(frm.doc.work != "Supply and Laying")return
        calculate_loading_cost(frm)
    },
    items_remove: function(frm){
        if(frm.doc.work != "Supply and Laying")return
        calculate_loading_cost(frm)
    }
})


async function bundle_calc(frm, cdt, cdn){
    let row = locals[cdt][cdn]
    let uom=row.uom
    let conv1
    let conv2
    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
		let bundle_conv=1
		let other_conv=1;
		let nos_conv=1
		for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
			if(doc.uoms[doc_row].uom==uom){
				other_conv=doc.uoms[doc_row].conversion_factor
			}
			if(doc.uoms[doc_row].uom=='bundle'){
				bundle_conv=doc.uoms[doc_row].conversion_factor
			}
			if(doc.uoms[doc_row].uom=='Nos'){
				nos_conv=doc.uoms[doc_row].conversion_factor
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
    setup: function(frm){
        frm.set_query('employee', 'ts_loadman_info',function(frm){
            return {
                filters:{
                    'status':'Active',
                    'designation':'Loader',
                    'company':cur_frm.doc.company
                }
            }
        })
    },
	return_odometer_value: function(frm){
        var  total_distance= (cur_frm.doc.return_odometer_value - cur_frm.doc.current_odometer_value)
        cur_frm.set_value("total_distance",total_distance)
    },
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
                        let bundle_conv=1
                        let other_conv=1;
                        let nos_conv=1
                        for(let doc_row=0; doc_row<doc.uoms.length; doc_row++){
                            if(doc.uoms[doc_row].uom==uom){
                                other_conv=doc.uoms[doc_row].conversion_factor
                            }
                            if(doc.uoms[doc_row].uom=='bundle'){
                                bundle_conv=doc.uoms[doc_row].conversion_factor
                            }
                            if(doc.uoms[doc_row].uom=='Nos'){
                                nos_conv=doc.uoms[doc_row].conversion_factor
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
                    await frappe.model.set_value(cdt, cdn, 'pieces', Math.round((pieces_qty/conv2)+.5))
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
         
			setTimeout(() => {
				frm.remove_custom_button('Packing Slip', "Create");
				frm.remove_custom_button('Quality Inspection(s)', "Create");
				frm.remove_custom_button('E-Way Bill JSON', "Create");
				frm.remove_custom_button('Shipment', "Create");
				frm.remove_custom_button('Installation Note', "Create");
				frm.remove_custom_button('Delivery Trip', "Create");
				frm.remove_custom_button('Subscription', "Create");
			}, 500);    
    },
    work: function(frm){
        if(frm.doc.work === "Supply and Laying")return
        frm.clear_table('ts_loadman_info')
        cur_frm.refresh_field('ts_loadman_info')
        frm.set_value('ts_loadman_total_amount', 0)
        cur_frm.refresh_field('ts_loadman_total_amount')
    },
    ts_loadman_work: function(frm){
        if(frm.doc.work != "Supply and Laying")return
        calculate_loading_cost(frm)
    }
})


frappe.ui.form.on('TS Loadman Cost',{
    ts_loadman_info_add: function(frm, cdt, cdn){
        if(frm.doc.work === 'Supply and Laying' &&  !frm.doc.is_return)
        calculate_loading_cost(frm)
    },
    ts_loadman_info_remove: function(frm, cdt, cdn){
        if(frm.doc.work === 'Supply and Laying' &&  !frm.doc.is_return && frm.doc.ts_loadman_info.length)
        calculate_loading_cost(frm)
        else{
            cur_frm.set_value('ts_loadman_total_amount', 0)
            cur_frm.refresh_field('ts_loadman_total_amount')
        }
    },
    amount: function(frm){
        var loading_cost = 0
        for(var i = 0; i < frm.doc.ts_loadman_info.length; i++){
            loading_cost += frm.doc.ts_loadman_info[i].amount
        }
        cur_frm.set_value('ts_loadman_total_amount', loading_cost)
        cur_frm.refresh_field('ts_loadman_total_amount')
    }
})

function calculate_loading_cost(frm){
    var loading_cost = 0
    if(!frm.doc.ts_loadman_info.length)return
    frappe.call({
        method: "building_block_retail.building_block_retail.custom.py.delivery_note.get_item_loading_cost",
        args:{
            items: frm.doc.items,
            len:frm.doc.ts_loadman_info.length,
            work:frm.doc.ts_loadman_work
        },
        callback(r){
            for(var i = 0; i < frm.doc.ts_loadman_info.length; i++){
                frm.doc.ts_loadman_info[i]['amount'] = r.message;
                loading_cost += r.message
            }
            cur_frm.refresh_field('ts_loadman_info')
            cur_frm.set_value('ts_loadman_total_amount', loading_cost)
            cur_frm.refresh_field('ts_loadman_total_amount')
        }
    })
}
