from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Bolo(models.Model):
    TAMANHOS = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
    ]

    PRECO_POR_TAMANHO = {
        'P': 15.00,
        'M': 25.00,
        'G': 35.00,
    }

    sabor = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem_url = models.URLField()
    tamanho = models.CharField(max_length=1, choices=TAMANHOS)  # Campo para tamanho
    preco = models.DecimalField(max_digits=6, decimal_places=2, editable=False)  # Preço baseado no tamanho

    def save(self, *args, **kwargs):
        # Define o preço baseado no tamanho escolhido
        self.preco = self.PRECO_POR_TAMANHO[self.tamanho]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.sabor} ({self.get_tamanho_display()})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrinho = models.JSONField(default=list)  # Carrinho como lista de dicionários

    def __str__(self):
        return self.user.username

    def adicionar_bolo_ao_carrinho(self, bolo):
        # Verifica se o bolo já está no carrinho
        for item in self.carrinho:
            if item['bolo_id'] == bolo.id:
                # Incrementa a quantidade se o bolo já estiver no carrinho
                item['quantidade'] += 1
                break
        else:
            # Adiciona o bolo ao carrinho com quantidade 1 se ainda não estiver
            self.carrinho.append({'bolo_id': bolo.id, 'quantidade': 1})
        # Salva o perfil com o carrinho atualizado
        self.save()

    def listar_carrinho(self):
        return self.carrinho


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
