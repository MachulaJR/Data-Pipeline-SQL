
# Python-ETL-SQL

Automatizador de tratamento de dados do Kaggle com integração ao PostgreSQL. 
Este projeto realiza o download automático de datasets, aplica transformações e insere os dados tratados em um banco relacional para consultas SQL.

---

## 📦 Funcionalidades

- 🔽 Download automático do dataset público via API do Kaggle  
- 🧹 Tratamento e limpeza dos dados com Pandas  
- 🗄️ Inserção dos dados tratados em banco PostgreSQL  
- 🔍 Suporte para consultas SQL após ingestão  

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10  
- Pandas  
- SQLAlchemy  
- Psycopg2  
- PostgreSQL  
- Kaggle API  
- Requests — para chamadas HTTP  
- re — para expressões regulares  
- python-dotenv — para gerenciamento de variáveis de ambiente  
- os — para manipulação de sistema de arquivos  
- shutil — para operações de cópia e movimentação de arquivos

---

## 📁 Estrutura de Diretórios

AUTOMACAO-RELATORIOS/
├── __pycache__/                  # Arquivos compilados automaticamente pelo Python
│   ├── conexao.cpython-313.pyc
│   ├── download_kaggle.cpython-313.pyc
│   ├── processor.cpython-313.pyc
│   └── tratamento.cpython-313.pyc
│
├── data/
│   └── raw/                      # Dados brutos e credenciais
│       ├── Cars Datasets 2025.csv
│       └── kaggle.json
│
├── docs/                         # Documentação e relatórios gerados
│   └── relatorio_consultas.pdf
│   └── Consultas.sql             # Script com consultas SQL para análise
│
├── venv/                         # Ambiente virtual Python (não versionar)
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── .gitignore
│   └── pyvenv.cfg
│
├── .env                          # Variáveis de ambiente (ex: credenciais)
├── cars_data.db                  # Banco de dados SQLite gerado pelo pipeline
├── README.md                     # Documentação principal do projeto
├── requirements.txt              # Lista de dependências do projeto
│
├── main.py                       # Script principal que executa o pipeline ETL
├── conexao.py                    # Módulo de conexão e inserção no banco
├── download_kaggle.py           # Módulo para baixar datasets via API do Kaggle
├── processor.py                 # Módulo para processamento adicional dos dados
├── tratamento.py                # Módulo para limpeza e transformação dos dados
