from django.urls import path, include
from portfolio.views import listar_portfolio, cadastrar_portfolio, listar_carteira, deletar_portfolio, editar_portfolio, cadastrar_carteira, editar_carteira, listar_acao, deletar_carteira, cadastrar_acao, deletar_acao, editar_acao, detalhar_acao

urlpatterns = [
    #PORTFOLIO
    path('listar', listar_portfolio, name='listar_portfolio'),
    path('cadastrar', cadastrar_portfolio, name='cadastrar_portfolio'),
    path('<int:id_portfolio>/editar', editar_portfolio, name='editar_portfolio'),
    path('<int:id_portfolio>/deletar', deletar_portfolio, name='deletar_portfolio'),

    #CARTEIRA
    path('<int:id_portfolio>', listar_carteira, name='listar_carteira'),
    path('<int:id_portfolio>/cadastrar_carteira', cadastrar_carteira, name='cadastrar_carteira'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/editar_carteira', editar_carteira, name='editar_carteira'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/deletar_carteira', deletar_carteira, name='deletar_carteira'),

    #CARTEIRA AÇÃO
    path('<int:id_portfolio>/carteira/<int:id_carteira>', listar_acao,  name='listar_acao'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/carteira_acao/<int:id_carteira_acao>/acao/<int:id_acao>', detalhar_acao,  name='detalhar_acao'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/cadastrar_carteira_acao', cadastrar_acao, name='cadastrar_acao'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/editar_carteira_acao/<int:id_carteira_acao>', editar_acao, name='editar_acao'),
    path('<int:id_portfolio>/carteira/<int:id_carteira>/carteira_acao/<int:id_carteira_acao>/deletar_carteira_acao', deletar_acao, name='deletar_acao')
]