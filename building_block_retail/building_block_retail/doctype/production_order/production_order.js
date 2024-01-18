// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Order', {
	refresh: function(frm) {
        frm.set_query("from_job_card", "excess_and_shortage", function (doc, cdt, cdn) {
            return {
                query:"building_block_retail.building_block_retail.custom.py.job_card.job_card_search",
                filters: {
                    production_item:locals[cdt][cdn].item_code || null
                }
            }
        })
        var button = cur_frm.fields_dict.works.grid.add_custom_button("Refresh", ()=>{
            frm.call({
                doc:frm.doc,
                method: 'refresh_works',
                callback(r){
                    frm.reload_doc()
                }
            })
        })
        button[0].style.backgroundColor = '#2490ef' 
        button[0].style.color = 'white' 
        frm.events.today_produced_item_filter(frm)
        frm.set_query("item_template", function () {
            return {
                filters: {
                    has_variants:1,
                    disabled:0
                }
            }
        })
        let items =[];
        for(let i = 0; i<(frm.doc.production_order_details || []).length; i++){
                items.push(frm.doc.production_order_details[i].item_code)
        }

        if(!frm.is_new()){
            frm.add_custom_button('Make Job Card', function(){
                if(!frm.doc.today_produced_items || !frm.doc.today_produced_items.length){
                    frappe.show_alert({message:"Enter Today Produced Items with Qty", indicator: 'red'})
                    frm.scroll_to_field('today_produced_items')
                }
                else{
                    var data = []
                    for(let i=0; i<frm.doc.today_produced_items.length; i++){
                        data.push({
                            item_code: frm.doc.today_produced_items[i].item_code,
                            produced_qty: frm.doc.today_produced_items[i].produced_qty,
                            excess_qty: frm.doc.today_produced_items[i].excess_qty,
                            date: frm.doc.today_produced_items[i].date,
                            from_time:frm.doc.today_produced_items[i].from_time,
                            employee:frm.doc.today_produced_items[i].employee,
                            workstation:frm.doc.today_produced_items[i].workstation,
                            to_time:frm.doc.today_produced_items[i].to_time,
                            employee:frm.doc.employee,
                            workstation:frm.doc.workstation,
                            source_warehouse:frm.doc.source_warehouse,
                            target_warehouse:frm.doc.target_warehouse
                        })
                    }
                    var table_fields = [
                        {
                            fieldname:"item_code",
                            fieldtype:"Link",
                            options:"Item",
                            label:"Item",
                            reqd:1,
                            in_list_view: 1,
                            columns:2
                        },
                        {
                            fieldname:"employee",
                            fieldtype:"Link",
                            options:"Employee",
                            label:"Employee",
                            reqd:1,
                            in_list_view: 1,
                            columns:1
                        },
                        {
                            fieldname:"workstation",
                            fieldtype:"Link",
                            options:"Workstation",
                            label:"Workstation",
                            reqd:1,
                            in_list_view: 1,
                            columns:1
                        },
                        {
                            fieldname:"from_time",
                            fieldtype:"Datetime",
                            label:"From Time",
                            reqd:1,
                            in_list_view: 1,
                            columns:1
                        },
                        {
                            fieldname:"to_time",
                            fieldtype:"Datetime",
                            label:"To Time",
                            reqd:1,
                            in_list_view: 1,
                            columns:1
                        },
                        {
                            fieldname:"source_warehouse",
                            fieldtype:"Link",
                            label:"Source Warehouse",
                            options: "Warehouse",
                            reqd:1,
                            in_list_view: 1,
                            columns:2
                        },
                        {
                            fieldname:"target_warehouse",
                            fieldtype:"Link",
                            label:"Target Warehouse",
                            options: "Warehouse",
                            reqd:1,
                            in_list_view: 1,
                            columns:2
                        },
                        {
                            fieldname:"date",
                            fieldtype:"Date",
                            label:"Date",
                            in_list_view: 0,
                            hidden:1
                        },
                        {
                            fieldname:"produced_qty",
                            fieldtype:"Int",
                            label:"Produced Qty",
                            in_list_view: 0,
                            hidden:1
                        },
                        {
                            fieldname:"excess_qty",
                            fieldtype:"Int",
                            label:"Excess Qty",
                            in_list_view: 0,
                            hidden:1
                        },
                    ]
                    var d = new frappe.ui.Dialog({
                        title:'Select Employee',
                        size:"extra-large",
                        static:true,
                        fields:[
                            {
                                fieldname: "jobcard_data",
                                fieldtype: "Table",
                                fields:table_fields,
                                in_place_edit: true,
                                cannot_add_rows:false,
                                data:data,
                            },
                            {
                                label: "Submit Stock Entry",
                                fieldname:"submit_stock_entry",
                                fieldtype: "Check",
                                default:1,
                                data:data
                    
                            }
                        ],
                        primary_action (data){
                            
                            function validate_mandatory(dialog, data){
                                if(!data.jobcard_data){
                                    return
                                }
                                let message = "";
                                let reqd_df = dialog.fields_dict.jobcard_data.df.fields.filter(df=>{return df.reqd});
                                let reqd_fields = reqd_df.map(value => value.fieldname);
                                for(let i=0; i<data.jobcard_data.length; i++){
                                    var keys = Object.keys(data.jobcard_data[i]);
                                    for(let j=0; j<reqd_fields.length; j++){
                                        if(!keys.includes(reqd_fields[j])){
                                            message +=`<p>Row #${data.jobcard_data[i].idx}: Missing <b>${table_fields.find(df=> df.fieldname == reqd_fields[j]).label}</b></p>`
                                        }
                                    }
                                }
                                if(message){
                                    frappe.throw({title:"Missing Mandatory Field", message:message})
                                }

                            }
                            function set_data(frm, data){
                                if(!data.jobcard_data){
                                    return
                                }
                                for(let i=0; i<data.jobcard_data.length; i++){
                                    var keys = Object.keys(data.jobcard_data[i]);
                                    var row = frm.doc.today_produced_items[data.jobcard_data[i].idx-1]
                                    for(let j=0; j<keys.length; j++){
                                        if(!row[keys[j]]){
                                            row[keys[j]] = data.jobcard_data[i][keys[j]]
                                        }
                                    }
                                }
                            }
                            validate_mandatory(d, data)
                            set_data(frm, data)
                            frm.refresh_field("today_produced_items")
                            frm.call({
                                doc:frm.doc,
                                
                                method: 'make_job_card',
                                args:{
                                    "submit_stock_entry":data.submit_stock_entry
                                },
                                freeze:true,
                                callback(r){
                                    frm.reload_doc()
                                    setTimeout(()=>{
                                        frm.reload_doc()
                                    }, 1500)
                                    d.hide()
                                    if(r.message[0]){

                                        frappe.show_alert(`<p>Job Card(s) are Created.</p><p>${r.message[0]}</p>`)
                                    }
                                    if(r.message[1])
                                    {
                                        if(r.message[1].length==1){
                                            // if()
                                            frappe.set_route("Form", "Stock Entry", r.message[1][0])
                                        }
                                        else{
                                            frappe.set_route("List", "Stock Entry", {'name':['in', r.message[1]]})
                                        }
                                    }
                                }
                            })
                        },
                        secondary_action_label:"Close",
                        secondary_action(){
                            d.hide();
                        }
                    })
                    
                    // d.$wrapper.find(".modal-header")[0].id = "mydivheader"
                    // d.$wrapper.find(".modal-content")[0].id = "mydiv"
                    // d.$wrapper.find(".modal-content")[0].style.resize = "both"
                    // // d.$wrapper.find(".modal-content")[0].style.overflow = "auto"
                    // dragElement(d)
                    d.show()
                }
            })

            frm.add_custom_button("Update Work Order", function(){
                frm.call({
                    doc:frm.doc,
                    method:"update_work_order",
                    freeze:true,
                    callback(r){
                        frappe.show_alert("Work Orders Updated.")
                    }
                })
            })
        }
        frappe.realtime.off("no_qty_update_work_order")
        frappe.realtime.on("no_qty_update_work_order", ()=>{
            frappe.show_alert({
                message: "Please update today produced qty in Production Order Details",
                indicator: "red"
            })
            frm.scroll_to_field('production_order_details')
        })

        frappe.realtime.off("reload_doc")
        frappe.realtime.on("reload_doc", ()=>{
            frm.reload_doc()
        })
        
	},
    today_produced_item_filter: function(frm){
        let items =[];
        if(frm.doc.item_wise_production_qty){
            for(let i = 0; i<frm.doc.item_wise_production_qty.length; i++){
                if(frm.doc.item_wise_production_qty[i].qty){
                    items.push(frm.doc.item_wise_production_qty[i].item_code)
                }
            }
        }
       
        frm.set_query("item_code", "today_produced_items", function(){
            return {
                filters:{
                    'name':['in', items],
                    "disabled":0
                }
            }
        })
        if(frm.doc.is_template){
            frm.set_query("item_code", "excess_and_shortage", function(){
                return {
                    filters:{
                        'variant_of':frm.doc.name,
                        "disabled":0
                    }
                }
            })
        }
        else{
            frm.set_query("item_code", "excess_and_shortage", function(){
                return {
                    filters:{
                        'name':frm.doc.name,
                        "disabled":0
                    }
                }
            })
        }
        
    },
    calculate_final_qty: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'final_qty', row.produced_qty - row.excess_qty + row.shortage_qty)
    },
});

