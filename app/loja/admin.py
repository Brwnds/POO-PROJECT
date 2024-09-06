from django.contrib import admin
from .models import Bolo

# Registrar o modelo Bolo no admin
@admin.register(Bolo)
class BoloAdmin(admin.ModelAdmin):
    list_display = ('sabor', 'descricao', 'imagem_url')  # Exibe essas colunas na lista de bolos
    search_fields = ('sabor',)  # Permite pesquisar por sabor