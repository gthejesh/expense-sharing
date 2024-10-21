from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import RegistrationForm, LoginForm

# Method to register a new user
def register(request):
    if request.method == 'POST':
        #on registration form submission
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user is None:
                # Create new user
                name = form.cleaned_data['name']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']
                
                user = User(email=email, name=name, mobile_number=mobile_number)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful. Login to continue.')
                return redirect('login')
            elif user.password is None:
                # Update existing user, created for an expense by another user, without password
                name = form.cleaned_data['name']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']

                user.name = name
                user.mobile_number = mobile_number
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful. Login to continue.')
                return redirect('login')
            else:
                # User already exists error handle
                messages.error(request, 'User already exists.')
                return redirect('register')
    else:
        # GET request 
        form = RegistrationForm()

    return render(request, 'expenses/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        #on login form submission
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email == '' or password == '':
                messages.error(request, 'Email and password are required.')
            try:
                user = User.objects.get(email=email)
                if user.password is None:
                    #if user created, for an expense by another user
                    messages.error(request, 'User needed to register.')
                    return redirect('register')
                if user.check_password(password):
                    #else proceed to check password and creates session
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    #if password is incorrect
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                #if user does not exist
                messages.error(request, 'User does not exist.')
    elif 'user_id' in request.session:
        #if user is already logged in
        return redirect('home')
    else:
        #GET request
        form = LoginForm()
    
    return render(request, 'expenses/login.html', {'form': form})

def logout(request):
    #handling logout, clear sessions
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')
