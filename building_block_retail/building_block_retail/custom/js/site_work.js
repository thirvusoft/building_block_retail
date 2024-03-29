function setquery(frm,cdt,cdn){
	frm.set_query("item", "item_details", function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
	return {
		filters: {
			'item_group': cur_frm.doc.project_type,
			'has_variants': 0
		}
	}
});
	frm.set_query("item", "item_details_compound_wall", function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
	return {
		filters: {
			'item_group': cur_frm.doc.project_type,
			'has_variants': 0
		}
	}
});
}

var update_value=true

function calc_er_cost(frm){
	var er_cost_sqft = frm.doc.er_cost_sqft?frm.doc.er_cost_sqft:0
	frm.set_value('er_total_sqft', frm.doc.total_completed_area)
	frm.set_value('er_total_amount', frm.doc.er_cost_sqft * frm.doc.er_total_sqft)
	frm.refresh()
}

frappe.ui.form.on("Project",{
	er_employee: function(frm){
		calc_er_cost(frm)
	},
	total_completed_area: function(frm){
		calc_er_cost(frm)
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
    project_type:function(frm,cdt,cdn){
        setquery(frm,cdt,cdn)
    },
    status: function(frm){
		if(frm.doc.status == 'Completed')
		calc_er_cost(frm)
	},
    refresh:function(frm,cdt,cdn){
        if(!cur_frm.is_new()){
            cur_frm.set_df_property('is_multi_customer', 'read_only', 1)
            cur_frm.set_df_property('customer_name', 'read_only', 1)
            cur_frm.set_df_property('customer', 'read_only', 1)
        }
		cur_frm.remove_custom_button('Duplicate Project with Tasks')
		cur_frm.remove_custom_button('Kanban Board')
		cur_frm.remove_custom_button('Gantt Chart')
        setquery(frm,cdt,cdn)

		let sw_items=[];
		for(let item=0;item<(frm.doc.item_details?frm.doc.item_details.length:0);item++){
			if(!(sw_items.includes(frm.doc.item_details[item].item))){
				sw_items.push(frm.doc.item_details[item].item)
			}
		}
		for(let item=0;item<(frm.doc.item_details_compound_wall?frm.doc.item_details_compound_wall.length:0);item++){
			if(!(sw_items.includes(frm.doc.item_details_compound_wall[item].item))){
				sw_items.push(frm.doc.item_details_compound_wall[item].item)
			}
		}
		frm.set_query('item','job_worker', function(frm){
			return {
				filters:[
					['item_code' ,'in', sw_items]
				]
			}
		})

        frm.set_query('name1','job_worker',function(frm){
            return{
                filters:
					{
						'designation': 'Job Worker'
					}
			}
        })
		frm.set_query('item','finalised_job_worker_details', function(frm){
			return {
				filters:[
					['item_code' ,'in', sw_items]
				]
			}
		})

        frm.set_query('name1','finalised_job_worker_details',function(frm){
            return{
                filters:
					{
						'designation': 'Job Worker'
					}
			}
        })
        frm.set_query('supervisor', function(frm){
            return {
                filters:{
                    'designation': 'Supervisor'
                }
            }
        });
        
		customer_query()
    },
    is_multi_customer:function(frm){
        if(cur_frm.doc.is_multi_customer){
            cur_frm.set_df_property('customer','reqd',0)
            cur_frm.set_df_property('customer','hidden',1)
            cur_frm.set_df_property('customer_name','hidden',0)
        }
        else{
            cur_frm.set_df_property('customer','reqd',1)
            cur_frm.set_df_property('customer','hidden',0)
            cur_frm.set_df_property('customer_name','hidden',1)
        }	
    },
    onload:function(frm){
	let  additional_cost=cur_frm.doc.additional_cost?cur_frm.doc.additional_cost:[]
	 if(additional_cost.length==0 && cur_frm.is_new()){
	
		let add_on_cost=["Any Food Exp in Site","Other Labour Work","Site Advance"]
			for(let row=0;row<add_on_cost.length;row++){
			
			var new_row = frm.add_child("additional_cost");
			new_row.description=add_on_cost[row]
			}
				refresh_field("additional_cost");
		}
}
})

function percent_complete(frm,cdt,cdn){ 
	let total_area=0;
	let total_bundle = 0;
	let paver= cur_frm.doc.item_details?cur_frm.doc.item_details:[]
	for(let row=0;row<paver.length;row++){
		total_area+= cur_frm.doc.item_details[row].required_area
		total_bundle += cur_frm.doc.item_details[row].number_of_bundle
	        }
	let completed_area=0;
	let total_comp_bundle = 0;
	let work= cur_frm.doc.job_worker?cur_frm.doc.job_worker:[]
	for(let row=0;row<work.length;row++){
		completed_area+= cur_frm.doc.job_worker[row].sqft_allocated
		total_comp_bundle += cur_frm.doc.job_worker[row].completed_bundle
	}
	let percent=(total_comp_bundle/total_bundle)*100
	frm.set_value('total_required_area',total_area)
	frm.set_value('total_completed_area',completed_area)
	frm.set_value('er_total_sqft', completed_area?completed_area:0)
	var er_cost = frm.doc.er_cost_sqft?frm.doc.er_cost_sqft:0
	frm.set_value('er_total_amount', completed_area * er_cost)
	frm.set_value('total_required_bundle',total_bundle)
	frm.set_value('total_completed_bundle',total_comp_bundle)
	frm.set_value('completed',percent)
}


frappe.ui.form.on("Item Detail Pavers", {
	item : function(frm,cdt,cdn) {
		let data = locals[cdt][cdn]
		let item_code = data.item
		if (item_code){
			frappe.call({
				method:"building_block_retail.building_block_retail.custom.py.site_work.item_details_fetching_pavers",
				args:{item_code},
				callback(r)
				{
					frappe.model.set_value(cdt,cdn,"area_per_bundle",r['message'][0]?parseFloat(r["message"][0]):0)
					frappe.model.set_value(cdt,cdn,"rate",r["message"][1]?parseFloat(r["message"][1]):0)
					frappe.model.set_value(cdt,cdn,"pieces_per_bundle",r["message"][2]?parseFloat(r["message"][2]):0)
					frappe.model.set_value(cdt,cdn,"pcs_per_sqft",r["message"][3]?parseFloat(r["message"][3]):0)
				}
			})
		}
	},
	required_area : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let bundle = data.area_per_bundle?data.required_area / data.area_per_bundle :0
			let no_of_bundle = Math.ceil(bundle)
			frappe.model.set_value(cdt,cdn,"number_of_bundle",bundle?bundle:0)
			frappe.model.set_value(cdt,cdn,"req_pcs",Math.ceil(data.required_area*data.pcs_per_sqft))
			frappe.model.set_value(cdt,cdn,"allocated_paver_area",data.required_area)
	},
	number_of_bundle : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let allocated_paver = data.number_of_bundle * data.area_per_bundle
			frappe.model.set_value(cdt,cdn,"allocated_paver_area",allocated_paver?allocated_paver:data.required_area)
	},
	allocated_paver_area :function(frm,cdt,cdn) {
			
			let data = locals[cdt][cdn]
			let allocated_paver = data.allocated_paver_area
			let tot_amount = data.rate * allocated_paver
			frappe.model.set_value(cdt,cdn,"amount",tot_amount?tot_amount:0)
			get_possible_delivery_date(frm, data)
			
	},
	rate : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let rate = data.rate
			let tot_amount = rate * data.allocated_paver_area
			frappe.model.set_value(cdt,cdn,"amount",tot_amount?tot_amount:0)
	},
	req_pcs: function(frm, cdt, cdn){
		var row = locals[cdt][cdn]
		frappe.model.set_value(cdt, cdn, 'required_area', row.req_pcs/row.pcs_per_sqft)
	}  
})




