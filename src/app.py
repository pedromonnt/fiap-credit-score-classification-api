"""
Função para executar predição de score de crédito com base no histórico do cliente.
Utiliza modelo que precisa ser baixado do repositório de registro de modelos em toda 
implantação nova.
"""

from datetime import datetime
import json
import boto3
import joblib

model = joblib.load('model/model.pkl')

with open('model/model_metadata.json', 'r', encoding="utf-8") as f:
    model_info = json.load(f)

cloudwatch = boto3.client('cloudwatch')

def write_real_data(data, prediction):
    """
    Função para escrever os dados consumidos para depois serem estudados 
    para desvios de dados, modelo ou conceito.

    Args:
        data (dict): dicionário de dados com todos os atributos.
        prediction (int): valor de predição.
    """

    now = datetime.now()
    now_formatted = now.strftime("%d-%m-%Y %H:%M")

    file_name = f"{now.strftime('%Y-%m-%d')}_credit_score_classification_data.csv"

    data["credit_score"] = prediction
    data["timestamp"] = now_formatted
    data["model_version"] = model_info["version"]

    s3 = boto3.client('s3')

    bucket_name = 'pedromonnerat-mlops'
    s3_path = 'dataset'

    try:
        existing_object = s3.get_object(Bucket=bucket_name, Key=f"{s3_path}/{file_name}")
        existing_data = existing_object['Body'].read().decode('utf-8').strip().split('\n')
        existing_data.append(','.join(map(str, data.values())))
        update_content = '\n'.join(existing_data)

    except s3.exceptions.NoSuchKey:
        update_content = ','.join(data.keys()) + '\n' + ','.join(map(str, data.values()))

    s3.put_object(Body=update_content, Bucket=bucket_name, Key=f"{s3_path}/{file_name}")

def input_metrics(data, prediction):
    """
    Função para escrever métricas customizadas no Cloudwatch.

    Args:
        data (dict): dicionário de dados com todos os atributos.
        prediction (int): valor de predição.
    """

    cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'Credit Score',
                'Value': prediction
            },
        ], Namespace='Credit Score Classification')

    for key, value in data.items():
        cloudwatch.put_metric_data(
        MetricData = [
            {
                'MetricName': 'Client Feature',
                'Value': 1,
                'Unit': 'Count',
                'Dimensions': [{'Name': key, 'Value': str(value)}]
            },
        ], Namespace='Credit Score Classification Features')

def prepare_payload(data):
    """
    Função para padronizar o payload de entrada de modo
    a ser compatível com a execução do modelo.

    Args:
        data (dict): dicionário de dados com todos os atributos.

     Returns:
        dict: payload padronizado.

    """

    data_processed = []

    data_processed.append(int(data["Age"]))
    data_processed.append(float(data["Annual_Income"]))
    data_processed.append(float(data["Monthly_Inhand_Salary"]))  
    data_processed.append(int(data["Num_Bank_Accounts"]))
    data_processed.append(int(data["Num_Credit_Card"]))
    data_processed.append(int(data["Interest_Rate"]))
    data_processed.append(int(data["Num_of_Loan"]))
    data_processed.append(int(data["Delay_from_due_date"]))
    data_processed.append(int(data["Num_of_Delayed_Payment"]))
    data_processed.append(float(data["Changed_Credit_Limit"]))
    data_processed.append(int(data["Num_Credit_Inquiries"]))
    data_processed.append(float(data["Outstanding_Debt"]))
    data_processed.append(float(data["Credit_Utilization_Ratio"]))
    data_processed.append(int(data["Credit_History_Age"]))
    data_processed.append(float(data["Total_EMI_per_month"]))
    data_processed.append(float(data["Amount_invested_monthly"]))   
    data_processed.append(float(data["Monthly_Balance"]))
    data_processed.append(1) if data["Occupation"] == "Accountant" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Architect" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Desconhecido" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Developer" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Doctor" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Engineer" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Entrepreneur" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Journalist" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Lawyer" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Manager" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Mechanic" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Media_Manager" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Musician" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Scientist" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Teacher" else data_processed.append(0)
    data_processed.append(1) if data["Occupation"] == "Writer" else data_processed.append(0)
    data_processed.append(1) if data["Credit_Mix"] == "Bad" else data_processed.append(0)
    data_processed.append(1) if data["Credit_Mix"] == "Desconhecido" else data_processed.append(0)
    data_processed.append(1) if data["Credit_Mix"] == "Good" else data_processed.append(0)
    data_processed.append(1) if data["Credit_Mix"] == "Standard" else data_processed.append(0)
    data_processed.append(1) if data["Payment_of_Min_Amount"] == "NM" else data_processed.append(0)
    data_processed.append(1) if data["Payment_of_Min_Amount"] == "No" else data_processed.append(0)
    data_processed.append(1) if data["Payment_of_Min_Amount"] == "Yes" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "Desconhecido" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "High_spent_Large_value_payments" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "High_spent_Medium_value_payments" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "High_spent_Small_value_payments" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "Low_spent_Large_value_payments" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "Low_spent_Medium_value_payments" else data_processed.append(0)
    data_processed.append(1) if data["Payment_Behaviour"] == "Low_spent_Small_value_payments" else data_processed.append(0)

    return data_processed

def handler(event, context=False):
    """
    Função principal de execução da API no Lambda

    Args:
        event (json): payload para processamento.
        context (json): dados adicionais ao contexto (opcional).

     Returns:
        json: Predição de score de crédito.
    """

    print(event)
    print(context)

    if "body" in event:
        print("Body found in event, invoke by API Gateway")

        body_str = event.get("body", "{}")
        body = json.loads(body_str)
        print(body)

        data = body.get("data", {})

    else:
        print("Body not found in event, invoke by Lambda")

        data = event.get("data", {})

    print(data)

    data_processed = prepare_payload(data)
    prediction = model.predict([data_processed])
    prediction = int(prediction[0])

    print(f"Prediction: {prediction}")

    input_metrics(data, prediction)
    write_real_data(data, prediction)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            {
                "prediction": prediction,
                "version": model_info["version"],
            })
    }
