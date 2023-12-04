from django.shortcuts import render, redirect
from portfolio.models import Portfolio
from carteira.models import Carteira
from acao.models import Acao
from usuario.models import Usuario
from carteira_acao.models import Carteira_Acao
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime  # Adicionando a importação do datetime

@login_required
def listar_portfolio(request):
    user = request.user.id
    portfolios_list = Portfolio.objects.filter(id_usuario=user)
    usuario = Usuario.objects.get(id=user)

    # Lógica para contar a quantidade de carteira em um portfolio
    dados_portfolio = []
    for portfolio in portfolios_list:
        carteiras = Carteira.objects.filter(id_portfolio=portfolio.id_portfolio)
        quantidade_carteira = carteiras.count()
        somatorio = 0.0
        for carteira in carteiras:
            somatorio += carteira.valor_total_carteira

        dados_portfolio.append({
            'portfolio': portfolio,
            'quantidade_carteira': quantidade_carteira,
            'valor_total_portfolio': somatorio
        })

    # Paginação
    portfolio_paginator = Paginator(dados_portfolio, 6)  # Paginar dados_portfolio, não portfolios_list
    page_num = request.GET.get('page')
    page = portfolio_paginator.get_page(page_num)

    return render(request, 'listar_portfolio.html', {'page': page, 'usuario': usuario, 'dados_portfolio': page.object_list})

@login_required
def cadastrar_portfolio(request):
    usuario = request.user
    if request.method == 'POST':
        nome_portfolio = request.POST.get('nome_portfolio')
        descricao_portfolio = request.POST.get('descricao_portfolio')

        portfolio_cadastro = Portfolio(
            nome_portfolio=nome_portfolio,
            descricao_portfolio=descricao_portfolio,
            id_usuario=usuario
        )

        portfolio_cadastro.save()
        return redirect(listar_portfolio)
    else:
        return render(request, 'cadastrar_portfolio.html', {'usuario': usuario})

@login_required
def editar_portfolio(request, id_portfolio):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    if request.method == 'POST':
        nome = request.POST.get('nome_portfolio')
        descricao = request.POST.get('descricao_portfolio')

        portfolio.nome_portfolio = nome
        portfolio.descricao_portfolio = descricao

        portfolio.save()

        return redirect(listar_portfolio)
    else:
        return render(request, 'editar_portfolio.html', {'portfolio': portfolio, 'usuario': usuario})

@login_required
def deletar_portfolio(request, id_portfolio):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolios_list = Portfolio.objects.filter(id_portfolio=id_portfolio)

    dados_portfolio = []
    for portfolio in portfolios_list:
        carteiras = Carteira.objects.filter(id_portfolio=portfolio.id_portfolio)
        quantidade_carteira = carteiras.count()
        somatorio = 0.0
        for carteira in carteiras:
            somatorio += carteira.valor_total_carteira

        dados_portfolio.append({
            'portfolio': portfolio,
            'quantidade_carteira': quantidade_carteira,
            'valor_total_portfolio': somatorio
        })

    if request.method == 'POST':
        portfolio.delete()
        return redirect(listar_portfolio)
    else:
        return render(request, 'deletar_portfolio.html', {'portfolio': portfolio, 'usuario': usuario, 'dados_portfolio': dados_portfolio})

