from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_view, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Bolo, Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
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

def logout(request):
    logout_view(request)
    return redirect('login')
    
    

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

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        novo_nome = request.POST.get('name')
        nova_senha = request.POST.get('newPassword')
        
        # Atualiza o nome do usuário
        if novo_nome:
            user.username = novo_nome
        
        # Atualiza a senha do usuário
        if nova_senha:
            user.set_password(nova_senha)
        
        # Salva as mudanças no usuário
        user.save()

        # Desloga o usuário para que ele precise logar novamente com os novos dados
        logout(request)

        # Adiciona uma mensagem de sucesso
        messages.success(request, 'Seu perfil foi atualizado com sucesso. Por favor, faça login com suas novas credenciais.')

        # Redireciona para a página de login
        return redirect('login')

    # Caso seja GET, renderiza a página de edição de perfil
    return render(request, 'editar_perfil.html')

@login_required
def deletar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Remove o usuário e todas as suas associações
        
        messages.success(request, 'Perfil excluído com sucesso!')
        return redirect('cadastro')  # Redireciona para a página de cadastro ou login

    return redirect('adm')  # Redireciona para a página de administração se a requisição não for POST

