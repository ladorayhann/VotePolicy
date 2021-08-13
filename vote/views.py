from vote.models import Category, StatusJapat, Japat, Policy
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Japat


def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
def home(request):
    print(request.user)
    japats = Japat.objects.all().order_by('-voters')[:5]
    policies = Policy.objects.all()[:3]
    return render(request, 'home.html', {"japats":japats,"policies":policies})

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
    print(request.user)
    if not request.user.is_authenticated and not request.user.is_superuser:
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
    category = Category.objects.get(deskripsi="Ekonomi")
    qs = Japat.objects.all()
    japats = Japat.objects.filter(category=category)
    selected_category = request.GET.get('jenis_kampanye')
    if is_valid_queryparam(selected_category):
        if selected_category == 'ekonomi':
            category = Category.objects.get(deskripsi="Ekonomi")
            japats = qs.filter(category=category)
        elif selected_category == 'hukum':
            category = Category.objects.get(deskripsi="Hukum")
            japats = qs.filter(category=category)
        elif selected_category == 'lingkungan':
            category = Category.objects.get(deskripsi="Lingkungan")
            japats = qs.filter(category=category)
        elif selected_category == 'pendidikan':
            category = Category.objects.get(deskripsi="Pendidikan")
            japats = qs.filter(category=category)
        elif selected_category == 'sospol':
            category = Category.objects.get(deskripsi="Sosial Politik")
            japats = qs.filter(category=category)
        elif selected_category == 'others':
            category = Category.objects.get(deskripsi="Lainnya")
            japats = qs.filter(category=category)
    paginator = Paginator(japats, 4)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'campaign_search.html', {'page_obj':page_obj, 'category':category.deskripsi})

def vote(request):
    return render(request, 'vote.html')

def vote_detail(request):
    messages.success(request, "test")
    return render(request, 'vote_detail.html')

def kebijakan_search(request):
    category = Category.objects.get(deskripsi="Ekonomi")
    print(category.deskripsi)
    qs = Policy.objects.all()
    policies = Policy.objects.filter(category=category)
    selected_category = request.GET.get('jenis_kampanye')
    if is_valid_queryparam(selected_category):
        if selected_category == 'ekonomi':
            category = Category.objects.get(deskripsi="Ekonomi")
            policies = qs.filter(category=category)
            print(category.deskripsi)
        elif selected_category == 'hukum':
            category = Category.objects.get(deskripsi="Hukum")
            policies = qs.filter(category=category)
        elif selected_category == 'lingkungan':
            category = Category.objects.get(deskripsi="Lingkungan")
            policies = qs.filter(category=category)
        elif selected_category == 'pendidikan':
            category = Category.objects.get(deskripsi="Pendidikan")
            policies = qs.filter(category=category)
        elif selected_category == 'sospol':
            category = Category.objects.get(deskripsi="Sosial Politik")
            policies = qs.filter(category=category)
        elif selected_category == 'others':
            category = Category.objects.get(deskripsi="Lainnya")
            policies = qs.filter(category=category)
    paginator = Paginator(policies, 4)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'kebijakan_search.html', {'page_obj':page_obj, 'category':category.deskripsi})

def kebijakan_detail(request):
    return render(request, 'kebijakan_detail.html')

def kebijakan_add(request):
    if request.method == "POST":
        messages.success(request, "test")
    return render(request, 'kebijakan_add.html')