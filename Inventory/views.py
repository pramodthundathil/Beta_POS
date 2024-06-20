from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import ProductForm

# Create your views here.


########################################## vendor management ############################################
# 

def add_vendor(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gst_number = request.POST['gst_number']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        contact_info = request.POST.get('contact_info', '')
        supply_product = request.POST['supply_product']

        vendor = Vendor(
            name=name,
            email=email,
            phone_number=phone,
            gst_number=gst_number,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            contact_info=contact_info,
            supply_product=supply_product,
        )
        vendor.save()
        messages.success(request, 'Vendor added successfully')
        return redirect('list_vendor')
    return render(request,"add-vendor.html") 

def list_vendor(request):
    vendor = Vendor.objects.all()

    context = {
        "vendor":vendor
    }
    return render(request,'list-vendors.html',context)



############################ Product Management #################################


def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        active = 'active' in request.POST

        category = ProductCategory(
            name=name,
            active=active,
        )
        category.save()
        messages.success(request, 'Category added successfully')
        return redirect('list_category')

    return render(request, 'add-category.html')


def list_category(request):
    category = ProductCategory.objects.all()
    context = {
        "category":category
    }
    return render(request,"list-category.html",context)



def list_products(request):
    product = Product.objects.all()
    context = {
        "product":product
    }
    return render(request,'list-product.html',context)


def add_product(request):
    food_category = ProductCategory.objects.all()
    tax = Tax.objects.all()
    description = " "
    if request.method == "POST":
        name = request.POST['name']
        category = ProductCategory.objects.get(id = int(request.POST['category']))
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES['pic']
        description = request.POST['description']
        tax_name = request.POST["tax_name"]
        tax_value = request.POST["tax_value"]

        menu = Product.objects.create(
            name = name, 
            category = category, 
            image = image, 
            price = price, 
            stock = stock, 
            description = description,
            tax = tax_name,
            tax_value = Tax.objects.get(id = int(tax_value))

            )
        menu.save()
        messages.success(request,"Product  added Success...")
        return redirect("list_products")
    
    context = {
        "food_category":food_category,
        "tax":tax

    }
    return render(request,'add-product.html',context)


def AddTax(request):
    if request.method == "POST":
        name = request.POST.get('name')
        tax_rate = request.POST.get('tax')
        tax = Tax.objects.create(tax_name = name,tax_percentage = tax_rate )
        tax.save()
        messages.success(request,'Tax Value Added Success')
        return redirect("ListTax")
    return render(request,"add-tax-slab.html")

def ListTax(request):
    tax = Tax.objects.all()
    context = {
        "tax":tax
    }
    return render(request,"list-tax.html",context)


def invoice(request):
    return render(request,"invoice.html")