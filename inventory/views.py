from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import *

def index(request):
    latest_product_list = Product.objects.order_by('-date_obtained')
    context = {
        'latest_product_list': latest_product_list,
    }
    return render(request, 'inventory/index.html', context)

def detail(request, type_id, product_id):
    product = get_object_or_404(Product, pk=product_id)
    grade = dict(PRODUCT_GRADES)[product.rating]
    return render(request, 'inventory/detail.html', {'product': product, 'grade':grade})

def category_overview(request, type_id):
    return HttpResponse("You're looking at all of your %s products" % type_id)
