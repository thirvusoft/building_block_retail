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

var prop_name;
frappe.ui.form.on('Sales Order',{
    refresh:function(frm){

        if(frm.is_new()){
            frm.trigger("type")
        }
        else{
            if (frm.doc.items){
                 
                let qtyTable = `<h1>Delivered Qty Details</h1><table><thead><tr><th style="width: 06%">{%= __("Item") %}</th><th style="width: 3%">{%= __("Qty") %}</th>
                <th style="width: 3%">{%= __("🚚Delivered Qty") %}</th><th style="width: 3%">{%= __("Pending Qty") %}</th></tr></thead><tbody>`;
    
                let hasPendingQty = false; 

                frm.doc.items.forEach(d => {
                    let pending_qty = d.qty - d.delivered_qty;

                    if (1 < pending_qty ) {
                        hasPendingQty = true; 
                        qtyTable += `<tr>
                                        <td>${d.item_code}</td>
                                        <td>${d.qty}</td>
                                        <td>${d.delivered_qty}</td>
                                        <td>${pending_qty}</td>
                                    </tr>`;
                    }
                });

                qtyTable += '</tbody></table>';

                if (hasPendingQty) {
                    frm.set_df_property('delivered_qty_details', 'options', qtyTable);
                } else {
                    frm.set_df_property('delivered_qty_details', 'hidden', 1); 
                }

            }

        }
   
        setTimeout(() => {   
            frm.remove_custom_button('Pick List', "Create");
            frm.remove_custom_button('Material Request', "Create");
            frm.remove_custom_button('Request for Raw Materials', "Create");
            frm.remove_custom_button('Purchase Order', "Create");
            frm.remove_custom_button('Site Work', "Create");
            frm.remove_custom_button('Subscription', "Create");
        }, 500);   
        
        
        frappe.ui.form.ProjectQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
            render_dialog: async function() {
                this._super();
                let calling_doc = frappe._from_link?.doc;
                this.doc.additional_cost=[{'description': 'Any Food Exp in Site'}, 
                                    {'description': 'Other Labour Work'}, 
                                    {'description': 'Site Advance'}]
                if(calling_doc.doctype=='Sales Order'){ 
                    if(!calling_doc.is_multi_customer){
                        this.dialog.get_field("customer").set_value(calling_doc.customer)
                    }
                    else{
                        this.dialog.get_field("is_multi_customer").set_value(1).then(() => {
                            this.dialog.refresh()
                        })
                        this.doc.customer_name=calling_doc.customers_name
                    }
                };
            }
        });
        
        if(cur_frm.doc.is_multi_customer){
            cur_frm.set_df_property('customer','reqd',0);
            cur_frm.set_df_property('customer','hidden',1)
        }
        else{
            cur_frm.set_df_property('customer','reqd',1);
        }
        setquery(frm)
        cur_frm.set_df_property('items','reqd',0);
        cur_frm.set_df_property('items','hidden',1);
        frm.set_query('supervisor', function(frm){
            return {
                filters:{
                    // 'designation': 'Supervisor',
                    'status':'Active'
                }
            }
        });
        frm.set_query('item','raw_materials',function(frm){
            return {
                filters:{
                    'item_group':'Raw Material',
                    'has_variants':0
                }
            }
        })
        frm.set_query('site_work',function(frm){
            return {
                filters:{
                    'customer': cur_frm.doc.customer,
                    'status': 'Open',
                    'is_multi_customer':cur_frm.doc.is_multi_customer
                }
            }
        })
        if(cur_frm.doc.docstatus==0){
            cur_frm.fields_dict.site_work.$input.on("click", function() {
                if(!cur_frm.doc.customer && !cur_frm.doc.is_multi_customer){
                    frappe.throw('Please Select Customer')
                }
            });
        }
        if(frm.doc.docstatus === 1){
            frm.add_custom_button('Get Stock Availability', ()=>{
                frappe.call({
                    method:'building_block_retail.building_block_retail.custom.py.sales_order.get_stock_availability',
                    args:{
                        items: frm.doc.items,
                        sales_order: frm.doc.name
                    },
                    callback(r){
                        frm.set_value("available_qty", r.message)
                        frm.set_df_property('available_qty','hidden',0)
                        frm.refresh()
                        frm.save('Update')
                    }
                })
            })
            frm.add_custom_button('Work Order', ()=>{
                make_work_order(frm)
            },("Create"))
        }
        else{
            frm.set_df_property('available_qty','hidden',1)
        }
    },

    set_warehouse: function(frm){
        if(frm.doc.set_warehouse){
            let table=cur_frm.doc.pavers?cur_frm.doc.pavers:[]
            for(let row=0; row<table.length; row++){
                frappe.model.set_value(cur_frm.doc.pavers[row].doctype, cur_frm.doc.pavers[row].name, 'warehouse', frm.doc.set_warehouse)
            }
            table=cur_frm.doc.compoun_walls?cur_frm.doc.compoun_walls:[]
            for(let row=0; row<table.length; row++){
                frappe.model.set_value(cur_frm.doc.compoun_walls[row].doctype, cur_frm.doc.compoun_walls[row].name, 'warehouse', frm.doc.set_warehouse)
            }
        }
    },
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
        frm.doc.pavers.forEach(d=>{
            frappe.model.set_value(d.doctype, d.name, 'work', frm.doc.work)
        })
    },
    customer:function(frm){
        cur_frm.set_value('site_work','')
        frm.set_query('site_work',function(frm){
            return {
                filters:{
                    'customer': cur_frm.doc.customer,
                    'status': 'Open',
                    'is_multi_customer':cur_frm.doc.is_multi_customer
                }
            }
        })
    },

