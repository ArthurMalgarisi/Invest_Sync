from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario
from carteira.models import Carteira
from portfolio.models import Portfolio
from carteira_acao.models import Carteira_Acao

from django.shortcuts import render
import matplotlib.pyplot as plt
from django.db.models import Sum
from datetime import datetime
import calendar

def dashboard(request):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolios = Portfolio.objects.filter(id_usuario = user)

    dados_portfolio = []

    for portfolio in portfolios:
        carteiras = Carteira.objects.filter(id_portfolio=portfolio.id_portfolio)

        # Inicializa as variáveis dentro do loop do portfolio
        conta_carteira = 0
        valor_total_port = 0

        for carteira in carteiras:
            conta_carteira += 1
            valor_total_port += carteira.valor_total_carteira

        # Adiciona as informações ao dados_portfolio dentro do loop do portfolio
        dados_portfolio.append(
            {
                'nome': portfolio.nome_portfolio,
                'valor_total': valor_total_port,
                'quant_carteira': conta_carteira
            })

    return render(request, 'chart_template.html', {'usuario': usuario, 'dados_portfolio': dados_portfolio})

def pizzaChart(request, id_portfolio):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    portfolio = Portfolio.objects.get(id_portfolio =id_portfolio)
    carteiras = Carteira.objects.filter(id_portfolio = id_portfolio)
    return render(request, 'chart.html', {'usuario': usuario, 'carteiras': carteiras})

def barMonth(request, id_portfolio):
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

    return render(request, 'grafico_bar.html', {'dados_bar': dados_bar})