#CARTEIRA
@login_required
def listar_carteira(request, id_portfolio):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteiras = Carteira.objects.filter(id_portfolio=id_portfolio)

    #LÓGICA DE CRIAÇÃO DE GRÁFICOS
    traducao_meses_invertida = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
    'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
    'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
    'November': 'Novembro', 'December': 'Dezembro'
    }

    investimentos_por_mes = {month: 0 for month in traducao_meses_invertida.keys()}

    for carteira in carteiras:
        acoes = Carteira_Acao.objects.filter(id_carteira=carteira.id_carteira, data_compra__year=2023)
        for acao in acoes:
            mes_ingles = datetime.strftime(acao.data_compra, "%B")
            if mes_ingles in traducao_meses_invertida:
                mes = datetime.strftime(acao.data_compra, "%B")  # Obtém o nome do mês a partir da data da compra
                investimentos_por_mes[mes] += (acao.cotacao * acao.lote_acao)
            else:
                print(f"Mês não encontrado no dicionário: {mes_ingles}")

    dados_bar = [{'mes': mes, 'valor': valor} for mes, valor in investimentos_por_mes.items()]

    #FIM DA LÓGICA DE CRIAÇÃO DE GRÁFICO DE BARRA
    
     #LÓGICA DE CRIAÇÃO DE GRÁFICOS de Liinha
    traducao_meses_invertida = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
    'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho',
    'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro',
    'November': 'Novembro', 'December': 'Dezembro'
    }

    investimentos_por_mes = {month: 0 for month in traducao_meses_invertida.keys()}

    for carteira in carteiras:
        acoes = Carteira_Acao.objects.filter(id_carteira=carteira.id_carteira, data_compra__year=2023)
        for acao in acoes:
            mes_ingles = datetime.strftime(acao.data_compra, "%B")
            if mes_ingles in traducao_meses_invertida:
                mes = datetime.strftime(acao.data_compra, "%B")  # Obtém o nome do mês a partir da data da compra
                investimentos_por_mes[mes] += (acao.cotacao * acao.lote_acao)
            else:
                print(f"Mês não encontrado no dicionário: {mes_ingles}")

    dados_line = [{'mes': mes, 'valor': valor} for mes, valor in investimentos_por_mes.items()]

    #FIM DA LÓGICA DE CRIAÇÃO DE GRÁFICO DE Linha
    
    #INICIO LÓGICA CRIAÇÃO DE GRÁFICO DE PIZZA

    porcent_pizza = []
    valor_total_portfolio = 0
    
    for carteira in carteiras:
        valor_total_portfolio += carteira.valor_total_carteira

    for carteira in carteiras:
        if carteira.valor_total_carteira == 0:
            porcent_pizza.append({'nome_carteira': carteira.nome_carteira, 'porcent': 0, 'valor_total': valor_total_portfolio})
        else:
            porcent_pizza.append({'nome_carteira': carteira.nome_carteira, 'porcent': round((carteira.valor_total_carteira / valor_total_portfolio) * 100), 'valor_total_carteira': carteira.valor_total_carteira})

    #FIM DA LÓGICA DE CRIAÇÃO DE GRÁFICO DE PIZZA
    
    # Paginação
    carteira_paginator = Paginator(carteiras, 6)
    page_num = request.GET.get('page')
    page = carteira_paginator.get_page(page_num)

    return render(
        request,'listar_carteira.html',{'portfolio': portfolio,'page': page,'usuario': usuario,'dados_bar': dados_bar,'porcent_pizza': porcent_pizza, 'dados_line': dados_line})

@login_required
def cadastrar_carteira(request, id_portfolio):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)

    if request.method == 'POST':
        nome_carteira = request.POST.get('nome_carteira')
        descricao_carteira = request.POST.get('descricao_carteira')
        valor_total_carteira = 0

        carteira = Carteira(
            nome_carteira=nome_carteira,
            descricao_carteira=descricao_carteira,
            valor_total_carteira=valor_total_carteira,
            id_portfolio=portfolio
        )

        carteira.save()
        return redirect(listar_carteira, id_portfolio=id_portfolio)
    else:
        return render(request, 'cadastrar_carteira.html', {'portfolio': portfolio, 'usuario': usuario})

@login_required
def editar_carteira(request, id_portfolio, id_carteira):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira = Carteira.objects.get(id_carteira=id_carteira)

    if request.method == 'POST':
        nome_carteira = request.POST.get('nome_carteira')
        descricao_carteira = request.POST.get('descricao_carteira')

        carteira.nome_carteira = nome_carteira
        carteira.descricao_carteira = descricao_carteira
        carteira.save()

        return redirect(listar_carteira, id_portfolio=id_portfolio)
    else:
        return render(
            request,
            'editar_carteira.html',
            {
                'portfolio': portfolio,
                'carteira': carteira,
                'usuario': usuario
            }
        )

