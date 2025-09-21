'''
Módulo central para realização do tratamento da base de dados.

Realiza a importação dos outros módulos para centralizar a execução dos demais módulos e funções.


'''
from download_kaggle import  baixar_dataset
from tratamento import TratarDados
from conexao import criar_banco

# Executa o script diretamente
if __name__ == "__main__":
    # Executa a função de realizar o download do dataset
    caminho = baixar_dataset()
    print("Arquivo baixado em:", caminho)
    
    # Executa o tratamento de dados e retorna um DataFrame limpo
    df = TratarDados().tratamento()
    print("Arquivo tratado com sucesso!")

    # Valida se o DataFrame foi carregado corretamente e executa a função de criação do banco no PostgreSQL
    if df is not None:
        criar_banco(df)
    else:
        print("Erro: DataFrame não foi carregado corretamente.")

    