//   Thirvu_dual_accounting
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
    })}
},
    site_work:function(frm){
        cur_frm.set_value('project',cur_frm.doc.site_work)
    },
    type:function(frm){
        if(frm.doc.customer)
        {frm.set_query('site_work',function(frm){
            return {
                filters:{
                    'customer': cur_frm.doc.customer,
                    'status': 'Open',
                    'is_multi_customer':cur_frm.doc.is_multi_customer
                }
            }
        })}
        setquery(frm)
        if(cur_frm.is_new()==1){
        fill_paver_compound_table_from_item(frm)
        }
    },
    before_save:async function(frm){
        if(cur_frm.doc.is_multi_customer){
            cur_frm.set_value('customer','');
            await frappe.call({
                "method":"building_block_retail.building_block_retail.custom.py.sales_order.create_property",
                "callback":function(r){
                    prop_name=r.message;
                }
            })
        }
        else{
            frm.clear_table("customers_name");
        }
        var qtn_item = {}
        var item = []
        if(frm.doc.items){
            frm.doc.items.forEach(r => {
                if(r.prevdoc_docname){
                    item.push(r.item_code)
                    qtn_item[r.item_code] = r.prevdoc_docname
                }
            })
        }
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
        
       
        let rm= cur_frm.doc.raw_materials?cur_frm.doc.raw_materials:[]
        for(let row=0;row<rm.length;row++){
            if(!cur_frm.doc.raw_materials[row].item){frappe.throw("Row #"+(row+1)+": Please Fill the Item name in Raw Material Table")}
            var message;
            var new_row = frm.add_child("items");
            new_row.is_raw_material = 1
            new_row.item_code=cur_frm.doc.raw_materials[row].item
            new_row.qty=cur_frm.doc.raw_materials[row].qty
            new_row.uom=cur_frm.doc.raw_materials[row].uom
            new_row.rate=cur_frm.doc.raw_materials[row].rate
            new_row.amount=cur_frm.doc.raw_materials[row].amount
            await frappe.call({
                method:'building_block_retail.building_block_retail.custom.py.sales_order.get_item_value',
                args:{
                    'doctype':cur_frm.doc.raw_materials[row].item,
                },
                callback: function(r){
                    message=r.message;
                    new_row.item_name=message['item_name']
                    new_row.description=message['description']
                }
            })
            new_row.conversion_factor=1
            new_row.warehouse=cur_frm.doc.set_warehouse
            new_row.delivery_date=cur_frm.doc.delivery_date
            
        }
       
        frm.doc.items.forEach(r => {
            if(item.includes(r.item_code)){
                r.prevdoc_docname = qtn_item[r.item_code]
            }
        })
           
        refresh_field("items");
        
        let tax=false;
        let taxes=cur_frm.doc.taxes?cur_frm.doc.taxes:[]
        for(let i=0;i<taxes.length;i++){
            if(!cur_frm.doc.taxes[i].tax_amount){
                tax=true;
            }
        }

        if(taxes.length==0){
            tax=true;
        }
        
        if(tax){
            let tax_category=frm.doc.tax_category
            await cur_frm.set_value('tax_category', '')
            await cur_frm.set_value('tax_category', tax_category)
        }

    },
    after_save:function(frm){
        if(cur_frm.doc.is_multi_customer){
            frappe.call({
                "method":"building_block_retail.building_block_retail.custom.py.sales_order.remove_property",
                "args":{
                    'prop_name':prop_name
                }
            })
        }
    },
    on_submit:function(frm){
        frappe.call({
            method:"building_block_retail.building_block_retail.custom.py.sales_order.create_site",
            args:{
                doc: cur_frm.doc
            },
            callback: function(r){
                if(r.message){ 
                        frappe.show_alert({message: __("Site Work Updated Successfully"),indicator: 'green'});
                      }
                }
        })
    },
    is_multi_customer: function(frm){
        cur_frm.set_value('site_work','')
        if(cur_frm.doc.is_multi_customer){
            cur_frm.set_df_property('customer','reqd',0);
            cur_frm.set_df_property('customer','hidden',1);
            frm.set_query('site_work',function(frm){
                return {
                    filters:{
                        'status': 'Open',
                        'is_multi_customer':cur_frm.doc.is_multi_customer
                    }
                }
            })
        }
        else{
            cur_frm.set_df_property('customer','reqd',1);
            cur_frm.set_df_property('customer','hidden',0);
            frm.set_query('site_work',function(frm){
                return {
                    filters:{
                        'customer': cur_frm.doc.customer,
                        'status': 'Open',
                        'is_multi_customer':cur_frm.doc.is_multi_customer
                    }
                }
            })
        }
    },
    work: function(frm){
        if(frm.doc.work=="Supply Only"){
            frm.set_value('site_work','')
        }
        for(let row=0; row<(frm.doc.pavers?frm.doc.pavers.length:0);row++){
            frappe.model.set_value(frm.doc.pavers[row].doctype, frm.doc.pavers[row].name, 'work', frm.doc.work)
        }
    }
})

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


