from django import forms
from django.forms import ModelForm, Textarea, NumberInput
from .models import Avaliacao, Comentario, Receita, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulário para a Avaliação
class AvaliacaoForm(ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': '1-5'}),
        }
        labels = {
            'nota': 'Avaliação (1-5)',
        }

# Formulário para o Comentário
class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Seu comentário'}),
        }
        labels = {
            'texto': 'Comentário',
        }

# Formulário para o Registro de Usuário (CORRIGIDO)
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label="Endereço de e-mail", max_length=254, required=True, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        labels = {
            'username': 'Usuário',
            'email': 'Endereço de e-mail',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# NOVO: Formulário para editar os campos do modelo User
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# NOVO: Formulário para editar o modelo de Profile (para a foto)
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
# ----------------------------------------------------
# CORRIGIDO: Formulário para o envio de receitas por usuários
# ----------------------------------------------------
class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        # O campo 'imagem' agora é usado para o upload, em vez de 'imagem_url'
        fields = ['nome', 'ingredientes', 'instrucoes', 'categoria', 'area', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredientes': forms.Textarea(attrs={'class': 'form-control'}),
            'instrucoes': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            # O widget 'forms.FileInput' será usado automaticamente para o campo 'imagem'
        }