from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


class Bolo(models.Model):
    TAMANHOS = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
    ]

    sabor = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem_url = models.URLField()
    
    # Preços para cada tamanho
    preco_pequeno = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    preco_medio = models.DecimalField(max_digits=6, decimal_places=2, default=25.00)
    preco_grande = models.DecimalField(max_digits=6, decimal_places=2, default=35.00)

    def get_preco_por_tamanho(self, tamanho):
        if tamanho == 'P':
            return self.preco_pequeno
        elif tamanho == 'M':
            return self.preco_medio
        elif tamanho == 'G':
            return self.preco_grande
        else:
            return None

    def __str__(self):
        return self.sabor


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrinho = models.JSONField(default=list)  # Carrinho como lista de dicionários
    valor_total_carrinho = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

    def adicionar_bolo_ao_carrinho(self, bolo, tamanho):
        # Obtém o preço de acordo com o tamanho
        preco = bolo.get_preco_por_tamanho(tamanho)
        if preco is None:
            raise ValueError("Tamanho inválido")

        # Converte o preço de Decimal para float
        preco = float(preco)

        # Verifica se o bolo de tamanho específico já está no carrinho
        for item in self.carrinho:
            if item['bolo_id'] == bolo.id and item['tamanho'] == tamanho:
                # Incrementa a quantidade se o bolo já estiver no carrinho
                item['quantidade'] += 1
                # Atualiza o valor total
                self.valor_total_carrinho += Decimal(preco)
                break
        else:
            # Adiciona o bolo ao carrinho com quantidade 1
            self.carrinho.append({'bolo_id': bolo.id, 'tamanho': tamanho, 'preco': preco, 'quantidade': 1})
            # Atualiza o valor total
            self.valor_total_carrinho += Decimal(preco)

        # Salva o perfil com o carrinho atualizado e o valor total
        self.save()

    def listar_carrinho(self):
        return self.carrinho

    def obter_valor_total(self):
        return self.valor_total_carrinho
    
    def limpar_carrinho(self):
        # Limpa o carrinho e zera o valor total
        self.carrinho = []
        self.valor_total_carrinho = 0.00
        self.save()



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
