from cinema.models import members, orders, products, tickets, bad_requests
from partner.models import partners, responsable, payment_request
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
import string
import random
import base64
import hmac, hashlib

# Create your procedures here.

def hash_id_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_responsable_hash_id():
	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator()
		try:
			responsable = responsable.objects.all(hash_id = new_hash_id)
		except:
			verify_existence = False
	return new_hash_id

def generate_partner_hash_id():
	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator()
		try:
			partner = partners.objects.all(hash_id = new_hash_id)
		except:
			verify_existence = False
	return new_hash_id

def verify_username(request):
	username_try = request.GET['username']
	result = responsable.objects.filter(username = username_try)
	if len(result) > 0:
		return HttpResponse (400)
	else:
		return HttpResponse (200)

def verify_email(request):
	email_try = request.GET['email']
	result = responsable.objects.filter(email = email_try)
	if len(result) > 0:
		return HttpResponse (400)
	else:
		return HttpResponse (200)

def create_new_responsable(username, password, first_name, last_name, email, phone, zip_code, partner_id):
	hash_id = generate_responsable_hash_id()
	new_responsable = responsable(first_name = first_name, last_name = last_name, email = email, phone = phone, hash_id = hash_id, username = username, zip_code = zip_code, partner_id = partner_id)
	new_responsable.save()
	user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
	user.save()
	return 200

def create_new_partner(portal_name, portal_type, share=10):
	hash_id = generate_partner_hash_id()
	new_partner = partners(portal_name = portal_name, portal_type = portal_type, share = share, hash_id = hash_id)
	new_partner.save()
	return new_partner

def mandrill_send_payment_request(info):
	msg = EmailMessage(subject="Requisicao de Pagamento de Parceiro", from_email="QueroMeia <atendimento@queromeia.com>", to=["atendimento@queromeia.com"])
	msg.template_name = "payment-request"
	msg.global_merge_vars = {'INFO': info}
	msg.send()
	return None

def add_payment_request(partner_id, amount, request_type, hash_id):
	new_request = payment_request(partner_id = partner_id, amount = amount, request_type = request_type)
	new_request.save()
	partner_buys = orders.objects.filter(partner_hash_id = hash_id, status_paypal = 'Completed', payment_request_id = 0)
	for order in partner_buys:
		order.payment_request_id = new_request.id
		order.save()
	return new_request.id

# Create your views here.
def index(request):
	context = {}
	q = members.objects.all()
	return render(request, "home.html", context)

def contact(request):
	context = {}
	return render(request, "contact.html", context)

def new_partner(request):
	context = {}
	return render(request, "new-partner.html", context)

