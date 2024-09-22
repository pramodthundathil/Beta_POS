from django.urls import path, include
from .import views 
from .api import api_views
from django.urls import path 
# serializer view__________________________________

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




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

    # purchases....................

    path("purchase",views.purchase,name="purchase"),
    path("add_purchase",views.add_purchase,name="add_purchase"),


    #api datas

    path("product_list",api_views.product_list,name="product_list"),
    path("product_detail/<int:pk>",api_views.product_detail,name="product_detail"),
    path("product_add",api_views.product_add,name="product_add"),
    path("product_add_new",api_views.ProductListCreateView.as_view(),name="product_add_new"),

]

urlpatterns += [
    path('api/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
