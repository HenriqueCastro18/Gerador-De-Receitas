from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_receitas.urls')),
    
    # Adicione esta linha de volta para as URLs de autenticação padrão do Django
    path('', include('django.contrib.auth.urls')),
]

# Esta linha permite que o Django sirva arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)