frappe.ui.form.on("Pavers", {
	item : function(frm,cdt,cdn) {
		let data = locals[cdt][cdn]
		let item_code = data.item
		if (item_code){
			frappe.call({
				method:"building_block_retail.building_block_retail.custom.py.site_work.item_details_fetching_pavers",
				args:{item_code},
				callback(r)
				{
					frappe.model.set_value(cdt,cdn,"area_per_bundle",r['message'][0]?parseFloat(r["message"][0]):0)
					frappe.model.set_value(cdt,cdn,"rate",r["message"][1]?parseFloat(r["message"][1]):0)
				}
			})
		}
	},
	required_area : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let bundle = data.area_per_bundle?data.required_area / data.area_per_bundle :0
			let no_of_bundle = Math.ceil(bundle)
			frappe.model.set_value(cdt,cdn,"number_of_bundle",no_of_bundle?no_of_bundle:0)
			
			
	},
	number_of_bundle : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let allocated_paver = data.number_of_bundle * data.area_per_bundle
			frappe.model.set_value(cdt,cdn,"allocated_paver_area",allocated_paver?allocated_paver:0)
	},
	allocated_paver_area :function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let allocated_paver = data.allocated_paver_area
			let tot_amount = data.rate * allocated_paver
			frappe.model.set_value(cdt,cdn,"amount",tot_amount?tot_amount:0)
	},
	rate : function(frm,cdt,cdn) {
			let data = locals[cdt][cdn]
			let rate = data.rate
			let tot_amount = rate * data.allocated_paver_area
			frappe.model.set_value(cdt,cdn,"amount",tot_amount?tot_amount:0)
	}  
})




