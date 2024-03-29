frappe.ui.form.on('Quotation', {
    setup:function(frm){
        frm.set_query("supervisor", function() {
            return {
                filters: {"Designation":"Supervisor"}
            }
        })
        frm.set_query('item','raw_materials',function(frm){
            return {
                filters:{
                    'item_group':'Raw Material',
                    'has_variants':0
                }
            }
        })
        frm.set_query('item','service_item',function(frm){
            return {
                filters:{
                    'item_group':'Labour Work',
                }
            }
        })
    },
    refresh:function(frm){
        frm.set_query('item','raw_materials',function(frm){
            return {
                filters:{
                    'item_group':'Raw Material',
                    'has_variants':0
                }
            }
        })
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
function amount_rawmet(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount', (row.rate?row.rate:0)*(row.qty?row.qty:0))
}
frappe.ui.form.on('TS Raw Materials',{
    item: function(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        if(row.item){
            frappe.db.get_doc('Item',row.item).then((item)=>{
                frappe.model.set_value(cdt,cdn,'uom', item.stock_uom);
                frappe.call({
                    method: "building_block_retail.building_block_retail.custom.py.sales_order.get_item_rate",
                    args:{
                        item: row.item,
                        uom: item.stock_uom
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
    },
    uom: function(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        if(row.item && row.uom){
            frappe.db.get_list("Item Price",{filters:{'item_code': row.item,'uom' : row.uom,'price_list': frm.doc.selling_price_list}, fields:['price_list_rate']}).then((data)=>{
                
                if(!data.length){
                    frappe.show_alert({
                        message:'Price List Rate not found for <a href="/app/item-price/">'+row.item+'</a> with the UOM '+row.uom,
                        indicator:'orange'
                    })
                }
                else{
                    frappe.model.set_value(cdt,cdn,'rate', data[0].price_list_rate);
                }   
            })
        }
    }

})
frappe.ui.form.on("Quotation", {
    refresh: function(frm){
        setquery(frm)
        setTimeout(() => {
			frm.remove_custom_button('Subscription', "Create");
		}, 500);  
        frm.set_df_property('items','reqd',0);
        frm.set_df_property('items','hidden',1);
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
        if(!frm.doc.pavers){
            frm.doc.pavers = []
        }
        frm.doc.pavers.forEach(d=>{
            frappe.model.set_value(d.doctype, d.name, 'work', frm.doc.work)
        })
    },
    rounding_adjustment: function(frm){
            frm.set_value('rounded_total', (frm.doc.rounding_adjustment + frm.doc.grand_total))
            frm.refresh()
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
        if(frm.doc.type=='Pavers'){
            frm.set_value("compoun_walls",[])
            let rm= frm.doc.pavers?frm.doc.pavers:[]
            for(let row=0;row<rm.length;row++){
                if(!frm.doc.pavers[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Pavers Table")}
                var message;
                var new_row = frm.add_child("items");
                new_row.item_code=frm.doc.pavers[row].item
                new_row.qty=frm.doc.pavers[row].allocated_paver_area
                new_row.ts_qty=frm.doc.pavers[row].number_of_bundle
                new_row.area_per_bundle=frm.doc.pavers[row].area_per_bundle
                new_row.rate=frm.doc.pavers[row].rate
                new_row.amount=frm.doc.pavers[row].amount
                new_row.qty_in_sqft = frm.doc.pavers[row].allocated_paver_area
                new_row.qty_in_pcs = frm.doc.pavers[row].req_pcs
                new_row.print_uom = frm.doc.pavers[row].print_uom
                await frappe.call({
                    method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                    args:{
                        'doctype':frm.doc.pavers[row].item,
                    },
                    callback: function(r){
                        message=r.message;
                        new_row.item_name=message['item_name']
                        new_row.uom=message['uom']
                        new_row.description=message['description']
                        new_row.conversion_factor=message['uom_conversion']
                    }
                })
                new_row.warehouse=frm.doc.set_warehouse
                new_row.delivery_date=frm.doc.delivery_date
                new_row.work=frm.doc.pavers[row].work
            }
        }

        
        if(frm.doc.type=='Compound Wall'){
            let rmm= frm.doc.compoun_walls?frm.doc.compoun_walls:[]
            for(let row=0;row<rmm.length;row++){
                if(!frm.doc.compoun_walls[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Compound Wall Table")}
                var message;
                var new_row = frm.add_child("items");
                new_row.item_code=frm.doc.compoun_walls[row].item
                new_row.qty=frm.doc.compoun_walls[row].allocated_ft
                new_row.rate=frm.doc.compoun_walls[row].rate
                new_row.amount=frm.doc.compoun_walls[row].amount
                await frappe.call({
                    method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                    args:{
                        'doctype':frm.doc.compoun_walls[row].item,
                    },
                    callback: function(r){
                        message=r.message;
                        new_row.item_name=message['item_name']
                        new_row.uom=message['uom']
                        new_row.description=message['description']
                        new_row.conversion_factor=message['uom_conversion']
                    }
                })
                new_row.warehouse=frm.doc.set_warehouse
                new_row.delivery_date=frm.doc.delivery_date
                new_row.work=frm.doc.compoun_walls[row].work
            }
        }

        let rm= frm.doc.raw_materials?frm.doc.raw_materials:[]
        for(let row=0;row<rm.length;row++){
            if(!frm.doc.raw_materials[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Raw Material Table")}
            var message;
            var new_row = frm.add_child("items");
            new_row.is_raw_material = 1
            new_row.item_code=frm.doc.raw_materials[row].item
            new_row.qty=frm.doc.raw_materials[row].qty
            new_row.uom=frm.doc.raw_materials[row].uom
            new_row.rate=frm.doc.raw_materials[row].rate
            new_row.amount=frm.doc.raw_materials[row].amount
            await frappe.call({
                method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                args:{
                    'doctype':frm.doc.raw_materials[row].item,
                },
                callback: function(r){
                    message=r.message;
                    new_row.item_name=message['item_name']
                    new_row.description=message['description']
                }
            })
            new_row.conversion_factor=1
            new_row.warehouse=frm.doc.set_warehouse
            new_row.delivery_date=frm.doc.delivery_date
            
        }

        let srv= frm.doc.service_item?frm.doc.service_item:[]
        for(let row=0;row<srv.length;row++){
            // if(!frm.doc.service_item[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Raw Material Table")}
            var message;
            var new_row = frm.add_child("items");
            new_row.is_service_item = 1
            new_row.item_code=frm.doc.service_item[row].item
            new_row.qty=1
            new_row.uom='Nos'
            new_row.rate=frm.doc.service_item[row].rate
            new_row.amount=frm.doc.service_item[row].rate
            await frappe.call({
                method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                args:{
                    'doctype':frm.doc.service_item[row].item,
                },
                callback: function(r){
                    message=r.message;
                    new_row.item_name=message['item_name']
                    new_row.description=message['description']
                }
            })
            new_row.conversion_factor=1
            new_row.warehouse=frm.doc.set_warehouse
            new_row.delivery_date=frm.doc.delivery_date
            
        }
       
            
           
        refresh_field("items");
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
function amt(frm, cdt, cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount',Math.round(row.allocated_ft*row.rate));
}
frappe.ui.form.on('Item Detail Compound Wall',{
    compoun_walls_add: function(frm, cdt, cdn){
        let data = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'work', (data.idx>1)?frm.doc.compoun_walls[data.idx -2].work:'')
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
  frappe.realtime.on('show_poss_del_date_error', (item)=>{
    frappe.show_alert({'message':`Enter Daily maximum production qty in Item <b>${item}</b>`,'indicator':'red'}) 
})
var get_possible_delivery_date = function(frm, row){
    var child = []
    
    // frm.doc.pavers.forEach(row => {
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
    // })
}