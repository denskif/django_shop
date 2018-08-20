from django.contrib import admin
from django.conf.urls import url, include

from products import views

urlpatterns = [
    # url(r'^landing', views.landing, name='landing'),
    url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
]