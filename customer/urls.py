from django.urls import path
from .views import CustomerListView, CustomerCreateView
urlpatterns = [
    path('customer-list/',CustomerListView.as_view(), name='customer_list'),
    path('customer-create/',CustomerCreateView.as_view(), name='customer_create'),
]