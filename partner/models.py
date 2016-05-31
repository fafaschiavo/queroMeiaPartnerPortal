from __future__ import unicode_literals

from django.db import models

# Create your models here.
class partners(models.Model):
	hash_id = models.CharField(max_length=200, default=None)
	is_active = models.IntegerField(default=1)
	share = models.IntegerField(default=10)
	portal_name = models.CharField(max_length=200)
	portal_type = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __hash_id__(self):
		return self.hash_id

	def __is_active__(self):
		return self.is_active

	def __share__(self):
		return self.share

	def __portal_name__(self):
		return self.name

	def __portal_type__(self):
		return self.portal_type

	def __created_at__(self):
		return self.created_at

class responsable(models.Model):
	partner_id = models.IntegerField(default=0)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	zip_code = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	username = models.CharField(max_length=200)
	email_activated = models.IntegerField(default=0)
	hash_id = models.CharField(max_length=200, default=None)

	def __partner_id__(self):
		return self.partner_id

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email

	def __phone__(self):
		return self.phone

	def __zip_code__(self):
		return self.zip_code

	def __created_at__(self):
		return self.created_at

	def __username__(self):
		return self.username

	def __email_activated__(self):
		return self.email_activated

class payment_request(models.Model):
	partner_id = models.IntegerField(default=0)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	request_type = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	is_paid = models.IntegerField(default=0)
	paid_at = models.DateTimeField(auto_now=True)
	email_paypal = models.CharField(max_length=200, default = '')
	name_owner = models.CharField(max_length=400, default = '')
	cpf = models.CharField(max_length=200, default = '')
	agency = models.CharField(max_length=200, default = '')
	account = models.CharField(max_length=200, default = '')
	bank = models.CharField(max_length=200, default = '')

	def __partner_id__(self):
		return self.partner_id

	def __amount__(self):
		return self.amount

	def __request_type__(self):
		return self.request_type

	def __created_at__(self):
		return self.created_at

	def __is_paid__(self):
		return self.is_paid

	def __email_paypal__(self):
		return self.email_paypal

	def __name_owner__(self):
		return self.name

	def __cpf__(self):
		return self.cpf

	def __agency__(self):
		return self.agency

	def __account__(self):
		return self.account

	def __bank__(self):
		return self.bank