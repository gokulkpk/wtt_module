{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on("Supplier Quotation Item", {
	uom_rate: function(frm,cdt, cdn){
		calculate_total(frm, cdt, cdn);
	}
});

var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", ((child.stock_qty/child.qty)*child.uom_rate));
	}