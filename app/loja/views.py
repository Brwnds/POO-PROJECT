from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nome de usuário ou senha incorretos")
    
    return render(request, 'login.html')

def cadastro(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Usuário já existe")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Usuário cadastrado com sucesso")
                return redirect('login')
        else:
            messages.error(request, "As senhas não coincidem")
    return render(request, 'cadastro.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def basket(request):
    return render(request, 'basket.html')

def admin(request):
    return render(request, 'admin.html')