from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.contrib import messages, auth
from .models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            request.session['email'] = email
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            send_otp(request)
            messages.success(request, 'otp is sent to your email please verify')
            return render(request, 'accounts/otp.html' , {'email':email} )
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render (request, 'accounts/register.html', context)

@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are Logged In")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render (request, 'accounts/login.html')


def send_otp(request):
    s=""
    for x in range(0,6):
        s+=str(random.randint(1,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'fathimaakifa35@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"accounts/otp.html")

def  otp_verification(request):
    user = Account.objects.get(email=request.session['email'])
    if  request.method=='POST':
        user = Account.objects.get(email=request.session['email'])
        otp_=request.POST.get("otp")
        if otp_ == request.session["otp"]:
            user.is_active=True
            user.save()
            del request.session['email']
            del request.session['otp']
            messages.info(request,'"Your OTP has been verified. Please login." ')
            return redirect('login')
        else:
            messages.error(request,"otp doesn't match")
            return render(request,'accounts/otp.html')
    else:
        user.delete()
        del request.session['email']
        return redirect('login')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "You are Logged out")
    return redirect('login')


# # VERIFICATION EMAIL
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import EmailMessage


# def register(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = email.split("@")[0]
#             user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#             user.phone_number = phone_number
#             user.save()

#             #USER ACTIVATION

#             current_site = get_current_site(request)
#             mail_subject = "Please activate your account"
#             message = render_to_string('accounts/account_verification_email.html', {
#                 'user': user,
#                 'domain': current_site,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()
#             return redirect('/accounts/login?command=verification&email='+email)
#     else:
#         form = RegistrationForm()
#     context = {
#         'form':form,
#     }
#     return render (request, 'accounts/register.html', context)

# def login(request):

#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             auth.login(request, user)
#             messages.success(request, "You are Logged In")
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return redirect('login')
#     return render (request, 'accounts/login.html')


# def activate(request,uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulations! Your account is activated.')
#         return redirect('login')
#     else:
#         messages.error(request, "Invalid activation link")
#         return redirect('register')

# @login_required(login_url='login')
# def logout(request):
#     auth.logout(request)
#     messages.info(request, "You are Logged out")
#     return redirect('login')