function amount_rawmet(frm,cdt,cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount', (row.rate?row.rate:0)*(row.qty?row.qty:0))
}
 frappe.ui.form.on('Item Detail Pavers', {
    pavers_add: function(frm, cdt, cdn){
        frappe.model.set_value(cdt, cdn, 'work', frm.doc.work)
        frappe.model.set_value(cdt, cdn, 'warehouse', frm.doc.set_warehouse)
    }
 })


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
  
function amt(frm, cdt, cdn){
    let row=locals[cdt][cdn]
    frappe.model.set_value(cdt,cdn,'amount',Math.round(row.allocated_ft*row.rate));
}

function fill_paver_compound_table_from_item(frm){
    if(frm.doc.type=="Compound Wall"){
        if(!frm.doc.compoun_walls || frm.doc.compoun_walls==0){
        frm.doc.items.forEach((row) =>{
            if(row.item_group != 'Raw Material'){
            var child = frm.add_child('compoun_walls')
            child.item = row.item_code
            child.rate = row.rate
            child.allocated_ft = row.qty
            child.amount = row.amount
        }
        else{
            var child = frm.add_child('raw_materials')
            child.item = row.item_code
            child.rate = row.rate
            child.qty = row.qty
            child.amount = row.amount
            child.uom = row.uom
        }
        })
    }
    }
    else if(frm.doc.type == "Pavers"){
        if(!frm.doc.pavers || frm.doc.pavers==0){    
        frm.doc.items.forEach((row) =>{
            if(row.item_group != 'Raw Material'){
            var child = frm.add_child('pavers')
            child.item = row.item_code
            child.required_area=row.qty
            child.rate = row.rate
            child.amount = row.amount
            if(row.item_code){
            frappe.call({
				method:"building_block_retail.building_block_retail.custom.py.site_work.item_details_fetching_pavers",
				args:{item_code: row.item_code},
				callback(r)
				{
					child.area_per_bundle = r['message'][0]?parseFloat(r["message"][0]):0
                    var bundle = child.area_per_bundle?child.required_area / child.area_per_bundle :0
                    var no_of_bundle = Math.ceil(bundle)
                    child.number_of_bundle = no_of_bundle?no_of_bundle:0
                    var allocated_paver = child.number_of_bundle * child.area_per_bundle
			        child.allocated_paver_area = allocated_paver?allocated_paver:0
				}
			})
        }
        }
        else{
            var child = frm.add_child('raw_materials')
            child.item = row.item_code
            child.rate = row.rate
            child.qty = row.qty
            child.amount = row.amount
            child.uom = row.uom
        }
        })
    }
    }
    frm.refresh_field("pavers")
    frm.refresh_field("compoun_walls")
}

