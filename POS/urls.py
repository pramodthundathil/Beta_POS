from django.urls import path 
from .import views  



urlpatterns = [

    path("POS/<int:pk>",views.POS,name="POS"),
    path("search_product",views.search_product,name="search_product"),
    path("CreateOrder",views.CreateOrder,name="CreateOrder"),
    path("list_sale",views.list_sale,name="list_sale"),
    path("update_order",views.update_order,name="update_order"),
    path('update_order_customer',views.update_order_customer, name='update_order_customer'),
    path('add_order_item/<int:pk>', views.add_order_item, name='add_order_item'),
    path('update_order_item_quantity', views.update_order_item_quantity, name='update_order_item_quantity'),
    
]