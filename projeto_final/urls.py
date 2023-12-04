from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import handler404, handler403, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('usuario/', include('usuario.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('carteira_acao/', include('carteira_acao.urls')),
    path('carteira/', include('carteira.urls')),
    path('acao/', include('acao.urls')),
    path('erro/', include('erro.urls')),
    path('chart/', include('chart.urls')),
]

handler404 = 'erro.views.pagina_erro_404'
handler403 = 'erro.views.pagina_erro_403'
handler500 = 'erro.views.pagina_erro_500'