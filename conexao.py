"""
Módulo de gerenciamento de banco de dados PostgreSQL.

Este módulo contém funções para configuração e criação de bancos de dados PostgreSQL
utilizando as bibliotecas psycopg2 e SQLAlchemy com isolamento de transação configurado.

Dependências:
    - os: Para acesso a variáveis de ambiente
    - dotenv: Para carregar variáveis do arquivo .env
    - psycopg2: Driver PostgreSQL para Python
    - sqlalchemy: ORM e toolkit SQL para Python
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
# Carrega as variáveis de ambiente do arquivo.env
load_dotenv()

def criar_banco(df):
    """
    Cria um banco de dados PostgreSQL se ele não existir.
    
    Esta função estabelece uma conexão com o servidor PostgreSQL usando credenciais
    das variáveis de ambiente, verifica se o banco de dados especificado existe,
    e o cria caso não exista.
    
    Variáveis de ambiente requeridas:
        DB_USER (str): Nome do usuário do PostgreSQL
        DB_PASS (str): Senha do usuário do PostgreSQL
        DB_HOST (str): Endereço do servidor PostgreSQL
        DB_PORT (str): Porta do servidor PostgreSQL
        DB_NAME (str): Nome do banco de dados a ser criado
    
    Raises:
        psycopg2.Error: Para erros relacionados à conexão ou operações no PostgreSQL
        EnvironmentError: Se alguma variável de ambiente obrigatória não estiver definida
        
    Returns:
        None
        
    Example:
        >>> criar_banco() = Banco de dados 'meu_banco' criado com sucesso.
        ou
        >>> criar_banco() = Banco de dados 'meu_banco' já existe.
    """

    # Carrega as variáveis de ambiente
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")


    try:
        # Conecta ao servidor PostgreSQL
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Define o nível de isolamento para autocomit
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Cria um cursor para executar comandos SQL
        cur = conn.cursor()

        # Verifica se o banco já existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        existe = cur.fetchone()

        if not existe:
            # Cria o bando de dados se não existir com mensagem de confirmação ou se ele já existir
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"Banco de dados '{db_name}' já existe.")

        # Fecha as conexões
        cur.close()
        conn.close()

        # Cria a engine:
        connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(connection_string)

        # Grava o Dataframe:
        df.to_sql('cars_db_tratado', con=engine, if_exists='replace', index=False)
        print(f"Tabela cars_db_tratado criada com sucesso no banco.")

    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")