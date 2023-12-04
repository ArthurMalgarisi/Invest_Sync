from django.urls import path
from .views import pagina_erro_404, pagina_erro_500, pagina_erro_403

urlpatterns = [
    path('erro_404/', pagina_erro_404, name='pagina_erro_404'),
    path('erro_403/', pagina_erro_403, name='pagina_erro_403'),
    path('erro_500/', pagina_erro_500, name='pagina_erro_500'),
]
