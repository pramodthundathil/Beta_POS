from django.urls import path 
from .import views  



urlpatterns = [

    path("POS",views.POS,name="POS")
]