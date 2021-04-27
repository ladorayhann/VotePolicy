from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    if 'logged_in' not in request.session:
        return redirect('login')
    return render(request, 'home.html')

@csrf_exempt
def login(request):
    if 'logged_in' in request.session:
        return redirect('home')
    else:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                pengguna = User.objects.get(email=email)
                username = pengguna.username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    request.session['user_id'] = user.pk
                    request.session['logged_in'] = True
                    request.session['username'] = username
                    return redirect('home')
                else:
                    messages.error(request, "Email/Password salah", extra_tags="failed")
                    return redirect('login')
            messages.error(request, "Input yang Anda masukan salah", extra_tags="failed")
            return redirect('login')

        context = {'form':form}
        return render(request, 'login.html', context)

@csrf_exempt    
def register(request):
    if 'logged_in' in request.session:
        return redirect('home')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            check = request.POST.get('chk')
            if check == "True":
                form.save()
                messages.success(request, "Berhasil daftar akun", extra_tags="success")
                return redirect('login')
            messages.error(request, "Klik Checkbox Syarat Dahulu", extra_tags="failed")
            return redirect('register')
        
        user = User.objects.filter(username=request.POST["username"])
        if len(user) > 0:
            messages.error(request, "Nama sudah digunakan", extra_tags="failed")
            return redirect('register')
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "Kata sandi tidak cocok", extra_tags="failed")
            return redirect('register')
        if request.POST['password1'] == request.POST['password2'] and len(request.POST['password1']) < 8:
            messages.error(request, "Kata sandi setidaknya memiliki 8 karakter", extra_tags="failed")
            return redirect('register')
        

    context = {'form':form}
    return render(request, 'register.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login')

