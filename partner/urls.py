from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new-partner-user/$', views.new_partner, name='new_partner'),
    url(r'^include-new-partner-user/$', views.include_new_partner, name='include_new_partner'),
    url(r'^verify-username/', views.verify_username, name='verify_username'),
    url(r'^verify-email/', views.verify_email, name='verify_email'),
]