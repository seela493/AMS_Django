from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

def login_home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    messages.success(request, "You have successfully logged in Admin!")
                    return redirect('admin')
                else:
                    print("Not Admin")
                    return redirect('login')
                
            else:
                messages.warning(request, 'Invalid username or password')

        else:
            messages.error(request, 'Form is invalid')
    else:
        form = LoginForm()  # Initialize the form for GET requests (page load)
    return render(request, 'auth_app/login.html', {'form': form})

# def login_home(request):
#     next = request.GET.get('next')
#     if request.method == 'POST':
#         form = LoginForm(request.POST)

#         print("Post Request Form")
#         # print(form)

#         if form.is_valid():
#             print(form.cleaned_data)
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 print("User is authenticated")
#                 login(request, user)
#                 if user.is_superuser:
#                     return redirect('admin')
#                 # return redirect(next if next else 'admin-page-name')
#                 else:
#                     print("Not Admin")
#                     return redirect('login')
#             else:
#                 print("User is not authenticated")
#         else:
#             print("Form is invalid")
#     else: 
#         form = LoginForm()
#         print(f"Get Request Form")
#         # print(form

#     return render(request, 'auth_app/login.html', {'form': form})   


def admin_page(request):
    return render(request,'auth_app/admin.html')

def logout_page(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email= form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 != password2:
                messages.error(request,"The Password does not match")
                return redirect('register')
            if len(password1 & password2 >8):
                messages.error(request,"The length of the password should be atleast more than 8")
                return redirect('register')

            user= User.object.create_user(username=username,email=email,password=password1)
            user.save()

            messages.success(request, "User has been successfully registered! Please Login")
            return redirect('login')
        
        else:
            messages.error(request, "Form is invalid")
            form = RegisterForm()
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html')