frappe.ui.form.on("Item Wise Production Qty", {
    item_code: function(frm){
        frm.events.today_produced_item_filter(frm)
    },
    item_wise_production_qty_add: function(frm){
        frm.events.today_produced_item_filter(frm)
    },
    item_wise_production_qty_remove: function(frm){
        frm.events.today_produced_item_filter(frm)
    }
})

frappe.ui.form.on("Production Order Item", {
    today_produced_qty: function(frm, cdt, cdn){
        var row = locals[cdt][cdn]
        if(row.today_produced_qty < 0){
            frappe.model.set_value(cdt, cdn, 'today_produced_qty', 0)
            frappe.throw("Today Produced Qty Cannot be Negative")
        }

        var item_wise_qty = {}
        for(let i=0; i<frm.doc.production_order_details.length; i++){
            if(Object.keys(item_wise_qty).includes(frm.doc.production_order_details[i].item_code)){
                item_wise_qty[frm.doc.production_order_details[i].item_code] += frm.doc.production_order_details[i].today_produced_qty
            }
            else{
                item_wise_qty[frm.doc.production_order_details[i].item_code] = frm.doc.production_order_details[i].today_produced_qty
            }
        }
        for(let i=0; i<frm.doc.item_wise_production_qty.length; i++){
            if(Object.keys(item_wise_qty).includes(frm.doc.item_wise_production_qty[i].item_code)){
                var row = locals[frm.doc.item_wise_production_qty[i].doctype][frm.doc.item_wise_production_qty[i].name]
                frappe.model.set_value(frm.doc.item_wise_production_qty[i].doctype, frm.doc.item_wise_production_qty[i].name, 'pending_qty_to_allocate_in_work_order', row.qty_to_update_in_work_order - item_wise_qty[frm.doc.item_wise_production_qty[i].item_code])
            }
        }
        frm.refresh_field("item_wise_production_qty")

    }
})


