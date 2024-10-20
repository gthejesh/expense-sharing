from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user == None:
                name = form.cleaned_data['name']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']
                
                user = User(email=email, name=name, mobile_number=mobile_number)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful. Login to continue.')
                return redirect('login')
            elif user.password == None:
                name = form.cleaned_data['name']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']

                user = User.objects.get(email=email)
                user.name = name
                user.mobile_number = mobile_number
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful. Login to continue.')
                return redirect('login')

            else:
                messages.error(request, 'User already exists.')
                return redirect('register')
    else:
        form = RegistrationForm()

    return render(request, 'expenses/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email=='' or password=='':
                messages.error(request, 'Email and password are required.')
            try:
                user = User.objects.get(email=email)
                if(user):
                    if user.password == None:
                        messages.error(request, 'User needed to register.')
                        return redirect('register')
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
    elif 'user_id' in request.session:
        return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'expenses/login.html', {'form': form})

def logout(request):
    if('user_id' in request.session):
        del request.session['user_id']
    return redirect('login')
    