function completed_bundle_calc(frm,cdt,cdn){
	let data = locals[cdt][cdn]
	let bundle = data.completed_bundle
	var item_bundle_per_sqft
	let allocated_sqft
	var item = data.item
	if(bundle && item){
		frappe.db.get_doc('Item',item).then(value => {
			item_bundle_per_sqft = value.bundle_per_sqr_ft
			allocated_sqft = bundle * item_bundle_per_sqft
			frappe.model.set_value(cdt,cdn,"sqft_allocated",allocated_sqft?allocated_sqft:0)
		})
	}
}

frappe.ui.form.on('Finalised Job Worker Details',{
	rate: function(frm, cdt, cdn){
		amount(frm, cdt, cdn)
	},
	completed_bundle: function(frm,cdt,cdn){
		// completed_bundle_calc(frm,cdt,cdn)
		var row = locals[cdt][cdn]
		
		if (update_value==true){
			frappe.model.set_value(cdt, cdn, 'sqft_allocated', row.completed_bundle*row.area_per_bundle)
			frappe.model.set_value(cdt, cdn, 'completed_pieces', row.completed_bundle*row.pieces_per_bundle)
		}
		

	},
	completed_pieces: function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		
		if (update_value==true){
		frappe.model.set_value(cdt, cdn, 'sqft_allocated', row.completed_pieces/row.pcs_per_sqft)
		}
		// frappe.model.set_value(cdt, cdn, 'completed_bundle', row.completed_pieces*row.pcs_per_sqft)

	},
	item:function(frm,cdt,cdn){
		completed_bundle_calc(frm,cdt,cdn)
		let row = locals[cdt][cdn]
		if(row.item){
			frappe.db.get_value('Item', row.item, 'laying_cost').then( (data)=>{
				frappe.model.set_value(cdt, cdn, 'rate', data.message.laying_cost)
			})
			}
		let item_code = row.item
		if (item_code){
			frappe.call({
				method:"building_block_retail.building_block_retail.custom.py.site_work.item_details_fetching_pavers",
				args:{item_code},
				callback(r)
				{
					frappe.model.set_value(cdt,cdn,"area_per_bundle",r['message'][0]?parseFloat(r["message"][0]):0)
					// frappe.model.set_value(cdt,cdn,"rate",r["message"][1]?parseFloat(r["message"][1]):0)
					frappe.model.set_value(cdt,cdn,"pieces_per_bundle",r["message"][2]?parseFloat(r["message"][2]):0)
					frappe.model.set_value(cdt,cdn,"pcs_per_sqft",r["message"][3]?parseFloat(r["message"][3]):0)
				}
			})
		}
	},
	sqft_allocated:async function(frm, cdt, cdn){
		var row = locals[cdt][cdn]
		percent_complete(frm, cdt, cdn)
		amount(frm, cdt, cdn)
		if (update_value==true){
			update_value=false;
			if(row.area_per_bundle){
				await frappe.model.set_value(cdt, cdn, 'completed_bundle', row.sqft_allocated/row.area_per_bundle)
		
			}
			else{
				await frappe.model.set_value(cdt, cdn, 'completed_bundle', 0)
			}
			
			await frappe.model.set_value(cdt, cdn, 'completed_pieces', row.sqft_allocated*row.pcs_per_sqft)
			
		update_value=true;
	}
	
	

	},
	job_worker_add: function(frm, cdt, cdn){
		let work= cur_frm.doc.job_worker?cur_frm.doc.job_worker:[]
		var name
		var start_date
		let rate
		var date
		for(let row=0;row<work.length;row++){
			if(row){
				name = cur_frm.doc.job_worker[row-1].name1
				start_date = cur_frm.doc.job_worker[row-1].end_date?cur_frm.doc.job_worker[row-1].end_date:cur_frm.doc.job_worker[row-1].start_date
				rate = cur_frm.doc.job_worker[row-1].rate
				date = frappe.datetime.add_days(start_date,1)
			}
			else{
				date = start_date
			}
		}
		frappe.model.set_value(cdt,cdn,"name1",name)
		frappe.model.set_value(cdt,cdn,"start_date",date)
		frappe.model.set_value(cdt,cdn,"end_date",date)
		frappe.model.set_value(cdt,cdn,"rate",rate)
	},
})

