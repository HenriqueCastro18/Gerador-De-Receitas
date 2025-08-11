from django.contrib import admin
from .models import Receita, Avaliacao, Comentario, ReceitaFavorita

admin.site.register(Receita)
admin.site.register(Avaliacao)
admin.site.register(Comentario)
admin.site.register(ReceitaFavorita)