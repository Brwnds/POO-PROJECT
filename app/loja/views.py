from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Bolo, Profile
import json


@login_required
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

@login_required
def catalogo(request):
    bolos = Bolo.objects.all()  # Busca todos os bolos do banco de dados
    return render(request, 'catalogo.html', {'bolos': bolos})

@login_required
def basket(request):
    return render(request, 'basket.html')

@login_required
def admin(request):
    return render(request, 'admin.html')

@require_POST
def adicionar_ao_carrinho(request):
    data = json.loads(request.body)
    bolo_id = data['bolo_id']  # Agora recebemos o id do bolo
    tamanho = data['tamanho'].upper()  # Converte o tamanho para maiúsculas

    # Encontra o bolo pelo ID
    bolo = get_object_or_404(Bolo, id=bolo_id)

    # Obtém o perfil do usuário
    profile = Profile.objects.get(user=request.user)

    # Adiciona o bolo ao carrinho
    profile.adicionar_bolo_ao_carrinho(bolo, tamanho)
    
    return JsonResponse({'success': True})

@login_required
def obter_carrinho(request):
    profile = Profile.objects.get(user=request.user)
    carrinho = profile.listar_carrinho()
    total = profile.obter_valor_total()
    return JsonResponse({'carrinho': carrinho, 'total': str(total)})

def listar_carrinho(request):
    profile = Profile.objects.get(user=request.user)
    return JsonResponse({'carrinho': profile.listar_carrinho()})

@login_required
def finalizar_compra(request):
    profile = request.user.profile  # Obtém o perfil do usuário logado
    profile.limpar_carrinho()       # Limpa o carrinho
    return JsonResponse({'success': True})

