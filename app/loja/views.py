from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def basket(request):
    return render(request, 'basket.html')

def admin(request):
    return render(request, 'admin.html')