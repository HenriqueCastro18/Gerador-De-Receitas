from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from PIL import Image # Importação correta

# Altere apenas o modelo Receita
class Receita(models.Model):
    nome = models.CharField(max_length=255)
    external_id = models.CharField(max_length=50, unique=True)
    categoria = models.JSONField(encoder=DjangoJSONEncoder, default=list)
    area = models.JSONField(encoder=DjangoJSONEncoder, default=list)
    instrucoes = models.TextField(blank=True, null=True)
    imagem_url = models.URLField(max_length=500, blank=True, null=True)
    link_youtube = models.URLField(max_length=500, blank=True, null=True)
    ingredientes = models.JSONField(encoder=DjangoJSONEncoder, default=list, blank=True, null=True)

    # CAMPOS ADICIONADOS
    media_avaliacoes = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default='aprovado', choices=[('aprovado', 'Aprovado'), ('pendente', 'Pendente')])
    imagem = models.ImageField(upload_to='receitas_pics', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Salva o modelo e redimensiona a imagem se existir.
        """
        super().save(*args, **kwargs)
        if self.imagem:
            img = Image.open(self.imagem.path)
            tamanho_maximo = (600, 600)

            if img.height > tamanho_maximo[0] or img.width > tamanho_maximo[1]:
                img.thumbnail(tamanho_maximo)
                img.save(self.imagem.path)

    def __str__(self):
        return self.nome

    def update_media_avaliacoes(self):
        avg = self.avaliacoes.aggregate(Avg('nota'))['nota__avg']
        self.media_avaliacoes = avg if avg is not None else 0.00
        self.save()

class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'receita')

    def __str__(self):
        return f"{self.user.username} - {self.receita.nome} - {self.nota}"

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.receita.nome}"

class ReceitaFavorita(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receitas_favoritas')
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'receita')

    def __str__(self):
        return f"{self.user.username} gosta de {self.receita.nome}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(default='profile_pics/default-avatar.png', upload_to='profile_pics', blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def save(self, *args, **kwargs):
        """Salva a imagem do perfil e redimensiona se necessário."""
        super().save(*args, **kwargs)
        
        if self.foto and self.foto.name != 'profile_pics/default-avatar.png': # Verifica se não é a imagem padrão
            try:
                img = Image.open(self.foto.path)
                tamanho_maximo = (300, 300) # Tamanho ideal para fotos de perfil

                if img.height > tamanho_maximo[0] or img.width > tamanho_maximo[1]:
                    img.thumbnail(tamanho_maximo)
                    img.save(self.foto.path)
            except (IOError, FileNotFoundError):
                # Ignora erros se o arquivo não puder ser aberto ou não existir
                pass

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()