def include_new_partner(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	username = request.POST['username']
	password = request.POST['password']
	phone = request.POST['phone']
	zip_code = request.POST['zip_code']
	portal_name = request.POST['portal_name']
	portal_type = request.POST['portal_type']
	new_partner = create_new_partner(portal_name, portal_type)
	create_new_responsable(username, password, first_name, last_name, email, phone, zip_code, new_partner.id)
	user = authenticate(username=username, password=password)
	if user is not None:
	    if user.is_active:
	        login(request, user)
	        return HttpResponseRedirect('/dashboard/')
	    else:
	        context = {'error_credentials': 1}
	        return render(request, "new-partner.html", context)
	else:
	    context = {'error_credentials': 1}
	    return render(request, "new-partner.html", context)

def login_user(request):
	context = {}
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
	    if user.is_active:
	        login(request, user)
	        return HttpResponseRedirect('/dashboard/')
	    else:
	        context = {'error_credentials': 1}
	        return render(request, "home.html", context)
	else:
	    context = {'error_credentials': 1}
	    return render(request, "home.html", context)

def logout_user(request):
	logout(request)
	context = {}
	return render(request, "home.html", context)

@login_required
def dashboard(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id

	partner_orders = orders.objects.filter(partner_hash_id = hash_id)
	total_visits = len(partner_orders)/2
	total_visits = int(total_visits)

	partner_buys = orders.objects.filter(partner_hash_id = hash_id, status_paypal = 'Completed')
	number_partner_buys = len(partner_buys)

	cursor = connection.cursor()
	query = 'select sum(amount) as total from cinema_orders where status_paypal = "Completed" and partner_hash_id = "' + hash_id + '" and payment_request_id = 0;'
	cursor.execute(query)
	total_amount = cursor.fetchone()
	total_amount_sold = total_amount[0]
	partner_share = partner.share
	share_multiplier = float(partner_share) / 100
	if total_amount_sold != None:
		total_share_amount = float(total_amount_sold) * share_multiplier
		total_share_amount = round(total_share_amount, 2)
	else:
		total_share_amount = 0

	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id,
	'total_visits': total_visits,
	'number_partner_buys': number_partner_buys,
	'total_share_amount': total_share_amount
	}
	return render(request, "dashboard.html", context)

@login_required
def contact_dashboard(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id
	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id
	}
	return render(request, "contact-dashboard.html", context)

@login_required
def banners(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id
	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id
	}
	return render(request, "banners-dashboard.html", context)

@login_required
def password_change(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id
	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id
	}
	return render(request, "password-change.html", context)

@login_required
def password_update(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id

	try:
		password = request.POST['password']
		u = User.objects.get(username= username)
		u.set_password(password)
		u.save()
		success_password_reset = 1
	except:
		success_password_reset = 2

	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id,
	'success_password_reset': success_password_reset
	}
	return render(request, "password-change.html", context)

@login_required
def require_payment(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id

	partner_orders = orders.objects.filter(partner_hash_id = hash_id)
	total_visits = len(partner_orders)/2
	total_visits = int(total_visits)

	partner_buys = orders.objects.filter(partner_hash_id = hash_id, status_paypal = 'Completed')
	number_partner_buys = len(partner_buys)

	cursor = connection.cursor()
	query = 'select sum(amount) as total from cinema_orders where status_paypal = "Completed" and partner_hash_id = "' + hash_id + '" and payment_request_id = 0;'
	cursor.execute(query)
	total_amount = cursor.fetchone()
	total_amount_sold = total_amount[0]
	partner_share = partner.share
	share_multiplier = float(partner_share) / 100
	if total_amount_sold != None:
		total_share_amount = float(total_amount_sold) * share_multiplier
		total_share_amount = round(total_share_amount, 2)
	else:
		total_share_amount = 0

	minimun = 0
	if total_share_amount >= 10:
		minimun = 1

	context = {
	'name': name,
	'email': user.email,
	'partner_link': hash_id,
	'minimun': minimun
	}
	return render(request, "require-payment.html", context)

def payment_required(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id

	partner_orders = orders.objects.filter(partner_hash_id = hash_id)
	total_visits = len(partner_orders)/2
	total_visits = int(total_visits)

	partner_buys = orders.objects.filter(partner_hash_id = hash_id, status_paypal = 'Completed')
	number_partner_buys = len(partner_buys)

	cursor = connection.cursor()
	query = 'select sum(amount) as total from cinema_orders where status_paypal = "Completed" and partner_hash_id = "' + hash_id + '" and payment_request_id = 0;'
	cursor.execute(query)
	total_amount = cursor.fetchone()
	total_amount_sold = total_amount[0]
	partner_share = partner.share
	share_multiplier = float(partner_share) / 100
	if total_amount_sold != None:
		total_share_amount = float(total_amount_sold) * share_multiplier
		total_share_amount = round(total_share_amount, 2)
	else:
		total_share_amount = 0

	name = request.POST['name']
	cpf = request.POST['cpf']
	agency = request.POST['bank-agency']
	account = request.POST['bank-account']
	bank = request.POST['bank']
	info = 'Nome: ' + name + ' CPF: ' + cpf + ' Agencia: ' + agency + ' Conta: ' + account + ' Banco: ' + bank + ' Valor: ' + str(total_share_amount)   
	mandrill_send_payment_request(info)
	request_id = add_payment_request(user.partner_id, total_share_amount, 'banco', hash_id)
	payment_request_object = payment_request.objects.get(id = request_id)
	payment_request_object.name_owner = name
	payment_request_object.cpf = cpf
	payment_request_object.agency = agency
	payment_request_object.account = account
	payment_request_object.bank = bank
	payment_request_object.save()
	minimun = 2
	context = {
	'name': name,
	'email': user.email,
	'minimun': minimun
	}
	return render(request, "require-payment.html", context)

def payment_required_paypal(request):
	username = request.user
	result = responsable.objects.filter(username = username)
	user = result[0]
	name = user.first_name + ' ' + user.last_name
	name = name.title()
	partner_result = partners.objects.filter(id = user.partner_id)
	partner = partner_result[0]
	hash_id = partner.hash_id

	partner_orders = orders.objects.filter(partner_hash_id = hash_id)
	total_visits = len(partner_orders)/2
	total_visits = int(total_visits)

	partner_buys = orders.objects.filter(partner_hash_id = hash_id, status_paypal = 'Completed')
	number_partner_buys = len(partner_buys)

	cursor = connection.cursor()
	query = 'select sum(amount) as total from cinema_orders where status_paypal = "Completed" and partner_hash_id = "' + hash_id + '" and payment_request_id = 0;'
	cursor.execute(query)
	total_amount = cursor.fetchone()
	total_amount_sold = total_amount[0]
	partner_share = partner.share
	share_multiplier = float(partner_share) / 100
	if total_amount_sold != None:
		total_share_amount = float(total_amount_sold) * share_multiplier
		total_share_amount = round(total_share_amount, 2)
	else:
		total_share_amount = 0
	email_paypal = request.POST.get('email-paypal', 'Null')
	info = 'Email PayPal: ' + email_paypal + ' Value: ' + str(total_share_amount)
	if total_share_amount != 0:
		mandrill_send_payment_request(info)
		request_id = add_payment_request(user.partner_id, total_share_amount, 'paypal', hash_id)
		payment_request_object = payment_request.objects.get(id = request_id)
		payment_request_object.email_paypal = email_paypal
		payment_request_object.save()
	minimun = 2
	context = {
	'name': name,
	'email': user.email,
	'minimun': minimun
	}
	return render(request, "require-payment.html", context)