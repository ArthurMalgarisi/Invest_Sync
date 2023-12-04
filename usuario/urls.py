from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import meu_perfil, cadastrar_usuario, editar_usuario, deletar_usuario, confirma_deletar_usuario,tela_login, login_usuario, logout_usuario


urlpatterns = [
    #URL DE LISTAR USUARIOS
    path('meu_perfil/', meu_perfil, name='meu_perfil'),

    #URL PARA O CADASTRO DE USUARIOS
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),

    #URL PARA A EDIÇÃO DE USUARIOS
    path('editar_usuario/<int:id_usuario>', editar_usuario, name='editar_usuario'),

    #URL PARA A DELEÇÃO DE USUARIOS
    path('confirma_deletar_usuario/<int:id_usuario>', confirma_deletar_usuario, name='confirma_deletar_usuario'),
    path('deletar_usuario/<int:id_usuario>', deletar_usuario, name='deletar_usuario'),

    #URL PARA A AUTENTICAÇÃO DE USUARIOS
    path('tela_login/', tela_login, name="tela_login"),
    path('login_usuario/', login_usuario, name="login_usuario"),
    path('logout_usuario/', logout_usuario, name="logout_usuario"),

    #URL PARA REDEFINIÇÃO DE SENHA
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='redefinir_senha/alterar_com_email_senha.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='redefinir_senha/mensagem_email_senha.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='redefinir_senha/alteracao_senha.html'), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='redefinir_senha/sucesso_alteracao_senha.html'), name="password_reset_complete")
]
