// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Shifting', {
    refresh: function (frm) {
        frm.set_query('warehouse', (frm) => {
            return {
                filters: {
                    company: cur_frm.doc.company,
                    is_group:0,
                    disabled:0
                }
            }
        })
        frm.set_query('item_code', 'items', function (frm) {
            return {
                filters: {
                    'is_sales_item': 1,
                    'parent_item_group': 'Products',
                    'has_variants': 0
                }
            }
        })
        frm.set_query('item', 'ts_loadman_info', function (frm) {
            return {
                filters: {
                    'is_sales_item': 1,
                    'parent_item_group': 'Products',
                    'has_variants': 0
                }
            }
        })
        frm.set_query('employee', 'ts_only_loadman', function (frm) {
            return {
                filters: {
                    'status': 'Active'
                }
            }
        })
        frm.set_query('employee', 'ts_only_unloadman', function (frm) {
            return {
                filters: {
                    'status': 'Active'
                }
            }
        })
        frm.set_query('employee', 'ts_loadman_info', function (frm) {
            return {
                filters: {
                    'status': 'Active'
                }
            }
        })

        frm.fields_dict.curing_in_process.grid.add_custom_button("Add to Bundle", async function onclick() {
            let selected = frm.fields_dict.curing_in_process.grid.get_selected_children();
            if (!selected || !selected.length) {
                frappe.show_alert({ "message": "Select Rows from Curing in Process table to Bundle", indicator: "red" })
                frm.scroll_to_field("curing_in_process")
                return
            }
            let fields = [
                {
                    fieldname: "bundling_employee",
                    fieldtype: "Link",
                    label: "Bundling Employee",
                    options:"Employee",
                    reqd:1,
                },
                {
                    fieldtype: "Column Break"
                },
                {
                    fieldname: "fg_warehouse",
                    fieldtype: "Link",
                    label: "Bundle Warehouse",
                    options:"Warehouse",
                    reqd:1,
                },
                {
                    fieldtype: "Section Break"
                },
                {
                    fieldname: "curing_stock",
                    fieldtype: "Int",
                    label: "Stock in Curing",
                    read_only: 1
                },
                {
                    fieldname: "no_of_pieces",
                    fieldtype: "Int",
                    label: "No of Pieces",
                    onchange: function () {
                        let val = dialog.get_values()
                        if (!val["pcs_per_bundle"]) {
                            dialog.fields_dict.no_of_bundle.value = 0;
                            dialog.fields_dict.stock_qty.value = val["no_of_pieces"];
                            dialog.refresh()
                        }
                        else {
                            dialog.fields_dict.no_of_bundle.value = val["no_of_pieces"] / val["pcs_per_bundle"];
                            dialog.fields_dict.stock_qty.value = val["no_of_pieces"];
                            dialog.refresh()
                        }
                    }
                },
                {
                    fieldtype: "Column Break"
                },
                {
                    fieldname: "pcs_per_bundle",
                    fieldtype: "Int",
                    label: "Pcs per Bundle",
                    read_only: 1
                },
                {
                    fieldname: "no_of_bundle",
                    fieldtype: "Float",
                    label: "No of Bundle",
                    onchange: function () {
                        let val = dialog.get_values()
                        if (!val["pcs_per_bundle"]) {
                            dialog.fields_dict.no_of_bundle.value = 0;
                            dialog.fields_dict.no_of_pieces.value = 0;
                            dialog.fields_dict.stock_qty.value = 0;
                            dialog.refresh()
                        }
                        else {
                            dialog.fields_dict.no_of_pieces.value = val["pcs_per_bundle"] * val["no_of_bundle"];
                            dialog.fields_dict.stock_qty.value = val["pcs_per_bundle"] * val["no_of_bundle"];
                            dialog.refresh()
                        }
                    }
                },
                {
                    fieldtype: "Column Break"
                },
                {
                    fieldname: "stock_qty",
                    fieldtype: "Int",
                    label: "Qty in Stock UOM",
                    read_only: 1
                },
            ]
            let selected_production_qty = 0, pcs_per_bundle = 0, data = {};
            selected.forEach((r) => {
                selected_production_qty += r.pending_qty;
            })
            pcs_per_bundle = (await vb.uom_conversion(frm.doc.item_code, 'bundle', 1, 'Nos', false)) || 0;
            data = {
                "curing_stock": selected_production_qty,
                "pcs_per_bundle": pcs_per_bundle,
                "fg_warehouse": frm.doc.warehouse,
                "bundling_employee": frm.doc.bundling_employee  
            }

            let dialog = new frappe.ui.Dialog({
                size: "large",
                title: "Curing to Bundle",
                fields: fields,
                async primary_action(values) {
                    if(! values["stock_qty"]){
                        frappe.throw("Missing No of Pieces/Bundle.");
                        return;
                    }
                    if (values["stock_qty"] > values["curing_stock"]) {
                        frappe.throw(`Bundled Qty(${values["stock_qty"]}) should be less than Produced Qty(${values["curing_stock"]})`);
                        return;
                    }
                    let selected_rows_id = [];
                    selected.forEach((row) => {
                        selected_rows_id.push(row.name)
                    })
                    await frappe.call({
                        method: "building_block_retail.building_block_retail.doctype.material_shifting.material_shifting.update_curing_stock",
                        args: {
                            docname: frm.doc.name,
                            values: values,
                            selected_rows_id:selected_rows_id
                        },
                        freeze: true,
                        async callback(r) {
                            await frm.reload_doc()
                            dialog.hide()
                        }
                    })
                }
            })
            dialog.set_values(data);
            dialog.show();
        })
    },
    calculate_again: function (frm) {
        split_loading_unloading_qty_evenly(frm)
    },
    validate: function (frm) {
        if (frm.doc.ts_loadman_info) {
            var total = 0;
            frm.doc.ts_loadman_info.forEach(dt => {
                total = total + dt.amount
            })
            frm.set_value('ts_loadman_total_amount', total)
            frm.refresh_field('ts_loadman_total_amount')
        }
    }
});


