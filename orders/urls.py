from django.contrib import admin
from django.conf.urls import url, include

from orders import views

urlpatterns = [
    url(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^admin_orders/$', views.admin_orders, name='admin_orders'),
]