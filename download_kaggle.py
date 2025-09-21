'''
Módulo de download e gerenciamento de datasets do Kaggle.

Este módulo fornece funcionalidades para automatizar o download de datasets
da plataforma Kaggle, configurar credenciais da API, criar estrutura de 
diretórios e retornar caminhos dos arquivos baixados para uso em projetos
de ciência de dados.

Dependências:
    - os: Manipulação de sistema operacional e caminhos de arquivos
    - shutil: Operações de arquivos de alto nível (cópia, movimentação)
    - kaggle.api.kaggle_api_extended: Cliente oficial da API do Kaggle

Pré-requisitos:
    - Conta no Kaggle com API ativada
    - Arquivo kaggle.json com credenciais válidas no diretório do projeto
    - Conexão com internet para download dos datasets
'''
import os 
import shutil 
from kaggle.api.kaggle_api_extended import KaggleApi

def baixar_dataset():
    '''
    Realiza o download automaticamente de um dataset específico do Kaggle.

    Função para automatizar todo o processo de download, incluindo configuração de credenciais,
    criação de diretorios e autenticação de API.

    O dataset em questão contém dados sobre carros de 2025 no formata de CSV.

    Returns:
        str: Caminho completo para o arquivo CSV baixado no formato:
             'data/raw/cars-datasets-2025.csv'

    Note:
        - O arquivo kaggle.json deve estar presente no diretório raiz do projeto
        - É necessário ter uma conta Kaggle válida com API ativada
        - O download pode demorar dependendo do tamanho do dataset e conexão
        - Arquivos existentes serão sobrescritos sem aviso
        - As credenciais são copiadas para ~/.kaggle/ seguindo o padrão da API
    '''

    # Define a pasta de destino, verificando se ela exiate
    pasta_destino = os.path.join('data', 'raw') 
    os.makedirs(pasta_destino, exist_ok=True)

    # Copia o arquivo kaggle.json para o local padrão, verificando se a pasta destino existe.
    origem = os.path.join(pasta_destino, 'kaggle.json') 
    destino = os.path.join(os.path.expanduser('~'), '.kaggle') 
    os.makedirs(destino, exist_ok=True) 
    
    # Verifica caso não encontrar o arquivo na pasta destino, copia para a pasta padrão
    if not os.path.exists(os.path.join(destino, 'kaggle.json')):
        shutil.copy(origem, os.path.join(destino, 'kaggle.json')) 

    # Cria a isntância da API e autentica com o Kaggle
    api = KaggleApi() 
    api.authenticate() 
    
    # Define o dataset que será baixado
    dataset = 'abdulmalik1518/cars-datasets-2025' 

    # Faz o download do dataset e extrai o arquivo zip
    api.dataset_download_files(dataset, path=pasta_destino, unzip=True) 

    # Retorna o caminho do arquivo csv
    return os.path.join(pasta_destino, 'cars-datasets-2025.csv') 