frappe.ui.form.on('Loading Employee', {
    employee: function (frm) {
        split_loading_unloading_qty_evenly(frm)
    }
})

frappe.ui.form.on('Unloading Employee', {
    employee: function (frm) {
        split_loading_unloading_qty_evenly(frm)
    }
})

frappe.ui.form.on('TS Loadman Cost', {
    rate: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'amount', row.rate * row.qtypieces)
    },
    qtypieces: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'amount', row.rate * row.qtypieces)
    }
})

function get_employees_for_loadman(frm) {
    var employees = { 'Loading': [], 'Unloading': [], 'Both': [] }

    var load_emp = [], unload_emp = [];
    if (frm.doc.ts_only_loadman) {
        frm.doc.ts_only_loadman.forEach(e => {
            if (e.employee) {
                load_emp.push(e.employee)
            }
        })
    }
    if (frm.doc.ts_only_unloadman) {
        frm.doc.ts_only_unloadman.forEach(e => {
            if (e.employee) {
                unload_emp.push(e.employee)
            }
        })
    }

    load_emp.forEach(ld => {
        if (in_list(unload_emp, ld)) {
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

function get_items_for_loading(frm) {
    var items = {}
    frm.doc.items.forEach(itm => {
        if (!in_list(Object.keys(items), itm.item_code)) {
            items[itm.item_code] = Math.round(itm.stock_qty)
        }
        else {
            items[itm.item_code] += Math.round(itm.stock_qty)
        }
    })
    return items
}
function split_loading_unloading_qty_evenly(frm) {
    var qty_cost_conversion = { 'Loading': 1, 'Unloading': 1, 'Both': 2 }
    var employees = get_employees_for_loadman(frm)
    var items = get_items_for_loading(frm)
    var types = Object.keys(qty_cost_conversion)
    var loading_table = [], final_table = [];
    var loading_costs = {}, total_costs = 0;
    frm.doc.items.forEach(it => {
        loading_costs[it.item_code] = it.loading_cost ? it.loading_cost : 0
    })
    types.forEach(typ => {
        if (typ != 'Both') {
            employees[typ].forEach(emp => {
                Object.keys(items).forEach(itm => {
                    loading_table.push({ 'employee': emp, 'type': typ, 'item': itm, 'qtypieces': items[itm] * (qty_cost_conversion[typ] / employees[typ].length) })
                })
            })
        }
    })
    var employee_list = [];
    if (frm.doc.ts_only_loadman) {
        frm.doc.ts_only_loadman.forEach(e => {
            if (!in_list(employee_list, e.employee) && e.employee) {
                employee_list.push(e.employee)
            }
        })
    }
    if (frm.doc.ts_only_unloadman) {
        frm.doc.ts_only_unloadman.forEach(e => {
            if (!in_list(employee_list, e.employee) && e.employee) {
                employee_list.push(e.employee)
            }
        })
    }
    employee_list.forEach(emp => {
        Object.keys(items).forEach(itm => {


            var row = { 'employee': emp, 'item': itm, 'qtypieces': 0 }
            var load_type = []
            loading_table.forEach(lt => {
                if (lt.employee == emp && lt.item == itm) {
                    row.qtypieces += lt.qtypieces
                    load_type.push(lt.type)
                }
            })
            if (in_list(load_type, 'Loading') && in_list(load_type, 'Unloading')) {
                row.type = 'Both'
            }
            else {
                row.type = load_type[0]
            }
            row.qtypieces = Math.round(row.qtypieces)
            row.rate = loading_costs[row.item]
            row.amount = row.rate * row.qtypieces
            total_costs += row.amount
            final_table.push(row)
        })
    })

    frm.set_value('ts_loadman_info', final_table)
    frm.set_value('ts_loadman_total_amount', total_costs)
    frm.refresh_field('ts_loadman_info')
    frm.refresh_field('ts_loadman_total_amount')
}




frappe.ui.form.on("Curing Items", {
    excess_qty: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "pending_qty", (row["produced_qty"] || 0) - (row["excess_qty"] || 0))
    }
})