frappe.ui.form.on('TS Job Worker Details',{
	rate: function(frm, cdt, cdn){
		amount(frm, cdt, cdn)
	},
	completed_bundle: function(frm,cdt,cdn){
		completed_bundle_calc(frm,cdt,cdn)
		var row = locals[cdt][cdn]
		if (update_value==true){
		frappe.model.set_value(cdt, cdn, 'sqft_allocated', row.completed_bundle*row.area_per_bundle)
		frappe.model.set_value(cdt, cdn, 'completed_pieces', row.completed_bundle*row.pieces_per_bundle)
		}
	},
	completed_pieces: function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		if (update_value==true){
		frappe.model.set_value(cdt, cdn, 'sqft_allocated', row.completed_pieces/row.pcs_per_sqft)
		// frappe.model.set_value(cdt, cdn, 'completed_bundle', row.completed_pieces*row.pcs_per_sqft)
		}
	},
	item:function(frm,cdt,cdn){
		completed_bundle_calc(frm,cdt,cdn)
		let row = locals[cdt][cdn]
		if(row.item){
			frappe.db.get_value('Item', row.item, 'laying_cost').then( (data)=>{
				frappe.model.set_value(cdt, cdn, 'rate', data.message.laying_cost)
			})
			}
		let item_code = row.item
		if (item_code){
			frappe.call({
				method:"building_block_retail.building_block_retail.custom.py.site_work.item_details_fetching_pavers",
				args:{item_code},
				callback(r)
				{
					frappe.model.set_value(cdt,cdn,"area_per_bundle",r['message'][0]?parseFloat(r["message"][0]):0)
					// frappe.model.set_value(cdt,cdn,"rate",r["message"][1]?parseFloat(r["message"][1]):0)
					frappe.model.set_value(cdt,cdn,"pieces_per_bundle",r["message"][2]?parseFloat(r["message"][2]):0)
					frappe.model.set_value(cdt,cdn,"pcs_per_sqft",r["message"][3]?parseFloat(r["message"][3]):0)
				}
			})
		}
	},
	sqft_allocated: async function(frm, cdt, cdn){
		var row = locals[cdt][cdn]
		percent_complete(frm, cdt, cdn)
		amount(frm, cdt, cdn)
		if (update_value==true){
			update_value=false;
		if(row.area_per_bundle){
			await frappe.model.set_value(cdt, cdn, 'completed_bundle', row.sqft_allocated/row.area_per_bundle)
		}
		else{
			await frappe.model.set_value(cdt, cdn, 'completed_bundle', 0)
		}
		
		await frappe.model.set_value(cdt, cdn, 'completed_pieces', row.sqft_allocated*row.pcs_per_sqft)
	
		update_value=true;
	}

	},
	job_worker_add: function(frm, cdt, cdn){
		let work= cur_frm.doc.job_worker?cur_frm.doc.job_worker:[]
		var name
		var start_date
		let rate
		var date
		for(let row=0;row<work.length;row++){
			if(row){
				name = cur_frm.doc.job_worker[row-1].name1
				start_date = cur_frm.doc.job_worker[row-1].end_date?cur_frm.doc.job_worker[row-1].end_date:cur_frm.doc.job_worker[row-1].start_date
				rate = cur_frm.doc.job_worker[row-1].rate
				date = frappe.datetime.add_days(start_date,1)
			}
			else{
				date = start_date
			}
		}
		frappe.model.set_value(cdt,cdn,"name1",name)
		frappe.model.set_value(cdt,cdn,"start_date",date)
		frappe.model.set_value(cdt,cdn,"end_date",date)
		frappe.model.set_value(cdt,cdn,"rate",rate)
	},
})