function make_work_order(frm) {
    // var doc = frm.doc
    frappe.call({
        method: "building_block_retail.building_block_retail.custom.py.sales_order.remove_raw_materials_from_items",
        args: {doc:frm.doc},
        callback(so){
            frappe.call({
                // doc: so.message,
                method: 'building_block_retail.building_block_retail.custom.py.sales_order.get_work_order_items',
                args:{self: so.message},
                callback: function(r) {
                   if(!r.message.length) {
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
                            description: __('Select BOM and Qty for Production'),
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
                                fieldtype: 'Read Only',
                                fieldname: 'req_qty',
                                reqd: 1,
                                label: __('Order Qty'),
                                in_list_view: 1,
                                columns: 1,
                            }, {
                                fieldtype: 'Data',
                                fieldname: 'sales_order_item',
                                reqd: 1,
                                label: __('Sales Order Item'),
                                hidden: 1
                            },
                                {
                                    fieldtype: 'Read Only',
                                    fieldname: 'stock_availability',
                                    label: 'Available Stock',
                                    in_list_view: 1,
                                    columns: 1,
                                    // read_only :1
                                },
                                {
                                    fieldtype: 'Read Only',
                                    fieldname: 'actual_stock',
                                    label: 'Actual Stock',
                                    in_list_view: 1,
                                    columns: 1
                                },
                                {
                                    fieldtype: 'Read Only',
                                    fieldname: 'stock_taken',
                                    label: 'Stock Taken',
                                    // in_list_view: 1,
                                    columns: 1
                                },
                                {
                                    fieldtype: 'Read Only',
                                    fieldname: 'pending_qty',
                                    label: 'Required Qty',
                                    in_list_view: 1,
                                    columns: 1
                                },
                                {
                                    fieldtype: 'Int',
                                    fieldname: 'buffer_qty',
                                    label: 'Buffer Qty(Over Production Allowance)',
                                    in_list_view: 1,
                                    columns: 1,
                                    default:0
                                },
                                {
                                    fieldtype: 'Select',
                                    fieldname: 'priority',
                                    label: 'Priority',
                                    in_list_view: 1,
                                    options: 'Low Priority\nHigh Priority\nUrgent Priority',
                                    columns: 1,
                                }
                                     ],
                            data: r.message,
                            get_data: () => {
                                return r.message
                            }
                        }]
                        var d = new frappe.ui.Dialog({
                            title: __('Items to Manufacture'),
                            fields: fields,
                            size: 'extra-large',
                            primary_action: function() {
                                var data = {items: d.fields_dict.items.grid.data};
                                frappe.call({
                                    method: 'building_block_retail.building_block_retail.custom.py.sales_order.make_work_orders',
                                    args: {
                                        items: data,
                                        company: so.message.company,
                                        sales_order: so.message.name,
                                        project: frm.doc.site_work
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
        }
    })
    
}