from vote.models import Category, StatusJapat, Japat
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Japat

# Create your views here.
def home(request):
    japats = Japat.objects.all().order_by('-voters')[:5]
    return render(request, 'home.html', {"japats":japats})

@csrf_exempt
def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
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
            except:
                messages.error(request, "Email/Password salah", extra_tags="failed")
                return redirect('login')
        messages.error(request, "Input yang Anda masukan salah", extra_tags="failed")
        return redirect('login')

    context = {'form':form}
    return render(request, 'login.html', context)

@csrf_exempt    
def register(request):
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

# progress
def campaign_make(request):
    if 'logged_in' not in request.session:
        return redirect('login')
    if request.method == 'POST':        
        category = None
        if request.POST['jenis_kampanye'] == 'lingkungan':
            category = Category.objects.get(deskripsi='Lingkungan')
        elif request.POST['jenis_kampanye'] == 'sospol':
            category = Category.objects.get(deskripsi='Sosial Politik')
        elif request.POST['jenis_kampanye'] == 'hukum':
            category = Category.objects.get(deskripsi='Hukum')
        elif request.POST['jenis_kampanye'] == 'ekonomi':
            category = Category.objects.get(deskripsi='Ekonomi')
        elif request.POST['jenis_kampanye'] == 'pendidikan':
            category = Category.objects.get(deskripsi='Pendidikan')
        elif request.POST['jenis_kampanye'] == 'others':
            category = Category.objects.get(deskripsi='Lainnya')
        

        title = request.POST['title']
        target = request.POST['target']
        deskripsi = request.POST['deskripsi']
        status = None
        if 'file' in request.FILES:
            files = request.FILES['file']
        else:
            files = None
        try:
            status = StatusJapat.objects.get(deskripsi="Pending")
        except:
            status = StatusJapat.objects.create(deskripsi="Pending")

        japat = Japat.objects.create(user=request.user, statusJapat=status, category=category, title=title, content=deskripsi, target=target, file1=files)
        japat.save()
        messages.success(request, "Kebijakan akan dinilai oleh tim vote.policy,status akan di update paling lama 2x24 jam", extra_tags="success")
        return redirect('campaign_make')

    return render(request, 'campaign_make.html')

def campaign_home(request):
    return render(request, 'campaign_home.html')

def campaign_detail(request):
    return render(request, 'campaign_detail.html')

def campaign_search(request):
    return render(request, 'campaign_search.html')

def vote(request):
    return render(request, 'vote.html')

def vote_detail(request):
    messages.success(request, "test")
    return render(request, 'vote_detail.html')

def kebijakan_search(request):
    return render(request, 'kebijakan_search.html')

def kebijakan_detail(request):
    return render(request, 'kebijakan_detail.html')

def kebijakan_add(request):
    if request.method == "POST":
        print("====================FIRED======================")
        messages.success(request, "test")
    return render(request, 'kebijakan_add.html')