from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Acao
import requests
import re
import time
import investpy as inv

# implementar lógica da api para popular o banco com as ações
def get_stock_quote(ticker, api_token):
    url = f"https://brapi.dev/api/quote/{ticker}?range=5d&interval=1d&token={api_token}"
    response = requests.get(url).json()
    return response


def popula_acoes(request):
    api_token = "9ueU3f4oS1qp1epkf35xWd"

    br = inv.stocks.get_stocks(country='brazil')

    # Obtém a lista de ações do Brasil
    acoes_brasil = []
    br = inv.stocks.get_stocks(country='brazil')
    for stock in br['symbol']:
        if len(stock) <= 5:
            acoes_brasil.append(stock)

    # Obtém a lista de ações dos Estados Unidos
    acoes_eua = []
    us = inv.stocks.get_stocks(country='united states')
    for stock in us['symbol']:
        if len(stock) <= 5:
            acoes_eua.append(stock)

    # Combina as listas de ações do Brasil e dos Estados Unidos
    todas_acoes = acoes_brasil + acoes_eua

    for acao in todas_acoes:
        try:
            stock = get_stock_quote(acao, api_token)

            # Verifica se 'results' está presente no dicionário retornado
            if 'results' in stock:
                nome_acao_completo = stock['results'][0]['shortName']
                nome_acao_formatado = re.sub(r'\s+', ' ', nome_acao_completo).strip()

                # Dados das ações para guardar no banco
                nome_acao = nome_acao_formatado
                preco_mais_baixo = stock['results'][0]['regularMarketDayLow']
                preco_mais_alto = stock['results'][0]['regularMarketDayHigh']
                simbolo_acao = stock['results'][0]['symbol']
                nome_empresa = stock['results'][0]['longName']

                # Criação de uma nova instância do modelo Acao
                acao = Acao(
                    nome_acao=nome_acao,
                    preco_mais_baixo=preco_mais_baixo,
                    preco_mais_alto=preco_mais_alto,
                    simbolo_acao=simbolo_acao,
                    nome_empresa=nome_empresa,
                    data_acao=timezone.now()
                )

                # Salvando a instância no banco de dados
                acao.save()
            else:
                print(f"A chave 'results' não está presente na resposta para a ação {acao}")

        except KeyError as e:
            print(f"Erro ao processar ação {acao}: {e}")
            continue

    return HttpResponse("Ações populadas com sucesso!")