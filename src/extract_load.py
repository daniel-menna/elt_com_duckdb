# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das minhas variaveis de ambiente

load_dotenv()

commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST=os.getenv('DB_HOST_PROD')
DB_PORT=os.getenv('DP_PORT_PROD')
DB_NAME=os.getenv('DB_NAME_PROD')
DB_USER=os.getenv('DB_USER_PROD')
DB_PASS=os.getenv('DB_PASS_PROD')
DB_SCHEMA=os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

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

def salvar_no_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Data', schema=schema )

if __name__ == "__main__":
    dados_concatenado = buscar_todos_commodities(commodities)
    salvar_no_postgres(dados_concatenado, schema='public')
