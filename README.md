
# Projeto de Pipeline ETL com Prefect

Este projeto implementa uma pipeline **ETL (Extract, Transform, Load)** para consumir dados da [API BrasilAPI](https://brasilapi.com.br/api/banks/v1), transformar os dados no formato necessário e carregá-los em um banco de dados MySQL.

A pipeline utiliza as seguintes tecnologias:
- **Prefect**: Para orquestração das tarefas.
- **SQLAlchemy**: Para interação com o banco de dados.
- **Requests**: Para consumir a API.
- **MySQL**: Como banco de dados de destino.

## Estrutura do Projeto

```
/seu-projeto/
├── pipeline.py            # Arquivo principal da pipeline
├── test_pipeline_bancos.py  # Testes automatizados
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação
```

---

## Funcionalidades

1. **Extração de Dados**: Consome os dados da API pública [BrasilAPI](https://brasilapi.com.br/api/banks/v1) que retorna informações de bancos brasileiros, como:
   - Código ISPB
   - Nome do Banco
   - Código de compensação bancária
   - Nome completo da instituição

2. **Transformação dos Dados**: Converte os dados brutos da API para o formato compatível com o modelo relacional do banco de dados.

3. **Carregamento no Banco de Dados**: Insere os dados transformados em um banco de dados MySQL.

---

## Pré-requisitos

- Python 3.10+
- Banco de Dados MySQL
- Dependências listadas no arquivo `requirements.txt`

---

## Como Configurar o Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados MySQL:
   - Crie o banco de dados `banks_db`:

```sql
CREATE DATABASE banks_db;
```

- Certifique-se de que as credenciais no `pipeline.py` estão corretas:

```python
DATABASE_URL = "mysql+mysqlconnector://usuario:senha@localhost/banks_db"
```

---

## Como Executar a Pipeline

1. Execute o script principal:

```bash
python pipeline.py
```

2. O script realizará as seguintes etapas:
   - Extrairá os dados da API BrasilAPI.
   - Transformará os dados para o formato adequado.
   - Inserirá os dados no banco de dados MySQL.

---

## Como Testar

Os testes automatizados utilizam **pytest**. Para executá-los:

```bash
pytest test_pipeline_bancos.py
```

Os testes incluem:
- Validação da extração de dados da API.
- Testes de transformação de dados.
- Inserção dos dados em um banco de dados SQLite em memória.

---

## Endereço da API Consumida

A pipeline consome os dados da seguinte API:

- **BrasilAPI - Lista de Bancos**
  - Endpoint: [https://brasilapi.com.br/api/banks/v1](https://brasilapi.com.br/api/banks/v1)
  - Retorna informações sobre os bancos brasileiros.

Exemplo de resposta:

```json
[
  {
    "ispb": "00000000",
    "name": "Banco do Brasil S.A.",
    "code": 1,
    "fullName": "Banco do Brasil S.A."
  },
  {
    "ispb": "11111111",
    "name": "Caixa Econômica Federal",
    "code": 104,
    "fullName": "Caixa Econômica Federal"
  }
]
```

---

## Estrutura do Banco de Dados

A tabela criada no banco de dados MySQL é:

| **Campo**    | **Tipo**     | **Descrição**                  |
|--------------|--------------|--------------------------------|
| `id`         | `INT`        | Chave primária, autoincremento |
| `ispb`       | `VARCHAR(20)`| Código ISPB do banco           |
| `name`       | `VARCHAR(255)`| Nome do banco                 |
| `code`       | `INT`        | Código de compensação          |
| `full_name`  | `VARCHAR(255)`| Nome completo do banco         |

---

## Monitoramento da Pipeline com Prefect

1. Inicie o servidor Prefect:

```bash
prefect server start
```

2. Registre e execute a pipeline:

```bash
prefect deployment build pipeline.py:etl_pipeline -n "ETL Pipeline for Banks"
prefect deployment apply etl_pipeline-deployment.yaml
prefect agent start --work-queue "default"
```

3. Acesse o painel do Prefect para monitorar a execução: [http://localhost:4200](http://localhost:4200)

---

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Prefect**: Para orquestração e monitoramento.
- **SQLAlchemy**: Para interação com o banco de dados.
- **MySQL**: Banco de dados relacional.
- **Requests**: Para consumo da API.
- **pytest**: Para testes automatizados.

---

## Autor

Desenvolvido por [Cosme Sousa](https://github.com/cosmess).

---
