from django.urls import path
from . import views

urlpatterns = [
    path('shipping_address', views.shipping_address, name='shipping_address'),
    path('place_order/', views.place_order, name='place_order'),
    path('cod/<int:order_id>', views.cod, name='cod'),
    path('payments', views.payments, name='payments'),
    path('order_complete', views.order_complete, name='order_complete'),
]