from django.db.models.fields import PositiveBigIntegerField
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
from .models import Comment, Japat, Vote, StatusVote
from django.db.models import Q
from django.urls import reverse
import requests
from vp.settings import MEDIA_ROOT, MEDIA_URL
from vp.settings import RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY
from vp.settings import storage


def is_valid_queryparam(param):
    return param != '' and param is not None

# Create your views here.
def home(request):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
    japats = Japat.objects.all().order_by('-voters')[:5]
    print(japats)
    policies = Policy.objects.all().order_by('id')[:3]
    return render(request, 'home.html', {"japats":japats,"policies":policies})

@csrf_exempt
def login(request):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
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
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
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
        else:
            print(form.errors)

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
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
    auth_logout(request)
    return redirect('login')

# progress'
def campaign_make(request):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
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
        try:
            status = StatusJapat.objects.get(deskripsi="Pending")
        except:
            status = StatusJapat.objects.create(deskripsi="Pending")
        if 'file' in request.FILES:
            files = request.FILES['file']
        else:
            files = None
        
        japat = Japat.objects.create(user=request.user, statusJapat=status, category=category, title=title, content=deskripsi, target=target, url_file=files)
        japat.save()
        japat_pk = japat.pk
        storage.child(f"japat-files/{japat_pk}/{files.name}").put(files)
        file_url = storage.child(f"japat-files/{japat_pk}/{files.name}").get_url(None)
        japat.url_file = file_url
        japat.save()
        messages.success(request, "Kebijakan akan dinilai oleh tim vote.policy,status akan di update paling lama 2x24 jam", extra_tags="success")
        return redirect(reverse('vote_detail', kwargs={"id": japat.id}))
    return render(request, 'campaign_make.html')

def campaign_home(request):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
    if not request.user.is_authenticated:
        return redirect('login')
    campaign = Japat.objects.filter(user=request.user)
    return render(request, 'campaign_home.html', {"campaigns":campaign})

