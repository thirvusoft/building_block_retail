# Copyright (c) 2022, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GP_Test(Document):
	pass
	
def before_insert(self, action):
	if(self.is_private==1):
		print('before\n'*5)
		print(self.is_private)
		print(self.file_url)
		self.is_private=0
		print(self.__dict__)
		print('\n'*5)
	
def after_insert(self, action):
	print('after\n'*5)
	print(self.is_private)
	print(self.file_url)
	print('\n'*5)