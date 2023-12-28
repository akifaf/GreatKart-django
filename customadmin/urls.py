from django.urls import path
from . import views

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('admin_logout', views.admin_logout, name='admin_logout'),

    path('user_management', views.user_management, name='user_management'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('block_user/<int:pk>/', views.block_user, name='block_user'),
    path('unblock_user/<int:pk>/', views.unblock_user, name='unblock_user'),

    path('product', views.product, name='product'),
    path('prod_gallery', views.prod_gallery, name='prod_gallery'),
    path('add_prod_gallery', views.add_prod_gallery, name='add_prod_gallery'),
    path('add_product', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('undelete_product/<int:pk>/', views.undelete_product, name='undelete_product'),

    path('category', views.category, name='category'),
    path('add_category', views.add_category, name='add_category'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('undelete_category/<int:pk>/', views.undelete_category, name='undelete_category'),

    path('order_management', views.order_management, name='order_management'),
    path('view_order_detail/<int:order_id>/', views.view_order_detail, name='view_order_detail'),
    path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('admin_cancel_order/<int:order_id>/', views.admin_cancel_order, name='admin_cancel_order'),
    path('view_return_order/<int:order_id>/', views.view_return_order, name='view_return_order'),
    path('admin_grant_return_request/<int:order_id>/', views.admin_grant_return_request, name='admin_grant_return_request'),

]
