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
    


    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('otp', views.send_otp, name='otp'),
    # path('otp_verification',views.otp_verification,name="otp_verification")

    # path('admin_login', views.admin_login, name='admin_login'),
    # path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    # path('admin_logout', views.admin_logout, name='admin_logout'),
]