@login_required
def deletar_carteira(request, id_portfolio, id_carteira):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira = Carteira.objects.get(id_carteira=id_carteira)

    if request.method == 'POST':
        carteira.delete()
        return redirect(listar_carteira, id_portfolio)
    else:
        return render(request, 'deletar_carteira.html', {'portfolio': portfolio, 'carteira': carteira, 'usuario': usuario})


#CARTEIRA_AÇÃO
@login_required
def listar_acao(request, id_portfolio, id_carteira):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira = Carteira.objects.get(id_carteira=id_carteira)
    carteira_acao = Carteira_Acao.objects.filter(id_carteira=id_carteira)
    
    acoes_ids = [carteira_item.id_acao_id for carteira_item in carteira_acao]  # Obtenha os IDs das ações
    # Agora você pode filtrar as ações associadas à carteira
    acoes_associadas = Acao.objects.filter(id_acao__in=acoes_ids)

    carteira_acao_paginator = Paginator(carteira_acao, 8)
    page_num = request.GET.get('page')
    page = carteira_acao_paginator.get_page(page_num)

    return render(
        request,
        'listar_acao.html',
        {
            'portfolio': portfolio,
            'carteira': carteira,
            'page': page,
            'acao': acoes_associadas,
            'usuario': usuario
        }
    )

@login_required
def deletar_acao(request, id_portfolio, id_carteira, id_carteira_acao):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira_acao = Carteira_Acao.objects.get(id_carteira_acao=id_carteira_acao)
    carteira = Carteira.objects.get(id_carteira=id_carteira)
    acao = Acao.objects.filter(id_acao=carteira_acao.id_acao.id_acao)
    # acao = Acao.objects.filter(id_acao=carteira_acao.id_acao.id_acao).all()
    # print(carteira_acao.id_aca.id_acao)

    if request.method == 'POST':

        #LOGICA DE SOMATÓRIO DE AÇÕES POR CARTEIRA
        valor_carteira = carteira.valor_total_carteira
        valor_carteira = valor_carteira - (carteira_acao.lote_acao * carteira_acao.cotacao)

        carteira_valor_total = Carteira(
            id_carteira = carteira.id_carteira,
            nome_carteira = carteira.nome_carteira,
            valor_total_carteira = valor_carteira,
            descricao_carteira = carteira.descricao_carteira,
            id_portfolio = carteira.id_portfolio
        )
        #FIM LÓGICA SOMATÓRIO

        carteira_valor_total.save()
        carteira_acao.delete()
        return listar_acao(request, id_portfolio, id_carteira)
    else:
        return render(request, 'deletar_acao.html', {'portfolio':portfolio, 'carteira': carteira, 'carteira_acao': carteira_acao, 'acao': acao, 'usuario': usuario})

def editar_acao(request, id_portfolio, id_carteira, id_carteira_acao):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    
    # Adicione estas linhas para recuperar os objetos do banco de dados
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira_acao = Carteira_Acao.objects.get(id_carteira_acao=id_carteira_acao)
    carteira = Carteira.objects.get(id_carteira=id_carteira)

    if request.method == 'POST':
        lote_acao = request.POST.get('lote_acao')
        cotacao = request.POST.get('cotacao')
        data_compra_str = request.POST.get('data_compra')

        try:
            data_compra_obj = datetime.strptime(data_compra_str, '%d/%m/%Y')
        except ValueError:
            return render(request, "editar_acao.html", {'portfolio': portfolio, 'carteira': carteira, 'carteira_acao': carteira_acao, 'usuario': usuario, 'error_message_data': 'Formato de data inválido'})

        cotacao = float(cotacao)
        lote_acao = int(lote_acao)

        valor_carteira = carteira.valor_total_carteira
        valor_carteira = valor_carteira - (carteira_acao.lote_acao * carteira_acao.cotacao)

        carteira_acao.lote_acao = lote_acao
        carteira_acao.cotacao = cotacao
        carteira_acao.data_compra = data_compra_obj

        valor_carteira += (lote_acao * cotacao)

        carteira.valor_total_carteira = valor_carteira

        carteira.save()
        carteira_acao.save()
        return redirect(listar_acao, id_portfolio=id_portfolio, id_carteira=id_carteira)
    else:
        return render(request, 'editar_acao.html', {'portfolio': portfolio, 'carteira': carteira, 'carteira_acao': carteira_acao, 'usuario': usuario})

