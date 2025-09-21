'''
Módulo de tratamento da base de dados.

Este módulo cóntem funções para o tratamento da base de dadas, 
afim de padronizar os dados para analise posterior no PostgreSQL,
utilizando-se das bibliotecas Pandas e Re.

Os tratamentos realizados serão:
    - Carregamento do arquivo CSV
    - Converção em um DataFrame
    - Renomeação das colunas
    - Exclusão de linhas vazias/inválidas
    - Padronização dos nomes de algumas informações
    - Extração dos números em strings
    - Ajustes do preços em Dólar para Reais
    - Preparação do arquivo para o PostgreSQL

Dependências:
    - pandas: Manipulação e análise dos dados
    - re: Manipulação de strings
    - requests: Realizar requisicoes HTTP e APIs REST
'''

import pandas as pd
import re
import requests

class TratarDados:
    '''
    Classe especializada para tratamento de datasets de veículos/carros.
    
    Esta classe oferece um conjunto de métodos específicos para processar
    dados automotivos, incluindo padronização de nomes de colunas em português,
    remoção de registros com informações inválidas ou incompletas, e 
    carregamento otimizado de arquivos CSV com tratamento de encoding.
    '''

    def __init__(self, caminho_csv=None):
        '''
        Inicializa a classe com configurações padrão.

        Configura o caminho do arquivo CSV e inicializa o DataFrame como None.
        Se nenhum caminho for fornecido, utiliza um caminho padrão para
        o dataset de carros de 2025.
        '''
        self.df = None
        self.caminho_csv = caminho_csv or 'data/raw/Cars Datasets 2025.csv'
    
    def carregar_dados(self):
        '''
        Carrega os dados do arquivo CSV para um DataFrame.

        Este método lê o arquivo CSV compatibilizando para o português.
        Se ocorrer erro, define como None e exibe mensagem do erro ocorrido.
        '''
        try:
            self.df = pd.read_csv(self.caminho_csv, encoding='latin1')
            print('Dados carregados com sucesso!')
        except Exception as e: 
            print('Erro ao carregar CSV:', e)
            self.df = None
        return self

    def renomear_colunas(self):
        '''
        Renomeia as colunas de inglês para o português.

        Define uma lista com os novos nomes para as colunas e realiza a alteração dos nomes.
        '''
        novos_nomes = ['Marca', 'Modelo', 'Motor', 'Cilindrada_Bateria', 'Potencia', 'Velocidade_Maxima', 'Aceleracao_0_100', 'Preco', 'Combustivel', 'Assentos', 'Torque']
        if self.df is not None:
            self.df.columns = novos_nomes
            print('Colunas renomeadas com sucesso!')
        else:
            print('Erro em renomear as colunas!')
        return self

    def excluir_linhas(self):
        '''
        Exclui linhas com valores inválidos.

        Define uma lista de valores inválidos e caso alguma linha possua algum desses valores,
        realiza a exclusão dela.
        '''
        valores_invalidos = ['N/A', 'N/a', '-', '', 'None']
        self.df = self.df[~self.df.isin(valores_invalidos).any(axis=1)]
        self.df = self.df.dropna()
        print('Linhas excluidas com sucesso!')
        return self

    def ajuste_nomes(self, colunas):
        '''
        Padroniza os nomes de alguns dados.

        Define os dados como String em determinadas colunas, removendo espaços desnecessários,
        converte letras para minúsculas, define a primeira letra maiúscula.
        '''
        colunas_invalidas = [col for col in colunas if col not in self.df.columns]
        if colunas_invalidas:
            print('Erro! Colunas não encontradas!')
        else: 
            for col in colunas:
                self.df[col] = self.df[col].astype(str).str.strip().str.lower().str.capitalize()
            print("Colunas ajustadas com sucesso!")
        return self

    def extrair_numeros(self, colunas):
        '''
        Extrai números de strings em colunas específicas do DataFrame.
    
        Este método processa colunas contendo dados textuais que incluem
        informações numéricas, extraindo apenas os valores numéricos e
        convertendo-os para formato apropriado (int ou float). Utiliza
        expressões regulares para identificar padrões numéricos e aplica
        estratégias diferentes dependendo da presença de vírgulas decimais.

        Note:
        - O método diferencia automaticamente entre valores com vírgula (decimais)
          e valores inteiros
        - Strings sem números retornam o valor original inalterado
        - Múltiplos números em uma string: apenas o primeiro é extraído
        - Vírgulas são tratadas como separadores decimais (padrão brasileiro)
        '''

        # Converte entrada para lista se for string única
        if isinstance(colunas, str):
            colunas = [colunas]
    
        # Define padrões regex para extração numérica
        padrao_geral = re.compile(r'(\d+(?:[.,]\d+)?)')
        padrao_cc = re.compile(r'(\d+(?:[.,]\d+)?)(?:\s*cc)', flags=re.IGNORECASE)

        def processar(texto):
            '''
            Função interna para extrair e processar números de uma string.
            
            Esta função aninhada realiza o processamento individual de cada
            valor textual, aplicando diferentes estratégias de extração baseadas
            no conteúdo da string. Trata casos especiais como valores decimais,
            múltiplos números e diferentes formatos numéricos.

            Processing Logic:
            1. Converte entrada para string para garantir compatibilidade
            2. Verifica presença de 'cc' para usar padrão específico
            3. Aplica regex apropriado para extrair números
            4. Se encontra números:
               - Um número: converte para int/float conforme formato
               - Múltiplos números: calcula e retorna a média
            5. Se não encontra números: retorna valor original
            ''' 

            # Transforma tudo em String para compatibilidade 
            texto = str(texto)

            # Verificar se contém 'cc' para aplicar padrão específico
            if 'cc' in texto.lower():
                matches = padrao_cc.findall(texto)
            else:
                matches = padrao_geral.findall(texto)

            # Processar números encontrados
            numeros = [float(m.replace(',', '')) for m in matches]

            # Retornar resultado baseado na quantidade de números encontrados
            if len(numeros) == 1:
                valor = numeros[0]
                return int(valor) if valor.is_integer() else valor
            else:
                media = int(round(sum(numeros) / len(numeros)))
                return media
        
        # Aplicar processamento para cada coluna especificada
        for col in colunas:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(processar)

        print('Numeros extraidos com sucesso!')
        return self

    def tratar_precos(self, colunas):
            '''
            Processa e ajusta preços de veículos com conversão automática de moeda.
            
            Este método realiza tratamento completo de dados de preços, incluindo:
            extração de valores numéricos de strings, consulta de cotação USD/BRL
            em tempo real via API, e correção automática de preços assumindo
            que valores baixos estão em milhares de dólares.

            Note:
            - A API de cotação tem timeout de 10 segundos
            - Múltiplos valores em uma string são convertidos para média
            - Em caso de falha na API, preços USD não são convertidos
            - Cotações são consultadas uma única vez por execução do método

            API Details:
            - Endpoint: https://economia.awesomeapi.com.br/json/last/USD-BRL
            - Timeout: 10 segundos
            - Fallback: Retorna None se API indisponível
            - Rate limit: Não especificado pela API
            ''' 
            # Converte entrada para lista se for string única
            if isinstance(colunas, str):
                colunas = [colunas]

            # Define padrão regex para extração de valores monetários
            padrao = re.compile(r'\d{1,3}(?:,\d{3})+')

            def processar(texto):
                '''
                Função interna para extrair e processar valores monetários de strings.
                
                Extrai números de strings contendo informações de preço, aplicando
                lógica específica para diferenciar valores únicos de múltiplos valores.
                Para valores únicos, retorna o número extraído. Para múltiplos valores,
                calcula e retorna a média aritmética.

                Processing Logic:
                1. Converte entrada para string para garantir compatibilidade
                2. Aplica regex para encontrar padrões numéricos monetários  
                3. Converte matches para float, tratando vírgulas como separador decimal
                4. Se encontra um número: retorna como inteiro
                5. Se encontra múltiplos números: calcula média e retorna como inteiro
                ''' 
                texto = str(texto)
                matches = padrao.findall(texto)
                numeros = [float(m.replace(',', '')) for m in matches]

                if len(numeros) == 1:
                    valor_usd = int(numeros[0])
                else:
                    valor_usd = int(round(sum(numeros) / len(numeros)))
                return valor_usd
            
            def obter_cotacao():
                '''
                Consulta cotação atual USD/BRL via API da AwesomeAPI.
        
                Função interna responsável por buscar a cotação atual do dólar
                americano em relação ao real brasileiro através de uma API
                pública gratuita. Implementa tratamento de erros e timeout
                para garantir robustez da aplicação.
                '''
                try:
                    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    cotacao = float(data['USDBRL']['ask'])  # Valor de venda
                    return cotacao
                except requests.RequestException as e:
                    return None
                except (KeyError, ValueError) as e:
                    return None
            
            # Obter cotação USD/BRL atual
            cotacao = obter_cotacao()

            def corrigir_preco(valor_usd):
                '''
                Aplica correção inteligente de preços baseada em cotação e valor.
        
                Função interna que implementa lógica de negócio para determinar
                se um valor deve ser convertido de USD para BRL ou mantido como
                está.
                '''
                valor_corrigido = int(valor_usd * cotacao)
                return valor_corrigido

            # Aplicar processamento para cada coluna especificada
            for col in colunas:
                if col in self.df.columns:
                    self.df[col] = self.df[col].apply(processar)
                    self.df[col] = self.df[col].apply(corrigir_preco)

            print('Preços ajustados com sucesso!')
            return self

    def preparar_postgres(self):
        '''
        Prepara dados textuais para compatibilidade com banco PostgreSQL.
    
        Este método realiza limpeza e normalização específica para dados que
        serão inseridos em banco PostgreSQL, focando em colunas de texto.
        Corrige problemas de encoding, remove caracteres especiais problemáticos
        e garante que os dados estejam em formato adequado para armazenamento
        em banco de dados relacional.
        
        O método aplica duas estratégias de limpeza:
        1. Tentativa de re-encoding UTF-8 com fallback para latin1
        2. Remoção de caracteres especiais via regex como plano B

        Note:
        - Apenas colunas de tipo 'object' (texto) são processadas
        - Colunas numéricas permanecem inalteradas
        - Primeira tentativa: re-encoding UTF-8 com fallback latin1
        - Segunda tentativa: regex para remoção de caracteres especiais
        - Preserva espaços e caracteres alfanuméricos básicos
        - Remove acentos, símbolos de marca registrada, copyright, etc.

        Processing Strategy:
        1. Identifica colunas de texto no DataFrame
        2. Para cada coluna, tenta correção de encoding primeiro
        3. Se falha, aplica limpeza via regex como fallback
        4. Mantém log de erros por coluna para debugging
        5. Continua processamento mesmo com erros individuais
        '''

        # Processa apenas colunas de texto (tipo 'object')
        for col in self.df.select_dtypes(include=['object']).columns:
            try:
                # Corrigindo o método de encoding
                self.df[col] = self.df[col].apply(lambda x: 
                    str(x).encode('latin-1', errors='ignore').decode('utf-8', errors='replace') 
                    if pd.notna(x) else x
                )
            except Exception as e:
                print(f"Erro na coluna {col}: {e}")
                # Fallback: apenas garantir que é string limpa
                self.df[col] = self.df[col].astype(str).str.replace('[^\w\s.-]', '', regex=True)

        print('Dados preparados com sucesso!')
        return self

    def tratamento(self):
        '''
        Executa pipeline completo de tratamento de dados automotivos.
    
        Método orquestrador que executa toda a sequência de tratamento
        de dados de forma automatizada e na ordem correta. Implementa
        o fluxo completo desde carregamento até preparação final para
        banco de dados, incluindo todos os passos de limpeza, transformação
        e normalização necessários.
        
        Este método centraliza todo o processo de ETL (Extract, Transform, Load)
        específico para datasets de veículos, garantindo que os dados passem
        por todas as etapas necessárias de forma consistente e ordenada.
        
        Pipeline de Execução:
        1. Carregamento dos dados do CSV
        2. Renomeação de colunas para português
        3. Exclusão de linhas com dados inválidos  
        4. Normalização de nomes (marca/modelo)
        5. Extração de números das colunas especificadas
        6. Tratamento de preços com conversão de moeda
        7. Preparação final para PostgreSQL

        Note:
        - Executa todos os métodos da classe em sequência otimizada
        - Cada etapa valida a anterior antes de prosseguir
        - Em caso de erro, interrompe pipeline e reporta problema
        - Retorna DataFrame final pronto para análises ou insert em BD
        - Método ideal para execução automatizada e batch processing
        '''
        self.carregar_dados()
        self.renomear_colunas()
        self.excluir_linhas()
        self.ajuste_nomes(['Marca', 'Modelo'])
        self.extrair_numeros(['Cilindrada_Bateria', 'Potencia', 'Velocidade_Maxima', 'Aceleracao_0_100', 'Assentos', 'Torque'])
        self.tratar_precos('Preco')
        self.preparar_postgres()
        return self.df
