frappe.ui.form.on('Quotation', {
    setup:function(frm){
        frm.set_query("supervisor", function() {
            return {
                filters: {"Designation":"Supervisor"}
            }
        })
    },
    refresh:function(frm){
        if(frm.doc.workflow_state == "Rejected" ){
            frm.grid_buttons.find('.btn-custom').addClass('hidden');
        }
        frappe.call({
            method: "building_block_retail.building_block_retail.custom.py.quotation.get_permission_for_attachment",
            args:{user: frappe.session.user},
            callback(r){
                if(r.message){
                    // window.navigator.mediaDevices = true
                }
                else{
                    // window.navigator.mediaDevices = false
                }
            }
        })
    }
})

frappe.ui.form.on("Quotation", {
    refresh: function(frm){
        setquery(frm)
        setTimeout(() => {
			frm.remove_custom_button('Subscription', "Create");
		}, 500);  
        cur_frm.set_df_property('items','reqd',0);
        cur_frm.set_df_property('items','hidden',1);
    },
    work: function(frm){
        if(frm.doc.work=="Supply Only"){
            frm.set_value('site_work','')
        }
        for(let row=0; row<(frm.doc.items?frm.doc.items.length:0);row++){
            frappe.model.set_value(frm.doc.items[row].doctype, frm.doc.items[row].name, 'work', frm.doc.work)
        }
    },
    validate(frm){
        frm.doc.pavers.forEach(d=>{
            frappe.model.set_value(d.doctype, d.name, 'work', frm.doc.work)
        })
    },
    rounding_adjustment: function(frm){
            cur_frm.set_value('rounded_total', (frm.doc.rounding_adjustment + frm.doc.grand_total))
            cur_frm.refresh()
    },
    type(frm){
        setquery(frm)
    },
    work: function(frm){
        if(frm.doc.work=="Supply Only"){
            frm.set_value('site_work','')
        }
        for(let row=0; row<(frm.doc.pavers?frm.doc.pavers.length:0);row++){
            frappe.model.set_value(frm.doc.pavers[row].doctype, frm.doc.pavers[row].name, 'work', frm.doc.work)
        }
    },
    async before_save(frm){
        frm.clear_table("items");
        if(cur_frm.doc.type=='Pavers'){
            cur_frm.set_value("compoun_walls",[])
            let rm= cur_frm.doc.pavers?cur_frm.doc.pavers:[]
            for(let row=0;row<rm.length;row++){
                if(!cur_frm.doc.pavers[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Pavers Table")}
                var message;
                var new_row = frm.add_child("items");
                new_row.item_code=cur_frm.doc.pavers[row].item
                new_row.qty=cur_frm.doc.pavers[row].allocated_paver_area
                new_row.ts_qty=cur_frm.doc.pavers[row].number_of_bundle
                new_row.area_per_bundle=cur_frm.doc.pavers[row].area_per_bundle
                new_row.rate=cur_frm.doc.pavers[row].rate
                new_row.amount=cur_frm.doc.pavers[row].amount
                await frappe.call({
                    method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                    args:{
                        'doctype':cur_frm.doc.pavers[row].item,
                    },
                    callback: function(r){
                        message=r.message;
                        new_row.item_name=message['item_name']
                        new_row.uom=message['uom']
                        new_row.description=message['description']
                        new_row.conversion_factor=message['uom_conversion']
                    }
                })
                new_row.warehouse=cur_frm.doc.set_warehouse
                new_row.delivery_date=cur_frm.doc.delivery_date
                new_row.work=cur_frm.doc.pavers[row].work
            }
        }

        
        if(cur_frm.doc.type=='Compound Wall'){
            let rmm= cur_frm.doc.compoun_walls?cur_frm.doc.compoun_walls:[]
            for(let row=0;row<rmm.length;row++){
                if(!cur_frm.doc.compoun_walls[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Compound Wall Table")}
                var message;
                var new_row = frm.add_child("items");
                new_row.item_code=cur_frm.doc.compoun_walls[row].item
                new_row.qty=cur_frm.doc.compoun_walls[row].allocated_ft
                new_row.rate=cur_frm.doc.compoun_walls[row].rate
                new_row.amount=cur_frm.doc.compoun_walls[row].amount
                await frappe.call({
                    method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                    args:{
                        'doctype':cur_frm.doc.compoun_walls[row].item,
                    },
                    callback: function(r){
                        message=r.message;
                        new_row.item_name=message['item_name']
                        new_row.uom=message['uom']
                        new_row.description=message['description']
                        new_row.conversion_factor=message['uom_conversion']
                    }
                })
                new_row.warehouse=cur_frm.doc.set_warehouse
                new_row.delivery_date=cur_frm.doc.delivery_date
                new_row.work=cur_frm.doc.compoun_walls[row].work
            }
        }
    }
})

function setquery(frm){
   
    
    frm.set_query('item','pavers',function(frm){
        return {
            filters:{
                'is_sales_item':1,
                'parent_item_group':'Products',
                'has_variants':0
            }
        }
    })
    frm.set_query('item','compoun_walls',function(frm){
        return {
            filters:{
                'is_sales_item':1,
                'item_group':'Compound Walls',
                'has_variants':0
            }
        }
    })
}

frappe.ui.form.on('Item Detail Pavers', {
    pavers_add: function(frm, cdt, cdn){
        frappe.model.set_value(cdt, cdn, 'work', frm.doc.work)
        frappe.model.set_value(cdt, cdn, 'warehouse', frm.doc.set_warehouse)
    }
 })
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
            frappe.model.set_value(cdt,cdn,"allocated_paver_area", data.required_area)	
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
            get_possible_delivery_date(frm)
			
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
function amt(frm, cdt, cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount',Math.round(row.allocated_ft*row.rate));
}
frappe.ui.form.on('Item Detail Compound Wall',{
    compoun_walls_add: function(frm, cdt, cdn){
        let data = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'work', (data.idx>1)?cur_frm.doc.compoun_walls[data.idx -2].work:'')
    },
    allocated_ft:function(frm,cdt,cdn){
       amt(frm, cdt, cdn)
    },
    rate:function(frm,cdt,cdn){
      amt(frm, cdt, cdn)
  
    },
    item:async function(frm,cdt,cdn){
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
    }
  
  })

var get_possible_delivery_date = function(frm){
    var child = []
    frm.doc.pavers.forEach(row => {
        if(row.item && row.req_pcs){
            frappe.call({
                method: 'building_block_retail.building_block_retail.report.get_possible_delivery_date_of_item.get_possible_delivery_date_of_item.get_data',
                args:{
                    filters:{'item_code':row.item, 'order_qty':row.req_pcs},
                    call_from_report : 0
                },
                callback(r){
                    child.push({'item':row.item, 'possible_delivery_date':r.message})
                    frm.set_value('possible_delivery_dates', child)
                    frm.refresh_field('possible_delivery_dates')
                }
            })
        }
    })
}