frappe.ui.form.on("Today Produced Items", {
    item_code: function(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let items = {}
        if(!frm.doc.excess_and_shortage){
            return
        }
        for(let i=0; i<frm.doc.excess_and_shortage.length; i++){
            if(Object.keys(items).includes(frm.doc.excess_and_shortage[i].item_code)){
                items[frm.doc.excess_and_shortage[i].item_code]['excess_qty'] += (frm.doc.excess_and_shortage[i].excess_qty || 0)
                items[frm.doc.excess_and_shortage[i].item_code]['shortage_qty'] += (frm.doc.excess_and_shortage[i].shortage_qty || 0)
            }
            else{
                items[frm.doc.excess_and_shortage[i].item_code] = {
                    "excess_qty":(frm.doc.excess_and_shortage[i].excess_qty || 0),
                    "shortage_qty":(frm.doc.excess_and_shortage[i].shortage_qty || 0)
                }
            }
        }
        if(Object.keys(items).includes(row.item_code)){
            frappe.model.set_value(cdt, cdn, "excess_qty", items[row.item_code]["excess_qty"])
            frappe.model.set_value(cdt, cdn, "shortage_qty", items[row.item_code]["shortage_qty"])
        }
    }
})



// Code Reference : https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_draggable
function dragElement(dialog) {
  var elmnt = dialog.$wrapper.find('#mydiv')[0]
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (dialog.$wrapper.find('#mydivheader').length) {
    /* if present, the header is where you move the DIV from:*/
    dialog.$wrapper.find('#mydivheader')[0].onmousedown = dragMouseDown;
  } else {
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    /* stop moving when mouse button is released:*/
    document.onmouseup = null;
    document.onmousemove = null;
  }
}