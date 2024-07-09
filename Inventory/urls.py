from django.urls import path 
from .import views  



urlpatterns = [

    # vendor management ..............................
    path("add_vendor",views.add_vendor,name="add_vendor"),
    path("list_vendor",views.list_vendor,name="list_vendor"),


    #product management........................................
    path('add-category/', views.add_category, name='add_category'),
    path("list_category/",views.list_category,name="list_category"),
    path("list_products",views.list_products,name="list_products"),
    path("add_product",views.add_product,name="add_product"),

    path('AddTax', views.AddTax, name='AddTax'),
    path('ListTax', views.ListTax, name='ListTax'),


    path("add_customer/<int:pk>",views.add_customer,name="add_customer"),
    path("list_customer",views.list_customer,name="list_customer"),
]