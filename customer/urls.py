from django.urls import path
from .views import CustomerListView, CustomerCreateView
urlpatterns = [
    path('list/',CustomerListView.as_view(), name='customer_list'),
    path('create/',CustomerCreateView.as_view(), name='customer_create'),
]