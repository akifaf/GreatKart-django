from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    path('otp', views.send_otp, name='otp'),
    path('otp_verification',views.otp_verification,name="otp_verification"),
    path('forgotPassword',views.forgotPassword,name="forgotPassword"),
    path('resetPassword',views.resetPassword,name="resetPassword"),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),

    path('my_orders', views.my_orders, name='my_orders'),
    path('my_wallet', views.my_wallet, name='my_wallet'),
    path('my_address', views.my_address, name='my_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('request_refund/<int:order_id>/', views.request_refund, name='request_refund'),
    


    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('otp', views.send_otp, name='otp'),
    # path('otp_verification',views.otp_verification,name="otp_verification")

    # path('admin_login', views.admin_login, name='admin_login'),
    # path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    # path('admin_logout', views.admin_logout, name='admin_logout'),
]
