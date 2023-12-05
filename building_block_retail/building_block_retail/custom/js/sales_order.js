frappe.ui.form.on('Sales Order Item', {
    conversion_factor: function (frm, cdt, cdn) {
        bundle_calc(frm, cdt, cdn)
    },
    pieces: function (frm, cdt, cdn) {
        bundle_calc(frm, cdt, cdn)
    },
    required_sqft: function (frm, cdt, cdn) {
        bundle_calc(frm, cdt, cdn)
    },
    item_code: async function(frm, cdt, cdn) {
        let data = locals[cdt][cdn];

        let pieces_per_sqft = (await vb.uom_conversion(data.item_code, 'Square Foot', 1, 'Nos', false)) || 0;
        let pieces_per_bdl = (await vb.uom_conversion(data.item_code, 'bundle', 1, 'Nos', false)) || 0;

        frappe.model.set_value(cdt, cdn, 'pieces_per_sqft', pieces_per_sqft);
        frappe.model.set_value(cdt, cdn, 'pieces_per_bundle', pieces_per_bdl);
    },
    items_add: function(frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, 'work', frm.doc.work);
    },
    qty: function(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        get_possible_delivery_date(frm, row)
    }
})
var get_possible_delivery_date = function(frm, row){
    var child = frm.doc.possible_delivery_dates || []
	var child_items = []
	child.forEach((a)=>{
		child_items.push(a.item)
	})
	
        if(row.item_code && row.qty){
            frappe.call({
                method: 'building_block_retail.building_block_retail.report.get_possible_delivery_date_of_item.get_possible_delivery_date_of_item.get_data',
                args:{
                    filters:{'item_code':row.item_code, 'order_qty':row.qty*row.conversion_factor},
                    call_from_report : 0
                },
                callback(r){
					if(!child_items.includes(row.item_code)){
						child_items.push(row.item_code)
						var new_child = frm.add_child("possible_delivery_dates")
						new_child.item = row.item_code
						new_child.possible_delivery_date = r.message
						frm.refresh_field('possible_delivery_dates')
					}
					else{
						frm.doc.possible_delivery_dates.forEach((a)=>{
							if(a.item == row.item_code){
								frappe.model.set_value(a.doctype, a.name, "possible_delivery_date", r.message)
								frm.refresh_field('possible_delivery_dates')
							}
						})
					}
                }
            })
        }
}

async function bundle_calc(frm, cdt, cdn) {
    let row = locals[cdt][cdn]
    let uom = row.uom
    let conv1, conv2;

    await frappe.db.get_doc('Item', row.item_code).then((doc) => {
        let sqf_conv = 1
        let other_conv = 1;
        let nos_conv = 1
        for (let doc_row = 0; doc_row < doc.uoms.length; doc_row++) {
            if (doc.uoms[doc_row].uom == uom) {
                other_conv = doc.uoms[doc_row].conversion_factor
            }
            if (doc.uoms[doc_row].uom == 'Square Foot') {
                sqf_conv = doc.uoms[doc_row].conversion_factor
            }
            if (doc.uoms[doc_row].uom == 'Nos') {
                nos_conv = doc.uoms[doc_row].conversion_factor
            }
        }
        conv1 = (sqf_conv / other_conv) || 0
        conv2 = (nos_conv / other_conv) || 0
    })
    if (row.uom == "SQF") {
        frappe.model.set_value(cdt, cdn, 'qty', (row.required_sqft || 0) * conv1 + (row.pieces || 0) * conv2)
    } else {
        frappe.model.set_value(cdt, cdn, 'qty', (row.required_sqft || 0) * conv1 + (row.pieces || 0) * conv2)
    }
    let rate = row.rate
    frappe.model.set_value(cdt, cdn, 'rate', 0)
    frappe.model.set_value(cdt, cdn, 'rate', rate)

}

