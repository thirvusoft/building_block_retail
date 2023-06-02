import frappe
import erpnext
from frappe.desk.form import assign_to
from frappe import _, bold
from frappe.model.document import Document
from frappe.utils.data import get_link_to_form
from erpnext.manufacturing.doctype.job_card.job_card import JobCard


class Jobcard(JobCard):
	def validate(self):
		self.validate_time_logs()
		self.set_status()
		self.validate_operation_id()
		self.validate_sequence_id()
		self.set_sub_operations()
		self.update_sub_operation_status()
		self.validate_work_order()

	def after_insert(self):
		if(self.work_order):
			if(frappe.db.get_value('Work Order', self.work_order, 'status') == "Not Started"):
				frappe.db.set_value('Work Order', self.work_order, 'status', 'Job Card Created')
				
	def validate_job_card(self):
		if (
			self.work_order
			and frappe.get_cached_value("Work Order", self.work_order, "status") == "Stopped"
		):
			frappe.throw(
				_("Transaction not allowed against stopped Work Order {0}").format(
					get_link_to_form("Work Order", self.work_order)
				)
			)

		if not self.time_logs:
			frappe.throw(
				_("Time logs are required for {0} {1}").format(
					bold("Job Card"), get_link_to_form("Job Card", self.name)
				)
			)

		if self.for_quantity and self.total_completed_qty != self.for_quantity and not self.reason:
   			pass
	def set_transferred_qty(self, update_status=False):
		"Set total FG Qty in Job Card for which RM was transferred."
		if not self.items:
			self.transferred_qty = self.for_quantity if self.docstatus == 1 else 0
		if(self.work_order):
			doc = frappe.get_doc("Work Order", self.get("work_order"))
			if doc.transfer_material_against == "Work Order" or doc.skip_transfer:
				return

			if self.items:
				# sum of 'For Quantity' of Stock Entries against JC
				self.transferred_qty = (
					frappe.db.get_value(
						"Stock Entry",
						{
							"job_card": self.name,
							"work_order": self.work_order,
							"docstatus": 1,
							"purpose": "Material Transfer for Manufacture",
						},
						"sum(fg_completed_qty)",
					)
					or 0
				)

			self.db_set("transferred_qty", self.transferred_qty)

		qty = 0
		if self.work_order:
			doc = frappe.get_doc("Work Order", self.work_order)
			if doc.transfer_material_against == "Job Card" and not doc.skip_transfer:
				completed = True
				for d in doc.operations:
					if d.status != "Completed":
						completed = False
						break

				if completed:
					job_cards = frappe.get_all(
						"Job Card",
						filters={"work_order": self.work_order, "docstatus": ("!=", 2)},
						fields="sum(transferred_qty) as qty",
						group_by="operation_id",
					)

					if job_cards:
						qty = min(d.qty for d in job_cards)

			doc.db_set("material_transferred_for_manufacturing", qty)

		self.set_status(update_status)

@frappe.whitelist()
def get_workorder_doc(work_order, opr, workstation, qty=0):
	wo=frappe.get_doc("Work Order", work_order)
	over_prdn_prcnt = frappe.db.get_singles_value("Manufacturing Settings", 'overproduction_percentage_for_work_order')
	wo.update({
		'over_prdn_prcnt' : over_prdn_prcnt
	})
	return wo
	
@frappe.whitelist()
def calculate_max_qty(job_card):
	cur_job_card = frappe.get_doc("Job Card",job_card)
	get_job_card = frappe.get_all("Stock Entry", pluck = 'fg_completed_qty', filters={"ts_job_card": job_card,"docstatus": 1})  
	max = float(cur_job_card.total_completed_qty) - float(sum(get_job_card))
	return max
@frappe.whitelist()
def update_operation_completed_qty(work_order, opr, workstation, qty=0):
	completed_qty = frappe.get_value("Work Order Operation",{'operation':opr,'parent':work_order},'completed_qty') or 0
	frappe.db.set_value("Work Order Operation",{'operation':opr,'parent':work_order},'completed_qty', float(qty)+float(completed_qty))
	frappe.db.commit()

def before_submit(doc, event):
	make_stock_entry(doc.name, doc.total_completed_qty, "Manufacture")

# def update_production_order
@frappe.whitelist()
def make_stock_entry(job_card, qty=None, purpose="Manufacture"):
	job_card = frappe.get_doc("Job Card", job_card)
	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.update({
		'ts_job_card': job_card.name,
		'production_order': job_card.production_order,
		'purpose': purpose,
		'company': erpnext.get_default_company(),
		'from_bom' : 1,
		'bom_no' : job_card.bom_no,
		'use_multi_level_bom' : 1,
		'fg_completed_qty' : ( qty if qty is not None else (job_card.total_completed_qty or 0))
	})

	if job_card.bom_no:
		stock_entry.update({
			'inspection_required' : frappe.db.get_value("BOM", job_card.bom_no, "inspection_required")
		})

	stock_entry.from_warehouse = job_card.source_warehouse
	stock_entry.to_warehouse = job_card.target_warehouse
	stock_entry.project = job_card.project

	stock_entry.set_stock_entry_type()
	stock_entry.get_items()
	stock_entry.set_serial_no_batch_for_finished_good()
	stock_entry.save()
	frappe.msgprint(f"""Stock Entry Created: {get_link_to_form("Stock Entry" ,stock_entry.name)}""")
	return

def validate(doc, event):
	for i in doc.time_logs:
		i.final_qty = i.completed_qty - (i.get('excess_qty') or 0) + (i.get('shortage_qty') or 0)