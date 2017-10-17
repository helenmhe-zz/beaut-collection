from django.conf.urls import url
from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<type_id>[0-9]+)/$', views.category_overview, name='category'),
    url(r'^(?P<type_id>[0-9]+)/(?P<product_id>[0-9]+)/$', views.detail, name='detail')
]
