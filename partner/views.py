from cinema.models import members, orders, products, tickets, bad_requests
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.


def index(request):
	context = {}
	q = members.objects.all()
	print q
	return render(request, "home.html", context)
