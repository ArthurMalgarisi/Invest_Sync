from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
#VALIDAÇÃO DE SENHAS
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect


# Create your views here.

# LISTAGEM DE USUARIOS
@login_required
def meu_perfil(request):  # não vai ser usado apenas para teste
    if request.user.is_authenticated:
        user_id = request.user.id
        usuario_logado_obj = Usuario.objects.filter(id=user_id).first()
        usuario = Usuario.objects.filter(username=usuario_logado_obj.username).first()
        return render(request, 'listar_usuario.html', {'usuario': usuario})

# CADASTRO DE USUARIOS
def cadastrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_usuario.html')
    else:
        nome_usuario = request.POST.get('nome_usuario')
        email_usuario = request.POST.get('email_usuario')
        senha_usuario = request.POST.get('senha_usuario')
        data_nascimento_str = request.POST.get('nascimento_usuario')
        endereco = request.POST.get('endereco_usuario')

        # Validar se a data de nascimento está no formato correto
        try:
            data_nascimento_obj = datetime.strptime(data_nascimento_str, '%d/%m/%Y')
        except ValueError:
            return render(request, "cadastrar_usuario.html", {'error_message': 'Formato de data de nascimento inválido. Use o formato dd/mm/yyyy'})

        user = Usuario.objects.filter(email=email_usuario).first()

        # VALIDAÇÃO SE JÁ EXISTE UM USUARIO NA TABELA auth_user COM ESSE EMAIL DIGITADO
        if user:
            return render(request, "cadastrar_usuario.html", {'error_message': 'Este e-mail já está sendo utilizado por outro usuário'})
        # SE NÃO HOUVER, CADASTRE UM NOVO USUÁRIO
        else:
            user = Usuario.objects.create_user(
                username=nome_usuario,
                email=email_usuario,
                password=senha_usuario,
                data_nascimento=data_nascimento_obj,
                endereco=endereco
            )
            user.save()

            messages.success(request, 'Você foi cadastrado com sucesso!')

            return render(request, "login_usuario.html")
            # return redirect(tela_login)

# EDIÇÃO DE USUARIOS
@login_required
def editar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    
    if request.method == 'POST':
        nome = request.POST.get('nome_usuario')
        email = request.POST.get('email_usuario')

        # Converta a data do formato 'DD/MM/YYYY' para 'YYYY-MM-DD'
        data_nascimento_str = request.POST.get('nascimento_usuario')
        data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').strftime('%Y-%m-%d')

        # Verifique se a data de nascimento é válida e não é superior à data atual
        data_nascimento_dt = datetime.strptime(data_nascimento, '%Y-%m-%d')
        data_atual = datetime.now()

        if data_nascimento_dt > data_atual:
            return render(request, "editar_usuario.html", {'usuario': usuario, 'error_message_data_nascimento': 'A data de nascimento não pode ser superior à data atual.'})

        endereco = request.POST.get('endereco_usuario')
        senha = request.POST.get('senha_usuario')

        # Atualize os campos do usuário
        usuario.username = nome
        usuario.email = email
        usuario.data_nascimento = data_nascimento
        usuario.endereco = endereco

        if senha:
            # Atualize a senha do usuário de forma segura
            usuario.set_password(senha)

        # Salve as alterações no usuário
        usuario.save()

        # Atualize a sessão de autenticação para evitar logout
        update_session_auth_hash(request, usuario)

        return redirect(meu_perfil)
    else:
        return render(request, 'editar_usuario.html', {'usuario': usuario})

# EXCLUSÃO DE USUARIOS
@login_required
def confirma_deletar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    return render(request, 'deletar_usuario.html', {'usuario': usuario})

@login_required
def deletar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect(cadastrar_usuario)


# AUTENTICAÇÃO DE USUARIOS
def tela_login(request):
    return render(request, "login_usuario.html")

def login_usuario(request):
    if request.method == "POST":
        # if form.is_valid():
        email = request.POST.get('email_usuario')
        password = request.POST.get('senha_usuario')

        # Encontre o usuário com base no email
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return render(request, "login_usuario.html", {'error_message': 'usuário não encontrado'})

        if user:
            #VALIDAÇÃO FEITA COM O VALIDATE_PASSOWRD
            # validate_password(password, user=user)
            # Autenticar o usuário com base no email e senha
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Se autenticado com sucesso, faça o login
                login(request, user)
                if request.user.is_authenticated:
                    user_id = request.user.id
                    usuario_logado_obj = Usuario.objects.filter(id=user_id).first()
                    usuario = Usuario.objects.filter(username=usuario_logado_obj.username).first()
                    
                return render(request, "listar_portfolio.html", {'usuario': usuario})
            else:
                # Caso contrário, mensagem de erro
                return render(request, "login_usuario.html", {'error_message': 'senha incorreta'})
    else:
        # As credenciais estão incorretas
                return render(request, "login_usuario.html", {'error_message': 'senha incorreta'})



def logout_usuario(request):
    logout(request)
    return redirect("tela_login")