var prop_name;
frappe.ui.form.on('Sales Order',{
    onload:async function(frm){
        if(frm.is_new()  ){
            for(let ind=0;ind<frm.doc.items.length;ind++){
                if(row.item_group.indexOf('Paver')>=0 || row.item_group.indexOf('paver')>=0){
                    let cdt=frm.doc.items[ind].doctype
                    let cdn=frm.doc.items[ind].name
                    let row=locals[cdt][cdn]
                    if(row.item_code){
                        let pieces_per_sqft = (await vb.uom_conversion(row.item_code, 'Square Foot', 1, 'Nos', false)) || 0;
                        let pieces_per_bdl = (await vb.uom_conversion(row.item_code, 'bundle', 1, 'Nos', false)) || 0;

                        frappe.model.set_value(cdt, cdn, 'pieces_per_sqft', pieces_per_sqft);
                        frappe.model.set_value(cdt, cdn, 'pieces_per_bundle', pieces_per_bdl);       
                    
                    
                        let total_qty=row.qty
                        let sqft_qty = Math.floor(row.qty)
                        let pcs_in_sqft = total_qty - sqft_qty
                        await frappe.model.set_value(cdt, cdn, 'required_sqft', sqft_qty)
                        if(pieces_per_sqft && pcs_in_sqft){
                            await frappe.model.set_value(cdt, cdn, 'pieces', Math.round(pcs_in_sqft*pieces_per_sqft))
                        }
                    }    
                }
            }
            let items = frm.doc.items || [];
            let len = items.length;
            while (len--)
            {
                if(items[len].qty == 0)
                {
                    await cur_frm.get_field("items").grid.grid_rows[len].remove();
                }
            }
            frm.refresh();
            }

    },
    refresh:function(frm){
        if(frm.is_new()){
            frm.trigger("type")
        }
        else{
            frm.add_custom_button(__('Update Items'), () => {
				erpnext.utils.update_child_items({
					frm: frm,
					child_docname: "items",
					child_doctype: "Sales Order Detail",
					cannot_add_row: false,
				})
			});
            if (frm.doc.items){
                let qtyTable = `<p style="font-size:15px;font-weight:bold;">Delivered Qty Details</p><table><thead><tr><th style="width: 06%">{%= __("Item") %}</th><th style="width: 3%">{%= __("Qty") %}</th>
                <th style="width: 3%">{%= __("🚚Delivered Qty") %}</th><th style="width: 3%">{%= __("Pending Qty") %}</th></tr></thead><tbody>`;
    
                // let hasPendingQty = false; 

                frm.doc.items.forEach(d => {
                    let pending_qty = Math.round(d.conversion_factor*(d.qty - d.delivered_qty));
                    let qty= Math.round(d.conversion_factor*(d.qty));
                    let del_qty= Math.round(d.conversion_factor*(d.delivered_qty));

                    // if (1 < pending_qty ) {
                        // hasPendingQty = true; 
                        qtyTable += `<tr>
                                        <td>${d.item_code}</td>
                                        <td>${qty}</td>
                                        <td>${del_qty}</td>
                                        <td>${pending_qty}</td>
                                    </tr>`;
                    // }
                });

                qtyTable += '</tbody></table>';

                // if (hasPendingQty) {
                    frm.set_df_property('delivered_qty_details', 'options', qtyTable);
                // } else {
                //     frm.set_df_property('delivered_qty_details', 'hidden', 1); 
                // }

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
        // cur_frm.set_df_property('items','reqd',0);
        // cur_frm.set_df_property('items','hidden',1);
        frm.set_query('supervisor', function(frm){
            return {
                filters:{
                    // 'designation': 'Supervisor',
                    'status':'Active'
                }
            }
        });
        
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
    taxes_and_charges: function(frm) {
        if(frm.doc.branch && frm.doc.docstatus != 1) {
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
        frm.doc.items.forEach(d=>{
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
        for(let row=0; row<(frm.doc.items?frm.doc.items.length:0);row++){
            frappe.model.set_value(frm.doc.items[row].doctype, frm.doc.items[row].name, 'work', frm.doc.work)
        }
    }
});

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


erpnext.utils.update_child_items = function(opts) {
	const frm = opts.frm;
	const cannot_add_row = (typeof opts.cannot_add_row === 'undefined') ? true : opts.cannot_add_row;
	const child_docname = (typeof opts.cannot_add_row === 'undefined') ? "items" : opts.child_docname;
	const child_meta = frappe.get_meta(`${frm.doc.doctype} Item`);
	const get_precision = (fieldname) => child_meta.fields.find(f => f.fieldname == fieldname).precision;

    async function bundle_calc(frm, cdt, cdn) {
        let row = locals[cdt][cdn]
        let uom = row.uom
        let conv1, conv2;
    
        await frappe.db.get_doc('Item', row.item_code).then((doc) => {
            let sqf_conv = 1
            let other_conv = 1;
            let nos_conv = 1
            for (let doc_row = 0; doc_row < doc.uoms.length; doc_row++) {
                if (doc.uoms[doc_row].uom == uom) {
                    other_conv = doc.uoms[doc_row].conversion_factor
                }
                if (doc.uoms[doc_row].uom == 'Square Foot') {
                    sqf_conv = doc.uoms[doc_row].conversion_factor
                }
                if (doc.uoms[doc_row].uom == 'Nos') {
                    nos_conv = doc.uoms[doc_row].conversion_factor
                }
            }
            conv1 = (sqf_conv / other_conv) || 0
            conv2 = (nos_conv / other_conv) || 0
        })
        if (row.uom == "SQF") {
            frappe.model.set_value(cdt, cdn, 'qty', (row.required_sqft || 0) * conv1 + (row.pieces || 0) * conv2)
        } else {
            frappe.model.set_value(cdt, cdn, 'qty', (row.required_sqft || 0) * conv1 + (row.pieces || 0) * conv2)
        }
        let rate = row.rate
        frappe.model.set_value(cdt, cdn, 'rate', 0)
        frappe.model.set_value(cdt, cdn, 'rate', rate)
    
    }


	this.data = frm.doc[opts.child_docname].map((d) => {
		return {
			"docname": d.name,
			"name": d.name,
			"item_code": d.item_code,
			"delivery_date": d.delivery_date,
			"schedule_date": d.schedule_date,
			"conversion_factor": d.conversion_factor,
			"qty": d.qty,
			"rate": d.rate,
			"uom": d.uom,
            "pieces":d.pieces,
            "required_sqft":d.required_sqft,
            "pieces_per_sqft":d.pieces_per_sqft,
            "pieces_per_bundle":d.pieces_per_bundle,
            "stock_qty":d.stock_qty
		}
	});
    function calculate_item_values(data){
        if((data.pieces || data.required_sqft) && data.pieces_per_sqft){
            data.qty = (data.required_sqft || 0) + ((data.pieces|| 0)/data.pieces_per_sqft)
        }
        else if(data.pieces || data.required_sqft){
            data.qty = data.required_sqft || data.pieces
        }
        data.stock_qty = data.qty*data.conversion_factor || 0;
        if(!data.delivery_date){
            data.delivery_date = cur_frm.doc.delivery_date
        }
        cur_dialog.refresh()
    }

	let fields = [{
		fieldtype:'Data',
		fieldname:"docname",
		read_only: 1,
		hidden: 1,
	}, {
		fieldtype:'Link',
		fieldname:"item_code",
		options: 'Item',
		in_list_view: 1,
		read_only: 0,
		disabled: 0,
		label: __('Item Code'),
        columns:2,
		get_query: function() {
			let filters;
			if (frm.doc.doctype == 'Sales Order') {
				filters = {"is_sales_item": 1};
			} else if (frm.doc.doctype == 'Purchase Order') {
				if (frm.doc.is_subcontracted == "Yes") {
					filters = {"is_sub_contracted_item": 1};
				} else {
					filters = {"is_purchase_item": 1};
				}
			}
			return {
				query: "erpnext.controllers.queries.item_query",
				filters: filters
			};
		},
        onchange: async function(){
            let row_idx = document.activeElement.closest(".grid-row").getAttribute("data-idx")-1;
            let data = cur_dialog.fields_dict.trans_items.grid.data[row_idx];
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.sales_order.get_item_details_for_update_items",
                args: {
                    item: data.item_code
                },
                callback(r){
                    if(r.message){
                        let keys=Object.keys(r.message)
                        keys.forEach((a, i) => {
                            data[a] = r.message[a]
                            if(i==(keys.length-1)){
                                calculate_item_values(data)
                            }
                        })
                    }
                }
            })
        }
	}, 
    {
		fieldtype:'Link',
		fieldname:'uom',
		options: 'UOM',
		read_only: 0,
		label: __('UOM'),
		reqd: 1,
        // in_list_view: 1,
		onchange: function () {
			frappe.call({
				method: "erpnext.stock.get_item_details.get_conversion_factor",
				args: { item_code: this.doc.item_code, uom: this.value },
				callback: r => {
					if(!r.exc) {
						if (this.doc.conversion_factor == r.message.conversion_factor) return;

						const docname = this.doc.docname;
						dialog.fields_dict.trans_items.df.data.some(doc => {
							if (doc.docname == docname) {
								doc.conversion_factor = r.message.conversion_factor;
								dialog.fields_dict.trans_items.grid.refresh();
								return true;
							}
						})
					}
				}
			});
		}
	}, {
		fieldtype:'Float',
		fieldname:"qty",
		default: 0,
		read_only: 0,
		// in_list_view: 1,
		label: __('Qty'),
		precision: get_precision("qty"),
        columns:1,
        onchange: function(e){
            let row_idx = e.target.closest(".grid-row").getAttribute("data-idx")-1;
            let data = cur_dialog.fields_dict.trans_items.grid.data[row_idx];
            calculate_item_values(data)
        }
	}, 
    {
		fieldtype:'Currency',
		fieldname:"rate",
		options: "currency",
		default: 0,
		read_only: 0,
		in_list_view: 1,
		label: __('Rate'),
		precision: get_precision("rate"),
        columns:1
	}];

	if (frm.doc.doctype == 'Sales Order' || frm.doc.doctype == 'Purchase Order' ) {
		fields.splice(2, 0, {
			fieldtype: 'Date',
			fieldname: frm.doc.doctype == 'Sales Order' ? "delivery_date" : "schedule_date",
			// in_list_view: 1,
			label: frm.doc.doctype == 'Sales Order' ? __("Delivery Date") : __("Reqd by date"),
			reqd: 1
		})
		fields.splice(3, 0, {
			fieldtype: 'Float',
			fieldname: "conversion_factor",
			label: __("Conversion Factor"),
			precision: get_precision('conversion_factor')
		})
	}
    if (frm.doc.doctype == 'Sales Order'){
        let so_fields = [
            {
                fieldtype:'Float',
                fieldname:"pieces_per_sqft",
                default: 0,
                read_only: 1,
                in_list_view: 1,
                label: __('Pieces/Sqft'),
                columns:1
            },
            {
                fieldtype:'Float',
                fieldname:"pieces_per_bundle",
                default: 0,
                read_only: 1,
                in_list_view: 1,
                label: __('Pieces/Bundle'),
                columns:1
            },
            {
                fieldtype:'Float',
                fieldname:"required_sqft",
                default: 0,
                read_only: 0,
                in_list_view: 1,
                label: __('Required Sqft'),
                columns:1,
                onchange: function(e){
                    let row_idx = e.target.closest(".grid-row").getAttribute("data-idx")-1;
                    let data = cur_dialog.fields_dict.trans_items.grid.data[row_idx];
                    calculate_item_values(data)
                }
            },
            {
                fieldtype:'Int',
                fieldname:"pieces",
                default: 0,
                read_only: 0,
                in_list_view: 1,
                label: __('Pieces'),
                columns:1,
                onchange: function(e){
                    let row_idx = e.target.closest(".grid-row").getAttribute("data-idx")-1;
                    let data = cur_dialog.fields_dict.trans_items.grid.data[row_idx];
                    calculate_item_values(data)
                }
            },
            {
                fieldtype:'Float',
                fieldname:"stock_qty",
                default: 0,
                read_only: 1,
                in_list_view: 1,
                label: __('Qty in Stock UOM'),
                columns:1
            }
        ]
        fields = [...fields, ...so_fields]
    }

	new frappe.ui.Dialog({
		title: __("Update Items"),
		size: "extra-large",
		fields: [
			{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: cannot_add_row,
				in_place_edit: false,
				reqd: 1,
				data: this.data,
				get_data: () => {
					return this.data;
				},
				fields: fields
			},
		],
		primary_action: function() {
			const trans_items = this.get_values()["trans_items"].filter((item) => !!item.item_code);
			frappe.call({
				method: 'erpnext.controllers.accounts_controller.update_child_qty_rate',
				freeze: true,
				args: {
					'parent_doctype': frm.doc.doctype,
					'trans_items': trans_items,
					'parent_doctype_name': frm.doc.name,
					'child_docname': child_docname
				},
				callback: function() {
					frm.reload_doc();
				}
			});
			this.hide();
			refresh_field("items");
		},
		primary_action_label: __('Update')
	}).show();
}