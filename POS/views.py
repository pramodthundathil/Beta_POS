from django.shortcuts import render, redirect
from Inventory.models import *
from django.http import JsonResponse

# Create your views here.

def POS(request):
    customer = Customer.objects.all()

    context = {
        "customer":customer
    }
    return render(request,'pos.html',context)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def search_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'search' in request.GET:
        query = request.GET.get('search', '')
        products = Product.objects.filter(name__icontains=query, status=True)
        product_list = [{
            'name': product.name,
            'price': product.price,
            'tax': product.tax_amount,
            'stock': product.stock,
        } for product in products]
        return JsonResponse({'products': product_list})
    return JsonResponse({'products': []})
