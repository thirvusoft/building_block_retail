// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Shifting', {
	refresh: function(frm) {
		frm.set_query('warehouse', (frm)=>{
			return {
				filters:{
					company:cur_frm.doc.company
				}
			}
		})
		frm.set_query('item_code','items',function(frm){
			return {
				filters:{
					'is_sales_item':1,
					'parent_item_group':'Products',
					'has_variants':0
				}
			}
		})
		frm.set_query('item','ts_loadman_info',function(frm){
			return {
				filters:{
					'is_sales_item':1,
					'parent_item_group':'Products',
					'has_variants':0
				}
			}
		})
		frm.set_query('employee','ts_only_loadman',function(frm){
			return {
				filters:{
					'status':'Active'
				}
			}
		})
		frm.set_query('employee','ts_only_unloadman',function(frm){
			return {
				filters:{
					'status':'Active'
				}
			}
		})
		frm.set_query('employee','ts_loadman_info',function(frm){
			return {
				filters:{
					'status':'Active'
				}
			}
		})
	}
});


frappe.ui.form.on('Loading Employee',{
    employee:function(frm){
        split_loading_unloading_qty_evenly(frm)
    }  
})

frappe.ui.form.on('Unloading Employee',{
    employee: function(frm){
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
            if(!in_list(Object.keys(items), itm.item_code)){
                items[itm.item_code] = Math.round(itm.stock_qty)
            }
            else{
                items[itm.item_code] += Math.round(itm.stock_qty)
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
    frm.doc.ts_only_loadman.forEach(e => {
        if(!in_list(employee_list, e.employee) && e.employee){
        employee_list.push(e.employee)
        }
    })
    frm.doc.ts_only_unloadman.forEach(e => {
        if(!in_list(employee_list, e.employee) && e.employee){
            employee_list.push(e.employee)
            }
    })
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



