# app_receitas/urls.py

from django.urls import path, include
from . import views
from .views import CustomPasswordChangeView, mudar_senha_sucesso

app_name = 'app_receitas'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('receita/<str:external_id>/', views.detalhes_receita, name='detalhes_receita'),
    path('favoritos/<str:external_id>/', views.adicionar_remover_favoritos, name='adicionar_remover_favoritos'),
    path('receitas-favoritas/', views.receitas_favoritas, name='receitas_favoritas'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/mudar-senha/', CustomPasswordChangeView.as_view(), name='mudar_senha'),
    path('perfil/mudar-senha/sucesso/', mudar_senha_sucesso, name='mudar_senha_sucesso'),
    path('buscar/', views.buscar_receitas, name='buscar_receitas'),
    path('moderar-receitas/', views.moderar_receitas, name='moderar_receitas'),
    path('aprovar-receita/<int:pk>/', views.aprovar_receita, name='aprovar_receita'),
    path('rejeitar-receita/<int:pk>/', views.rejeitar_receita, name='rejeitar_receita'),
]

