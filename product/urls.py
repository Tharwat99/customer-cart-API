from django.urls import path
from .views import ProductListView, ProductCreateView
urlpatterns = [
    path('list/',ProductListView.as_view(), name='product_list'),
    path('create/',ProductCreateView.as_view(), name='product_create'),
]