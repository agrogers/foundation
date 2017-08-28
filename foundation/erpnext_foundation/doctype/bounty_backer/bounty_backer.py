# -*- coding: utf-8 -*-
# Copyright (c) 2017, EOSSF and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BountyBacker(Document):
	def validate(self):
		self.parenttype = 'Bounty'
		self.parentfield = 'bounty_backer'
		self.parent = self.bounty_name

		doc = frappe.get_doc('Bounty', self.bounty_name)
		self.idx = len(doc.bounty_backer)

	def on_payment_authorized(self, status_changed_to=None):
		if status_changed_to in ("Completed", "Authorized"):
			self.db_set('paid', 1)
			# to trigger form events of Bounty doctype
			doc = frappe.get_doc('Bounty', self.bounty_name)
			doc.save()
			return '/' + doc.route
		return '/bounties'

