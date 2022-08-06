var salary_balance,standard_hrs=0;
frappe.ui.form.on('Salary Slip',{
    refresh: function(frm){
        cur_frm.set_df_property('total_amount', 'read_only', 1)
        frm.set_query("payment_account", function () {
			var account_types = ["Bank", "Cash"];
			return {
				filters: {
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
			};
		});
    },
    validate:function(frm,cdt,cdn){
        if(frm.doc.total_unpaid_amount<0){
            cur_frm.scroll_to_field('total_paid_amount')
            frappe.throw("Total Paid Amount cannot be greater than Total Amount")

        }
    },
    employee:function(frm,cdt,cdn){
        if(frm.doc.designation=='Job Worker' || frm.doc.designation == "Loader"){
            frappe.db.get_doc('Employee', frm.doc.employee).then((doc) => {
                salary_balance=doc.salary_balance
                frm.set_value('salary_balance',salary_balance)
            });
            if(frm.doc.employee && frm.doc.start_date && frm.doc.end_date){
            get_employee_advance(frm)
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.salary_slip.site_work_details",
                args:{
                    employee:frm.doc.employee,
                    start_date:frm.doc.start_date,
                    end_date:frm.doc.end_date,
                    designation: frm.doc.designation
                },
                callback:function(r){
                    let paid_amount = 0,total_unpaid_amount=0,total_amount=0;
                    frm.clear_table('site_work_details');
                    cur_frm.set_value('site_work_details',r.message)
                    for (let data in r.message){
                        total_amount = total_amount+r.message[data].amount
                        total_unpaid_amount=total_unpaid_amount+r.message[data].amount
                       
                    }
                    cur_frm.refresh()
                    cur_frm.set_value("total_paid_amount",paid_amount);
                    cur_frm.set_value("total_amount",total_amount - frm.doc.total_advance_amount);
                    cur_frm.set_value("total_unpaid_amount",(frm.doc.total_amount-frm.doc.total_paid_amount)+frm.doc.salary_balance);
                }
        })
    }
        }
        
    },
    end_date:function(frm,cdt,cdn){
        if(frm.doc.designation=='Job Worker' || frm.doc.designation == "Loader"){
            frappe.db.get_doc('Employee', frm.doc.employee).then((doc) => {
                salary_balance=doc.salary_balance
            });
            if(frm.doc.employee && frm.doc.start_date && frm.doc.end_date){
            get_employee_advance(frm)
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.salary_slip.site_work_details",
                args:{
                    employee:frm.doc.employee,
                    start_date:frm.doc.start_date,
                    end_date:frm.doc.end_date,
                    designation: frm.doc.designation
                },
                callback:function(r){
                    let paid_amount = 0,total_unpaid_amount=0,total_amount=0;
                    frm.clear_table('site_work_details');
                    cur_frm.set_value('site_work_details',r.message)
                    for (let data in r.message){
                        total_amount = total_amount+r.message[data].amount
                        total_unpaid_amount=total_unpaid_amount+r.message[data].amount
                       
                    }
                    cur_frm.refresh_field("site_work_details")
                    cur_frm.set_value("total_paid_amount",paid_amount);
                    cur_frm.set_value("total_amount",total_amount-frm.doc.total_advance_amount);
                    cur_frm.set_value("total_unpaid_amount",(frm.doc.total_amount-frm.doc.total_paid_amount)+frm.doc.salary_balance);
                }
        })
    }
        }
        
    },
    start_date:function(frm,cdt,cdn){
        if(frm.doc.designation=='Job Worker' || frm.doc.designation == "Loader"){
            frappe.db.get_doc('Employee', frm.doc.employee).then((doc) => {
                salary_balance=doc.salary_balance
            });
            if(frm.doc.employee && frm.doc.start_date && frm.doc.end_date){
            get_employee_advance(frm)
            frappe.call({
                method:"building_block_retail.building_block_retail.custom.py.salary_slip.site_work_details",
                args:{
                    employee:frm.doc.employee,
                    start_date:frm.doc.start_date,
                    end_date:frm.doc.end_date,
                    designation: frm.doc.designation
                },
                callback:function(r){
                    let paid_amount = 0,total_unpaid_amount=0,total_amount=0;
                    frm.clear_table('site_work_details');
                    cur_frm.set_value('site_work_details',r.message)
                    for (let data in r.message){
                        total_amount = total_amount+r.message[data].amount
                        total_unpaid_amount=total_unpaid_amount+r.message[data].amount
                       
                    }
                    cur_frm.refresh_field("site_work_details")
                    cur_frm.set_value("total_paid_amount",paid_amount);
                    cur_frm.set_value("total_amount",total_amount-frm.doc.total_advance_amount);
                    cur_frm.set_value("total_unpaid_amount",(frm.doc.total_amount-frm.doc.total_paid_amount)+frm.doc.salary_balance);
                }
        })
    }
        }
        
    },
    pay_the_balance:function(frm){
        if(frm.doc.pay_the_balance==1){
            frm.set_value('total_paid_amount',frm.doc.total_paid_amount+frm.doc.salary_balance)
            frm.set_value('total_amount',frm.doc.total_amount+frm.doc.salary_balance)
            frm.set_value('salary_balance',0)
        }
        else{
                frappe.db.get_value("Employee", {"name": frm.doc.employee}, "salary_balance", (r) => {
                    salary_balance=r.salary_balance                    
                });
                frm.set_value('salary_balance',salary_balance)
                frm.set_value('total_amount',frm.doc.total_amount-frm.doc.salary_balance)
                frm.set_value('total_paid_amount',frm.doc.total_paid_amount-frm.doc.salary_balance)
        }

    },
    
    total_paid_amount:function(frm){
        var sal = 0
        if(frm.doc.pay_the_balance)sal=frm.doc.salary_balance
        frm.set_value('total_unpaid_amount',(frm.doc.total_amount-frm.doc.total_paid_amount)+sal) 
        let earnings = frm.doc.earnings
        
        var exit=0
        for (let data in earnings){
            if(earnings[data].salary_component=='Basic'){
                frappe.model.set_value(earnings[data].doctype,earnings[data].name,'amount',frm.doc.total_paid_amount)
                exit=1
            }
            cur_frm.refresh_field("earnings")
        }   
        if(exit==0){
            var child = cur_frm.add_child("earnings");
            frappe.model.set_value(child.doctype, child.name, "salary_component",'Basic') 
            setTimeout(() => {    
                frappe.model.set_value(child.doctype, child.name, "amount",frm.doc.total_paid_amount)
                cur_frm.refresh_field("earnings")            }, 100);
        }   
    }
})


frappe.ui.form.on('Site work Details',{
    paid_amount:function(frm,cdt,cdn){
        var row = locals[cdt][cdn];
        var amount_to_pay = 0
        var paid_data = frm.doc.site_work_details
        for (var value in paid_data){
            amount_to_pay+=paid_data[value].paid_amount
            
        }
        frappe.model.set_value(row.doctype,row.name, "balance_amount",row.amount - row.paid_amount)
        if(frm.doc.pay_the_balance){

            frm.set_value('total_paid_amount',salary_balance+amount_to_pay)
        }  
        else{
            frm.set_value('total_paid_amount',amount_to_pay)
        }     
    }
})

function get_employee_advance(frm){
    frappe.call({
        method:"building_block_retail.building_block_retail.custom.py.salary_slip.get_employee_advance_amount",
        args:{
            name: frm.doc.employee,
            start_date:frm.doc.start_date,
            end_date: frm.doc.end_date
        },
        callback(r){
            frm.set_value('total_advance_amount', r.message)
            frm.refresh_field('total_advance_amount')
        }
    })
}