# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das minhas variaveis de ambiente

commodities = ['CL=F', 'GC=F', 'SI=F']

def buscar_dados_commodities(ticker, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(ticker)
    dados = ticker.history(period=periodo, interval = intervalo)[['Close']]
    dados['ticker'] = ticker
    return dados

def buscar_todos_commodities(commodities):
    todos_dados = []
    for ticker in commodities:
        dados = buscar_dados_commodities(ticker)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

# pegar a cotação dos meus ativos

# concatenar os meus ativos (1...2..3) -> (1)


if __name__ == "__main__":
    dados_concatenado = buscar_todos_commodities(commodities)
    print(dados_concatenado)
