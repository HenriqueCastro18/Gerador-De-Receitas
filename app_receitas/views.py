# app_receitas/views.py

import requests
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import PasswordChangeView
from googletrans import Translator

from .models import Receita, Avaliacao, Comentario, ReceitaFavorita
from .forms import (
    AvaliacaoForm, ComentarioForm, RegistroUsuarioForm,
    UserEditForm, ProfileEditForm,
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
translator = Translator()

def _translate_to_en(text):
    """Função auxiliar para traduzir para inglês com tratamento de erro."""
    if not text:
        return ""
    try:
        return translator.translate(text, dest='en').text
    except Exception as e:
        logging.error(f"Erro na tradução para inglês: {e}")
        return text

def _translate_to_pt(text):
    """Função auxiliar para traduzir para português com tratamento de erro."""
    if not text:
        return ""
    try:
        return translator.translate(text, dest='pt').text
    except Exception as e:
        logging.error(f"Erro na tradução para português: {e}")
        return text

def _fetch_from_themealdb(query_type, query_value):
    """Função auxiliar para buscar receitas na API TheMealDB."""
    if not query_value:
        return [], ""
    
    query_value_en = _translate_to_en(query_value)
    
    api_map = {
        'nome': f'https://www.themealdb.com/api/json/v1/1/search.php?s={query_value_en}',
        'ingredientes': f'https://www.themealdb.com/api/json/v1/1/filter.php?i={query_value_en}',
        'categoria': f'https://www.themealdb.com/api/json/v1/1/filter.php?c={query_value_en}',
        'area': f'https://www.themealdb.com/api/json/v1/1/filter.php?a={query_value_en}',
        'id': f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={query_value_en}'
    }
    
    api_url = api_map.get(query_type)
    if not api_url:
        return [], f"Tipo de busca '{query_type}' inválido."
        
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        meals = data.get('meals', [])
        
        if not meals:
            return [], f"Nenhuma receita encontrada na API TheMealDB para '{query_value}'."
        
        receitas_api = []
        for meal_data in meals:
            receitas_api.append({
                'nome': _translate_to_pt(meal_data.get('strMeal')),
                'external_id': f"tmdb_{meal_data.get('idMeal')}",
                'imagem_url': meal_data.get('strMealThumb')
            })
        return receitas_api, ""
        
    except (requests.exceptions.RequestException, json.JSONDecodeError, Exception) as e:
        logging.error(f"Erro ao buscar na API TheMealDB ({query_type}): {e}")
        return [], f"Erro ao buscar receitas na API TheMealDB: {e}"

def registro(request):
    """View para o registro de novos usuários."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registro efetuado com sucesso! Faça o login para continuar.")
            return redirect('app_receitas:login')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name.capitalize()}: {error}")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'app_receitas/registro.html', {'form': form})

def buscar_receitas(request):
    query_nome = request.GET.get('nome')
    query_ingredientes = request.GET.get('ingredientes')
    query_area = request.GET.get('area')
    query_categoria = request.GET.get('categoria')

    todas_receitas = []
    
    # Busca na API
    if query_nome:
        receitas_api, msg = _fetch_from_themealdb('nome', query_nome)
        todas_receitas.extend(receitas_api)
        if msg:
            messages.info(request, msg)

    if query_ingredientes:
        ingredientes_list = [ing.strip() for ing in query_ingredientes.split(',') if ing.strip()]
        for ingrediente in ingredientes_list:
            receitas_api, msg = _fetch_from_themealdb('ingredientes', ingrediente)
            todas_receitas.extend(receitas_api)
            if msg:
                messages.info(request, msg)

    if query_categoria:
        receitas_api, msg = _fetch_from_themealdb('categoria', query_categoria)
        todas_receitas.extend(receitas_api)
        if msg:
            messages.info(request, msg)
            
    if query_area:
        receitas_api, msg = _fetch_from_themealdb('area', query_area)
        todas_receitas.extend(receitas_api)
        if msg:
            messages.info(request, msg)

    # Busca no banco de dados local
    receitas_local = Receita.objects.all()
    q_objects = Q()
    
    if query_nome:
        q_objects &= Q(nome__icontains=query_nome) | Q(nome__icontains=_translate_to_pt(query_nome))
    
    if query_ingredientes:
        ingredientes_list = [ing.strip() for ing in query_ingredientes.split(',') if ing.strip()]
        ing_q = Q()
        for ingrediente in ingredientes_list:
            ing_q |= Q(ingredientes__icontains=ingrediente) | Q(ingredientes__icontains=_translate_to_pt(ingrediente))
        q_objects &= ing_q
        
    if query_area:
        q_objects &= Q(area__icontains=query_area) | Q(area__icontains=_translate_to_pt(query_area))
    
    if query_categoria:
        q_objects &= Q(categoria__icontains=query_categoria) | Q(categoria__icontains=_translate_to_pt(query_categoria))
    
    if q_objects:
        receitas_local = receitas_local.filter(q_objects).order_by('nome')
    else:
        receitas_local = receitas_local.order_by('nome')

    todas_receitas.extend(list(receitas_local))

    paginator = Paginator(todas_receitas, 9)
    page = request.GET.get('page')
    
    try:
        receitas_encontradas = paginator.page(page)
    except PageNotAnInteger:
        receitas_encontradas = paginator.page(1)
    except EmptyPage:
        receitas_encontradas = paginator.page(paginator.num_pages)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()

    context = {
        'query_nome': query_nome,
        'query_ingredientes': query_ingredientes,
        'query_area': query_area,
        'query_categoria': query_categoria,
        'receitas_encontradas': receitas_encontradas,
        'query_string': query_string,
        'message': f'{len(todas_receitas)} receitas encontradas.' if todas_receitas else 'Nenhuma receita encontrada.',
    }
    return render(request, 'app_receitas/buscar_receitas.html', context)


def detalhes_receita(request, external_id):
    receita = None
    
    if external_id.startswith('tmdb_'):
        recipe_id = external_id.replace('tmdb_', '')

        # Tenta obter a receita do banco de dados, se não existir, busca na API e a cria
        try:
            receita, created = Receita.objects.get_or_create(external_id=external_id)

            if created or not receita.instrucoes or not receita.ingredientes:
                # Se a receita foi criada agora ou está incompleta, busca os detalhes da API
                response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}')
                if response.status_code == 200:
                    data = response.json()
                    meals = data.get('meals')
                    if meals:
                        meal_data = meals[0]
                        
                        # Traduzindo e preenchendo os dados
                        receita.nome = _translate_to_pt(meal_data.get('strMeal'))
                        receita.instrucoes = _translate_to_pt(meal_data.get('strInstructions', ''))
                        receita.categoria = [ _translate_to_pt(meal_data.get('strCategory', '')) ] if meal_data.get('strCategory') else []
                        receita.area = [ _translate_to_pt(meal_data.get('strArea', '')) ] if meal_data.get('strArea') else []
                        receita.imagem_url = meal_data.get('strMealThumb')
                        receita.link_youtube = meal_data.get('strYoutube')
                        
                        ingredientes_traduzidos = []
                        for i in range(1, 21):
                            ingrediente = meal_data.get(f'strIngredient{i}')
                            medida = meal_data.get(f'strMeasure{i}')
                            
                            if ingrediente and ingrediente.strip():
                                medida_str = medida.strip() if medida is not None else ''
                                texto_completo = f"{medida_str} {ingrediente.strip()}"
                                ingrediente_traduzido = _translate_to_pt(texto_completo)
                                ingredientes_traduzidos.append(ingrediente_traduzido)
                        
                        receita.ingredientes = ingredientes_traduzidos
                        receita.status = 'aprovado' # Define o status como aprovado para novas receitas
                        receita.save()
                    else:
                        messages.warning(request, "Nenhuma receita encontrada na API TheMealDB.")
                        return redirect('app_receitas:buscar_receitas')
                else:
                    messages.error(request, "Erro ao buscar a receita na API.")
                    return redirect('app_receitas:buscar_receitas')

        except Exception as e:
            messages.error(request, f"Erro inesperado: {e}")
            return redirect('app_receitas:buscar_receitas')

    else:
        receita = get_object_or_404(Receita, external_id=external_id)

    if not receita:
        messages.error(request, "A receita não foi encontrada.")
        return redirect('app_receitas:buscar_receitas')

    # ... restante do código da sua view
    is_favorita = False
    if request.user.is_authenticated:
        is_favorita = ReceitaFavorita.objects.filter(user=request.user, receita=receita).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar logado para avaliar ou comentar.")
            return redirect('app_receitas:login')
        
        if 'submit_avaliacao' in request.POST:
            avaliacao_form = AvaliacaoForm(request.POST)
            if avaliacao_form.is_valid():
                avaliacao, created = Avaliacao.objects.get_or_create(
                    user=request.user,
                    receita=receita,
                    defaults={'nota': avaliacao_form.cleaned_data['nota']}
                )
                if not created:
                    avaliacao.nota = avaliacao_form.cleaned_data['nota']
                    avaliacao.save()
                receita.update_media_avaliacoes()
                messages.success(request, "Avaliação adicionada/atualizada com sucesso!")
        
        elif 'submit_comentario' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.user = request.user
                comentario.receita = receita
                comentario.save()
                messages.success(request, "Comentário adicionado com sucesso!")
        
        return redirect('app_receitas:detalhes_receita', external_id=external_id)

    avaliacao_form = AvaliacaoForm()
    comentario_form = ComentarioForm()
    avaliacoes = Avaliacao.objects.filter(receita=receita)
    comentarios = Comentario.objects.filter(receita=receita).order_by('-data_comentario')
    
    media_avaliacoes = receita.media_avaliacoes
    contador_favoritos = ReceitaFavorita.objects.filter(receita=receita).count()

    context = {
        'receita': receita,
        'is_favorita': is_favorita,
        'avaliacao_form': avaliacao_form,
        'comentario_form': comentario_form,
        'avaliacoes': avaliacoes,
        'comentarios': comentarios,
        'media_avaliacoes': media_avaliacoes,
        'contador_favoritos': contador_favoritos
    }
    return render(request, 'app_receitas/detalhes_receita.html', context)


@login_required
def adicionar_remover_favoritos(request, external_id):
    """View para adicionar ou remover uma receita dos favoritos."""
    try:
        receita = Receita.objects.get(external_id=external_id)
    except Receita.DoesNotExist:
        messages.error(request, "A receita deve ser visualizada e salva antes de ser adicionada aos favoritos.")
        return redirect('app_receitas:index')

    favorito, created = ReceitaFavorita.objects.get_or_create(user=request.user, receita=receita)

    if not created:
        favorito.delete()
        messages.success(request, f"Receita '{receita.nome}' removida dos favoritos.")
    else:
        messages.success(request, f"Receita '{receita.nome}' adicionada aos favoritos!")

    return redirect('app_receitas:detalhes_receita', external_id=external_id)


@login_required
def receitas_favoritas(request):
    """View para listar as receitas favoritas do usuário logado com paginação."""
    receitas_favoritas = request.user.receitas_favoritas.all()

    paginator = Paginator(receitas_favoritas, 6)
    page = request.GET.get('page')

    try:
        receitas_por_pagina = paginator.page(page)
    except PageNotAnInteger:
        receitas_por_pagina = paginator.page(1)
    except EmptyPage:
        receitas_por_pagina = paginator.page(paginator.num_pages)

    context = {
        'receitas_favoritas': receitas_por_pagina,
    }

    return render(request, 'app_receitas/receitas_favoritas.html', context)


def login_view(request):
    """View para o login de usuários."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {username}!")
                return redirect('app_receitas:index')
            else:
                messages.error(request, "Nome de utilizador ou palavra-passe inválidos.")
        else:
            messages.error(request, "Nome de utilizador ou palavra-passe inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def custom_logout_view(request):
    """View para o logout de usuários."""
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('app_receitas:index')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'app_receitas/mudar_senha.html'
    success_url = reverse_lazy('app_receitas:mudar_senha_sucesso')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return response

@login_required
def perfil_usuario(request):
    """
    View para exibir o perfil do usuário, suas receitas favoritas e as que ele enviou.
    """
    receitas_favoritas = ReceitaFavorita.objects.filter(user=request.user).select_related('receita')
    receitas_enviadas = Receita.objects.filter(autor=request.user)

    context = {
        'receitas_favoritas': receitas_favoritas,
        'receitas_enviadas': receitas_enviadas,
    }
    return render(request, 'app_receitas/perfil_usuario.html', context)


@login_required
def editar_perfil(request):
    """
    Permite que o usuário autenticado edite seu perfil e sua foto.
    """
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('app_receitas:perfil_usuario')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'app_receitas/editar_perfil.html', context)


@login_required
def mudar_senha_sucesso(request):
    """View para exibir uma mensagem de sucesso após a mudança de senha."""
    return render(request, 'app_receitas/mudar_senha_sucesso.html')

def index(request):
    """
    View para a página inicial, agora exibindo o ranking de receitas.
    """
    top_receitas = Receita.objects.filter(status='aprovado').exclude(media_avaliacoes__isnull=True).order_by('-media_avaliacoes')[:12]

    context = {
        'top_receitas': top_receitas,
    }

    return render(request, 'app_receitas/index.html', context)

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def moderar_receitas(request):
    receitas_pendentes = Receita.objects.filter(status='pendente')
    return render(request, 'app_receitas/moderar_receitas.html', {'receitas_pendentes': receitas_pendentes})

@login_required
@user_passes_test(is_superuser)
def aprovar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    receita.status = 'aprovado'
    receita.save()
    messages.success(request, f"A receita '{receita.nome}' foi aprovada com sucesso.")
    return redirect('app_receitas:moderar_receitas')

@login_required
@user_passes_test(is_superuser)
def rejeitar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    receita.delete()
    messages.success(request, f"A receita '{receita.nome}' foi rejeitada e removida.")
    return redirect('app_receitas:moderar_receitas')