from django.shortcuts import render, redirect
from Inventory.models import *
from django.http import JsonResponse
from datetime import datetime
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string





# Create your views here.
def generate_serial_number():
        current_time = datetime.now()
        serial_number = current_time.strftime("%Y%m%d%H%M%S")
        return serial_number


def CreateOrder(resuest):
    TokenU = generate_serial_number()

    order = Order.objects.create(invoice_number=TokenU)
    order.save()

    return redirect(POS,pk = order.id)
     

def POS(request,pk):
    customer = Customer.objects.all()
    order = Order.objects.get(id = pk)
    product = Product.objects.all()

    context = {
        "customer":customer,
        "order":order,
        'product':product
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


@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            # Assuming you have a way to get the current order, e.g., through session or context
            order = Order.objects.get(id = order_id)
            order.customer = customer
            order.save()
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def update_order_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            customer = Customer.objects.get(id=customer_id)
            order.customer = customer
            order.save()
            customer_details_html = render_to_string('ajaxtemplates/customerdetailsonpos.html', {'customers': customer,"order" : order})
            print(customer_details_html)
            return JsonResponse({"success": True, "html": customer_details_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Customer not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})



def AddItemsToorder(reuest):
     return redirect('POS',pk=10)



def list_sale(request):
    order = Order.objects.all()

    context = {
         "order":order
    }
    return render(request,'list-sale.html',context)



@csrf_exempt
def add_order_item(request,pk):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print(product_id,")))))))))))))))))))))))))))))))))))))))))))")
        try:
            order = Order.objects.get(id=pk)
            product = Product.objects.get(id=product_id)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                order_item.quantity += 1
                order_item.save()
            
            # Update order totals
            order.update_totals()
            
            # Render the order items table
            order_items_html = render_to_string('ajaxtemplates/order_items_table.html', {'order': order})
            return JsonResponse({"success": True, "html": order_items_html})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt
def update_order_item_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        try:
            order_item = OrderItem.objects.get(id=item_id)
            if action == 'increase':
                order_item.quantity += 1
            elif action == 'decrease' and order_item.quantity > 1:
                order_item.quantity -= 1
            order_item.save()

            # Update order totals
            order_item.order.update_totals()

            # Render the order items table
            order_items_html = render_to_string('order_items_table.html', {'order': order_item.order})
            return JsonResponse({"success": True, "html": order_items_html})
        except OrderItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


