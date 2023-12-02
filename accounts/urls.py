from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('otp', views.send_otp, name='otp'),
    path('otp_verification',views.otp_verification,name="otp_verification"),

    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('otp', views.send_otp, name='otp'),
    # path('otp_verification',views.otp_verification,name="otp_verification")

    # path('admin_login', views.admin_login, name='admin_login'),
    # path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    # path('admin_logout', views.admin_logout, name='admin_logout'),
]
