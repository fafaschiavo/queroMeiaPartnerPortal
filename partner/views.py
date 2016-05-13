from cinema.models import members, orders, products, tickets, bad_requests
from partner.models import partners, responsable
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings
import string
import random
import base64
import hmac, hashlib

# Create your procedures here.

def hash_id_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_member_hash_id():

	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator()
		try:
			member = members.objects.all(hash_id = new_hash_id)
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

def create_new_member(username, password, first_name, last_name, email, phone, zip_code):
	hash_id = generate_member_hash_id()
	# if phone == False:
	# 	phone = ''
	# if email == False:
	# 	email = ''
	new_member = responsable(first_name = first_name, last_name = last_name, email = email, phone = phone, hash_id = hash_id, username = username, zip_code = zip_code)
	new_member.save()
	user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
	user.save()
	return 200

# Create your views here.
def index(request):
	context = {}
	q = members.objects.all()
	print q
	return render(request, "home.html", context)

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
	create_new_member(username, password, first_name, last_name, email, phone, zip_code)
	return HttpResponse('Sucesso')