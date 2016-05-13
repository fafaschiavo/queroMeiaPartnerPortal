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

