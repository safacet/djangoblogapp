from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)
            messages.success(request, "<strong>Hoşgeldin!</strong> Başarıyla kayıt olundu!")
            return redirect("index")
    else:
        context = {
        "form": form
    }
        return render(request, "register.html", context)

   

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    valueNext = request.POST.get('next')

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        if user is not None and valueNext == '':
            messages.success(request, "<strong>Hoşgeldin!</strong> Giriş yapıldı!")
            login(request, user)
            return redirect("index")
        elif user is not None and valueNext != '':
            messages.success(request, "<strong>Hoşgeldin!</strong> Giriş yapıldı!")
            login(request, user)
            return redirect(valueNext)
        else:
            messages.error(request, "<strong>Opps!</strogn> Kullanıcı adı veya parola hatalı")
            return render(request, "login.html", context)
            
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "<strong>Güle Güle!</strong> Çıkış Yapıldı")
    return redirect("index")