from django.urls import path
from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout', views.admin_logout, name='admin_logout'),

    path('user_management', views.user_management, name='user_management'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('block_user/<int:pk>/', views.block_user, name='block_user'),
    path('unblock_user/<int:pk>/', views.unblock_user, name='unblock_user'),

    path('product', views.product, name='product'),
    path('add_product', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('undelete_product/<int:pk>/', views.undelete_product, name='undelete_product'),

    path('category', views.category, name='category'),
     path('add_category', views.add_category, name='add_category'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('undelete_category/<int:pk>/', views.undelete_category, name='undelete_category'),
]
