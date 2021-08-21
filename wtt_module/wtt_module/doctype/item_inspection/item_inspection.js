cur_frm.cscript.refresh = cur_frm.cscript.inspection_type;

frappe.ui.form.on("Item Inspection", {
	
refresh: function(frm) {
	if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Purchase Receipt'), function() {
				erpnext.utils.map_current_doc({
					method: "wtt_custom.customization.custom.purchase_receipt.make_quality",
					source_doctype: "Purchase Receipt",
					target: frm,
					date_field: "posting_date",
					setters: {
						supplier: frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 0
					}
				})
			}, __("Get items from"));
}
},
s_warehouse: function(frm) {
$.each(frm.doc.items || [], function(i, d) {
if(!d.s_warehouse) d.s_warehouse = frm.doc.s_warehouse;
});
refresh_field("s_warehouse");
}
});

frappe.ui.form.on("Item Inspection item", {
	acc_qty: function(frm,cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	ins_status: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	s_warehouse: function(frm, cdt, cdn) {
	if(!frm.doc.s_warehouse) {
	erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items","s_warehouse");
	refresh_field("s_warehouse");
	}
	}
});
var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", child.acc_qty * child.rate);

	var i,sum=0,sum_amount=0,sub=0,sub_amount=0,val,val2,r;
	var temp = frm.doc.items;

	for(i=0;i<temp.length;i++)
	{
		if(temp[i].ins_status=="Accepted")
		{
		sum+=temp[i].acc_qty;
		sum_amount+=temp[i].amount;
		}
	}
	if(child.ins_status=="Accepted")
	{
	frm.set_value("total_qty",sum);
	frm.set_value("total",sum_amount);
	}
	else if(child.ins_status=="Rejected")
	{
	frappe.model.set_value(cdt, cdn, "acc_qty",0.00);
	frm.set_value("total_qty",sum);
	frm.set_value("total",sum_amount);
	}
}
/*
function set_warehouse(frm) {
	if(frm.doc.s_warehouse){
		alert(frm.doc.s_warehouse);
		erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "items", "s_warehouse");
		frm.refresh_field('items');
	}
}
*/