def campaign_search(request):
    try:
        del request.session['policy_category']
    except KeyError:
        pass
    keyword = None
    qs = Japat.objects.all().order_by('id')
    if request.method == "POST":
        keyword = request.POST['search']
        selected_category = request.session['campaign_category']
        category = None
        campaigns = None
        if is_valid_queryparam(selected_category):
            category, _ = getCategoryCampaigns(qs, selected_category)
        else:
            selected_category = request.session['campaign_category']
        campaigns = Japat.objects.filter(Q(category=category, content__icontains=keyword) | Q(category=category, title__icontains=keyword))
        print(campaigns)
    elif request.GET.get('page') is not None and request.GET.get('keyword') is not None:
        if is_valid_queryparam(request.session['campaign_category']):
            category, _ = getCategoryCampaigns(qs, request.session['campaign_category'])
        else:
            selected_category = request.session['campaign_category']
        keyword = request.GET.get('keyword')
        campaigns = Japat.objects.filter(Q(category=category, content__icontains=keyword) | Q(category=category, title__icontains=keyword))
    else:
        category = Category.objects.get(deskripsi="Ekonomi")
        campaigns = Japat.objects.filter(category=category)
        selected_category = request.GET.get('jenis_kampanye')
        if is_valid_queryparam(selected_category):
            request.session['campaign_category'] = selected_category
            category, campaigns = getCategoryCampaigns(qs, selected_category)
            selected_category = request.session['campaign_category']
        else:
            selected_category = 'ekonomi'
            request.session['campaign_category'] = selected_category
    
    paginator = Paginator(campaigns, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    selected_category = request.session['campaign_category']

    return render(request, 'campaign_search.html', {'page_obj':page_obj, 'category':category.deskripsi, 'keyword':keyword, 'jenis_kampanye':selected_category})

def vote_detail(request,id):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
    user_voted = False
    user_comments = False
    campaign_detail = Japat.objects.get(pk=id)
    category = campaign_detail.category
    status_vote_no = StatusVote.objects.get(statusVote=False)
    status_vote_ok = StatusVote.objects.get(statusVote=True)
    if request.method == "POST":
        if 'g-recaptcha-response' in request.POST and not recaptcha_verified(request.POST['g-recaptcha-response']):
            return redirect(reverse('vote_detail'))
        if 'setuju' in request.POST:
            email = request.POST['email']
            Vote.objects.create(japat=campaign_detail, user=request.user, statusVote=status_vote_ok, email=email)
            messages.success(request, "test")
        if 'tidak' in request.POST:
            email = request.POST['email']
            Vote.objects.create(japat=campaign_detail, user=request.user, statusVote=status_vote_no, email=email)
            messages.success(request, "test")
        
        voters = Vote.objects.filter(japat=campaign_detail)
        campaign_detail.voters = len(voters)
        campaign_detail.save()

        if 'comment' in request.POST:
            email = request.POST['email']
            content = request.POST['content']
            Comment.objects.create(japat=campaign_detail, email=email, content=content, is_policy=False)

    comments_vote = Comment.objects.filter(japat=campaign_detail)
    if comments_vote.exists():
        user_comments = True
    if request.user.is_authenticated:
        vote = Vote.objects.filter(user=request.user, japat=campaign_detail)
        if vote.exists():
            vote = Vote.objects.get(user=request.user, japat=campaign_detail)
            user_voted = True
    setuju_votes = len(Vote.objects.filter(japat=campaign_detail,statusVote=status_vote_ok))
    all_votes = len(Vote.objects.filter(japat=campaign_detail))
    try:
        setuju_percetage = round((setuju_votes/all_votes) * 100)
    except ZeroDivisionError:
        setuju_percetage = 0
    paginator = Paginator(comments_vote, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "campaign": campaign_detail,
        "category": category.deskripsi,
        "voted": user_voted,
        "setuju": setuju_percetage,
        "tidak_setuju": 100 - setuju_percetage,
        "comments": user_comments,
        "page_obj": page_obj,
        "recaptcha_sitekey" : RECAPTCHA_SITE_KEY,
        "media_root":MEDIA_ROOT,
        "media_url":MEDIA_URL,
    }
    return render(request, 'vote_detail.html', context)


def getCategoryPolicies(qs,selected_category):
    category = None
    policies = None
    if selected_category == 'ekonomi':
        category = Category.objects.get(deskripsi="Ekonomi")
        policies = qs.filter(category=category)
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
    return category, policies

def getCategoryCampaigns(qs,selected_category):
    category = None
    campaign = None
    if selected_category == 'ekonomi':
        category = Category.objects.get(deskripsi="Ekonomi")
        campaign = qs.filter(category=category)
    elif selected_category == 'hukum':
        category = Category.objects.get(deskripsi="Hukum")
        campaign = qs.filter(category=category)
    elif selected_category == 'lingkungan':
        category = Category.objects.get(deskripsi="Lingkungan")
        campaign = qs.filter(category=category)
    elif selected_category == 'pendidikan':
        category = Category.objects.get(deskripsi="Pendidikan")
        campaign = qs.filter(category=category)
    elif selected_category == 'sospol':
        category = Category.objects.get(deskripsi="Sosial Politik")
        campaign = qs.filter(category=category)
    elif selected_category == 'others':
        category = Category.objects.get(deskripsi="Lainnya")
        campaign = qs.filter(category=category)
    return category, campaign

def kebijakan_search(request):
    try:
        del request.session['campaign_category']
    except KeyError:
        pass
    qs = Policy.objects.all().order_by('id')
    keyword = None
    if request.method == "POST":
        keyword = request.POST['search']
        selected_category = request.session['policy_category']
        category = None
        policies = None
        if is_valid_queryparam(selected_category):
            category, _ = getCategoryPolicies(qs, selected_category)
        else:
            selected_category = request.session['policy_category']
        policies = Policy.objects.filter(Q(category=category, content__icontains=keyword) | Q(category=category, title__icontains=keyword))
    elif request.GET.get('page') is not None and request.GET.get('keyword') is not None:
        if is_valid_queryparam(request.session['policy_category']):
            category, _ = getCategoryPolicies(qs, request.session['policy_category'])
        else:
            selected_category = request.session['policy_category']
        keyword = request.GET.get('keyword')
        print(keyword)
        policies = Policy.objects.filter(Q(category=category, content__icontains=keyword) | Q(category=category, title__icontains=keyword))
    else:
        category = Category.objects.get(deskripsi="Ekonomi")
        policies = Policy.objects.filter(category=category)
        selected_category = request.GET.get('jenis_kebijakan')
        if is_valid_queryparam(selected_category):
            request.session['policy_category'] = selected_category
            category, policies = getCategoryPolicies(qs, selected_category)
            selected_category = request.session['policy_category']
        else:
            selected_category = 'ekonomi'
            request.session['policy_category'] = selected_category
    paginator = Paginator(policies, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    selected_category = request.session['policy_category']

    return render(request, 'kebijakan_search.html', {'page_obj':page_obj, 'category':category.deskripsi, 'keyword':keyword, 'jenis_kebijakan':selected_category})

def kebijakan_detail(request, id):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass

    user_comments = False
    policy = Policy.objects.get(pk=id)
    if 'comment' in request.POST:
        email = request.POST['email']
        content = request.POST['content']
        Comment.objects.create(policy=policy, email=email, content=content, is_policy=False)
                    
    comments_policy = Comment.objects.filter(policy=policy)
    if comments_policy.exists():
        user_comments = True

    paginator = Paginator(comments_policy, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'kebijakan_detail.html', {'policy':policy, "comments":user_comments, "page_obj":page_obj})

def kebijakan_add(request):
    try:
        del request.session['policy_category']
        del request.session['campaign_category']
    except KeyError:
        pass
    if request.method == "POST":
        messages.success(request, "test")
    return render(request, 'kebijakan_add.html')

def profile(request):
    return render(request, "profile.html")

def profile_update(request):
    return render(request, "profile_update.html")

def recaptcha_verified(recaptcha_response):
    data = {
        'secret' : RECAPTCHA_SECRET_KEY,
        'response' : recaptcha_response
    }
    res = requests.post('https://www.google.com/recaptcha/api/siteverify', data)
    content = res.json()
    return content['success'] 