function amount(frm,cdt,cdn){
	let row=locals[cdt][cdn]
	if(row.rate && row.sqft_allocated){
		frappe.model.set_value(cdt, cdn, 'amount', row.rate*row.sqft_allocated)
	}
	else{
		frappe.model.set_value(cdt, cdn, 'amount', 0)
	}
}



frappe.ui.form.on('Raw Materials',{
    item: function(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        if(row.item){
            frappe.db.get_doc('Item',row.item).then((item)=>{
                frappe.call({
                    method: "building_block_retail.building_block_retail.custom.py.sales_order.get_item_rate",
                    args:{
                        item: row.item
                    },
                    callback: async function(r){
                       await frappe.model.set_value(cdt,cdn,'rate', r.message?r.message:0);
                    }
                })
                frappe.model.set_value(cdt,cdn,'uom', item.stock_uom);
            })
        }
    },
    rate: function(frm,cdt,cdn){
        amount_rawmet(frm,cdt,cdn)
    },
    qty: function(frm,cdt,cdn){
        amount_rawmet(frm,cdt,cdn)
    }
})


function amount_rawmet(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount', (row.rate?row.rate:0)*(row.qty?row.qty:0))
}


function customer_query(){
	let frm=cur_frm;
	let customer_list = []
	for(let row=0; row<frm.doc.customer_name.length; row++){
		if(!(customer_list.includes(frm.doc.customer_name[row].customer))){
			customer_list.push(frm.doc.customer_name[row].customer)
		}
	}
	frm.set_query('customer', 'additional_cost', function(){
		return {
			filters: {
				name: ['in', customer_list]
			}
		}
	})
}
frappe.realtime.on('show_poss_del_date_error', (item)=>{
	frappe.show_alert({'message':`Enter Daily maximum production qty in Item <b>${item}</b>`,'indicator':'red'}) 
})
var get_possible_delivery_date = function(frm, row){
    var child = frm.doc.possible_delivery_dates || []
	var child_items = []
	child.forEach((a)=>{
		child_items.push(a.item)
	})
	
        if(row.item && row.req_pcs){
            frappe.call({
                method: 'building_block_retail.building_block_retail.report.get_possible_delivery_date_of_item.get_possible_delivery_date_of_item.get_data',
                args:{
                    filters:{'item_code':row.item, 'order_qty':row.req_pcs},
                    call_from_report : 0
                },
                callback(r){
					if(!child_items.includes(row.item)){
						child_items.push(row.item)
						var new_child = frm.add_child("possible_delivery_dates")
						new_child.item = row.item
						new_child.possible_delivery_date = r.message
						frm.refresh_field('possible_delivery_dates')
					}
					else{
						frm.doc.possible_delivery_dates.forEach((a)=>{
							if(a.item == row.item){
								frappe.model.set_value(a.doctype, a.name, "possible_delivery_date", r.message)
								frm.refresh_field('possible_delivery_dates')
							}
						})
					}
                }
            })
        }
}