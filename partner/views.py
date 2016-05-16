from cinema.models import members, orders, products, tickets, bad_requests
from partner.models import partners, responsable
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
	context = {}
	return render(request, "dashboard.html", context)