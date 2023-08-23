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
        if(frm.doc.work != "Supply and Laying" || frm.doc.work != "Laying Only")return
        calculate_loading_cost(frm)
        frm.trigger('refresh');
    },
    qty: function(frm){
        if(frm.doc.work != "Supply and Laying" || frm.doc.work != "Laying Only")return
        calculate_loading_cost(frm)
    },
    items_remove: function(frm){
        if(frm.doc.work != "Supply and Laying" || frm.doc.work != "Laying Only")return
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
        frm.set_query('employee', 'ts_only_loadman',function(frm){
            return {
                filters:{
                    'status':'Active',
                    'designation':'Loader',
                    'company':cur_frm.doc.company
                }
            }
        })
        frm.set_query('employee', 'ts_only_unloadman',function(frm){
            return {
                filters:{
                    'status':'Active',
                    'designation':'Loader',
                    'company':cur_frm.doc.company
                }
            }
        })
       
    },
    
    refresh: async function(frm){
        if(frm.doc.docstatus == 0){
            frm.doc.items.forEach( m => {
                frappe.model.set_value(m.doctype, m.name, 'work', frm.doc.work)
            })
        }
        let item_list=[];
        for(var i=0; i<frm.doc.items.length; i++){
            if(!frm.doc.items[i].dont_include_in_loadman_cost){
                var item=frm.doc.items[i].item_code
                const res = await frappe.db.get_value("Item", {"name": frm.doc.items[i].item_code}, "parent_item_group");    
                if(res.message.parent_item_group=="Products"){
                    item_list.push(frm.doc.items[i].item_code)
                    }      
            }          
        }
            frm.set_query("item","ts_loadman_info",function(frm){
            return {
                "filters": {
                    name:['in',item_list],   
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
            // return
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
                            let bundle_conv=0;
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
                        var bundle_qty = 0
                        if(conv1){
                        await frappe.model.set_value(cdt, cdn, 'ts_qty', parseInt(row.qty/conv1))
                        await frappe.model.set_value(cdt, cdn, 'pieces', 0)
                        bundle_qty=row.qty
                        }
                        let pieces_qty=parseInt(total_qty/conv1)?total_qty-bundle_qty:total_qty
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
                setTimeout(() => {
                    frm.trigger("calculate_again");
                }, 500);
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
        frm.doc.items.forEach( m => {
            frappe.model.set_value(m.doctype, m.name, 'work', frm.doc.work)
        })
        if(frm.doc.work === "Supply and Laying" || frm.doc.work === "Laying Only")return
        frm.clear_table('ts_loadman_info')
        cur_frm.refresh_field('ts_loadman_info')
        frm.set_value('ts_loadman_total_amount', 0)
        cur_frm.refresh_field('ts_loadman_total_amount')
    },
    ts_loadman_work: function(frm){
        if(frm.doc.work != "Supply and Laying" || frm.doc.work != "Laying Only")return
        calculate_loading_cost(frm)
        
        if(frm.doc.ts_loadman_work == 'Loading Only'){
            frm.doc.ts_loadman_info.forEach(d => {
                frappe.model.set_value(d.doctype, d.name, 'type', 'Loading')
            })
        }
        else if(frm.doc.ts_loadman_work == 'Unloading Only'){
            frm.doc.ts_loadman_info.forEach(d => {
                frappe.model.set_value(d.doctype, d.name, 'type', 'Unloading')
            })
        }
        frm.refresh()
    },
    ts_open_link: function(frm){
        if(!frm.doc.ts_map_link){
            cur_frm.scroll_to_field('ts_map_link')
            frappe.throw('Enter Google Map Link')
        }
        else{
        window.open(frm.doc.ts_map_link, '_blank')
        }
    },
    ts_only_loadman_remove: function(frm){
        split_loading_unloading_qty_evenly(frm)
    },
    ts_only_unloadman_remove: function(frm){
        split_loading_unloading_qty_evenly(frm)
    },
    calculate_again: function(frm){
        split_loading_unloading_qty_evenly(frm)
    },
    
})

frappe.ui.form.on('Loading Employee',{
    employee:function(frm){
        split_loading_unloading_qty_evenly(frm)
    }  
})
function get_employees_for_loadman(frm){
    var employees = {'Loading':[], 'Unloading':[], 'Both':[]}
    
    var load_emp = [], unload_emp = [], used_unload_emp = [];
    if(frm.doc.ts_only_loadman){
    frm.doc.ts_only_loadman.forEach(e => {
        if(e.employee){
        load_emp.push(e.employee)
        }
    })
    }
    if(frm.doc.ts_only_unloadman){
    frm.doc.ts_only_unloadman.forEach(e => {
        if(e.employee){
        unload_emp.push(e.employee)
        }
    })
    }
    load_emp.forEach(ld => {
        if(in_list(unload_emp, ld)){
            employees['Both'].push(ld)
            // used_unload_emp.push(ld)
        }
        // else{
            employees['Loading'].push(ld)
        // }
    })
    unload_emp.forEach(unld => {
        // if(!in_list(used_unload_emp, unld)){
            employees['Unloading'].push(unld)
        // }
    })
    return employees
}

function get_items_for_loading(frm){
    var items={}
    frm.doc.items.forEach(itm => {
        if(!itm.dont_include_in_loadman_cost){
            if(!in_list(Object.keys(items), itm.item_code)){
                items[itm.item_code] = Math.abs(Math.round(itm.stock_qty))
            }
            else{
                items[itm.item_code] += Math.abs(Math.round(itm.stock_qty))
            }
        }
    })
    return items
}
function split_loading_unloading_qty_evenly(frm){
    var qty_cost_conversion = {'Loading':1, 'Unloading':1, 'Both':2}
    var employees = get_employees_for_loadman(frm)
    var items = get_items_for_loading(frm)
    var types = Object.keys(qty_cost_conversion)
    var loading_table = [], final_table = [];
    var loading_costs = {}, total_costs = 0;
    frm.doc.items.forEach(it=>{
        loading_costs[it.item_code] = it.loading_cost?it.loading_cost:0
    })
    types.forEach(typ => {
        if(typ != 'Both'){
        employees[typ].forEach(emp => {
            Object.keys(items).forEach(itm => {
                loading_table.push({'employee':emp, 'type':typ, 'item':itm, 'qtypieces':items[itm]*(qty_cost_conversion[typ]/employees[typ].length)})
            })
        })
    }
    })
    var employee_list=[];
    if(frm.doc.ts_only_loadman){
    frm.doc.ts_only_loadman.forEach(e => {
        if(!in_list(employee_list, e.employee) && e.employee){
        employee_list.push(e.employee)
        }
    })
    }
    if(frm.doc.ts_only_unloadman){
    frm.doc.ts_only_unloadman.forEach(e => {
        if(!in_list(employee_list, e.employee) && e.employee){
            employee_list.push(e.employee)
            }
    })
    }
    employee_list.forEach(emp => {
        Object.keys(items).forEach(itm => {
    
        
            var row = {'employee':emp, 'item':itm, 'qtypieces':0}
            var load_type = []
            loading_table.forEach(lt => {
                if(lt.employee == emp && lt.item == itm){
                    row.qtypieces += lt.qtypieces
                    load_type.push(lt.type)
                }
            })
            if(in_list(load_type, 'Loading') && in_list(load_type, 'Unloading')){
                row.type = 'Both'
            }
            else{
                row.type = load_type[0]
            }
            row.qtypieces = Math.round(row.qtypieces)
            row.rate = loading_costs[row.item]
            row.amount = row.rate*row.qtypieces
            total_costs += row.amount
            final_table.push(row)
        })
    })

    frm.set_value('ts_loadman_info', final_table)
    frm.set_value('ts_loadman_total_amount', total_costs)
    frm.refresh_field('ts_loadman_info')
    frm.refresh_field('ts_loadman_total_amount')
}


frappe.ui.form.on('Unloading Employee',{
    employee: function(frm){
        split_loading_unloading_qty_evenly(frm)
    }  
})
frappe.ui.form.on('TS Loadman Cost', {
    rate: function(frm, cdt, cdn){
    var row = locals[cdt][cdn]
    frappe.model.set_value(cdt, cdn, 'amount', row.rate*row.qtypieces)
    },
    qtypieces: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'amount', row.rate*row.qtypieces) 
    }
})


function calculate_loading_cost(frm){
    return
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
