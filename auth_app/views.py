from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm, TeacherForm
from django.contrib.auth.models import User
from .models import Teacher

def login_home(request):
    # Django Django987&
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
                    print(form.errors)
                    return redirect('login')
                
            else:   
                messages.warning(request, 'Invalid username or password')

        else:
            print(form.errors)
            messages.error(request, 'Form is invalid')
    else:
        form = LoginForm()  # Initialize the form for GET requests (page load)
    return render(request, 'auth_app/login.html', {'form': form})

@login_required
def admin_page(request):
    return render(request,'auth_app/admin.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def register_page(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email= form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            user= User.objects.create_user(username=username,email=email,password=password1, first_name=first_name, last_name=last_name,)    
            messages.success(request, "User has been successfully registered! Please Login")
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html',{'form':form})

@login_required 
def teacher_detail(request):
    user_list = User.objects.exclude(is_superuser=True)
    print(user_list)
    
    if request.method == 'POST':
        print(request.POST)  # Debug: Print POST data
        print(request.FILES)
        form  = TeacherForm(request.POST, request.FILES)  
        if form.is_valid():
            print("Cleaned Data")
            print("********")
            print(form.cleaned_data)
            user = form.cleaned_data['teacher']
            address = form.cleaned_data['address']
            primary_number = form.cleaned_data['primary_number']
            secondary_number = form.cleaned_data['secondary_number']
            dob = form.cleaned_data['dob']
            sex = form.cleaned_data['sex']
            image = form.cleaned_data['image']

            if Teacher.objects.filter(user = user).exist():
                print("user already exists")
                form.add_error('teacher', f'user with {user.username} already exists')
            else:
                Teacher.objects.create(user=user, address=address, primary_number=primary_number, secondary_number=secondary_number,dob=dob, sex=sex,image=image)
                messages.success(request, "Teacher has been successfully added!")
        else:
            messages.error(request, "There was an error with the form. Please try again.")
            print(form.errors)

    else:
        form=TeacherForm()
    return render(request, 'auth_app/teacher.html', {'teachers': user_list, 'form':form})

def teacher_image(request):
    teacher = Teacher.objects.all()
    for item in teacher:
        print(item.image.url)
    return render(request, 'auth_app/')

