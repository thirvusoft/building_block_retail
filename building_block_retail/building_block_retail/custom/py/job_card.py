import frappe
from frappe.desk.form import assign_to
from frappe import _, bold
from frappe.model.document import Document
from frappe.utils.data import get_link_to_form
from erpnext.manufacturing.doctype.job_card.job_card import JobCard
class Jobcard(JobCard):
	def validate(self):
		# self.validate_time_logs()
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