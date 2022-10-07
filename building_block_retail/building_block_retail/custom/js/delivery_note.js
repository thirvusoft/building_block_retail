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
    if(row.item_group.indexOf('Paver')>=0 || row.item_group.indexOf('paver')>=0 ){
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
    refresh:function(frm){
        let item_list=[]
        for(var i=0; i<frm.doc.items.length; i++){
            item_list.push(frm.doc.items[i].item_code)
        }
        frm.set_query("item","ts_loadman_info",function(frm){
            return {
                "filters": {
                    name:['in',item_list]             
                }
            }
        })

    },

   
    // ts_both_loading_unloading: function(frm) {
	// 	$.each(frm.doc.ts_loadman_info|| [], function(i, d) {
	// 		if((d.ts_both_loading_unloading==1)=frm.doc.lode_type);
	// 	});
	// 	refresh_field("ts_loadman_info");
	// },

    

	return_odometer_value: function(frm){
        var  total_distance= (cur_frm.doc.return_odometer_value - cur_frm.doc.current_odometer_value)
        cur_frm.set_value("total_distance",total_distance)
    },
     // Thirvu_dual_accoutning
     company:function(frm){
        if(frm.doc.company){
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.sales_order.branch_list",
            args:{
                company:frm.doc.company
            },
            callback: function(r){
               
            frm.set_query('branch',function(frm){
                return{
                    filters:{
                        'name':['in',r.message]
                    }
                }
            
            })
            }
        })}},
    taxes_and_charges: function(frm) {
        if(frm.doc.branch) {
            frappe.db.get_value("Branch", frm.doc.branch, "is_accounting").then( value => {
                if (!value.message.is_accounting) {
                    if(frm.doc.taxes_and_charges)
                        frm.set_value("taxes_and_charges", "")
                    if(frm.doc.tax_category)
                        frm.set_value("tax_category", "")
                        console.log("pppp")
                    if(frm.doc.taxes)
                        frm.clear_table("taxes")
                        refresh_field("taxes")
                }
            })
        }
    },
    tax_category: function(frm) {
        frm.trigger("taxes_and_charges")
    },
    branch: function (frm) {
        frm.trigger("taxes_and_charges")
    },
    validate: function(frm) {
        frm.trigger("taxes_and_charges")
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
            
                
               
                if(row.item_group.indexOf('Paver')>=0 || row.item_group.indexOf('paver')>=0){
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
    },
    ts_open_link: function(frm){
        if(!frm.doc.ts_map_link){
            cur_frm.scroll_to_field('ts_map_link')
            frappe.throw('Enter Google Map Link')
        }
        else{
        window.open(frm.doc.ts_map_link, '_blank')
        }
    }
})

frappe.ui.form.on('TS Loadman Cost',{
    item:function(frm, cdt, cdn){
        var row=locals[cdt][cdn]
        frappe.db.get_list("Item",{filters:{"item_code":row.item},fields:["loading_cost"]}).then(function(e){
                frappe.model.set_value(cdt, cdn, 'rate', e[0].loading_cost)
                if (row.type=="Both"){
                    frappe.model.set_value(cdt, cdn, 'rate', e[0].loading_cost*2)
                }
            })
            
    },
    type:function(frm, cdt, cdn){
        var row=locals[cdt][cdn]
        frappe.db.get_list("Item",{filters:{"item_code":row.item},fields:["loading_cost"]}).then(function(e){
                frappe.model.set_value(cdt, cdn, 'rate', e[0].loading_cost)
                if (row.type=="Both"){
                    frappe.model.set_value(cdt, cdn, 'rate', e[0].loading_cost*2)
                }
            })
    },
    qtypieces:function(frm, cdt, cdn){
        var row=locals[cdt][cdn]
        var amount= (row.qtypieces*row.rate)
        frappe.model.set_value(cdt, cdn, 'amount', amount )

    },
    rate:function(frm, cdt, cdn){
        var row=locals[cdt][cdn]
        var amount= (row.rate*row.qtypieces)
        frappe.model.set_value(cdt, cdn, 'amount', amount )

    },
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
    },
   


   
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