@login_required
def cadastrar_acao(request, id_portfolio, id_carteira):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira = Carteira.objects.get(id_carteira=id_carteira)
    acoes = Acao.objects.all()
    simbolos_acao = list(Acao.objects.values_list('simbolo_acao', flat=True))

    if request.method == 'POST':
        nome_empresa = request.POST.get('nome_empresa')
        simbolo_acao = request.POST.get('simbolo_acao')
        lote_acao = request.POST.get('lote_acao')
        cotacao = request.POST.get('cotacao')
        data_compra_str = request.POST.get('data_compra')  # Corrigido para data_compra_str

        #LOGICA DE DATAS ARTHUR
        cotacao = cotacao.replace(',', '.')
        cotacao = float(cotacao)
        lote_acao = int(lote_acao)

        #LOGICA DE SOMATÓRIO DE AÇÕES POR CARTEIRA
        valor_carteira = carteira.valor_total_carteira
        valor_carteira += (lote_acao * cotacao)

        id_acao = 0
        acao_obj = None
        if acoes:
            for acao in acoes:
                if acao.simbolo_acao == simbolo_acao:
                    id_acao = acao.id_acao
                    acao_obj = acao
            if id_acao == 0:
                return render(request, "cadastrar_acao.html", {'portfolio': portfolio, 'carteira': carteira, 'error_message': 'A ação informada não existe em nosso banco de dados'})
        else:
            return render(request, "cadastrar_acao.html", {'portfolio': portfolio, 'carteira': carteira, 'error_message': 'A ação informada não existe em nosso banco de dados'})

        # Converta a string da data de compra para um objeto datetime
        try:
            data_compra_obj = datetime.strptime(data_compra_str, '%d/%m/%Y')
        except ValueError:
            return render(request, "cadastrar_acao.html", {'portfolio': portfolio, 'carteira': carteira, 'error_message_data': 'Formato de data inválido'})

        carteira_acao = Carteira_Acao(
            lote_acao=lote_acao,
            cotacao=cotacao,
            data_compra=data_compra_obj,
            id_acao=acao_obj,
            id_carteira=carteira
        )

        carteira_valor_total = Carteira(
            id_carteira = carteira.id_carteira,
            nome_carteira = carteira.nome_carteira,
            valor_total_carteira = valor_carteira,
            descricao_carteira = carteira.descricao_carteira,
            id_portfolio = carteira.id_portfolio
        )

        carteira_acao.save()
        carteira_valor_total.save()
        return redirect(listar_acao, id_portfolio=id_portfolio, id_carteira=id_carteira)
    else:
        return render(request, 'cadastrar_acao.html', {'portfolio': portfolio, 'carteira': carteira, 'usuario': usuario, 'simbolos_acao': simbolos_acao})
    
def detalhar_acao(request, id_portfolio, id_carteira, id_carteira_acao, id_acao):
    user = request.user.id
    portfolio = Portfolio.objects.get(id_portfolio=id_portfolio)
    carteira = Carteira.objects.get(id_carteira=id_carteira)
    usuario = Usuario.objects.get(id=user)
    carteira_acao = Carteira_Acao.objects.get(id_carteira_acao=id_carteira_acao)
    acao = Acao.objects.get(id_acao=id_acao)

    return render(
        request,
        'detalhar_acao.html',
        {
            'acao' : acao,
            'usuario': usuario,
            'carteira_acao': carteira_acao,
            'portfolio': portfolio,
            'carteira': carteira
        }
    )