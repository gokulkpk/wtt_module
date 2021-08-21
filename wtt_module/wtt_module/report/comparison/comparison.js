frappe.query_reports["Comparison"] = {
	"filters": [
		{
			fieldtype: "Link",
			label: __("Request for Quotation"),
			options: "Request for Quotation",
			fieldname: "request_for_quotation",
			"reqd": 1,
			default: "",
			get_query: () => {
				return { filters: { "docstatus": ["<", 2] } }
			}
		},
		/*
		{
			fieldtype: "Link",
			label: __("Material Request"),
			options: "Material Request",
			fieldname: "mr",
			"reqd": 1,
			default: "",
			get_query: () => {
				return { filters: { "docstatus": ["<", 2] } }
			}
		},
		*/
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			fieldtype: "Link",
			label: __("Company"),
			options: "Company",
			fieldname: "company",
			default: "W.t.t technology Services India Pvt Ltd"
		}
	],
	formatter: (value, row, column, data, default_formatter,datum) => {
		value = default_formatter(value, row, column, data);
			if(data['item_code']=='Total')
			{
				value = `<div style="font-weight:bold">${value}</div>`;	
			}
			if(data['item_code']=='Grand Total')
			{
				value = `<div style="font-weight:bold">${value}</div>`;	
			}
			return value;
		}
	}
