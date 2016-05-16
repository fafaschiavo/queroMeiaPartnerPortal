from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new-partner-user/$', views.new_partner, name='new_partner'),
    url(r'^include-new-partner-user/$', views.include_new_partner, name='include_new_partner'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^login-user/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^verify-username/', views.verify_username, name='verify_username'),
    url(r'^verify-email/', views.verify_email, name='verify_email'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^contact-dashboard/', views.contact_dashboard, name='contact_dashboard'),
    url(r'^banners/', views.banners, name='banners'),
]