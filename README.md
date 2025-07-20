# Trabalho Final - FIAP - 10DTSR - MLOPS

Ana Cristina Lourenço Maria: RM359310

Jayana da Silva Alves: RM359631

Pedro Silva de Sá Monnerat: RM359532

# Predição de Score de Crédito

Este projeto implementa uma API para predição de score de crédito usando um modelo de Machine Learning. O modelo é versionado e baixado de um registro de modelos (MLflow via DagsHub) e a aplicação é empacotada em um contêiner Docker para deployment como uma função AWS Lambda.

# Estrutura do Projeto

- data.json: Um arquivo JSON de exemplo contendo os dados de entrada para a predição.

- Dockerfile: Define a imagem Docker para a aplicação Lambda.

- model_downloader.py: Script para baixar a versão mais recente do modelo e seus metadados do MLflow.

- requirements.txt: Lista as dependências Python do projeto.

- test.py: Um script simples para testar a função app.handler localmente com o data.json de exemplo.

- src/app.py: Contém o código da função Lambda principal que realiza a predição, registra métricas no CloudWatch e armazena os dados de entrada e predição no S3.

- tests/app_test.py: Testes unitários para a funcionalidade da aplicação.

- tests/conftest.py: Configuração para os testes Pytest, ajustando o sys.path para importar módulos do diretório src.

- .github/deploy.yml: Workflow do GitHub Actions para o deployment contínuo da API no AWS Lambda via ECR.

- .github/review.yml: Workflow do GitHub Actions para a revisão de Pull Request, incluindo testes e linting.

# API (Função Lambda)

A função Lambda (src/app.py) é responsável por:

- Carregar o modelo de predição e seus metadados.

- Processar o payload de entrada, que pode vir de um API Gateway ou de uma invocação direta da Lambda.

- Padronizar os dados de entrada (prepare_payload) para que sejam compatíveis com o modelo.

- Realizar a predição do score de crédito.

- Registrar métricas customizadas no AWS CloudWatch (input_metrics) para monitoramento.

- Armazenar os dados de entrada e a predição em um bucket S3 (write_real_data) para análise posterior e detecção de desvios.

- Retornar a predição e a versão do modelo em formato JSON.

## Estrutura do Payload de Entrada

A API espera um payload JSON com a seguinte estrutura:

```json
{
  "data": {
    "Age": "40",
    "Annual_Income": "100000",
    "Monthly_Inhand_Salary": "8000",
    "Num_Bank_Accounts": "2",
    "Num_Credit_Card": "4",
    "Interest_Rate": "10",
    "Num_of_Loan": "2",
    "Delay_from_due_date": "4",
    "Num_of_Delayed_Payment": "11",
    "Changed_Credit_Limit": "6",
    "Num_Credit_Inquiries": "3",
    "Outstanding_Debt": "2000",
    "Credit_Utilization_Ratio": "30",
    "Credit_History_Age": "200",
    "Total_EMI_per_month": "50",
    "Amount_invested_monthly": "250",
    "Monthly_Balance": "400",
    "Occupation": "Doctor",
    "Credit_Mix": "Good",
    "Payment_of_Min_Amount": "No",
    "Payment_Behaviour": "High_spent_Large_value_payments"
  }
}
```

## Exemplo de resposta:

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"prediction\": <valor_do_score>, \"version\": \"<versao_do_modelo>\"}"
}
```
