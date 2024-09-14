"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loja import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('basket/', views.basket, name='basket'),
    path('adm/', views.admin, name='adm'),
    path('adicionar_ao_carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('listar_carrinho/', views.listar_carrinho, name='listar_carrinho'),
    path('obter_carrinho/', views.obter_carrinho, name='obter_carrinho'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('logout/', views.logout, name='logout'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('deletar_perfil/', views.deletar_perfil, name='deletar_perfil'),
]
